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
    # Separate state and district fields — district must NEVER be the state name
    state = Column(String(255), nullable=True, default="Tamil Nadu")
    state_tamil = Column(String(255), nullable=True, default="தமிழ்நாடு")
    district = Column(String(255), nullable=True)
    district_tamil = Column(String(255), nullable=True)
    taluk = Column(String(255), nullable=True)
    taluk_tamil = Column(String(255), nullable=True)
    category = Column(String(100), nullable=True)
    category_tamil = Column(String(100), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    description = Column(Text, nullable=True)
    description_tamil = Column(Text, nullable=True)
    meaning_tamil = Column(Text, nullable=True)
    origin_tamil = Column(Text, nullable=True)
    evidence_status = Column(String(50), default="verified")
    is_cached_research = Column(Integer, default=0)
    last_researched_at = Column(String(50), nullable=True)

    historical_names = relationship("HistoricalName", back_populates="place", cascade="all, delete-orphan")
    events = relationship("Event", back_populates="place", cascade="all, delete-orphan")
    village = Column(String(255), nullable=True)
    village_tamil = Column(String(255), nullable=True)
    name_origin_type = Column(String(50), default="documented_fact")  # documented_fact | scholarly_hypothesis | traditional_explanation | unknown_origin

    # Structured Source-Grounded Research Fields (SQLite as Single Source of Truth)
    place_name_tamil = Column(String(255), nullable=True)
    place_name_english = Column(String(255), nullable=True)
    historical_period = Column(String(255), nullable=True)
    name_origin_explanation = Column(Text, nullable=True)
    origin_evidence_status = Column(String(50), default="historically_documented")  # historically_documented | scholarly_interpretation | local_tradition | unknown_origin
    historical_events_summary = Column(Text, nullable=True)
    source_title = Column(String(500), nullable=True)
    source_url = Column(String(1000), nullable=True)
    source_page = Column(String(100), nullable=True)
    evidence_quote = Column(Text, nullable=True)
    verification_status = Column(String(50), default="verified")  # verified | partially_verified | unverified

    @property
    def effective_name_en(self) -> str:
        return self.place_name_english or self.current_name or ""

    @property
    def effective_name_ta(self) -> str:
        return self.place_name_tamil or self.current_name_tamil or self.current_name or ""


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


class Document(Base):
    """
    Ingested historical research document (Gazetteer, Inscription, G.O., Census, etc.)
    Stores title, author/issuing authority, publication year, URL, and access date.
    """
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False, index=True)
    title_tamil = Column(String(500), nullable=True)
    author_or_authority = Column(String(300), nullable=True)
    publication_year = Column(String(50), nullable=True)
    source_url = Column(String(1000), nullable=True)
    document_type = Column(String(100), nullable=True)  # gazetteer | archaeological_publication | inscription | government_record | census_directory
    access_date = Column(String(50), nullable=True)
    total_pages = Column(Integer, default=1)
    file_path = Column(String(500), nullable=True)
    full_text = Column(Text, nullable=True)

    passages = relationship("DocumentPassage", back_populates="document", cascade="all, delete-orphan")


class DocumentPassage(Base):
    """
    Searchable extracted passage chunk from an ingested document with exact page number,
    topic, and evidence classification level.
    """
    __tablename__ = "document_passages"
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False, index=True)
    page_number = Column(String(50), nullable=True)
    passage_text = Column(Text, nullable=False)
    passage_text_tamil = Column(Text, nullable=True)
    place_name = Column(String(255), nullable=True, index=True)
    district = Column(String(255), nullable=True, index=True)
    taluk = Column(String(255), nullable=True)
    topic = Column(String(100), nullable=True)  # name_origin | renaming | historical_event | inscription | administration
    evidence_level = Column(String(50), default="documented_fact")  # documented_fact | scholarly_hypothesis | traditional_explanation | unknown_origin

    document = relationship("Document", back_populates="passages")


def get_db():
    """Dependency that yields a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all tables and migrate columns if necessary."""
    Base.metadata.create_all(bind=engine)
    
    # Check for missing columns in existing tables and add them dynamically
    from sqlalchemy import text
    with engine.connect() as conn:
        try:
            res = conn.execute(text("PRAGMA table_info(places)")).fetchall()
            existing_cols = {row[1] for row in res}
            cols_to_add = [
                ("state", "VARCHAR(255) DEFAULT 'Tamil Nadu'"),
                ("state_tamil", "VARCHAR(255) DEFAULT 'தமிழ்நாடு'"),
                ("district_tamil", "VARCHAR(255)"),
                ("taluk", "VARCHAR(255)"),
                ("taluk_tamil", "VARCHAR(255)"),
                ("village", "VARCHAR(255)"),
                ("village_tamil", "VARCHAR(255)"),
                ("category", "VARCHAR(100)"),
                ("category_tamil", "VARCHAR(100)"),
                ("meaning_tamil", "TEXT"),
                ("origin_tamil", "TEXT"),
                ("name_origin_type", "VARCHAR(50) DEFAULT 'documented_fact'"),
                ("evidence_status", "VARCHAR(50) DEFAULT 'verified'"),
                ("is_cached_research", "INTEGER DEFAULT 0"),
                ("last_researched_at", "VARCHAR(50)"),
                ("place_name_tamil", "VARCHAR(255)"),
                ("place_name_english", "VARCHAR(255)"),
                ("historical_period", "VARCHAR(255)"),
                ("name_origin_explanation", "TEXT"),
                ("origin_evidence_status", "VARCHAR(50) DEFAULT 'historically_documented'"),
                ("historical_events_summary", "TEXT"),
                ("source_title", "VARCHAR(500)"),
                ("source_url", "VARCHAR(1000)"),
                ("source_page", "VARCHAR(100)"),
                ("evidence_quote", "TEXT"),
                ("verification_status", "VARCHAR(50) DEFAULT 'verified'"),
            ]
            for col_name, col_type in cols_to_add:
                if col_name not in existing_cols:
                    conn.execute(text(f"ALTER TABLE places ADD COLUMN {col_name} {col_type}"))
            
            # Data Integrity Cleanup: Purge any corrupted records where district was mistakenly set to state name
            conn.execute(text("DELETE FROM places WHERE district = 'Tamil Nadu' OR taluk = 'Tamil Nadu Taluk'"))
            conn.commit()
        except Exception as e:
            print(f"[WARN] Database schema migration error: {e}")

