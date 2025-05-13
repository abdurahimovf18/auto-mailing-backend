from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from uuid import UUID

from src.auto_mailing_backend.utils.session import session
from src.auto_mailing_backend.services.db import queries
from src.auto_mailing_backend.services.db.dto import r, p
from . import dto
from ..utils import get_jwt_data



@session
async def get_current_user(param: dto.p.GetCurrentUserDTO, session: AsyncSession) -> dto.r.GetCurrentUserDTO:
    data = get_jwt_data(token=param.access_token)

    if data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token is invalid or expired."
        )
    
    sub = data.get("sub")
    
    if sub is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token does not contain a valid 'sub' claim."
        )

    try:
        sub = UUID(sub)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Access token 'sub' claim is not a valid UUID."
        )

    user = await queries.users.get_full(p.users.GetFullDTO(id=sub), session=session)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    return dto.r.GetCurrentUserDTO.model_validate(user)
