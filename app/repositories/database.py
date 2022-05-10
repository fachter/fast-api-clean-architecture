from fastapi import Depends
from pydantic import BaseModel
from pymongo import MongoClient
from bson.objectid import ObjectId
from abc import ABC, abstractmethod
import os
from dotenv import load_dotenv


class Database(object):
    DATABASE = None

    @staticmethod
    def initialize(db_name='my-db'):
        load_dotenv()
        mongo_username = os.getenv('MONGO_USERNAME')
        mongo_password = os.getenv('MONGO_PASSWORD')
        client = MongoClient(host='localhost',
                             port=27017,
                             username=mongo_username,
                             password=mongo_password,
                             authSource='admin',
                             authMechanism='SCRAM-SHA-256')
        Database.DATABASE = client[db_name]

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert_one(data)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def find(collection, query):
        return list(Database.DATABASE[collection].find(query))

    @staticmethod
    def delete(collection, mongo_id):
        Database.DATABASE[collection].delete_one({'_id': ObjectId(mongo_id)})

    @staticmethod
    def update(collection, mongo_id, data):
        Database.DATABASE[collection].update_one({'_id': ObjectId(mongo_id)}, {'$set': data}, upsert=False)


class BaseRepository(ABC):
    def __init__(self, db: Database = Depends()):
        self._db = db

    @property
    @abstractmethod
    def _collection(self):
        pass

    def find_all(self):
        return self._db.find(self._collection, {})

    def find_one(self, mongo_id):
        return self._db.find_one(self._collection, {'_id': ObjectId(mongo_id)})

    def insert(self, data: BaseModel):
        self._db.insert(self._collection, data.dict())

    def delete(self, data_id: str):
        self._db.delete(self._collection, data_id)

    def update(self, mongo_id: str, data: BaseModel):
        self._db.update(self._collection, mongo_id, data.dict(exclude_none=True))
