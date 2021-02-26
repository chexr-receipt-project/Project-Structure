from motor import motor_asyncio
from .config import settings


class Database:
    client: motor_asyncio.AsyncIOMotorClient = None


db = Database()


def get_database():
    return db.client[settings.MONGO_DATABASE]


def connect_db():
    db.client = motor_asyncio.AsyncIOMotorClient(settings.MONGO_URL)


def close_db():
    db.client.close()
