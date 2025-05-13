from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status, Depends

from . import flow
from .dto import r


oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")


async def current_user(token: str = Depends(oauth2_schema)) -> r.CurrentUserDTO:
    user = await flow.get_current_user(
        flow.dto.p.GetCurrentUserDTO(access_token=token))
    
    return r.CurrentUserDTO.model_validate(user)
