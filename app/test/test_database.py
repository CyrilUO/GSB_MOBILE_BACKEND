from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.core.dependencies import get_db
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.drop_all(bind=engine)  # Supprime l'ancienne base de test
    Base.metadata.create_all(bind=engine)  # Crée une nouvelle base propre

def get_test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
