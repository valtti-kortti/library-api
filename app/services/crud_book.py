from sqlalchemy import select, update, delete

from app.models.models import Book
from db import async_session


def connection(func):
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)
    return wrapper


# crud для книг
@connection
async def create_book(session, title: str, author: str, quantity: int, year: int = None, isbn: str = None) -> dict:
    try:
        book = Book(title=title, author=author, quantity=quantity, year=year, isbn=isbn)

        session.add(book)
        await session.flush()
        await session.commit()

        return {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "quantity": book.quantity,
            "year": book.year,
            "isbn": book.isbn
        }
    except Exception as e:
        await session.rollback()
        print(f"Error to create book - {e}")
        return {}
    

@connection
async def get_book_by_id(session, id_book: int) -> dict:
    try:
        book = await session.scalar(select(Book).where(Book.id == id_book))

        if book:
            return {
                'id': book.id,
                'title': book.title, 
                'author': book.author, 
                'quantity': book.quantity, 
                'year': book.year, 
                'isbn': book.isbn,
            }
        
        return {}
    except Exception as e:
        print(f"Error to get book {e}")
        return {}
    

@connection
async def get_all_books(session) -> list:
    try:
        books = await session.scalars(select(Book))
        result = []

        for book in books:
            result.append({
                'id': book.id,
                'title': book.title, 
                'author': book.author, 
                'quantity': book.quantity, 
                'year': book.year, 
                'isbn': book.isbn,
            })

        print(result)
        return result
    except Exception as e:
        print(f"Error to get books {e}")
        return []
    

@connection
async def update_book_by_id(session, id_book: int, **update_data) -> dict:
    try:
        valid_attrs = {
            k: v for k, v in update_data.items() 
            if hasattr(Book, k) and k != "id"
        }

        if not valid_attrs:
            return False
        
        stmt = update(Book).where(Book.id == id_book).values(**valid_attrs)
        result = await session.execute(stmt)

        if result.rowcount > 0:
                book = await session.scalar(select(Book).where(Book.id == id_book))
                await session.commit()
        else:
            await session.rollback()


        return {
            'id': book.id,
            'title': book.title, 
            'author': book.author, 
            'quantity': book.quantity, 
            'year': book.year, 
            'isbn': book.isbn,
        }
    
    except Exception as e:
        await session.rollback()
        print(f"Error to update book {e}")
        return {}
    

@connection
async def delete_book_by_id(session, id_book: str) -> bool:
    try:
        book = delete(Book).where(Book.id == id_book)

        result = await session.execute(book)

        if result.rowcount > 0:
            await session.commit()
            return True
        
        await session.rollback()

        return False
    
    except Exception as e:
        print(f"Error to delete book {e}")
        return False

    
