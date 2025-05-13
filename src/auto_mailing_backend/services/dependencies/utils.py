from typing import Any

import jwt
from loguru import logger

from src.auto_mailing_backend.config.settings import JWT_ALGORITHM, JWT_TOKEN


def get_jwt_data(token: str) -> Any | None:
    try:
        data = jwt.decode(jwt=token, algorithms=[JWT_ALGORITHM], key=JWT_TOKEN)
        return data
    except Exception as exc:
        logger.exception("Exception on jwt decoding")
        