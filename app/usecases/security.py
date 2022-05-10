import os
from datetime import timedelta, datetime

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from repositories.user_repository import UserRepository
from jose import jwt, JWTError
from passlib.context import CryptContext

from viewmodels.token import TokenData, Token
from viewmodels.user import UserModel


class GetAuthenticatedUserUseCase:
    def __init__(self, user_repo: UserRepository = Depends()):
        load_dotenv()
        self._SECRET_KEY = os.getenv('SECRET_KEY')
        self._user_repo = user_repo

    def get(self, token: str):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
        try:
            payload = jwt.decode(token, self._SECRET_KEY, algorithms=['HS256'])
            return self._get_user_from_username(payload.get('sub'), credentials_exception)
        except JWTError:
            raise credentials_exception

    def _get_user_from_username(self, username: str, credentials_exception: HTTPException):
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
        user = self._user_repo.find_one_by_username(token_data.username)
        if user is None:
            raise credentials_exception
        return UserModel(**user.dict())


class AuthenticateUseCase:
    def __init__(self, user_repo: UserRepository = Depends()):
        load_dotenv()
        self._SECRET_KEY = os.getenv('SECRET_KEY')
        self._ACCESS_TOKEN_EXPIRES_MINUTES = 30
        self._user_repo = user_repo
        self._pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    def authenticate(self, username: str, password: str):
        user = self._validate_and_get_user(username, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"}
            )
        access_token_expires = timedelta(minutes=self._ACCESS_TOKEN_EXPIRES_MINUTES)
        access_token = self._create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
        return Token(access_token=access_token, token_type='bearer')

    def _validate_and_get_user(self, username: str, password: str):
        user = self._user_repo.find_one_by_username(username)
        if not user:
            return False
        if not self._verify_password(password, user.password):
            return False
        return user

    def _verify_password(self, plain_pwd, hashed_pwd):
        return self._pwd_context.verify(plain_pwd, hashed_pwd)

    def _create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({'exp': expire})
        return jwt.encode(to_encode, self._SECRET_KEY, algorithm='HS256')
