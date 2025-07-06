from fastapi import FastAPI
from app.api.v1.calcul import router as calcul_router

app = FastAPI(
    title="Module Calcul Score",
    description="API pour calculer score employés selon compétences",
    version="1.0"
)

app.include_router(calcul_router, prefix="/api/v1/calcul")
