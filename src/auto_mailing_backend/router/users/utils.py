from datetime import datetime

from argon2 import PasswordHasher
import jwt
from loguru import logger

from src.auto_mailing_backend.config.settings import JWT_TOKEN, JWT_ALGORITHM, JWT_EXP, JWT_ISS, TIMEZONE


ph = PasswordHasher(
    time_cost=1,
    memory_cost=4096,
    parallelism=1
)


def hash_password(password: str) -> str:
    return ph.hash(password=password)


def verify_password(password: str, hashed_password: str) -> bool:
    return ph.verify(hash=hashed_password, password=password)


def generate_jwt_token(sub: str, **data) -> str | None:
    now = datetime.now(TIMEZONE)

    payload = {
        "sub": sub,
        "iat": int(now.timestamp()),
        "nbf": int(now.timestamp()),
        "exp": int((now + JWT_EXP).timestamp()),
        "iss": JWT_ISS,
        **data
    }

    try:
        token = jwt.encode(payload=payload, algorithm=JWT_ALGORITHM, key=JWT_TOKEN)
        return token
    except Exception as exc:
        logger.exception("Exception while generating jwt token")
    
