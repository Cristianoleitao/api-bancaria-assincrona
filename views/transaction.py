from pydantic import BaseModel, ConfigDict, Field


class TransactionCreate(BaseModel):
    type: str
    amount: float = Field(gt=0, description="Valor deve ser positivo")


class TransactionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    type: str
    amount: float
    account_id: int
