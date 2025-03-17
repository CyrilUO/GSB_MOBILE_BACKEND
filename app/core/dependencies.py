# Gestion des sessions pour FastAPI (dépendance de route)
from app.db.database import SessionLocal


#Appel de la dbb et fermture
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
