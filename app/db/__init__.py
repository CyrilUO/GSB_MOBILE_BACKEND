from app.db.database import engine
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

Base.metadata.create_all(bind=engine)