from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from deps import get_current_user, get_db
from models import User
from services import user_service
from views.user import UserCreate, UserRead

router = APIRouter()


@router.get("/users", response_model=UserRead)
async def get_current_user_profile(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user

@router.post("/register")
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    await user_service.register(db, user)
    return {"msg": "Usuário criado"}


@router.post("/login")
async def login(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await user_service.login(db, user)

