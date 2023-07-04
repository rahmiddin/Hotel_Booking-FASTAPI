from fastapi import APIRouter, Depends, Response

from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.dependecies import get_current_user
from app.users.schemas import SUserAuth, SUserLogin
from app.users.dao import UsersDAO
from app.users.models import Users
from app.exeptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException

router = APIRouter(
    prefix='/auth',
    tags=['Auth'],
)


@router.post('/register')
async def register_user(user_data: SUserAuth):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException

    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)


@router.post('/login')
async def login_user(response: Response, user_data: SUserLogin):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return access_token


@router.post('/logout')
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")
    return 'Success'


@router.get('/me')
async def get_user_data(current_user: Users = Depends(get_current_user)):
    return current_user



