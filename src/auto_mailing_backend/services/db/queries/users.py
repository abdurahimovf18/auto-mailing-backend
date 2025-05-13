from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa
from sqlalchemy.orm import load_only

from src.auto_mailing_backend.domain import models
from ..dto import p, r


async def get_full(param: p.users.GetFullDTO, session: AsyncSession) -> r.users.GetFullDTO | None:
    query = (
        sa.select(models.User)
        .where(models.User.id == param.id)
    )
    response = await session.execute(query)
    user = response.scalar()

    if user is not None:
        return r.users.GetFullDTO.model_validate(user)
    

async def create(param: p.users.CreateDTO, session: AsyncSession) -> r.users.CreateDTO:
    new_user = models.User(**param.to_dict())
    session.add(new_user)
    await session.flush([new_user])
    return r.users.CreateDTO.model_validate(new_user)


async def exists(param: p.users.ExistsDTO, session: AsyncSession) -> r.users.ExistsDTO:
    query = (
        sa.select(
            sa.exists(models.User)
            .where(
                models.User.username == param.username
                if param.username else
                models.User.id == param.id
            )
        )
    )
    response = await session.execute(query)
    return r.users.ExistsDTO(
        exists=response.scalar_one()
    )


async def get_login_user(param: p.users.GetLoginUserDTO, session: AsyncSession) -> r.users.GetLoginUserDTO | None:
    query = (
        sa.select(models.User)
        .where(models.User.username == param.username)
        .options(
            load_only(
                models.User.username,
                models.User.password,
            )
        )
    )
    response = await session.execute(query)
    user = response.scalar()

    if user is not None:
        return r.users.GetLoginUserDTO.model_validate(user)
