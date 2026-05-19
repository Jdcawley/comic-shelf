from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Create an SQLite database named 'comic_shelf.db' in the current directory
engine = create_engine('sqlite:///comic_shelf.db', echo=False)

Session = sessionmaker(bind=engine)
session = Session()

def init_db():
    Base.metadata.create_all(engine)

def get_session():
    return Session()