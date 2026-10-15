"""
Place-related API routes and Universal Historical Research endpoint.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db, Place, HistoricalName, Event, Source
from app.schemas import (
    PlaceSummary, 
    PlaceDetail, 
    EventOut, 
    SourceOut, 
    DocumentPassageOut,
    EvidenceClassificationOut,
    HistoricalNameOut,
    ResearchRequest,
    ResearchResponse,
    AmbiguityCandidate,
    HistoricalReport
)
from app.services.local_search import search_local_places
from app.services.history_research import research_place
from app.services.rag_service import search_local_passages, classify_evidence_passages

router = APIRouter(prefix="/api", tags=["places"])


@router.get("/places", response_model=List[PlaceSummary])
@router.get("/places/search", response_model=List[PlaceSummary])
def list_or_search_places(
    q: Optional[str] = Query(None, description="Search query (Tamil or English)"),
    district: Optional[str] = Query(None, description="Optional district filter"),
    db: Session = Depends(get_db),
):
    """Search places in SQLite database or list all if no query provided."""
    if q and q.strip():
        results = search_local_places(db, q.strip(), district=district)
        out = []
        for place, reason, score in results:
            summary = PlaceSummary(
                id=place.id,
                current_name=place.current_name,
                current_name_tamil=place.current_name_tamil,
                state=getattr(place, "state", "Tamil Nadu"),
                state_tamil=getattr(place, "state_tamil", "தமிழ்நாடு"),
                district=place.district,
                district_tamil=getattr(place, "district_tamil", None),
                taluk=place.taluk,
                taluk_tamil=getattr(place, "taluk_tamil", None),
                village=getattr(place, "village", None),
                village_tamil=getattr(place, "village_tamil", None),
                category=place.category,
                category_tamil=place.category_tamil,
                description=place.description,
                description_tamil=place.description_tamil,
                name_origin_type=getattr(place, "name_origin_type", "documented_fact"),
                evidence_status=place.evidence_status or "verified",
                is_cached_research=bool(place.is_cached_research),
                historical_names=[
                    HistoricalNameOut.model_validate(hn) for hn in place.historical_names
                ],
                match_reason=f"{reason} (score: {score})",
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
                state=getattr(p, "state", "Tamil Nadu"),
                state_tamil=getattr(p, "state_tamil", "தமிழ்நாடு"),
                district=p.district,
                district_tamil=getattr(p, "district_tamil", None),
                taluk=p.taluk,
                taluk_tamil=getattr(p, "taluk_tamil", None),
                village=getattr(p, "village", None),
                village_tamil=getattr(p, "village_tamil", None),
                category=p.category,
                category_tamil=p.category_tamil,
                description=p.description,
                description_tamil=p.description_tamil,
                name_origin_type=getattr(p, "name_origin_type", "documented_fact"),
                evidence_status=p.evidence_status or "verified",
                is_cached_research=bool(p.is_cached_research),
                historical_names=[
                    HistoricalNameOut.model_validate(hn) for hn in p.historical_names
                ],
            )
            for p in places
        ]


@router.post("/history/research", response_model=ResearchResponse)
def conduct_place_research(req: ResearchRequest, db: Session = Depends(get_db)):
    """
    Universal place research pipeline:
    Identifies any village, town, panchayat, river, hill, street, or district.
    Handles ambiguity if multiple places share the name.
    Retrieves archival/gazetteer evidence and synthesizes a complete 10-section Tamil report.
    Caches results into SQLite.
    """
    res = research_place(
        db=db,
        query=req.place_name,
        district_hint=req.district,
        language=req.language
    )

    candidates_out = []
    for cand in res.get("candidates", []):
        candidates_out.append(AmbiguityCandidate(**cand))

    place_detail = None
    if res.get("place"):
        p_data = res["place"]
        # Fetch full relations if id is present
        if p_data.get("id"):
            db_p = db.query(Place).filter(Place.id == p_data["id"]).first()
            if db_p:
                place_detail = PlaceDetail(
                    id=db_p.id,
                    current_name=db_p.current_name,
                    current_name_tamil=db_p.current_name_tamil,
                    state=getattr(db_p, "state", "Tamil Nadu"),
                    state_tamil=getattr(db_p, "state_tamil", "தமிழ்நாடு"),
                    district=db_p.district,
                    district_tamil=getattr(db_p, "district_tamil", None),
                    taluk=db_p.taluk,
                    taluk_tamil=getattr(db_p, "taluk_tamil", None),
                    village=getattr(db_p, "village", None),
                    village_tamil=getattr(db_p, "village_tamil", None),
                    category=db_p.category,
                    category_tamil=db_p.category_tamil,
                    latitude=db_p.latitude,
                    longitude=db_p.longitude,
                    description=db_p.description,
                    description_tamil=db_p.description_tamil,
                    meaning_tamil=db_p.meaning_tamil,
                    origin_tamil=db_p.origin_tamil,
                    name_origin_type=getattr(db_p, "name_origin_type", "documented_fact"),
                    evidence_status=db_p.evidence_status or "verified",
                    is_cached_research=bool(db_p.is_cached_research),
                    last_researched_at=db_p.last_researched_at,
                    # Structured source-grounded research fields
                    place_name_tamil=getattr(db_p, "place_name_tamil", None),
                    place_name_english=getattr(db_p, "place_name_english", None),
                    historical_period=getattr(db_p, "historical_period", None),
                    name_origin_explanation=getattr(db_p, "name_origin_explanation", None),
                    origin_evidence_status=getattr(db_p, "origin_evidence_status", None),
                    historical_events_summary=getattr(db_p, "historical_events_summary", None),
                    source_title=getattr(db_p, "source_title", None),
                    source_url=getattr(db_p, "source_url", None),
                    source_page=getattr(db_p, "source_page", None),
                    evidence_quote=getattr(db_p, "evidence_quote", None),
                    verification_status=getattr(db_p, "verification_status", None),
                    historical_names=[
                        HistoricalNameOut.model_validate(hn) for hn in db_p.historical_names
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
                        for evt in db_p.events
                    ]
                )

    report_out = None
    if res.get("report"):
        rep = res["report"]
        matched_passages = search_local_passages(db, req.place_name, req.district, top_k=6)
        p_out = [
            DocumentPassageOut(
                id=p["passage_id"],
                document_id=p["document_id"],
                document_title=p["document_title"],
                author_or_authority=p["author_or_authority"],
                publication_year=p["publication_year"],
                page_number=p["page_number"],
                passage_text=p["passage_text"],
                passage_text_tamil=p["passage_text_tamil"],
                place_name=p["place_name"],
                district=p["district"],
                taluk=p["taluk"],
                topic=p["topic"],
                evidence_level=p["evidence_level"],
            )
            for p in matched_passages
        ]
        classified_e = classify_evidence_passages(matched_passages)
        report_out = HistoricalReport(
            raw_markdown=rep.get("raw_markdown", ""),
            ai_generated=rep.get("ai_generated", False),
            evidence_status=rep.get("evidence_status", "verified"),
            sources=[SourceOut.model_validate(s) for s in rep.get("sources", [])],
            passages=p_out,
            evidence_classification=EvidenceClassificationOut(**classified_e) if matched_passages else None,
            place_name=rep.get("place_name"),
            district=rep.get("district")
        )

    return ResearchResponse(
        status=res.get("status", "success"),
        query=res.get("query", req.place_name),
        language=res.get("language", req.language),
        is_ambiguous=res.get("is_ambiguous", False),
        candidates=candidates_out,
        message=res.get("message"),
        place=place_detail,
        report=report_out,
        raw_markdown=res.get("raw_markdown"),
        source_type=res.get("source_type", "live_research"),
        ai_generated=res.get("ai_generated", False)
    )


@router.get("/places/{place_id}", response_model=PlaceDetail)
def get_place(place_id: int, db: Session = Depends(get_db)):
    """Get full place details including historical names, events, and RAG document passages."""
    place = db.query(Place).filter(Place.id == place_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")

    passages = search_local_passages(db, place.current_name, place.district, top_k=6)
    passages_out = [
        DocumentPassageOut(
            id=p["passage_id"],
            document_id=p["document_id"],
            document_title=p["document_title"],
            author_or_authority=p["author_or_authority"],
            publication_year=p["publication_year"],
            page_number=p["page_number"],
            passage_text=p["passage_text"],
            passage_text_tamil=p["passage_text_tamil"],
            place_name=p["place_name"],
            district=p["district"],
            taluk=p["taluk"],
            topic=p["topic"],
            evidence_level=p["evidence_level"],
        )
        for p in passages
    ]

    return PlaceDetail(
        id=place.id,
        current_name=place.current_name,
        current_name_tamil=place.current_name_tamil,
        state=getattr(place, "state", "Tamil Nadu"),
        state_tamil=getattr(place, "state_tamil", "தமிழ்நாடு"),
        district=place.district,
        district_tamil=getattr(place, "district_tamil", None),
        taluk=place.taluk,
        taluk_tamil=getattr(place, "taluk_tamil", None),
        village=getattr(place, "village", None),
        village_tamil=getattr(place, "village_tamil", None),
        category=place.category,
        category_tamil=place.category_tamil,
        latitude=place.latitude,
        longitude=place.longitude,
        description=place.description,
        description_tamil=place.description_tamil,
        meaning_tamil=place.meaning_tamil,
        origin_tamil=place.origin_tamil,
        name_origin_type=getattr(place, "name_origin_type", "documented_fact"),
        evidence_status=place.evidence_status or "verified",
        is_cached_research=bool(place.is_cached_research),
        last_researched_at=place.last_researched_at,
        # Structured source-grounded research fields
        place_name_tamil=getattr(place, "place_name_tamil", None),
        place_name_english=getattr(place, "place_name_english", None),
        historical_period=getattr(place, "historical_period", None),
        name_origin_explanation=getattr(place, "name_origin_explanation", None),
        origin_evidence_status=getattr(place, "origin_evidence_status", None),
        historical_events_summary=getattr(place, "historical_events_summary", None),
        source_title=getattr(place, "source_title", None),
        source_url=getattr(place, "source_url", None),
        source_page=getattr(place, "source_page", None),
        evidence_quote=getattr(place, "evidence_quote", None),
        verification_status=getattr(place, "verification_status", None),
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
        passages=passages_out,
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
