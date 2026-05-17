from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Publisher(Base):
    __tablename__ = 'publishers'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    def __repr__(self):
        return f"<Publisher(id={self.id}, name='{self.name}')>"
    
class Series(Base):
    __tablename__ = 'series'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    Publisher_id = Column(Integer, ForeignKey('publishers.id'), nullable=False)

    def __repr__(self):
        return f"<Series(id={self.id}, name='{self.name}')>"