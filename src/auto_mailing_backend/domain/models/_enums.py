from typing import Final
from enum import Enum


class STREnum(str, Enum): pass


class OnDelete:
    """Defines database on-delete actions."""
    __slots__ = ()

    CASCADE: Final[str] = "CASCADE"
    RESTRICT: Final[str] = "RESTRICT"
    SET_NULL: Final[str] = "SET NULL"
    NO_ACTION: Final[str] = "NO ACTION"
    SET_DEFAULT: Final[str] = "SET DEFAULT"


class UserLanguages(STREnum):
    """Supported user languages."""
    EN = "EN"
    UZ = "UZ"
    RU = "RU"


class MessageMediaTypes(STREnum):
    """Types of media that can be attached to a message."""
    PHOTO = "PHOTO"
    VIDEO = "VIDEO"
    AUDIO = "AUDIO"


class MessageStatus(STREnum):
    """Status of a message in the system."""
    BUILDING = "BUILDING"
    SENDING = "SENDING"
    FINISHED = "FINISHED"
    WAITING = "WAITING"


class UserPrivileges(STREnum):
    """User privilege levels."""
    ADMIN = "ADMIN"
    USER = "USER"
    

class UserAccountStatus(STREnum):
    REGISTERED = "REGISTERED"
    CREATED = "CREATED"
    