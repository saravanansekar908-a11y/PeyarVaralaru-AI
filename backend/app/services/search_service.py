"""
Search service — fuzzy + exact matching for places and historical names.
"""
import unicodedata
import re
from typing import List, Tuple
from sqlalchemy.orm import Session
from rapidfuzz import fuzz
from app.database import Place, HistoricalName


def normalize_text(text: str) -> str:
    """Normalize unicode, strip whitespace, lowercase."""
    if not text:
        return ""
    text = unicodedata.normalize("NFC", text)
    text = re.sub(r"\s+", " ", text).strip().lower()
    return text


def search_places(db: Session, query: str, limit: int = 20) -> List[Tuple[Place, str]]:
    """
    Search places by current name and historical names.
    Returns list of (Place, match_reason) tuples.
    Uses exact matching first, then fuzzy matching.
    """
    if not query or not query.strip():
        return []

    q = normalize_text(query)
    results = []
    seen_ids = set()

    # 1) Exact match on current_name
    all_places = db.query(Place).all()
    for place in all_places:
        cn = normalize_text(place.current_name)
        cnt = normalize_text(place.current_name_tamil or "")
        if cn == q or cnt == q:
            results.append((place, "exact_current_name"))
            seen_ids.add(place.id)

    # 2) Exact match on historical names
    all_hist = db.query(HistoricalName).all()
    for hn in all_hist:
        hn_norm = normalize_text(hn.name)
        if hn_norm == q and hn.place_id not in seen_ids:
            place = db.query(Place).filter(Place.id == hn.place_id).first()
            if place:
                results.append((place, f"exact_historical_name:{hn.name}"))
                seen_ids.add(place.id)

    # 3) Substring match on current name
    for place in all_places:
        if place.id in seen_ids:
            continue
        cn = normalize_text(place.current_name)
        cnt = normalize_text(place.current_name_tamil or "")
        if q in cn or q in cnt:
            results.append((place, "substring_current_name"))
            seen_ids.add(place.id)

    # 4) Substring match on historical names
    for hn in all_hist:
        if hn.place_id in seen_ids:
            continue
        hn_norm = normalize_text(hn.name)
        if q in hn_norm:
            place = db.query(Place).filter(Place.id == hn.place_id).first()
            if place:
                results.append((place, f"substring_historical_name:{hn.name}"))
                seen_ids.add(place.id)

    # 5) Fuzzy match on current name (threshold: 70)
    for place in all_places:
        if place.id in seen_ids:
            continue
        cn = normalize_text(place.current_name)
        score = fuzz.ratio(q, cn)
        if score >= 70:
            results.append((place, f"fuzzy_current_name (similarity: {score}%)"))
            seen_ids.add(place.id)

    # 6) Fuzzy match on historical names (threshold: 70)
    for hn in all_hist:
        if hn.place_id in seen_ids:
            continue
        hn_norm = normalize_text(hn.name)
        score = fuzz.ratio(q, hn_norm)
        if score >= 70:
            place = db.query(Place).filter(Place.id == hn.place_id).first()
            if place:
                results.append((place, f"fuzzy_historical_name:{hn.name} (similarity: {score}%)"))
                seen_ids.add(place.id)

    return results[:limit]
