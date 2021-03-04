from fastapi import FastAPI
from mangum import Mangum
from app.core.config import settings
from app.merchant.routers.v1 import merchant_v1
from app.core.database import startup_db, close_db
import uvicorn


def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME)
    _app.include_router(merchant_v1)
    _app.add_event_handler("startup", startup_db)
    _app.add_event_handler("shutdown", close_db)
    return _app


app = get_application()

handler = Mangum(app=app)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
