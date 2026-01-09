from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class CreateAccount(BaseModel):
    name:str
    phone_no:int
    address:str
    age:int

class AccountResponse(BaseModel):
    id:int
    name:str
    phone_no:int
    address:str
    age:int
    balance:float
    created_at:datetime
    updated_at:datetime

    
    class Config:
        from_attributes = True

class BalanceResponse(BaseModel):
    balance_after:float
    amount:float
    description:str
    created_at:datetime
    updated_at:datetime

class AccountRequest(BaseModel):
    id:int
    amount:float

class RequestID(BaseModel):
    id:int

class ShowBalance(BaseModel):
    balance:float

class Transaction(BaseModel):
    description:str
    balance_after:float
    created_at:datetime
    updated_at:datetime


class AcountUpdate(BaseModel):
    name: Optional[str]
    phone_no: Optional[int] 
    address: Optional[str] 
    age: Optional[int] 

class UpdateResponse(BaseModel):
    name:str
    phone_no:int
    address:str
    age:int