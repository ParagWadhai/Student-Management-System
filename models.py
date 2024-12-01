from pydantic import BaseModel
from typing import Optional, Dict

class Address(BaseModel):
    city: str
    country: str

class StudentCreateRequest(BaseModel):
    name: str
    age: int
    address: Address

class StudentResponse(BaseModel):
    id: str
    name: str
    age: int
    address: Address

class StudentUpdateRequest(BaseModel):
    name: Optional[str]
    age: Optional[int]
    address: Optional[Dict[str, str]]
