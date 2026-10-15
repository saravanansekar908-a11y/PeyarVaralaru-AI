"""
PeyarVaralaru AI — Database models using SQLAlchemy ORM.
Tables: places, historical_names, events, sources, event_sources (association)
"""
from sqlalchemy import (
    Column, Integer, String, Float, Text, ForeignKey, Table,
    create_engine
)
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./peyarvaralaru.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- Association table ---
event_sources = Table(
    "event_sources",
    Base.metadata,
    Column("event_id", Integer, ForeignKey("events.id"), primary_key=True),
    Column("source_id", Integer, ForeignKey("sources.id"), primary_key=True),
)


class Place(Base):
    __tablename__ = "places"
    id = Column(Integer, primary_key=True, index=True)
    current_name = Column(String(255), nullable=False, index=True)
    current_name_tamil = Column(String(255), nullable=True)
    district = Column(String(255), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    description = Column(Text, nullable=True)
    description_tamil = Column(Text, nullable=True)

    historical_names = relationship("HistoricalName", back_populates="place", cascade="all, delete-orphan")
    events = relationship("Event", back_populates="place", cascade="all, delete-orphan")


class HistoricalName(Base):
    __tablename__ = "historical_names"
    id = Column(Integer, primary_key=True, index=True)
    place_id = Column(Integer, ForeignKey("places.id"), nullable=False)
    name = Column(String(255), nullable=False, index=True)
    language = Column(String(50), nullable=True)           # e.g. "Tamil", "English", "Portuguese"
    name_type = Column(String(100), nullable=True)         # official_renaming | historical_variant | transliteration | uncertain
    valid_from = Column(String(50), nullable=True)         # Flexible string to support "1639", "16th century", etc.
    valid_to = Column(String(50), nullable=True)

    place = relationship("Place", back_populates="historical_names")


class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    place_id = Column(Integer, ForeignKey("places.id"), nullable=False)
    event_type = Column(String(100), nullable=False)       # official_renaming | name_variant_recorded | transliteration_change | settlement_founded
    event_date = Column(String(50), nullable=True)         # Flexible string: "1996", "3 March 1906", "Unknown"
    date_precision = Column(String(50), nullable=True)     # exact | year | century | unknown
    description = Column(Text, nullable=True)
    description_tamil = Column(Text, nullable=True)
    evidence_status = Column(String(50), default="unverified")  # verified | partially_verified | unverified

    place = relationship("Place", back_populates="events")
    sources = relationship("Source", secondary=event_sources, back_populates="events")


class Source(Base):
    __tablename__ = "sources"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    title_tamil = Column(String(500), nullable=True)
    publisher = Column(String(255), nullable=True)
    source_url = Column(String(1000), nullable=True)
    document_identifier = Column(String(255), nullable=True)  # G.O. number, page, etc.
    publication_date = Column(String(100), nullable=True)
    page_number = Column(String(100), nullable=True)
    evidence_excerpt = Column(Text, nullable=True)
    evidence_excerpt_tamil = Column(Text, nullable=True)

    events = relationship("Event", secondary=event_sources, back_populates="sources")


def get_db():
    """Dependency that yields a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all tables."""
    Base.metadata.create_all(bind=engine)
