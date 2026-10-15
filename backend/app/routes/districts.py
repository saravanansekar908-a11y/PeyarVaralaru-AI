"""
District Intelligence API routes for PeyarVaralaru AI.
Serves official dataset for all 38 districts, official sources, and research guidance.
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional, Dict, Any
import json
import os

router = APIRouter(prefix="/api/districts", tags=["districts"])

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "tamil_nadu_38_districts_intelligence.json")

def load_district_data() -> Dict[str, Any]:
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"total_districts": 0, "districts": [], "official_sources": [], "research_guidance": []}


@router.get("", response_model=Dict[str, Any])
def get_all_districts(
    q: Optional[str] = Query(None, description="Search query in English or Tamil"),
    region: Optional[str] = Query(None, description="Filter by geographical region")
):
    """Retrieve all 38 districts with optional search and region filters."""
    data = load_district_data()
    districts = data.get("districts", [])
    
    if q and q.strip():
        query = q.strip().lower()
        matched = []
        for d in districts:
            eng_name = d.get("district_english", "").lower()
            tam_name = d.get("district_tamil", "").lower()
            aliases = [a.lower() for a in d.get("search_aliases", [])]
            former_en = (d.get("former_administrative_name_history_en") or d.get("former_administrative_name_history", "")).lower()
            former_ta = (d.get("former_administrative_name_history_ta", "")).lower()
            ancient_en = (d.get("ancient_or_historical_name_context_en") or d.get("ancient_or_historical_name_context", "")).lower()
            ancient_ta = (d.get("ancient_or_historical_name_context_ta", "")).lower()
            spec_names = [s.get("name_en", "").lower() + " " + s.get("name_ta", "").lower() for s in d.get("specialities", [])]
            place_names = [p.get("name_en", "").lower() + " " + p.get("name_ta", "").lower() for p in d.get("famous_places", [])]
            
            if (query in eng_name or 
                query in tam_name or 
                any(query in a for a in aliases) or
                query in former_en or
                query in former_ta or
                query in ancient_en or
                query in ancient_ta or
                any(query in sn for sn in spec_names) or
                any(query in pn for pn in place_names)):
                matched.append(d)
        districts = matched
        
    if region and region != "all":
        districts = [d for d in districts if region.lower() in (d.get("region", "") + " " + d.get("region_en", "") + " " + d.get("region_ta", "")).lower()]
        
    return {
        "total_districts": len(districts),
        "districts": districts,
        "official_sources": data.get("official_sources", []),
        "research_guidance": data.get("research_guidance", [])
    }


@router.get("/suggestions", response_model=Dict[str, Any])
def get_district_suggestions(q: str = Query(..., min_length=1, description="Search query string")):
    """
    Returns search suggestions grouped into:
    - Districts (Direct district matches)
    - Historical Names (Ancient/Colonial/Administrative former names)
    - Heritage & Specialities (Landmarks, GI products, famous sites)
    """
    data = load_district_data()
    districts = data.get("districts", [])
    query = q.strip().lower()

    grouped = {
        "districts": [],
        "historical_names": [],
        "heritage_places": []
    }

    seen_districts = set()
    seen_history = set()
    seen_places = set()

    for d in districts:
        d_no = d.get("no")
        d_en = d.get("district_english", "")
        d_ta = d.get("district_tamil", "")
        region = d.get("region_en") or d.get("region", "")
        region_ta = d.get("region_ta") or region

        # 1. District direct match
        if (query in d_en.lower() or query in d_ta.lower() or any(query == a.lower() for a in d.get("search_aliases", []))):
            if d_no not in seen_districts:
                grouped["districts"].append({
                    "title": d_en,
                    "title_ta": d_ta,
                    "district_no": d_no,
                    "region": region,
                    "region_ta": region_ta,
                    "type": "district",
                    "subtitle": f"District #{d_no} • {region}",
                    "subtitle_ta": f"மாவட்டம் #{d_no} • {region_ta}"
                })
                seen_districts.add(d_no)

        # 2. Historical / Ancient Name match
        former_en = d.get("former_administrative_name_history_en") or d.get("former_administrative_name_history", "")
        former_ta = d.get("former_administrative_name_history_ta", "")
        ancient_en = d.get("ancient_or_historical_name_context_en") or d.get("ancient_or_historical_name_context", "")
        ancient_ta = d.get("ancient_or_historical_name_context_ta", "")

        matched_hist = None
        # Check aliases first for concise title
        for alias in d.get("search_aliases", []):
            if query in alias.lower():
                matched_hist = (alias, alias, "Historical Alias / Variant", "வரலாற்று மாற்றுப் பெயர்")
                break

        if not matched_hist:
            if query in former_en.lower() or query in former_ta.lower():
                short_desc = former_en.split(";")[0].split(".")[0].strip()
                short_desc_ta = former_ta.split(";")[0].split(".")[0].strip() if former_ta else short_desc
                matched_hist = (short_desc, short_desc_ta, "Former Administrative Name", "முந்தைய நிர்வாகப் பெயர்")
            elif query in ancient_en.lower() or query in ancient_ta.lower():
                short_desc = ancient_en.split(";")[0].split(".")[0].strip()
                short_desc_ta = ancient_ta.split(";")[0].split(".")[0].strip() if ancient_ta else short_desc
                matched_hist = (short_desc, short_desc_ta, "Ancient Historical Context", "பண்டைய வரலாற்றுப் பெயர்")

        if matched_hist and d_no not in seen_history:
            grouped["historical_names"].append({
                "title": matched_hist[0],
                "title_ta": matched_hist[1],
                "district_no": d_no,
                "district_name": d_en,
                "district_name_ta": d_ta,
                "category": matched_hist[2],
                "category_ta": matched_hist[3],
                "type": "historical_name",
                "subtitle": f"Historical record for {d_en} (#{d_no})",
                "subtitle_ta": f"{d_ta} (#{d_no}) மாவட்டத்தின் வரலாற்றுப் பதிவு"
            })
            seen_history.add(d_no)

        # 3. Famous Places & Specialities
        for s in d.get("specialities", []):
            s_en = s.get("name_en", "")
            s_ta = s.get("name_ta", "")
            if query in s_en.lower() or query in s_ta.lower():
                key = (d_no, s_en)
                if key not in seen_places:
                    grouped["heritage_places"].append({
                        "title": s_en,
                        "title_ta": s_ta,
                        "district_no": d_no,
                        "district_name": d_en,
                        "district_name_ta": d_ta,
                        "category": s.get("category_en", "Speciality"),
                        "category_ta": s.get("category_ta", "சிறப்பம்சம்"),
                        "type": "speciality",
                        "subtitle": f"Speciality in {d_en} (#{d_no})",
                        "subtitle_ta": f"{d_ta} (#{d_no}) மாவட்டத்தின் சிறப்பம்சம்"
                    })
                    seen_places.add(key)
                if len(grouped["heritage_places"]) >= 5:
                    break

        for p in d.get("famous_places", []):
            p_en = p.get("name_en", "")
            p_ta = p.get("name_ta", "")
            if query in p_en.lower() or query in p_ta.lower():
                key = (d_no, p_en)
                if key not in seen_places:
                    grouped["heritage_places"].append({
                        "title": p_en,
                        "title_ta": p_ta,
                        "district_no": d_no,
                        "district_name": d_en,
                        "district_name_ta": d_ta,
                        "category": p.get("category_en", "Heritage Site"),
                        "category_ta": p.get("category_ta", "வரலாற்றுத் தலம்"),
                        "type": "famous_place",
                        "subtitle": f"Heritage site in {d_en} (#{d_no})",
                        "subtitle_ta": f"{d_ta} (#{d_no}) வரலாற்றுத் தலம்"
                    })
                    seen_places.add(key)
                if len(grouped["heritage_places"]) >= 6:
                    break

    # Cap suggestions for crisp, fast display
    grouped["districts"] = grouped["districts"][:5]
    grouped["historical_names"] = grouped["historical_names"][:5]
    grouped["heritage_places"] = grouped["heritage_places"][:5]

    total_matches = len(grouped["districts"]) + len(grouped["historical_names"]) + len(grouped["heritage_places"])
    return {
        "query": q,
        "total_matches": total_matches,
        "suggestions": grouped
    }


@router.get("/{identifier}", response_model=Dict[str, Any])
def get_district_by_id_or_name(identifier: str):
    """Get single district profile by number (1-38) or name (English or Tamil)."""
    data = load_district_data()
    districts = data.get("districts", [])
    
    # Try by numeric No.
    if identifier.isdigit():
        target_no = int(identifier)
        for d in districts:
            if d.get("no") == target_no:
                return d
                
    # Try by name
    target_clean = identifier.strip().lower()
    for d in districts:
        if (d.get("district_english", "").lower() == target_clean or 
            d.get("district_tamil", "").strip() == identifier.strip() or
            any(target_clean == a.lower() for a in d.get("search_aliases", []))):
            return d
            
    raise HTTPException(status_code=404, detail="District not found in 38 Tamil Nadu districts registry")
