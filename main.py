from fastapi import FastAPI
from app.routers import auth_router, borrow_router, reader_router, book_router


app = FastAPI()

app.include_router(auth_router.router, prefix="/auth")
app.include_router(borrow_router.router, prefix="/borrow")
app.include_router(reader_router.router, prefix="/reader")
app.include_router(book_router.router, prefix="/book")