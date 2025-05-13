from typing import Annotated
from functools import partial
from datetime import datetime, timedelta
from uuid import uuid4, UUID

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import BigInteger, ForeignKey, DateTime, text, Boolean, Index, Table, Column, UUID as SQLUUID

from src.auto_mailing_backend.config.settings import TIMEZONE
from src.auto_mailing_backend.infrastructure.db import Base

from . import _enums as enums


SQLUUID = SQLUUID(as_uuid=True)


id_ = Annotated[UUID, mapped_column(SQLUUID, primary_key=True, default=lambda: uuid4())]
created_at = Annotated[datetime, mapped_column(DateTime, server_default=text("TIMEZONE('UTC', NOW())"))]
updated_at = Annotated[datetime, mapped_column(DateTime, server_default=text("TIMEZONE('UTC', NOW())"), 
                                               onupdate=partial(datetime.now, TIMEZONE))]

bigint = Annotated[int, mapped_column(BigInteger)]

tb = Annotated[bool, mapped_column(Boolean, server_default=text("true"))]
fb = Annotated[bool, mapped_column(Boolean, server_default=text("false"))]


MESSAGE_DEFAULT_INTERVAL = timedelta(hours=1)


message_group_m2m = Table(
    "message_group_m2m",
    Base.metadata,
    Column("message_id", SQLUUID, ForeignKey("messages.id", ondelete="CASCADE"), primary_key=True),
    Column("group_id", SQLUUID, ForeignKey("groups.id", ondelete="CASCADE"), primary_key=True),
)

message_account_m2m = Table(
    "message_account_m2m",
    Base.metadata,
    Column("message_id", SQLUUID, ForeignKey("messages.id", ondelete="CASCADE"), primary_key=True),
    Column("account_id", SQLUUID, ForeignKey("accounts.id", ondelete="CASCADE"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[id_]

    username: Mapped[str]
    password: Mapped[str]

    privilage: Mapped[enums.UserPrivileges] = mapped_column(server_default=enums.UserPrivileges.USER.value)

    language: Mapped[enums.UserLanguages]

    is_active: Mapped[tb]
    is_deleted: Mapped[fb]

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    accounts: Mapped[list["Account"]] = relationship("Account", back_populates="user")


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[id_]
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"))
    phone: Mapped[str]
    
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    messages: Mapped[list["Message"]] = relationship("Message", back_populates="accounts", secondary=message_account_m2m)
    user: Mapped["User"] = relationship("User", back_populates="accounts", uselist=False)


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[id_]
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    link: Mapped[str]

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    messages: Mapped[list["Message"]] = relationship("Message", back_populates="groups", secondary=message_group_m2m)


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[id_]
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    text: Mapped[str | None]
    interval: Mapped[timedelta] = mapped_column(default=MESSAGE_DEFAULT_INTERVAL)

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    groups: Mapped[list["Group"]] = relationship("Group", back_populates="messages", secondary=message_group_m2m)
    accounts: Mapped[list["Account"]] = relationship("Account", back_populates="messages", secondary=message_account_m2m)
    media: Mapped[list["MessageMedia"]] = relationship("MessageMedia", back_populates="message")


class MessageMedia(Base):
    __tablename__ = "message_media"

    id: Mapped[id_]
    message_id: Mapped[UUID] = mapped_column(ForeignKey("messages.id", ondelete="CASCADE"))

    url: Mapped[str]

    message: Mapped["Message"] = relationship("Message", uselist=False, back_populates="media")
