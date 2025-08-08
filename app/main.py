from app.api.v1.endpoints import training_recommendations
from fastapi import FastAPI
from app.api.v1 import calcul  

app = FastAPI()



# ✅ Route par défaut "/"
@app.get("/")
def root():
    return {"message": "welcome to fast api service"}


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

