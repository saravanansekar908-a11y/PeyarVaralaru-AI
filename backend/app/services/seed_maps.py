"""
Database seeding service for Historical Maps and Observations.
Loads historical_maps_data.json and syncs HistoricalMap and MapObservation records idempotently.
"""
import json
import os
from sqlalchemy.orm import Session
from app.database import HistoricalMap, MapObservation

MAPS_DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "data", "historical_maps_data.json")


def seed_historical_maps(db: Session) -> bool:
    """
    Sync historical maps data into SQLite database.
    Updates existing records or inserts new records, then syncs observations.
    """
    data_path = os.path.normpath(MAPS_DATA_FILE)
    if not os.path.exists(data_path):
        print(f"[WARN] Historical maps data file not found: {data_path}")
        return False

    with open(data_path, "r", encoding="utf-8") as f:
        maps_data = json.load(f)

    inserted_or_updated = 0
    obs_count = 0

    for m_data in maps_data:
        map_id = m_data.get("id")
        h_map = db.query(HistoricalMap).filter(HistoricalMap.id == map_id).first()
        if not h_map:
            h_map = HistoricalMap(id=map_id)
            db.add(h_map)

        h_map.title = m_data.get("title", "")
        h_map.title_tamil = m_data.get("title_tamil")
        h_map.place_name = m_data.get("place_name", "")
        h_map.place_name_tamil = m_data.get("place_name_tamil")
        h_map.district = m_data.get("district", "")
        h_map.district_tamil = m_data.get("district_tamil")
        h_map.historical_period = m_data.get("historical_period")
        h_map.year_start = m_data.get("year_start")
        h_map.year_end = m_data.get("year_end")
        h_map.creator = m_data.get("creator")
        h_map.creator_tamil = m_data.get("creator_tamil")
        h_map.source_name = m_data.get("source_name")
        h_map.source_url = m_data.get("source_url")
        h_map.image_url = m_data.get("image_url", "")
        h_map.map_service_url = m_data.get("map_service_url")
        h_map.license_info = m_data.get("license_info")
        h_map.georeferencing_status = m_data.get("georeferencing_status", "georeferenced")
        h_map.bounds_json = m_data.get("bounds_json")
        h_map.center_lat = m_data.get("center_lat", 13.0827)
        h_map.center_lng = m_data.get("center_lng", 80.2707)
        h_map.default_zoom = m_data.get("default_zoom", 13)
        h_map.scale = m_data.get("scale")
        h_map.description = m_data.get("description")
        h_map.description_tamil = m_data.get("description_tamil")
        h_map.limitations = m_data.get("limitations")
        h_map.limitations_tamil = m_data.get("limitations_tamil")
        h_map.verification_status = m_data.get("verification_status", "verified")

        db.flush()

        # Sync observations for this map
        # Remove existing observations for clean idempotent seed
        db.query(MapObservation).filter(MapObservation.map_id == map_id).delete()

        observations = m_data.get("observations", [])
        for obs in observations:
            new_obs = MapObservation(
                map_id=map_id,
                place_name=m_data.get("place_name", ""),
                category=obs.get("category", "place_names"),
                title=obs.get("title", ""),
                title_tamil=obs.get("title_tamil"),
                observation_text=obs.get("observation_text", ""),
                observation_text_tamil=obs.get("observation_text_tamil"),
                evidence_type=obs.get("evidence_type", "verified_archival_finding"),
                historical_year_ref=obs.get("historical_year_ref"),
                modern_comparison=obs.get("modern_comparison"),
                modern_comparison_tamil=obs.get("modern_comparison_tamil"),
                source_citation=obs.get("source_citation"),
                source_url=obs.get("source_url"),
                coordinates_json=obs.get("coordinates_json"),
                verification_status=obs.get("verification_status", "verified")
            )
            db.add(new_obs)
            obs_count += 1

        inserted_or_updated += 1

    db.commit()
    print(f"[INFO] Seeded {inserted_or_updated} historical maps and {obs_count} verified observations.")
    return True
