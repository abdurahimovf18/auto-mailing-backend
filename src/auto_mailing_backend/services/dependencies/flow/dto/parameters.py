from src.auto_mailing_backend.utils.dto import BaseDTO


class GetCurrentUserDTO(BaseDTO):
    access_token: str
    