from fastapi import FastAPI
from app.api import street
from app.core.config import settings

app = FastAPI(title=settings.app_name)

app.include_router(street.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Street Light Management"}

