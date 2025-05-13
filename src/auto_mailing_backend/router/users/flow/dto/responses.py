from datetime import datetime
from uuid import UUID

from pydantic import field_validator

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
        

class CreateUserDTO(BaseDTO):
    created_user: CreatedUserDTO

    
class GenerateAccessTokenDTO(BaseDTO):
    access_token: str
    