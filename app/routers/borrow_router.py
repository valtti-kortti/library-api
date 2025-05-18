from fastapi import APIRouter, HTTPException, Depends
from app.routers.schemas import BorrowBookSchema

from app.auth.jwt_token import check_token_valid
from app.services.cruds import get_the_number_of_reader_borrow_books, create_borrow, return_book, get_borrow_by_reader_id
from app.services.crud_book import get_book_by_id
from app.services.crud_reader import get_reader_by_id


router = APIRouter()


'''Выдача книги читатель.
    Проверяется есть ли книги если больше 0 то выдается
    Проверяется сколько книг сейчас у пользователя, если меньше 3 то выдается
    Защищено токеном'''
@router.post("/create")
async def create_borrow_book(data: BorrowBookSchema, email: str = Depends(check_token_valid)):
    try:
        book = await get_book_by_id(id_book=data.id_book)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")

        if book["quantity"] < 1:
            raise HTTPException(status_code=400, detail="Book quantity is zero")

        reader = await get_reader_by_id(id_reader=data.id_reader)
        if not reader:
            raise HTTPException(status_code=404, detail="Reader not found")

        borrows_number = await get_the_number_of_reader_borrow_books(id_reader=data.id_reader)
        print(borrows_number)
        if borrows_number >= 3:
            raise HTTPException(status_code=409, detail="Reader has already borrowed 3 books")

        borrow = await create_borrow(id_reader=data.id_reader, id_book=data.id_book)

        if not borrow:
            raise HTTPException(status_code=500, detail="Failed to create borrow record")

        return borrow

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    


'''Возврат книги
    Проверяется есть ли такая выдача
    так же проверяется отсутствие возврата
    Устанавливается время возврата и добавляется колличество книг'''
@router.get("/return/{id_borrow}")
async def return_borrow_book(id_borrow: int, email: str = Depends(check_token_valid)):
        try:
            borrow = await return_book(id_borrow=id_borrow)

            if not borrow:
                raise HTTPException(status_code=404, detail="Borrow not found or returned")
            
            return borrow
        except HTTPException as http_exc:
            # Пробрасываем уже подготовленные HTTP-ошибки
            raise http_exc
        except Exception as e:
            # Логируем и возвращаем generic ошибку
            print(f"Unexpected error: {e}")  # или используй logging
            raise HTTPException(status_code=500, detail="Internal server error")
        

# Получение книг взятых пользователь по ID. Защищено токеном
@router.get("/{id_reader}")
async def get_borrows_reader(id_reader: int, email: str = Depends(check_token_valid)):
    try:
        books = await get_borrow_by_reader_id(id_reader=id_reader)

        if books:
            return books
        
        return []
    
    except Exception as e:
        print(f"Unexpected error: {e}") 
        raise HTTPException(status_code=500, detail="Internal server error")


        


