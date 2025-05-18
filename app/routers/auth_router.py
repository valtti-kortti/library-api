from fastapi import APIRouter, HTTPException
from app.routers.schemas import RegisterOrLoginLib
from app.auth.auth import register_librarian, login_librarian


router = APIRouter()

# Регистрация библиотекаря. Получение токена
@router.post("/register")
async def register(data: RegisterOrLoginLib):
    try:
        token = await register_librarian(data.email, data.password)

        if not token:
            raise HTTPException(status_code=400, detail="Registration failed")
        
        return {"access_token": token, "token_type": "bearer"}
    
    except HTTPException as httpexp:
        raise httpexp
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Вход библиотекаря. Получение токена
@router.post("/login")
async def login(data: RegisterOrLoginLib):
    try:
        token = await login_librarian(data.email, data.password)

        if not token:
            raise HTTPException(status_code=400, detail="Login failed")
        
        return {"access_token": token, "token_type": "bearer"}

    except HTTPException as httpexp:
        raise httpexp
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")