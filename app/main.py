from fastapi import FastAPI
from app.api.v1 import calcul

app = FastAPI()

app.include_router(calcul.router, prefix="/api/v1", tags=["Calcul"])
