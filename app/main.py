from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import test_db_connection
from app.routers import auth_controller
from app.routers.users import user_controller

app = FastAPI(title="My API", description="API for my project", version="1.0")

# Gérer les permissions CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app = FastAPI(title="GSB Mobile API", version="1.0")

# Ajouter les routes
app.include_router(user_controller.gsb_mobile_user_router)
app.include_router(auth_controller.gsb_mobile_router)


# Route de test
@app.get("/")
def read_root():
    return {"message": "Welcome to GSB Mobile API"}

# Point d’entrée
if __name__ == "__main__":
    test_db_connection()
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=5000, reload=True)
