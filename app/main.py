from app.api.v1.endpoints import skills, training_recommendations, trainings
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



app.include_router(skills.router, prefix="/api/v1", tags=["Skills"])
app.include_router(trainings.router, prefix="/api/v1", tags=["Trainings"])