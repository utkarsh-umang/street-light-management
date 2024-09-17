from fastapi import FastAPI
from app.api import street
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(street.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to StreetSmart - A Street Light Management System"}

