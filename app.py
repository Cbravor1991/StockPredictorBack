from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.user import user
from routes.prediction import prediction

app = FastAPI(
    title="CRUD BASICO USUARIOS",
    description="Consultas basicas a la base de datos sobre tabla usuarios",
    version="1.0.0",
    openapi_tags=[{
        "name": "users",
        "description": "users routes"
    }]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

app.include_router(user)
app.include_router(prediction)
