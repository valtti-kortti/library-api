from passlib.hash import bcrypt

from app.services.cruds import create_librarian, get_librarian_by_email
from app.auth.jwt_token import create_access_token



async def register_librarian(email: str, password: str) -> str:
    try:
        password_hash = bcrypt.hash(password)
        librarian = await create_librarian(email=email, password_hash=password_hash)

        if librarian:
            return create_access_token(email)

        return ""
    
    except Exception as e:
        print(f"Failed to register - {e}")
        return ""


async def login_librarian(email: str, password: str) -> str:
    try:
        librarian = await get_librarian_by_email(email=email)
        password_hash = librarian.get("password_hash")

        if librarian and bcrypt.verify(password, password_hash):
            return create_access_token(email)
        
        return ""
    except Exception as e:
        print(f"Failed to login - {e}")
        return ""
