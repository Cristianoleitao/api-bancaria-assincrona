from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from auth import create_token
from models import Account, User
from views.user import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"])


async def register(db: AsyncSession, data: UserCreate) -> None:
    hashed = pwd_context.hash(data.password)
    new_user = User(username=data.username, password=hashed)
    db.add(new_user)
    await db.flush()
    account = Account(user_id=new_user.id)
    db.add(account)
    await db.commit()


async def login(db: AsyncSession, data: UserCreate) -> dict:
    result = await db.execute(select(User).where(User.username == data.username))
    db_user = result.scalar_one_or_none()

    if not db_user or not pwd_context.verify(data.password, db_user.password):
        return {"error": "Credenciais inválidas"}

    token = create_token({"sub": db_user.username})
    return {"access_token": token, "token_type": "bearer"}
