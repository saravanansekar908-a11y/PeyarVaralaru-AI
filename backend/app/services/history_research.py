"""
PeyarVaralaru AI — Universal Historical Research Pipeline Service
Coordinates:
Step A: Place identification and disambiguation (place_resolver)
Step B: Local database search (local_search)
Step C: Source retrieval from archives, gazetteers, and web (source_retrieval)
Step D: Name origin analysis and evidence classification
Step E: Structured 10-section report generation in Tamil (history_ai)
Step F: Caching research results into SQLite with audit metadata
"""
import datetime
from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session

from app.database import Place, HistoricalName, Event, Source, event_sources
from app.services.place_resolver import resolve_place
from app.services.local_search import search_local_places
from app.services.source_retrieval import retrieve_sources_and_evidence
from app.services.history_ai import generate_structured_report, answer_history_question
from app.services.citation_service import validate_and_clean_source
from app.services.rag_service import search_local_passages, classify_evidence_passages, generate_rag_answer


def build_evidence_from_db_place(place: Place) -> Dict[str, Any]:
    """Constructs standard evidence bundle from an existing SQLite Place record."""
    h_names = [
        {
            "id": hn.id,
            "place_id": hn.place_id,
            "name": hn.name,
            "language": hn.language,
            "name_type": hn.name_type,
            "valid_from": hn.valid_from,
            "valid_to": hn.valid_to,
        }
        for hn in place.historical_names
    ]

    events = []
    sources = []
    seen_source_ids = set()

    for evt in place.events:
        evt_sources = []
        for s in evt.sources:
            if s.id not in seen_source_ids:
                s_dict = validate_and_clean_source({
                    "id": s.id,
                    "title": s.title,
                    "title_tamil": s.title_tamil,
                    "publisher": s.publisher,
                    "source_url": s.source_url,
                    "document_identifier": s.document_identifier,
                    "publication_date": s.publication_date,
                    "page_number": s.page_number,
                    "evidence_excerpt": s.evidence_excerpt,
                    "evidence_excerpt_tamil": s.evidence_excerpt_tamil,
                })
                sources.append(s_dict)
                seen_source_ids.add(s.id)
            evt_sources.append({
                "id": s.id,
                "title": s.title,
                "title_tamil": s.title_tamil
            })

        events.append({
            "id": evt.id,
            "event_type": evt.event_type,
            "event_date": evt.event_date,
            "date_precision": evt.date_precision,
            "description": evt.description,
            "description_tamil": evt.description_tamil,
            "evidence_status": evt.evidence_status,
            "sources": evt_sources,
        })

    return {
        "place_data": {
            "canonical_name": place.current_name,
            "canonical_name_tamil": place.current_name_tamil or place.current_name,
            # Use specific district name — NOT the state name
            "district": place.district or "",
            "district_tamil": place.district_tamil or place.district or "",
            "state": getattr(place, "state", "Tamil Nadu") or "Tamil Nadu",
            "state_tamil": getattr(place, "state_tamil", "தமிழ்நாடு") or "தமிழ்நாடு",
            "taluk": place.taluk or "",
            "taluk_tamil": getattr(place, "taluk_tamil", None) or place.taluk or "",
            "category": place.category or "Settlement",
            "category_tamil": place.category_tamil or "ஊர் / குடியிருப்பு",
            "latitude": place.latitude,
            "longitude": place.longitude,
        },
        "meaning_tamil": place.meaning_tamil,
        "origin_tamil": place.origin_tamil,
        "historical_names": h_names,
        "events": events,
        "sources": sources,
        "evidence_status": place.evidence_status or "verified",
        "is_uncertain": (place.evidence_status in ["unverified", "disputed"]),
    }


def cache_research_into_db(db: Session, place_meta: Dict[str, Any], evidence: Dict[str, Any], raw_markdown: str) -> Place:
    """
    Persists researched place into SQLite without marking automated AI text as verified.
    Distinguishes cached research from human-reviewed seed records.
    """
    c_name = place_meta.get("canonical_name", "").strip()
    c_name_ta = (place_meta.get("canonical_name_tamil") or c_name).strip()

    # Check if place already exists
    existing = db.query(Place).filter(
        (Place.current_name.ilike(c_name)) | (Place.current_name_tamil == c_name_ta)
    ).first()

    if existing:
        place = existing
        place.last_researched_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
    else:
        place = Place(
            current_name=c_name,
            current_name_tamil=c_name_ta,
            district=place_meta.get("district"),
            taluk=place_meta.get("taluk"),
            category=place_meta.get("category"),
            category_tamil=place_meta.get("category_tamil"),
            latitude=place_meta.get("latitude"),
            longitude=place_meta.get("longitude"),
            description=raw_markdown[:500] if raw_markdown else place_meta.get("description"),
            description_tamil=raw_markdown[:500] if raw_markdown else place_meta.get("description_tamil"),
            meaning_tamil=evidence.get("meaning_tamil"),
            origin_tamil=evidence.get("origin_tamil"),
            evidence_status="researched" if evidence.get("evidence_status") == "verified" else "unverified",
            is_cached_research=1,
            last_researched_at=datetime.datetime.now(datetime.timezone.utc).isoformat()
        )
        db.add(place)
        db.flush()

    # Cache Historical Names if not present
    existing_h_names = {hn.name.lower() for hn in place.historical_names}
    for hn_data in evidence.get("historical_names", []):
        hn_str = hn_data.get("name", "").strip()
        if hn_str and hn_str.lower() not in existing_h_names:
            h_obj = HistoricalName(
                place_id=place.id,
                name=hn_str,
                language=hn_data.get("language"),
                name_type=hn_data.get("name_type"),
                valid_from=hn_data.get("valid_from"),
                valid_to=hn_data.get("valid_to")
            )
            db.add(h_obj)
            existing_h_names.add(hn_str.lower())

    # Cache Sources if not present
    created_sources = []
    for s_data in evidence.get("sources", []):
        s_title = s_data.get("title", "").strip()
        s_obj = db.query(Source).filter(Source.title == s_title).first()
        if not s_obj:
            s_obj = Source(
                title=s_title,
                title_tamil=s_data.get("title_tamil"),
                publisher=s_data.get("publisher"),
                source_url=s_data.get("source_url"),
                document_identifier=s_data.get("document_identifier"),
                publication_date=s_data.get("publication_date"),
                page_number=s_data.get("page_number"),
                evidence_excerpt=s_data.get("evidence_excerpt"),
                evidence_excerpt_tamil=s_data.get("evidence_excerpt_tamil"),
            )
            db.add(s_obj)
            db.flush()
        created_sources.append(s_obj)

    # Cache Events if not present
    existing_evt_descs = {(e.description or "").strip() for e in place.events}
    for e_data in evidence.get("events", []):
        desc = (e_data.get("description") or "").strip()
        if desc and desc not in existing_evt_descs:
            evt_obj = Event(
                place_id=place.id,
                event_type=e_data.get("event_type", "historical_variant"),
                event_date=e_data.get("event_date"),
                date_precision=e_data.get("date_precision"),
                description=desc,
                description_tamil=e_data.get("description_tamil"),
                evidence_status=e_data.get("evidence_status", "researched")
            )
            db.add(evt_obj)
            db.flush()
            # Link to sources
            for s_idx in e_data.get("source_indices", []):
                if s_idx < len(created_sources):
                    evt_obj.sources.append(created_sources[s_idx])
            existing_evt_descs.add(desc)

    db.commit()
    return place


def research_place(
    db: Session,
    query: str,
    district_hint: Optional[str] = None,
    language: str = "ta"
) -> Dict[str, Any]:
    """
    Main research workflow:
    Accepts place name query -> Step A (Identify & Disambiguate) ->
    Step B (Search SQLite) -> Step C (External Research) ->
    Step D (Name Origin Analysis) -> Step E (Structured Report) ->
    Step F (Cache in SQLite).
    """
    if not query or not query.strip():
        return {
            "status": "error",
            "message": "தேடல் சொல்லை உள்ளிடுங்கள் (Please enter a place name)." if language == "ta" else "Please enter a place name.",
            "candidates": [],
            "report": None
        }

    # Step A: Identify place & check homonym ambiguity
    resolution = resolve_place(query, district_hint)
    if resolution.get("is_ambiguous"):
        return {
            "status": "ambiguous",
            "is_ambiguous": True,
            "query": query,
            "language": language,
            "candidates": resolution.get("candidates", []),
            "message": resolution.get("message_tamil" if language == "ta" else "message_english"),
            "place": None,
            "report": None,
            "raw_markdown": None,
            "source_type": "ambiguous_resolution",
            "ai_generated": False
        }

    resolved_place = resolution.get("place", {})
    canonical_en = resolved_place.get("canonical_name", query)
    canonical_ta = resolved_place.get("canonical_name_tamil", query)
    district = resolved_place.get("district")

    # Step B: Check SQLite Database
    local_matches = search_local_places(db, canonical_en, district, limit=1)
    if not local_matches and canonical_ta:
        local_matches = search_local_places(db, canonical_ta, district, limit=1)

    if local_matches and local_matches[0][2] >= 90:
        db_place = local_matches[0][0]
        # If place has verified events/sources, construct report directly from DB
        evidence = build_evidence_from_db_place(db_place)
        report_res = generate_structured_report(evidence, language=language)
        return {
            "status": "success",
            "is_ambiguous": False,
            "query": query,
            "language": language,
            "place": {
                "id": db_place.id,
                "current_name": db_place.current_name,
                "current_name_tamil": db_place.current_name_tamil,
                "state": getattr(db_place, "state", "Tamil Nadu") or "Tamil Nadu",
                "state_tamil": getattr(db_place, "state_tamil", "தமிழ்நாடு") or "தமிழ்நாடு",
                "district": db_place.district or "",
                "district_tamil": getattr(db_place, "district_tamil", None) or db_place.district or "",
                "taluk": db_place.taluk or "",
                "taluk_tamil": getattr(db_place, "taluk_tamil", None) or db_place.taluk or "",
                "category": db_place.category,
                "category_tamil": db_place.category_tamil,
                "latitude": db_place.latitude,
                "longitude": db_place.longitude,
                "description": db_place.description,
                "description_tamil": db_place.description_tamil,
                "evidence_status": db_place.evidence_status,
                "is_cached_research": bool(db_place.is_cached_research),
            },
            "candidates": [],
            "report": report_res,
            "raw_markdown": report_res.get("raw_markdown"),
            "source_type": "database_verified" if not db_place.is_cached_research else "cached_research",
            "ai_generated": report_res.get("ai_generated", False)
        }

    # Step C & D: Not in SQLite -> External / Archival Research
    evidence = retrieve_sources_and_evidence(
        canonical_name=canonical_en,
        canonical_name_tamil=canonical_ta,
        district=district
    )

    # Merge resolved place geography
    evidence["place_data"].update(resolved_place)

    # Step E: Synthesize 10-section report
    report_res = generate_structured_report(evidence, language=language)

    # Step F: Cache into SQLite
    cached_place = cache_research_into_db(
        db=db,
        place_meta=resolved_place,
        evidence=evidence,
        raw_markdown=report_res.get("raw_markdown", "")
    )

    return {
        "status": "success",
        "is_ambiguous": False,
        "query": query,
        "language": language,
        "place": {
            "id": cached_place.id,
            "current_name": cached_place.current_name,
            "current_name_tamil": cached_place.current_name_tamil,
            "state": getattr(cached_place, "state", "Tamil Nadu") or "Tamil Nadu",
            "state_tamil": getattr(cached_place, "state_tamil", "தமிழ்நாடு") or "தமிழ்நாடு",
            "district": cached_place.district or "",
            "district_tamil": getattr(cached_place, "district_tamil", None) or cached_place.district or "",
            "taluk": cached_place.taluk or "",
            "taluk_tamil": getattr(cached_place, "taluk_tamil", None) or cached_place.taluk or "",
            "category": cached_place.category,
            "category_tamil": cached_place.category_tamil,
            "latitude": cached_place.latitude,
            "longitude": cached_place.longitude,
            "description": cached_place.description,
            "description_tamil": cached_place.description_tamil,
            "evidence_status": cached_place.evidence_status,
            "is_cached_research": bool(cached_place.is_cached_research),
        },
        "candidates": [],
        "report": report_res,
        "raw_markdown": report_res.get("raw_markdown"),
        "source_type": "live_research",
        "ai_generated": report_res.get("ai_generated", False)
    }


def ask_place_question(
    db: Session,
    question: str,
    district_hint: Optional[str] = None,
    language: str = "ta"
) -> Dict[str, Any]:
    """
    Answers an ad-hoc or follow-up question for ANY place in Tamil Nadu.
    Extracts place -> Resolves -> Retrieves RAG document passages -> Answers with Gemini/fallback.
    """
    resolution = resolve_place(question, district_hint=district_hint)
    resolved_place = resolution.get("place", {})
    canonical_en = resolved_place.get("canonical_name", question)
    canonical_ta = resolved_place.get("canonical_name_tamil", question)
    district = resolved_place.get("district") or district_hint

    # Search DB for place object if present
    local_matches = search_local_places(db, canonical_en, district, limit=1)
    if not local_matches and canonical_ta:
        local_matches = search_local_places(db, canonical_ta, district, limit=1)
    place_obj = local_matches[0][0] if (local_matches and local_matches[0][2] >= 85) else None

    # Run RAG answer generation over local document collection
    rag_res = generate_rag_answer(db, query_or_place=question, district_hint=district, language=language)

    if rag_res.get("passages_used"):
        return {
            "answer": rag_res.get("answer"),
            "sources_used": rag_res.get("sources_used", []),
            "passages_used": rag_res.get("passages_used", []),
            "places_found": [place_obj] if place_obj else [],
            "evidence_classification": rag_res.get("evidence_classification"),
            "ai_generated": rag_res.get("ai_generated", False),
            "fallback": rag_res.get("fallback", False),
            "identified_place": canonical_ta if language == "ta" else canonical_en,
            "evidence_status": rag_res.get("evidence_status"),
            "is_uncertain": rag_res.get("is_uncertain", False)
        }

    # Fallback to existing research flow if RAG yielded no specific passages
    if place_obj:
        evidence = build_evidence_from_db_place(place_obj)
    else:
        evidence = retrieve_sources_and_evidence(
            canonical_name=canonical_en,
            canonical_name_tamil=canonical_ta,
            district=district
        )
        evidence["place_data"].update(resolved_place)
        place_obj = cache_research_into_db(
            db=db,
            place_meta=resolved_place,
            evidence=evidence,
            raw_markdown=""
        )

    ans_result = answer_history_question(question, evidence, language=language)

    return {
        "answer": ans_result.get("answer"),
        "sources_used": ans_result.get("sources_used", []),
        "passages_used": [],
        "places_found": [place_obj] if place_obj else [],
        "evidence_classification": None,
        "ai_generated": ans_result.get("ai_generated", False),
        "fallback": ans_result.get("fallback", False),
        "identified_place": canonical_ta if language == "ta" else canonical_en,
        "evidence_status": ans_result.get("evidence_status"),
        "is_uncertain": ans_result.get("is_uncertain", False)
    }
