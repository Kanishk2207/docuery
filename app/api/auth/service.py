from typing import Optional
import time
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from app.internal.model.model import User
from app.utils.hash_utils import verify_hash, get_password_hash
from app.utils.jwt_utils import generate_auth_token
from app.internal import crud
from app.utils.uuid_utils import get_uuid
from app.internal.db.postgres import get_db

current_time = time.time()

# Function to authenticate user credentials
async def authenticate_user(email: str, password: str) -> Optional[User]:
    """
    Authenticates a user by email and password.
    :param db: Database session
    :param email: User email
    :param password: User password
    :return: User instance if credentials are valid, else None
    """
    # Query the database for a user with the provided email
    async with get_db() as db:
        user = await crud.get_user_by_email(db=db, email=email)

    # If user does not exist or password is incorrect, return None
    if not user or not verify_hash(password, user.hashed_password):
        return None
    
    token = generate_auth_token(user=user)

    return token


# Function to register a new user
async def register_user(username: str, email: str, password: str):
    """
    Registers a new user by creating a record in the database.
    :param db: Database session
    :param username: New user's username
    :param email: New user's email
    :param password: New user's password
    :return: Access token for the newly registered user
    """
    global current_time

    async with get_db() as db:
        existing_user = await crud.get_user_by_email(db=db, email=email)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )

        # Hash the password before storing it
        hashed_password = get_password_hash(password)
        user_id = get_uuid()
        new_user = User(
            user_id=user_id,
            username=username, 
            email=email, 
            hashed_password=hashed_password,
            created_at=current_time,
            updated_at=current_time
            )

        created_user = await crud.create_user(db=db, new_user=new_user)

    # Generate an access token for the new user
    return created_user
