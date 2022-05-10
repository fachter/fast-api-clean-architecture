from fastapi import APIRouter

router = APIRouter()


@router.get('/demo')
async def public_demo():
    return {'Test': 'Response'}
