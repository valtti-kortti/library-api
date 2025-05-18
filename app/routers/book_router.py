from fastapi import APIRouter, HTTPException, Depends

from app.routers.schemas import CreateBookSchema, UpdateBookSchema
from app.auth.jwt_token import check_token_valid
from app.services.crud_book import create_book, get_book_by_id, get_all_books, update_book_by_id, delete_book_by_id


router = APIRouter()

# Создание книги. Защищено токеном
@router.post("/create")
async def register_book(data: CreateBookSchema, email: str = Depends(check_token_valid)):
    try:
        book = await create_book(title=data.title, author=data.author, quantity=data.quantity, year=data.year, isbn=data.isbn)

        return book

    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    

# Получение книги по ID. Защищено токеном
@router.get("/get/{id_book}")
async def get_book(id_book: int, email: str = Depends(check_token_valid)):
    try:
        book = await get_book_by_id(id_book=id_book)

        return book  
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# Выдача всех книг
@router.get("/all")
async def get_books():
    try:
        books = await get_all_books()

        return books
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# Обновление книги. Защищено токеном
@router.patch("/update/{id_book}")
async def update_reader(id_book: int, data: UpdateBookSchema, email: str = Depends(check_token_valid)):
    try:
        book = await update_book_by_id(id_book=id_book, **data.model_dump(exclude_unset=True))
        return book
        
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    

# Удаление книги. Защищено токеном
@router.delete("/delete/{id_book}")
async def delete_reader(id_book: int, email: str = Depends(check_token_valid)):
    try:
        reader = await delete_book_by_id(id_book=id_book)

        if reader:
            return "Book deleted"
        
        return "The book was not deleted"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete book - {e}")