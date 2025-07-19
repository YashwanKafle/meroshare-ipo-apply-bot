from pydantic import BaseModel


class Account(BaseModel):
    name: str
    capital_id: str
    username: str
    password: str
    quantity: str
    crn_number: str
    bank: str
    transcation_pin: str
