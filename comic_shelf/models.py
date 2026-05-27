from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship

# Base class for all ORM models; replaces raw SQL with Python class/object interaction
Base = declarative_base()

class Publisher(Base):
    __tablename__ = 'publishers'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    # cascade='all, delete-orphan' means deleting a Publisher automatically deletes all its Series rows
    # back_populates='series' links this Publisher to its Series, enabling easy access to all Series from a Publisher instance
    series = relationship('Series', back_populates='publisher', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Publisher(id={self.id}, name='{self.name}')>"

class Series(Base):
    __tablename__ = 'series'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    # ForeignKey enforces referential integrity: every Series must belong to an existing Publisher
    publisher_id = Column(Integer, ForeignKey('publishers.id'), nullable=False)

    # back_populates='series' links this Series to its Publisher, enabling easy access to the Publisher from a Series instance
    publisher = relationship('Publisher', back_populates='series')
    issues = relationship('Issue', back_populates='series', cascade='all, delete-orphan')
    pull_list = relationship('PullList', back_populates='series', cascade='all, delete-orphan')
    wish_list = relationship('Wishlist', back_populates='series', cascade='all, delete-orphan')

    comicvine_series = relationship('ComicVineSeries', back_populates='series', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Series(id={self.id}, name='{self.name}')>"
    
class Issue(Base):
    __tablename__ = 'issues'

    id = Column(Integer, primary_key=True)
    series_id = Column(Integer, ForeignKey('series.id'), nullable=False)
    issue_number = Column(Integer, nullable=False)
    title = Column(String)
    release_date = Column(String)

    __table_args__ = (UniqueConstraint('series_id', 'issue_number', name='uq_series_issue'),)

    series = relationship('Series', back_populates='issues')
    collections = relationship('Collection', back_populates='issue', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Issue(id={self.id}, title='{self.title}')>"
    
class Collection(Base):
    __tablename__ = 'collections'

    id = Column(Integer, primary_key=True)
    issue_id = Column(Integer, ForeignKey('issues.id'), nullable=False)
    read = Column(Boolean, default=False)
    condition = Column(String)

    issue = relationship('Issue', back_populates='collections')

    def __repr__(self):
        return f"<Collection(id={self.id}, issue_id={self.issue_id}, read={self.read})>"
    
class PullList(Base):
    __tablename__ = 'pull_list'

    id = Column(Integer, primary_key=True)
    series_id = Column(Integer, ForeignKey('series.id'), nullable=False)
    issue_number = Column(Integer)
    active = Column(Boolean, default=True)

    series = relationship('Series', back_populates='pull_list')

    def __repr__(self):
        return f"<PullList(id={self.id}, series='{self.series.name}', issue_number={self.issue_number})>"
    
class Wishlist(Base):
    __tablename__ = 'wishlist'

    id = Column(Integer, primary_key=True)
    series_id = Column(Integer, ForeignKey('series.id'), nullable=False)
    issue_number = Column(Integer)
    active = Column(Boolean, default=True)
    notes = Column(String)

    series = relationship('Series', back_populates='wish_list')

    def __repr__(self):
        return f"<Wishlist(id={self.id}, series='{self.series.name}', issue_number={self.issue_number})>"
    
class ComicVineSeries(Base):
    __tablename__ = 'comicvine_series'

    id = Column(Integer, primary_key=True)
    series_id = Column(Integer, ForeignKey('series.id'))
    comicvine_id = Column(Integer, unique=True)  # Unique ID from Comic Vine API
    start_year = Column(String)
    image_url = Column(String)
    deck = Column(String)
    count_of_issues = Column(Integer)

    series = relationship('Series', back_populates='comicvine_series')

    def __repr__(self):
        return f"<ComicVineSeries(id={self.id}, series_id={self.series_id}, comicvine_id={self.comicvine_id})>"