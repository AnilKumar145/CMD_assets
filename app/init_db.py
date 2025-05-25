from app.database import engine
from app.models.base import Base
from app.models.assets import Asset

def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()