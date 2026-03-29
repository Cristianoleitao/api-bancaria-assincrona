from fastapi import FastAPI

import models  # noqa: F401 — registra metadados ORM para create_all
from controllers import transaction, user
from database import Base, engine

app = FastAPI(title="API Bancária Assíncrona")


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(user.router)
app.include_router(transaction.router)