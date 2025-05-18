from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RegisterOrLoginLib(BaseModel):
    email: str
    password: str

class BorrowBookSchema(BaseModel):
    id_book: int
    id_reader: int

class ReturnBookSchema(BaseModel):
    id_borrow: str

class CreateReaderSchema(BaseModel):
    name: str
    email: str

class UpdateReaderSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

class CreateBookSchema(BaseModel):
    title: str
    author: str
    quantity: Optional[int] = 1
    year: Optional[int] = None
    isbn: Optional[str] = None

class UpdateBookSchema(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    quantity: Optional[int] = None
    year: Optional[int] = None
    isbn: Optional[str] = None