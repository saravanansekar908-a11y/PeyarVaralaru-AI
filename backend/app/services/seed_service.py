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
    valid_seed_ids = set()
    for p in data["places"]:
        valid_seed_ids.add(p["id"])
        place = db.query(Place).filter(Place.id == p["id"]).first()
        if not place:
            place = Place(id=p["id"])
            db.add(place)
        place.current_name = p["current_name"]
        place.current_name_tamil = p.get("current_name_tamil")
        place.place_name_english = p.get("place_name_english") or p["current_name"]
        place.place_name_tamil = p.get("place_name_tamil") or p.get("current_name_tamil")
        
        # State and district are separate fields — district must NEVER be the state name
        dist_val = p.get("district")
        if dist_val == "Tamil Nadu":
            dist_val = None
        place.state = p.get("state", "Tamil Nadu")
        place.state_tamil = p.get("state_tamil", "தமிழ்நாடு")
        place.district = dist_val
        place.district_tamil = p.get("district_tamil")
        place.taluk = p.get("taluk")
        place.taluk_tamil = p.get("taluk_tamil")
        place.category = p.get("category")
        place.category_tamil = p.get("category_tamil")
        place.latitude = p.get("latitude")
        place.longitude = p.get("longitude")
        place.description = p.get("description")
        place.description_tamil = p.get("description_tamil")
        place.meaning_tamil = p.get("meaning_tamil")
        place.origin_tamil = p.get("origin_tamil")
        place.village = p.get("village")
        place.village_tamil = p.get("village_tamil")
        place.name_origin_type = p.get("name_origin_type", "documented_fact")
        place.evidence_status = p.get("evidence_status", "verified")
        
        # Structured research fields
        place.historical_period = p.get("historical_period")
        place.name_origin_explanation = p.get("name_origin_explanation") or p.get("origin_tamil")
        place.origin_evidence_status = p.get("origin_evidence_status") or p.get("name_origin_type") or "historically_documented"
        place.historical_events_summary = p.get("historical_events_summary")
        place.source_title = p.get("source_title")
        place.source_url = p.get("source_url")
        place.source_page = p.get("source_page")
        place.evidence_quote = p.get("evidence_quote")
        place.verification_status = p.get("verification_status") or p.get("evidence_status") or "verified"
        place.is_cached_research = 0  # seed records are curated, not AI-generated
    
    # Purge any spurious / unverified cached entries in database
    db.query(Place).filter(
        (Place.district == "Tamil Nadu") | 
        (Place.taluk == "Tamil Nadu Taluk") |
        (~Place.id.in_(valid_seed_ids))
    ).delete(synchronize_session=False)
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
