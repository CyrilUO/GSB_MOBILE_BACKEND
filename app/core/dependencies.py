# Gestion propre des sessions pour FastAPI (dépendance de route)
from app.db.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
