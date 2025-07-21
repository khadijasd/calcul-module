from app.api.v1.endpoints import training_recommendations
from fastapi import FastAPI
from app.api.v1 import calcul  

app = FastAPI()

app.include_router(
    calcul.router,
    prefix="/api/v1",
    tags=["Calcul"]
)


app.include_router(
    training_recommendations.router,
    prefix="/api/v1",
    tags=["Training"]
)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
