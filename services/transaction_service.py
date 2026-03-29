from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models import Account, Transaction
from views.transaction import TransactionCreate


async def create_transaction(db: AsyncSession, data: TransactionCreate) -> dict:
    result = await db.execute(select(Account))
    account = result.scalar_one()

    if data.type not in ["deposit", "withdraw"]:
        raise HTTPException(400, "Tipo inválido")

    if data.type == "withdraw" and account.balance < data.amount:
        raise HTTPException(400, "Saldo insuficiente")

    if data.type == "deposit":
        account.balance += data.amount
    else:
        account.balance -= data.amount

    trans = Transaction(
        type=data.type,
        amount=data.amount,
        account_id=account.id,
    )
    db.add(trans)
    await db.commit()

    return {"balance": account.balance}


async def list_transactions(db: AsyncSession, user_id: int) -> list[Transaction]:
    result = await db.execute(
        select(Transaction)
        .join(Account, Transaction.account_id == Account.id)
        .where(Account.user_id == user_id)
    )
    return list(result.scalars().all())
