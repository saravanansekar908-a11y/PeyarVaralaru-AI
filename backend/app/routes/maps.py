"""
FastAPI route for Historical Maps Explorer & Cartographic Comparisons.
Provides endpoints for searching archival maps, retrieving georeferenced metadata,
and retrieving verified historical comparison observations.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, func

from app.database import get_db, HistoricalMap, MapObservation
from app.schemas import HistoricalMapOut, HistoricalMapDetailOut, MapObservationOut

router = APIRouter(prefix="/api/maps", tags=["historical_maps"])


@router.get("", response_model=List[HistoricalMapOut])
def get_historical_maps(
    q: Optional[str] = Query(None, description="Search by place name, title, or keywords in Tamil or English"),
    place: Optional[str] = Query(None, description="Filter by place name"),
    district: Optional[str] = Query(None, description="Filter by district"),
    period: Optional[str] = Query(None, description="Filter by historical period"),
    georeferencing_status: Optional[str] = Query(None, description="Filter by georeference status"),
    db: Session = Depends(get_db),
):
    """
    Search and list verified historical maps of Tamil Nadu.
    Only maps with authentic archival backing in the catalog are returned.
    """
    query = db.query(HistoricalMap)

    q = q if isinstance(q, str) else None
    place = place if isinstance(place, str) else None
    district = district if isinstance(district, str) else None
    period = period if isinstance(period, str) else None
    georeferencing_status = georeferencing_status if isinstance(georeferencing_status, str) else None

    if q and q.strip():
        term = f"%{q.strip().lower()}%"
        query = query.filter(
            or_(
                func.lower(HistoricalMap.place_name).like(term),
                func.lower(HistoricalMap.place_name_tamil).like(term),
                func.lower(HistoricalMap.title).like(term),
                func.lower(HistoricalMap.title_tamil).like(term),
                func.lower(HistoricalMap.district).like(term),
                func.lower(HistoricalMap.district_tamil).like(term),
                func.lower(HistoricalMap.creator).like(term),
                func.lower(HistoricalMap.source_name).like(term),
                func.lower(HistoricalMap.description).like(term),
            )
        )

    if place and place.strip():
        p_term = f"%{place.strip().lower()}%"
        query = query.filter(
            or_(
                func.lower(HistoricalMap.place_name).like(p_term),
                func.lower(HistoricalMap.place_name_tamil).like(p_term),
            )
        )

    if district and district.strip():
        d_term = f"%{district.strip().lower()}%"
        query = query.filter(
            or_(
                func.lower(HistoricalMap.district).like(d_term),
                func.lower(HistoricalMap.district_tamil).like(d_term),
            )
        )

    if period and period.strip():
        query = query.filter(HistoricalMap.historical_period == period.strip())

    if georeferencing_status and georeferencing_status.strip():
        query = query.filter(HistoricalMap.georeferencing_status == georeferencing_status.strip())

    maps = query.order_by(HistoricalMap.year_start.asc().nullslast()).all()

    # Populate observations_count for each map
    results = []
    for m in maps:
        obs_count = db.query(func.count(MapObservation.id)).filter(MapObservation.map_id == m.id).scalar() or 0
        m_dict = {
            "id": m.id,
            "title": m.title,
            "title_tamil": m.title_tamil,
            "place_name": m.place_name,
            "place_name_tamil": m.place_name_tamil,
            "district": m.district,
            "district_tamil": m.district_tamil,
            "historical_period": m.historical_period,
            "year_start": m.year_start,
            "year_end": m.year_end,
            "creator": m.creator,
            "creator_tamil": m.creator_tamil,
            "source_name": m.source_name,
            "source_url": m.source_url,
            "image_url": m.image_url,
            "map_service_url": m.map_service_url,
            "license_info": m.license_info,
            "georeferencing_status": m.georeferencing_status,
            "bounds_json": m.bounds_json,
            "center_lat": m.center_lat,
            "center_lng": m.center_lng,
            "default_zoom": m.default_zoom,
            "scale": m.scale,
            "description": m.description,
            "description_tamil": m.description_tamil,
            "limitations": m.limitations,
            "limitations_tamil": m.limitations_tamil,
            "verification_status": m.verification_status,
            "observations_count": obs_count,
        }
        results.append(m_dict)

    return results


@router.get("/periods", response_model=List[str])
def get_map_periods(db: Session = Depends(get_db)):
    """Return distinct historical periods present in the archival map catalog."""
    periods = db.query(HistoricalMap.historical_period).filter(HistoricalMap.historical_period.isnot(None)).distinct().all()
    return [p[0] for p in periods if p[0]]


@router.get("/places", response_model=List[dict])
def get_map_places(db: Session = Depends(get_db)):
    """Return places with available historical map records."""
    places = db.query(
        HistoricalMap.place_name,
        HistoricalMap.place_name_tamil,
        HistoricalMap.district,
        HistoricalMap.district_tamil,
        func.count(HistoricalMap.id).label("count")
    ).group_by(HistoricalMap.place_name).all()

    return [
        {
            "place_name": p.place_name,
            "place_name_tamil": p.place_name_tamil,
            "district": p.district,
            "district_tamil": p.district_tamil,
            "maps_count": p.count,
        }
        for p in places
    ]


@router.get("/observations/categories")
def get_observation_categories(db: Session = Depends(get_db)):
    """Return observation categories with observation counts."""
    categories = db.query(
        MapObservation.category,
        func.count(MapObservation.id).label("count")
    ).group_by(MapObservation.category).all()

    category_labels = {
        "place_names": {"en": "Place Name Changes", "ta": "இடப்பெயர் மாற்றங்கள்"},
        "road_network": {"en": "Road Network Evolution", "ta": "சாலைக் கட்டமைப்பு பரிணாமம்"},
        "settlement_expansion": {"en": "Settlement Expansion", "ta": "குடியிருப்பு விரிவாக்கம்"},
        "waterbodies": {"en": "River & Waterbody Changes", "ta": "நீர்நிலைகள் & ஆற்றுப் போக்கு மாற்றங்கள்"},
        "administrative_boundaries": {"en": "Administrative Boundaries", "ta": "நிர்வாக எல்லைகள்"},
        "historical_landmarks": {"en": "Historical Landmarks & Forts", "ta": "வரலாற்றுச் சின்னங்கள் & கோட்டைகள்"},
    }

    return [
        {
            "category": c.category,
            "name_en": category_labels.get(c.category, {}).get("en", c.category.replace("_", " ").title()),
            "name_ta": category_labels.get(c.category, {}).get("ta", c.category),
            "count": c.count,
        }
        for c in categories
    ]


@router.get("/observations/search", response_model=List[MapObservationOut])
def search_observations(
    q: Optional[str] = Query(None, description="Search observation findings"),
    category: Optional[str] = Query(None, description="Filter by category"),
    evidence_type: Optional[str] = Query(None, description="Filter by evidence type"),
    db: Session = Depends(get_db),
):
    """Search comparison findings across all historical maps."""
    query = db.query(MapObservation)

    q = q if isinstance(q, str) else None
    category = category if isinstance(category, str) else None
    evidence_type = evidence_type if isinstance(evidence_type, str) else None

    if category and category.strip():
        query = query.filter(MapObservation.category == category.strip())

    if evidence_type and evidence_type.strip():
        query = query.filter(MapObservation.evidence_type == evidence_type.strip())

    if q and q.strip():
        term = f"%{q.strip().lower()}%"
        query = query.filter(
            or_(
                func.lower(MapObservation.title).like(term),
                func.lower(MapObservation.title_tamil).like(term),
                func.lower(MapObservation.observation_text).like(term),
                func.lower(MapObservation.observation_text_tamil).like(term),
                func.lower(MapObservation.place_name).like(term),
            )
        )

    return query.order_by(MapObservation.id.asc()).limit(50).all()


@router.get("/{map_id}", response_model=HistoricalMapDetailOut)
def get_historical_map_detail(map_id: int, db: Session = Depends(get_db)):
    """Retrieve detailed metadata, georeference bounds, and verified observations for a map."""
    h_map = db.query(HistoricalMap).filter(HistoricalMap.id == map_id).first()
    if not h_map:
        raise HTTPException(status_code=404, detail="Historical map record not found in archival catalog")

    observations = db.query(MapObservation).filter(MapObservation.map_id == map_id).order_by(MapObservation.id.asc()).all()

    return {
        "id": h_map.id,
        "title": h_map.title,
        "title_tamil": h_map.title_tamil,
        "place_name": h_map.place_name,
        "place_name_tamil": h_map.place_name_tamil,
        "district": h_map.district,
        "district_tamil": h_map.district_tamil,
        "historical_period": h_map.historical_period,
        "year_start": h_map.year_start,
        "year_end": h_map.year_end,
        "creator": h_map.creator,
        "creator_tamil": h_map.creator_tamil,
        "source_name": h_map.source_name,
        "source_url": h_map.source_url,
        "image_url": h_map.image_url,
        "map_service_url": h_map.map_service_url,
        "license_info": h_map.license_info,
        "georeferencing_status": h_map.georeferencing_status,
        "bounds_json": h_map.bounds_json,
        "center_lat": h_map.center_lat,
        "center_lng": h_map.center_lng,
        "default_zoom": h_map.default_zoom,
        "scale": h_map.scale,
        "description": h_map.description,
        "description_tamil": h_map.description_tamil,
        "limitations": h_map.limitations,
        "limitations_tamil": h_map.limitations_tamil,
        "verification_status": h_map.verification_status,
        "observations_count": len(observations),
        "observations": observations,
    }


@router.get("/{map_id}/observations", response_model=List[MapObservationOut])
def get_map_observations(
    map_id: int,
    category: Optional[str] = Query(None, description="Filter observations by category"),
    db: Session = Depends(get_db)
):
    """Retrieve verified historical change observations for a specific map."""
    query = db.query(MapObservation).filter(MapObservation.map_id == map_id)
    if category and category.strip():
        query = query.filter(MapObservation.category == category.strip())
    return query.order_by(MapObservation.id.asc()).all()
