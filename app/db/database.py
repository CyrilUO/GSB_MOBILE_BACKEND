from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# URL de connexion
DB_URL = f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

# Création de l'engine SQLAlchemy (synchrone)
engine = create_engine(DB_URL, echo=True)  # echo=True pour voir les requêtes SQL en dev

# Création de la session locale (session synchrone)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def test_db_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Database connection successful!") if result.scalar() == 1 else print("Database connection failed!")
    except Exception as e:
        print(f"Database connection error: {e}")
