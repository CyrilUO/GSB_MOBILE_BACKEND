from app.db.base import Base
from app.db.database import engine


def init_db():
    print("Création des tables en base de données...")
    Base.metadata.create_all(bind=engine)
    print("Tables créés.")
    print("Checking registered tables...")
    print(Base.metadata.tables.keys())
