from fastapi import APIRouter, Depends
from config.security import get_authenticated_user
from viewmodels.user import UserModel

router = APIRouter(prefix='/demo')


@router.get('/public')
async def public_demo():
    return {'Test': 'Response'}


@router.get('/private')
async def private_demo(_: UserModel = Depends(get_authenticated_user)):
    return {'Another': 'Test'}
