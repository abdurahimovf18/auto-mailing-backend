from fastapi import APIRouter, Body, Query, status, Depends

from .dto import p, r
from . import flow

from src.auto_mailing_backend.services.dependencies import auth


router = APIRouter(prefix="/users")


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(param: p.CreateUserDTO = Body(...)) -> r.CreateUserDTO:
    created_user = await flow.create_user(
        flow.dto.p.CreateUserDTO.model_validate(param))

    response = r.CreateUserDTO.model_validate(created_user.to_dict())

    return response
    

@router.post("/access_token")
async def get_access_token(param: p.GetAccessTokenDTO = Body) -> r.GetAccessTokenDTO:
    token_response = await flow.generate_access_token(
        flow.dto.p.GenerateAccessTokenDTO.model_validate(param.to_dict()))
    
    response = r.GetAccessTokenDTO.model_validate(token_response.to_dict())
    return response    


@router.get("/me")
async def get_me(user: auth.r.CurrentUserDTO = Depends(auth.current_user)) -> auth.r.CurrentUserDTO:
    return user
