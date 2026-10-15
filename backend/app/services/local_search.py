"""
PeyarVaralaru AI — Local Search Service
Searches the SQLite database using Unicode NFC normalization,
case-insensitive matching, historical alias resolution, and fuzzy matching.
"""
import unicodedata
import re
from typing import List, Tuple, Optional
from sqlalchemy.orm import Session
from rapidfuzz import fuzz

from app.database import Place, HistoricalName, Event, Source


def normalize_text(text: str) -> str:
    """Normalize unicode NFC, strip extra whitespace, lowercase."""
    if not text:
        return ""
    text = unicodedata.normalize("NFC", text)
    text = re.sub(r"\s+", " ", text).strip().lower()
    return text


def search_local_places(
    db: Session, 
    query: str, 
    district: Optional[str] = None,
    limit: int = 15
) -> List[Tuple[Place, str, int]]:
    """
    Search SQLite for places by current name and historical aliases.
    Returns list of (Place, match_reason, confidence_score).
    Prioritizes:
    1. Exact match on current name (score 100)
    2. Exact match on historical names (score 95)
    3. Substring match on current name (score 85)
    4. Substring match on historical names (score 80)
    5. Fuzzy match on current or historical names (score 70-79)
    """
    if not query or not query.strip():
        return []

    q = normalize_text(query)
    dist_norm = normalize_text(district) if district else None
    results = []
    seen_ids = set()

    all_places = db.query(Place).all()
    all_hist = db.query(HistoricalName).all()

    # If district filter is supplied, filter eligible places
    def matches_district(p: Place) -> bool:
        if not dist_norm:
            return True
        p_dist = normalize_text(p.district or "")
        return dist_norm in p_dist or p_dist in dist_norm

    # 1. Exact match on current_name or current_name_tamil
    for place in all_places:
        if not matches_district(place):
            continue
        cn = normalize_text(place.current_name)
        cnt = normalize_text(place.current_name_tamil or "")
        if cn == q or cnt == q:
            results.append((place, "exact_current_name", 100))
            seen_ids.add(place.id)

    # 2. Exact match on historical names
    for hn in all_hist:
        if hn.place_id in seen_ids:
            continue
        hn_norm = normalize_text(hn.name)
        if hn_norm == q:
            place = db.query(Place).filter(Place.id == hn.place_id).first()
            if place and matches_district(place):
                results.append((place, f"exact_historical_name: {hn.name}", 95))
                seen_ids.add(place.id)

    # 3. Substring match on current name
    for place in all_places:
        if place.id in seen_ids or not matches_district(place):
            continue
        cn = normalize_text(place.current_name)
        cnt = normalize_text(place.current_name_tamil or "")
        if q in cn or q in cnt or (len(q) > 3 and (cn in q or cnt in q)):
            results.append((place, "substring_current_name", 85))
            seen_ids.add(place.id)

    # 4. Substring match on historical names
    for hn in all_hist:
        if hn.place_id in seen_ids:
            continue
        hn_norm = normalize_text(hn.name)
        if q in hn_norm or (len(q) > 3 and hn_norm in q):
            place = db.query(Place).filter(Place.id == hn.place_id).first()
            if place and matches_district(place):
                results.append((place, f"substring_historical_name: {hn.name}", 80))
                seen_ids.add(place.id)

    # 5. Fuzzy match on current name (threshold: 70)
    for place in all_places:
        if place.id in seen_ids or not matches_district(place):
            continue
        cn = normalize_text(place.current_name)
        score = fuzz.ratio(q, cn)
        cnt = normalize_text(place.current_name_tamil or "")
        score_ta = fuzz.ratio(q, cnt) if cnt else 0
        best_score = max(score, score_ta)
        if best_score >= 70:
            results.append((place, f"fuzzy_current_name ({best_score}%)", int(best_score)))
            seen_ids.add(place.id)

    # 6. Fuzzy match on historical names (threshold: 70)
    for hn in all_hist:
        if hn.place_id in seen_ids:
            continue
        hn_norm = normalize_text(hn.name)
        score = fuzz.ratio(q, hn_norm)
        if score >= 70:
            place = db.query(Place).filter(Place.id == hn.place_id).first()
            if place and matches_district(place):
                results.append((place, f"fuzzy_historical_name: {hn.name} ({score}%)", int(score)))
                seen_ids.add(place.id)

    # Sort results by confidence score descending
    results.sort(key=lambda x: x[2], reverse=True)
    return results[:limit]


def get_place_by_id(db: Session, place_id: int) -> Optional[Place]:
    """Retrieve place by primary key."""
    return db.query(Place).filter(Place.id == place_id).first()
