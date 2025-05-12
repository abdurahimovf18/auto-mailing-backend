from typing import Annotated
from functools import partial
from datetime import datetime, timedelta

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import BigInteger, String, ForeignKey, DateTime, text, Boolean, Index

from src.auto_mailing_backend.config.settings import TIMEZONE
from src.auto_mailing_backend.infrastructure.db import Base

from . import _enums as enums


id_ = Annotated[int, mapped_column(BigInteger, primary_key=True)]
created_at = Annotated[datetime, mapped_column(DateTime, server_default=text("TIMEZONE('UTC', NOW())"))]
updated_at = Annotated[datetime, mapped_column(DateTime, server_default=text("TIMEZONE('UTC', NOW())"), 
                                               onupdate=partial(datetime.now, TIMEZONE))]

bigint = Annotated[int, mapped_column(BigInteger)]

def_true_bool = Annotated[bool, mapped_column(Boolean, server_default=text("true"))]
def_false_bool = Annotated[bool, mapped_column(Boolean, server_default=text("false"))]


MESSAGE_DEFAULT_INTERVAL = timedelta(hours=1)
MESSAGE_DEFAULT_SQL_INTERVAL = "INTERVAL '1 hour'"


class User(Base):
    __tablename__ = "users"

    id: Mapped[id_]
    chat_id: Mapped[bigint]

    privilege: Mapped[enums.UserPrivileges] = mapped_column(server_default=enums.UserPrivileges.USER.value)

    is_active: Mapped[def_true_bool]
    is_deleted: Mapped[def_true_bool]

    language: Mapped[enums.UserLanguages] = mapped_column(server_default=enums.UserLanguages.UZ.value)

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    accounts: Mapped[list["Account"]] = relationship(back_populates="users", secondary="user_accounts")
    groups: Mapped[list["Group"]] = relationship(back_populates="user")


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[id_]
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete=enums.OnDelete.CASCADE))

    status: Mapped[enums.MessageStatus] = mapped_column(server_default=enums.MessageStatus.BUILDING.value)

    caption: Mapped[str | None]
    interval: Mapped[timedelta] = mapped_column(server_default=text(MESSAGE_DEFAULT_SQL_INTERVAL))
    created_at: Mapped[created_at]

    groups: Mapped[list["Group"]] = relationship(back_populates="messages", secondary="message_groups")
    media: Mapped[list["MessageMedia"]] = relationship(back_populates="message")
    accounts: Mapped[list["Account"]] = relationship(back_populates="messages", secondary="message_accounts")

    # __table_args__ = (
    #     Index("message_user_id_inx", "user_id"),
    # )


class MessageMedia(Base):
    __tablename__ = "message_media"

    id: Mapped[id_]
    message_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("messages.id", ondelete=enums.OnDelete.RESTRICT))
    tg_token: Mapped[str]
    content_type: Mapped[enums.MessageMediaTypes]

    message: Mapped["Message"] = relationship(back_populates="media", uselist=False)


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[id_]
    phone_number: Mapped[str] = mapped_column(String(30))
    created_at: Mapped[created_at]

    users: Mapped[list["User"]] = relationship(back_populates="accounts", secondary="user_accounts")
    messages: Mapped[list["Message"]] = relationship(back_populates="accounts", secondary="message_accounts")


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[id_]
    chat_id: Mapped[bigint]

    link: Mapped[str] = mapped_column(String(50))
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete=enums.OnDelete.RESTRICT))
    created_at: Mapped[created_at]

    user: Mapped["User"] = relationship(back_populates="groups", uselist=False)
    messages: Mapped[list["Message"]] = relationship(back_populates="groups", secondary="message_groups")


class MessageGroups(Base):
    __tablename__ = "message_groups"

    group_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("groups.id", ondelete=enums.OnDelete.CASCADE),
                                          primary_key=True)
    message_id: Mapped[int] = mapped_column(BigInteger, 
                                            ForeignKey("messages.id", ondelete=enums.OnDelete.CASCADE),
                                            primary_key=True)


class MessageAccount(Base):
    __tablename__ = "message_accounts"

    account_id: Mapped[int] = mapped_column(BigInteger, 
                                            ForeignKey("accounts.id", ondelete=enums.OnDelete.RESTRICT),
                                            primary_key=True)
    message_id: Mapped[int] = mapped_column(BigInteger, 
                                            ForeignKey("messages.id", ondelete=enums.OnDelete.CASCADE),
                                            primary_key=True)
    

class UserAccount(Base):
    __tablename__ = "user_accounts"

    account_id: Mapped[int] = mapped_column(BigInteger, 
                                            ForeignKey("accounts.id", ondelete="CASCADE"),
                                            primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, 
                                         ForeignKey("users.id", ondelete="CASCADE"),
                                         primary_key=True)


class BotSettings(Base):
    __tablename__ = "bot_settings"

    id: Mapped[id_]

    key: Mapped[str] = mapped_column(unique=True)
    value: Mapped[str | None]

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    
    __table_args__ = Index("inx_value", "value"), Index("inx_key", "key")
        