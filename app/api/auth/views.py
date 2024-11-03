from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.auth.model import UserRegister, UserLogin
from app.api.auth.service import authenticate_user, register_user

router = APIRouter(tags=["auth"])


@router.post("/register")
async def register_user_endpoint(user: UserRegister):
    """
    Endpoint to register a new user.
    :param user: User registration information (username, email, password)
    :return: Access token if registration is successful
    """
    created_user = await register_user(user.username, user.email, user.password)
    
    if not created_user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="User could not be created"
        )
    
    return {"message": "User signed up successfully"}


@router.post("/login")
async def login_user_endpoint(user: UserLogin):
    """
    Endpoint to log in a user.
    :param user: User login information (email, password)
    :return: Access token if login is successful
    """
    token = await authenticate_user(user.email, user.password)
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    return {"access_token": token}
