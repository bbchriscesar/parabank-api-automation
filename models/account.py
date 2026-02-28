from pydantic import BaseModel, ConfigDict

class Account(BaseModel):
    id: int
    customerId: int
    type: str  # e.g., CHECKING, SAVINGS, LOAN
    balance: float
    
    model_config = ConfigDict(extra='ignore')
