from pydantic import Field
from datetime import datetime

from src.auto_mailing_backend.utils.dto import BaseDTO
from src.auto_mailing_backend.domain import models


class CreateUserDTO(BaseDTO):
    username: str
    password: str

    privilage: models.enums.UserPrivileges = Field(default=models.enums.UserPrivileges.USER)

    language: models.enums.UserLanguages

    is_active: bool = Field(default=True)
    is_deleted: bool = Field(default=False)


class GenerateAccessTokenDTO(BaseDTO):
    username: str
    password: str
    