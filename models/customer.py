from pydantic import BaseModel, ConfigDict
from typing import Optional

class Address(BaseModel):
    street: str
    city: str
    state: str
    zipCode: str

class Customer(BaseModel):
    id: int
    firstName: str
    lastName: str
    address: Address
    phoneNumber: Optional[str] = None
    ssn: Optional[str] = None
    
    # Configure pydantic to ignore extra fields if the API adds them
    model_config = ConfigDict(extra='ignore')
