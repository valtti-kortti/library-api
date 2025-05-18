from sqlalchemy import select, update, delete

from app.models.models import Reader
from db import async_session


def connection(func):
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)
    return wrapper


# crud Для читателя

@connection
async def create_reader(session, name: str, email: str) -> dict:
    
    try:
        reader = Reader(name=name, email=email)

        session.add(reader)
        await session.flush()
        await session.commit()

        return {
            "id": reader.id,
            "name": reader.name,
            "email": reader.email
        }
    except Exception as e:
        await session.rollback()
        print(f"Error to create reader - {e}")
        return {}
    

@connection
async def get_reader_by_id(session, id_reader: int) -> dict:
    try:
        reader = await session.scalar(select(Reader).where(Reader.id == id_reader))

        if reader:
            return {
                'id': reader.id,
                'name': reader.name, 
                'email': reader.email, 
            }
        
        return {}
    except Exception as e:
        print(f"Error to get reader {e}")
        return {}
    

@connection
async def update_reader_by_id(session, id_reader: int, **update_data) -> dict:
    try:
        valid_attrs = {
            k: v for k, v in update_data.items() 
            if hasattr(Reader, k) and k != "id"
        }

        if not valid_attrs:
            return {}
        
        stmt = update(Reader).where(Reader.id == id_reader).values(**valid_attrs)
        result = await session.execute(stmt)

        if result.rowcount > 0:
                reader = await session.scalar(select(Reader).where(Reader.id == id_reader))
                await session.commit()
        else:
            await session.rollback()


        return {
                'id': reader.id,
                'name': reader.name, 
                'email': reader.email, 
            }
    
    except Exception as e:
        await session.rollback()
        print(f"Error to update reader {e}")
        return {}
    

@connection
async def delete_reader_by_id(session, id_reader: int) -> bool:
    try:
        reader = delete(Reader).where(Reader.id == id_reader)

        result = await session.execute(reader)

        if result.rowcount > 0:
            await session.commit()
            return True
        
        await session.rollback()

        return False
    
    except Exception as e:
        await session.commit()
        print(f"Error to delete reader {e}")
        return False