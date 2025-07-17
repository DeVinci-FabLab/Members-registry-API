from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.db.base import Base


from app.core.config import settings
from app.models import *  # Assure l'import de tous les modèles

engine = create_engine(settings.database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    """Create all tables in the database."""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

