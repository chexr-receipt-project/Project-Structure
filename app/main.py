from fastapi import FastAPI
from mangum import Mangum
from core.config import settings
from merchant.routers.v1 import merchant_v1
import uvicorn


def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME)
    _app.include_router(merchant_v1)
    return _app


app = get_application()

handler = Mangum(app=app)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
