from motor import motor_asyncio
from .config import settings
from odmantic import AIOEngine
from chexr.merchant import merchant_repository
from chexr.bank import bank_repository
from logging import info


class Database:
    client: motor_asyncio.AsyncIOMotorClient = None
    engine: AIOEngine = None


db = Database()


def get_database():
    return db.engine


async def startup_db():
    db.client = motor_asyncio.AsyncIOMotorClient(settings.MONGO_URL)
    db.engine = AIOEngine(motor_client=db.client, database=settings.MONGO_DATABASE)
    info("Initializing DB schema with indices")
    await merchant_repository.initialize_schema(db.engine)
    await bank_repository.initialize_schema(db.engine)


def close_db():
    db.client.close()

