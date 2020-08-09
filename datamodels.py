# -*- coding: utf-8 -*-


from pydantic import BaseModel
from datetime import date

class new_customer(BaseModel):
    FirstName: str
    LastName: str
    DateOfBirth: date
    StreetName: str
    HouseNumber: int
    PostCode: int
    City: str
    Country: str
    
class lastname_sort(BaseModel):
    LastName: str
    Sort: str

class new_account(BaseModel):
    CustomerId: int

class new_credit(BaseModel):
    AccountId: int
    CustomerId: int
    TotalCreditAmount: float
    CreditIssueDate: date
    ToBePaidBefore: date

class transfer_money(BaseModel):
    SendingAccountId: int
    ReceivingAccountId: int
    Amount: float

class all_postings_individual(BaseModel):
    SendingAccountId: int
    SendingCustomerFirstName: str
    SendingCustomerLastName: str
    ReceivingAccountId: int
    Sort: str
    Skip: int
    Limit: int

class payoff_credit(BaseModel):
    AccountId: int
    CreditId: int
    Amount: float
        
    