from fastapi import APIRouter, HTTPException, Depends

from app.routers.schemas import CreateReaderSchema, UpdateReaderSchema
from app.auth.jwt_token import check_token_valid
from app.services.crud_reader import create_reader, get_reader_by_id, update_reader_by_id, delete_reader_by_id


router = APIRouter()


# Создание читателя. Защищено токеном
@router.post("/create")
async def register_reader(data: CreateReaderSchema, email: str = Depends(check_token_valid)):
    try:
        reader = await create_reader(name=data.name, email=data.email)

        if reader:
            return reader
        
        raise HTTPException(status_code=500, detail=f"Failed to create reader")
    
    except HTTPException as httpexp:
        raise httpexp
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    

# Получение читателя. Защищено токеном
@router.get("/{id_reader}")
async def get_reader(id_reader: int, email: str = Depends(check_token_valid)):
    try:
        reader = await get_reader_by_id(id_reader=id_reader)

        if reader:
            return reader
        
        raise HTTPException(status_code=404, detail=f"Failed to get reader")
    
    except HTTPException as httpexp:
        raise httpexp
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# Обновление читателя. Защищено токеном
@router.patch("/update/{id_reader}")
async def update_reader(id_reader: int, data: UpdateReaderSchema, email: str = Depends(check_token_valid)):
    try:
        reader = await update_reader_by_id(id_reader=id_reader, **data.model_dump(exclude_unset=True))

        if reader:
            return reader
        
        raise HTTPException(status_code=500, detail=f"Failed to update reader")
    
    except HTTPException as httpexp:
        raise httpexp
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    

# Удлаение читателя. Защищено токеном
@router.delete("/delete/{id_reader}")
async def delete_reader(id_reader: int, email: str = Depends(check_token_valid)):
    try:
        reader = await delete_reader_by_id(id_reader=id_reader)

        if reader:
            return "Reader deleted"
        
        raise HTTPException(status_code=500, detail=f"Failed to delete reader")
    
    except HTTPException as httpexp:
        raise httpexp
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")