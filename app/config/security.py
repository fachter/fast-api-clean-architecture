from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from usecases.security import GetAuthenticatedUserUseCase, AuthenticateUseCase

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def verify_password(plain_pwd, hashed_pwd):
    return pwd_context.verify(plain_pwd, hashed_pwd)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_authenticated_user(token: str = Depends(oauth2_scheme),
                           get_authenticated_user_use_case: GetAuthenticatedUserUseCase = Depends()):
    return get_authenticated_user_use_case.get(token)


def authenticate_user(form_data: OAuth2PasswordRequestForm = Depends(), auth_use_case: AuthenticateUseCase = Depends()):
    return auth_use_case.authenticate(form_data.username, form_data.password)
