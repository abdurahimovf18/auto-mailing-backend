import re

from pydantic import Field, field_validator

from src.auto_mailing_backend.utils.dto import BaseDTO
from src.auto_mailing_backend.domain import models


class CreateUserDTO(BaseDTO):
    username: str = Field(min_length=3, max_length=32)
    password: str = Field(min_length=8, max_length=128)
    language: models.enums.UserLanguages

    @field_validator("password")
    def validate_password(cls, v):
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        return v
    
    @field_validator("username")
    def validate_username(cls, v):
        regex=r"^[a-zA-Z0-9_.-]+$"
        if not bool(re.fullmatch(regex, v)):
            raise ValueError("Username is invalid")
        return v
    

class GetAccessTokenDTO(BaseDTO):
    username: str
    password: str
    
