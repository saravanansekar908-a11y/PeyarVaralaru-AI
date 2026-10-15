"""
Place-related API routes.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db, Place, HistoricalName, Event, Source
from app.schemas import PlaceSummary, PlaceDetail, EventOut, SourceOut, HistoricalNameOut
from app.services.search_service import search_places

router = APIRouter(prefix="/api", tags=["places"])


@router.get("/places", response_model=List[PlaceSummary])
def list_or_search_places(
    q: Optional[str] = Query(None, description="Search query (Tamil or English)"),
    db: Session = Depends(get_db),
):
    """Search places or list all if no query provided."""
    if q and q.strip():
        results = search_places(db, q.strip())
        out = []
        for place, reason in results:
            summary = PlaceSummary(
                id=place.id,
                current_name=place.current_name,
                current_name_tamil=place.current_name_tamil,
                district=place.district,
                description=place.description,
                description_tamil=place.description_tamil,
                historical_names=[
                    HistoricalNameOut.model_validate(hn) for hn in place.historical_names
                ],
                match_reason=reason,
            )
            out.append(summary)
        return out
    else:
        places = db.query(Place).all()
        return [
            PlaceSummary(
                id=p.id,
                current_name=p.current_name,
                current_name_tamil=p.current_name_tamil,
                district=p.district,
                description=p.description,
                description_tamil=p.description_tamil,
                historical_names=[
                    HistoricalNameOut.model_validate(hn) for hn in p.historical_names
                ],
            )
            for p in places
        ]


@router.get("/places/{place_id}", response_model=PlaceDetail)
def get_place(place_id: int, db: Session = Depends(get_db)):
    """Get full place details including historical names and events."""
    place = db.query(Place).filter(Place.id == place_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")

    return PlaceDetail(
        id=place.id,
        current_name=place.current_name,
        current_name_tamil=place.current_name_tamil,
        district=place.district,
        latitude=place.latitude,
        longitude=place.longitude,
        description=place.description,
        description_tamil=place.description_tamil,
        historical_names=[
            HistoricalNameOut.model_validate(hn) for hn in place.historical_names
        ],
        events=[
            EventOut(
                id=evt.id,
                place_id=evt.place_id,
                event_type=evt.event_type,
                event_date=evt.event_date,
                date_precision=evt.date_precision,
                description=evt.description,
                description_tamil=evt.description_tamil,
                evidence_status=evt.evidence_status,
                sources=[SourceOut.model_validate(s) for s in evt.sources],
            )
            for evt in place.events
        ],
    )


@router.get("/places/{place_id}/timeline", response_model=List[EventOut])
def get_place_timeline(place_id: int, db: Session = Depends(get_db)):
    """Get chronological timeline of events for a place."""
    place = db.query(Place).filter(Place.id == place_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")

    events = db.query(Event).filter(Event.place_id == place_id).all()
    return [
        EventOut(
            id=evt.id,
            place_id=evt.place_id,
            event_type=evt.event_type,
            event_date=evt.event_date,
            date_precision=evt.date_precision,
            description=evt.description,
            description_tamil=evt.description_tamil,
            evidence_status=evt.evidence_status,
            sources=[SourceOut.model_validate(s) for s in evt.sources],
        )
        for evt in events
    ]


@router.get("/places/{place_id}/sources", response_model=List[SourceOut])
def get_place_sources(place_id: int, db: Session = Depends(get_db)):
    """Get all source documents related to a place's events."""
    place = db.query(Place).filter(Place.id == place_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")

    source_ids = set()
    sources = []
    for evt in place.events:
        for src in evt.sources:
            if src.id not in source_ids:
                sources.append(SourceOut.model_validate(src))
                source_ids.add(src.id)
    return sources


@router.get("/sources", response_model=List[SourceOut])
def get_all_sources(db: Session = Depends(get_db)):
    """Get all historical source documents."""
    sources = db.query(Source).all()
    return [SourceOut.model_validate(s) for s in sources]
