from fastapi import APIRouter, Depends
from config.security import authenticate_user, get_authenticated_user
from viewmodels.token import Token
from viewmodels.user import UserModel

router = APIRouter()


@router.post('/token', response_model=Token)
async def login_for_access_token(token: Token = Depends(authenticate_user)):
    return token


@router.get("/users/me", response_model=UserModel)
async def read_users_me(current_user: UserModel = Depends(get_authenticated_user)):
    return current_user
