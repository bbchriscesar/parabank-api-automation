from pydantic import BaseModel, ConfigDict
from typing import Optional

class LoanResponse(BaseModel):
    responseDate: int | str
    loanProviderName: str
    approved: bool
    message: str
    accountId: Optional[int] = None
    
    model_config = ConfigDict(extra='ignore')
