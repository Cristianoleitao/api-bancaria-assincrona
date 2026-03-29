from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from deps import get_current_user, get_db
from models import User
from services import transaction_service
from views.transaction import TransactionCreate, TransactionRead

router = APIRouter()


@router.get("/transactions", response_model=list[TransactionRead])
async def list_transactions(
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
):
    return await transaction_service.list_transactions(db, current_user.id)


@router.post("/transaction")
async def transaction(
    t: TransactionCreate,
    db: AsyncSession = Depends(get_db),
):
    return await transaction_service.create_transaction(db, t)


@router.get("/statement", response_model=list[TransactionRead])
async def statement(
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
):
    return await transaction_service.list_transactions(db, current_user.id)
