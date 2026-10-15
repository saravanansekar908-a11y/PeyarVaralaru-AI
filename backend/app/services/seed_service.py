"""
Database seeding service.
Loads seed_data.json and populates/syncs tables idempotently.
"""
import json
import os
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database import Place, HistoricalName, Event, Source, event_sources


SEED_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "data", "seed_data.json")


def seed_database(db: Session) -> bool:
    """
    Sync seed data into database.
    Updates existing records and inserts new records so that new places are always added.
    """
    seed_path = os.path.normpath(SEED_FILE)
    if not os.path.exists(seed_path):
        raise FileNotFoundError(f"Seed file not found: {seed_path}")

    with open(seed_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. Sync places
    for p in data["places"]:
        place = db.query(Place).filter(Place.id == p["id"]).first()
        if not place:
            place = Place(id=p["id"])
            db.add(place)
        place.current_name = p["current_name"]
        place.current_name_tamil = p.get("current_name_tamil")
        place.district = p.get("district")
        place.latitude = p.get("latitude")
        place.longitude = p.get("longitude")
        place.description = p.get("description")
        place.description_tamil = p.get("description_tamil")
    db.flush()

    # 2. Sync historical names
    for hn in data["historical_names"]:
        h = db.query(HistoricalName).filter(HistoricalName.id == hn["id"]).first()
        if not h:
            h = HistoricalName(id=hn["id"])
            db.add(h)
        h.place_id = hn["place_id"]
        h.name = hn["name"]
        h.language = hn.get("language")
        h.name_type = hn.get("name_type")
        h.valid_from = hn.get("valid_from")
        h.valid_to = hn.get("valid_to")
    db.flush()

    # 3. Sync sources
    for s in data["sources"]:
        src = db.query(Source).filter(Source.id == s["id"]).first()
        if not src:
            src = Source(id=s["id"])
            db.add(src)
        src.title = s["title"]
        src.title_tamil = s.get("title_tamil")
        src.publisher = s.get("publisher")
        src.source_url = s.get("source_url")
        src.document_identifier = s.get("document_identifier")
        src.publication_date = s.get("publication_date")
        src.page_number = s.get("page_number")
        src.evidence_excerpt = s.get("evidence_excerpt")
        src.evidence_excerpt_tamil = s.get("evidence_excerpt_tamil")
    db.flush()

    # 4. Sync events
    for e in data["events"]:
        evt = db.query(Event).filter(Event.id == e["id"]).first()
        if not evt:
            evt = Event(id=e["id"])
            db.add(evt)
        evt.place_id = e["place_id"]
        evt.event_type = e["event_type"]
        evt.event_date = e.get("event_date")
        evt.date_precision = e.get("date_precision")
        evt.description = e.get("description")
        evt.description_tamil = e.get("description_tamil")
        evt.evidence_status = e.get("evidence_status", "unverified")
    db.flush()

    # 5. Sync event_sources associations
    existing_links = set(
        db.query(event_sources.c.event_id, event_sources.c.source_id).all()
    )
    for es in data.get("event_sources", []):
        link = (es["event_id"], es["source_id"])
        if link not in existing_links:
            db.execute(event_sources.insert().values(
                event_id=es["event_id"],
                source_id=es["source_id"],
            ))
            existing_links.add(link)

    db.commit()
    return True
