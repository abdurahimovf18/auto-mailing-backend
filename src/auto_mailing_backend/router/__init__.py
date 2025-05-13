from fastapi import APIRouter

from .accounts.router import router as accounts_router
from .messages.router import router as messages_router
from .users.router import router as users_router


master_router = APIRouter()


master_router.include_router(accounts_router)
master_router.include_router(messages_router)
master_router.include_router(users_router)
