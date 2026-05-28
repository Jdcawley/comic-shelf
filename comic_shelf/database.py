from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from comic_shelf.models import Base
from pathlib import Path

# Create an SQLite database named 'comic_shelf.db' in the current directory
BASE_DIR = Path(__file__).parent
engine = create_engine(f'sqlite:///{BASE_DIR}/comic_shelf.db')

Session = sessionmaker(bind=engine)
session = Session()

def init_db():
    Base.metadata.create_all(engine)

def get_session():
    return Session()