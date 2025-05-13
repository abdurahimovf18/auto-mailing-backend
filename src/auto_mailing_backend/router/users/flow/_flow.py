from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from src.auto_mailing_backend.utils.session import session

from src.auto_mailing_backend.domain import models
from src.auto_mailing_backend.services.db.dto import p, r
from src.auto_mailing_backend.services.db import queries

from . import dto
from ..utils import hash_password, verify_password, generate_jwt_token


@session
async def create_user(param: dto.p.CreateUserDTO, session: AsyncSession) -> dto.r.CreateUserDTO:
    param.password = hash_password(param.password)

    user_exists = await queries.users.exists(
        p.users.ExistsDTO(username=param.username), session)

    if user_exists.exists:
        raise HTTPException(status.HTTP_409_CONFLICT, "User already exists.")

    created_user = await queries.users.create(
        p.users.CreateDTO.model_validate(param.to_dict()), session)
    
    await session.commit()
    
    return dto.r.CreateUserDTO(
        created_user=dto.r.CreatedUserDTO.model_validate(created_user.to_dict())
    )


@session
async def generate_access_token(param: dto.p.GenerateAccessTokenDTO, session: AsyncSession) -> dto.r.GenerateAccessTokenDTO:
    user = await queries.users.get_login_user(
        p.users.GetLoginUserDTO(username=param.username), session)

    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"User with username {param.username} was not found.")

    if not verify_password(param.password, user.password):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Username or password is incorrect.")
    
    jwt_token = generate_jwt_token(
        sub=str(user.id)
    )

    return dto.r.GenerateAccessTokenDTO(access_token=jwt_token)
    