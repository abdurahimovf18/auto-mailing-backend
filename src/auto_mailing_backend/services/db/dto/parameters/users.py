from pydantic import Field, model_validator
from datetime import datetime
from uuid import UUID

from src.auto_mailing_backend.utils.dto import BaseDTO
from src.auto_mailing_backend.domain import models


class GetFullDTO(BaseDTO):
    id: UUID


class CreateDTO(BaseDTO):
    username: str
    password: str

    privilage: models.enums.UserPrivileges = Field(default=models.enums.UserPrivileges.USER)

    language: models.enums.UserLanguages

    is_active: bool = Field(default=True)
    is_deleted: bool = Field(default=False)


class ExistsDTO(BaseDTO):
    username: str | None = Field(default=None)
    id: UUID | None = Field(default=None)

    @model_validator(mode="after")
    def check_fields(self, ):
        if self.id is not None and self.username is not None:
            raise ValueError("username and id should not be given together")
        
        if self.username is None and self.id is None:
            raise ValueError("username or id should be given")

        return self


class GetLoginUserDTO(BaseDTO):
    username: str
