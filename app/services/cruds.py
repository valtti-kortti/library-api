from sqlalchemy import select, update, and_
from datetime import datetime
from typing import Optional

from app.models.models import Book, Librarian, BorrowedBooks
from db import async_session


def connection(func):
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)
    return wrapper
    

# librarian
@connection
async def create_librarian(session, email: str, password_hash: str) -> dict:
    try:
        librarian = Librarian(email=email, password_hash=password_hash)

        session.add(librarian)
        
        await session.flush()
        await session.commit()

        return {
            "id": librarian.id,
            "email": email,
            "password_hash": password_hash
        }
    except Exception as e:
        await session.rollback()
        print(f"Error to create librarian - {e}")
        return {}
    
@connection
async def get_librarian_by_email(session, email: str) -> dict:
    try:
        librarian = await session.scalar(select(Librarian).where(Librarian.email == email))

        if librarian:
            return {
                "email": email,
                "password_hash": librarian.password_hash,
                }
        
        return {}
    
    except Exception as e:
        print(f"Error to get librarian - {e}")
        return {}
    

@connection
async def get_the_number_of_reader_borrow_books(session, id_reader: int) -> int:
    try:
        borrows = await session.scalars(select(BorrowedBooks).where(BorrowedBooks.reader_id == id_reader))
        return len(borrows.all())

    except Exception as e:
        print(f"Error to get borrows - {e}")
        return 3
    

@connection
async def create_borrow(session, id_reader: int, id_book: int) -> dict:
    try:
        # Создаём запись о заимствовании
        borrow = BorrowedBooks(
            book_id=id_book,
            reader_id=id_reader,
        )
        session.add(borrow)

        # Обновляем количество книг
        stmt = (
            update(Book)
            .where(Book.id == id_book)
            .values(quantity=Book.quantity - 1)
            .execution_options(synchronize_session="fetch")
        )
        await session.execute(stmt)

        await session.flush()  # чтобы получить ID новой записи
        await session.commit()

        return {
            "id": borrow.id,
            "book_id": borrow.book_id,
            "reader_id": borrow.reader_id,
            "borrow_date": borrow.borrow_date,
        }

    except Exception as e:
        await session.rollback()
        print(f"Error creating borrow: {e}")
        {}


@connection
async def return_book(session, id_borrow) -> dict:
    try:
        borrow = await session.scalar(select(BorrowedBooks).where(and_(BorrowedBooks.id==id_borrow, BorrowedBooks.return_date == None)))

        stmt = (
            update(BorrowedBooks)
            .where(BorrowedBooks.id == id_borrow)
            .values(return_date=datetime.now())
        )

        await session.execute(stmt)

        book = (
            update(Book)
            .where(Book.id == borrow.book_id)
            .values(quantity=Book.quantity + 1)
            .execution_options(synchronize_session="fetch")
        )

        await session.execute(book)

        await session.flush()  # чтобы получить ID новой записи
        await session.commit()

        return {
            "id": borrow.id,
            "book_id": borrow.book_id,
            "reader_id": borrow.reader_id,
            "borrow_date": borrow.borrow_date,
            "return_date": borrow.return_date
            }
    except Exception as e:
        await session.rollback()
        print(f"Error creating borrow: {e}")
        {}


@connection
async def get_borrow_by_reader_id(session, id_reader: int) -> list:
    try:
        borrows = await session.scalars(select(BorrowedBooks).where(and_(BorrowedBooks.reader_id == id_reader, BorrowedBooks.return_date == None)))
        result = []

        for borrow in borrows:
            book = await session.scalar(select(Book).where(Book.id == borrow.book_id))
            if book:
                result.append({
                    'id': book.id,
                    'title': book.title, 
                    'author': book.author, 
                    'quantity': book.quantity, 
                    'year': book.year, 
                    'isbn': book.isbn,
                })
        return result
    except Exception as e:
        await session.rollback()
        print(f"Error get books: {e}")
        []
