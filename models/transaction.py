from pydantic import BaseModel, ConfigDict

class Transaction(BaseModel):
    id: int
    accountId: int
    type: str  # e.g., Credit, Debit
    date: int | str  # Note: Can be timestamp or ISO string
    amount: float
    description: str
    
    model_config = ConfigDict(extra='ignore')
