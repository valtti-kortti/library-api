from sqlalchemy import String, DateTime, Integer, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from datetime import datetime
from sqlalchemy.sql import func

from db import Base


class Book(Base):

    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(32), nullable=False)
    author: Mapped[str] = mapped_column(String(32), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=True)
    isbn: Mapped[Optional[str]] = mapped_column(String(13), unique=True, nullable=True)
    quantity: Mapped[Optional[int]] = mapped_column(nullable=False, default=1)

    # Новое поле
    description: Mapped[str] = mapped_column(Text, nullable=True)


class Reader(Base):

    __tablename__ = "readers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(32), nullable=False)
    email: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)



class Librarian(Base):

    __tablename__ = "librarians"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(60), nullable=False)

class BorrowedBooks(Base):

    __tablename__ = "borrowedBooks"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    book_id : Mapped[int] = mapped_column(ForeignKey("books.id"))
    reader_id: Mapped[int] = mapped_column(ForeignKey("readers.id"))
    borrow_date: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    return_date: Mapped[Optional[datetime]] = mapped_column(nullable=True)