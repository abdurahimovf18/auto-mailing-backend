from datetime import datetime
from uuid import UUID

from src.auto_mailing_backend.utils.dto import BaseDTO
from src.auto_mailing_backend.domain import models


class CreatedUserDTO(BaseDTO):
    id: UUID
    username: str
    password: str

    privilage: models.enums.UserPrivileges
    language: models.enums.UserLanguages

    is_active: bool
    is_deleted: bool

    created_at: datetime
    updated_at: datetime

    def to_dict(self):
        data = self.model_dump()
        psw = data["password"]

        data["password"] = f"{psw[:5]}...{psw[-5:]}"
        return data


class CreateUserDTO(BaseDTO):
    created_user: CreatedUserDTO

    def to_dict(self, ) -> dict:
        data = self.model_dump()
        data["created_user"] = self.created_user.to_dict()
        return data


class GetAccessTokenDTO(BaseDTO):
    access_token: str
    