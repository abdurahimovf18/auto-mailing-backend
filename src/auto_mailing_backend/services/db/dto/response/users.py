from datetime import datetime
from uuid import UUID

from src.auto_mailing_backend.utils.dto import BaseDTO
from src.auto_mailing_backend.domain import models


class GetFullDTO(BaseDTO):
    id: UUID
    username: str
    password: str

    privilage: models.enums.UserPrivileges
    language: models.enums.UserLanguages

    is_active: bool
    is_deleted: bool

    created_at: datetime
    updated_at: datetime


class CreateDTO(BaseDTO):
    id: UUID
    username: str
    password: str

    privilage: models.enums.UserPrivileges
    language: models.enums.UserLanguages

    is_active: bool
    is_deleted: bool

    created_at: datetime
    updated_at: datetime


class ExistsDTO(BaseDTO):
    exists: bool


class GetLoginUserDTO(BaseDTO):
    id: UUID
    username: str
    password: str
