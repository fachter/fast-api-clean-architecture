from fastapi import Depends

from .database import Database, BaseRepository
from documents.user_documents import UserDocument


class UserRepository(BaseRepository):
    def __init__(self, db: Database = Depends()):
        super().__init__(db)

    @property
    def _collection(self):
        return 'user'

    def find_one_by_username(self, username) -> UserDocument:
        result = self._db.find_one(self._collection, {'username': username})
        user = UserDocument(**result, user_id=str(result['_id']))
        return user

