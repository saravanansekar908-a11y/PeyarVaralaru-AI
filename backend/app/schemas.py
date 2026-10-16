"""
Pydantic schemas for request/response validation.
"""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any


# --- Source ---
class SourceOut(BaseModel):
    id: Optional[int] = None
    title: str
    title_tamil: Optional[str] = None
    publisher: Optional[str] = None
    source_url: Optional[str] = None
    document_identifier: Optional[str] = None
    publication_date: Optional[str] = None
    page_number: Optional[str] = None
    evidence_excerpt: Optional[str] = None
    evidence_excerpt_tamil: Optional[str] = None

    class Config:
        from_attributes = True


# --- Historical Name ---
class HistoricalNameOut(BaseModel):
    id: Optional[int] = None
    place_id: Optional[int] = None
    name: str
    language: Optional[str] = None
    name_type: Optional[str] = None
    valid_from: Optional[str] = None
    valid_to: Optional[str] = None

    class Config:
        from_attributes = True


# --- Event ---
class EventOut(BaseModel):
    id: Optional[int] = None
    place_id: Optional[int] = None
    event_type: str
    event_date: Optional[str] = None
    date_precision: Optional[str] = None
    description: Optional[str] = None
    description_tamil: Optional[str] = None
    evidence_status: str = "unverified"
    sources: List[SourceOut] = []

    class Config:
        from_attributes = True


# --- Documents & RAG Passages ---
class DocumentPassageOut(BaseModel):
    id: Optional[int] = None
    document_id: Optional[int] = None
    document_title: Optional[str] = None
    author_or_authority: Optional[str] = None
    publication_year: Optional[str] = None
    page_number: Optional[str] = None
    passage_text: str
    passage_text_tamil: Optional[str] = None
    place_name: Optional[str] = None
    district: Optional[str] = None
    taluk: Optional[str] = None
    topic: Optional[str] = None
    evidence_level: str = "documented_fact"  # documented_fact | scholarly_hypothesis | traditional_explanation | unknown_origin

    class Config:
        from_attributes = True


class DocumentOut(BaseModel):
    id: int
    title: str
    title_tamil: Optional[str] = None
    author_or_authority: Optional[str] = None
    publication_year: Optional[str] = None
    source_url: Optional[str] = None
    document_type: Optional[str] = None
    access_date: Optional[str] = None
    total_pages: Optional[int] = 1
    passages_count: Optional[int] = 0
    passages: List[DocumentPassageOut] = []

    class Config:
        from_attributes = True


class PassageIngestItem(BaseModel):
    page_number: Optional[str] = None
    passage_text: str
    passage_text_tamil: Optional[str] = None
    place_name: Optional[str] = None
    district: Optional[str] = None
    taluk: Optional[str] = None
    topic: Optional[str] = "name_origin"
    evidence_level: Optional[str] = "documented_fact"


class DocumentIngestRequest(BaseModel):
    title: str
    title_tamil: Optional[str] = None
    author_or_authority: Optional[str] = None
    publication_year: Optional[str] = None
    source_url: Optional[str] = None
    document_type: Optional[str] = "gazetteer"
    access_date: Optional[str] = None
    raw_text: Optional[str] = None
    passages: Optional[List[PassageIngestItem]] = None


class DocumentIngestResponse(BaseModel):
    status: str
    document_id: int
    title: str
    total_passages: int
    message: str


class EvidenceClassificationOut(BaseModel):
    documented_facts: List[str] = []
    scholarly_hypotheses: List[str] = []
    traditional_explanations: List[str] = []
    unknown_origins: List[str] = []


# --- Place ---
class PlaceSummary(BaseModel):
    id: int
    current_name: str
    current_name_tamil: Optional[str] = None
    state: Optional[str] = "Tamil Nadu"
    state_tamil: Optional[str] = "தமிழ்நாடு"
    district: Optional[str] = None
    district_tamil: Optional[str] = None
    taluk: Optional[str] = None
    taluk_tamil: Optional[str] = None
    village: Optional[str] = None
    village_tamil: Optional[str] = None
    category: Optional[str] = None
    category_tamil: Optional[str] = None
    description: Optional[str] = None
    description_tamil: Optional[str] = None
    name_origin_type: Optional[str] = "documented_fact"
    evidence_status: Optional[str] = "verified"
    is_cached_research: Optional[bool] = False
    historical_names: List[HistoricalNameOut] = []
    match_reason: Optional[str] = None
    # Structured source-grounded research fields
    place_name_tamil: Optional[str] = None
    place_name_english: Optional[str] = None
    historical_period: Optional[str] = None
    name_origin_explanation: Optional[str] = None
    origin_evidence_status: Optional[str] = None  # historically_documented | scholarly_interpretation | local_tradition | unknown_origin
    historical_events_summary: Optional[str] = None
    source_title: Optional[str] = None
    source_url: Optional[str] = None
    source_page: Optional[str] = None
    evidence_quote: Optional[str] = None
    verification_status: Optional[str] = None  # verified | partially_verified | unverified

    class Config:
        from_attributes = True


class PlaceDetail(BaseModel):
    id: int
    current_name: str
    current_name_tamil: Optional[str] = None
    state: Optional[str] = "Tamil Nadu"
    state_tamil: Optional[str] = "தமிழ்நாடு"
    district: Optional[str] = None
    district_tamil: Optional[str] = None
    taluk: Optional[str] = None
    taluk_tamil: Optional[str] = None
    village: Optional[str] = None
    village_tamil: Optional[str] = None
    category: Optional[str] = None
    category_tamil: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    description: Optional[str] = None
    description_tamil: Optional[str] = None
    meaning_tamil: Optional[str] = None
    origin_tamil: Optional[str] = None
    name_origin_type: Optional[str] = "documented_fact"
    evidence_status: Optional[str] = "verified"
    is_cached_research: Optional[bool] = False
    last_researched_at: Optional[str] = None
    historical_names: List[HistoricalNameOut] = []
    events: List[EventOut] = []
    passages: List[DocumentPassageOut] = []
    # Structured source-grounded research fields
    place_name_tamil: Optional[str] = None
    place_name_english: Optional[str] = None
    historical_period: Optional[str] = None
    name_origin_explanation: Optional[str] = None
    origin_evidence_status: Optional[str] = None  # historically_documented | scholarly_interpretation | local_tradition | unknown_origin
    historical_events_summary: Optional[str] = None
    source_title: Optional[str] = None
    source_url: Optional[str] = None
    source_page: Optional[str] = None
    evidence_quote: Optional[str] = None
    verification_status: Optional[str] = None  # verified | partially_verified | unverified

    class Config:
        from_attributes = True


# --- Ambiguity & Research ---
class AmbiguityCandidate(BaseModel):
    canonical_name: str
    canonical_name_tamil: str
    district: str
    district_tamil: str
    taluk: Optional[str] = None
    taluk_tamil: Optional[str] = None
    category: Optional[str] = None
    category_tamil: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    description: Optional[str] = None
    description_tamil: Optional[str] = None


class HistoricalReport(BaseModel):
    raw_markdown: str
    ai_generated: bool = False
    evidence_status: str = "verified"
    sources: List[SourceOut] = []
    passages: List[DocumentPassageOut] = []
    evidence_classification: Optional[EvidenceClassificationOut] = None
    place_name: Optional[str] = None
    district: Optional[str] = None


class ResearchRequest(BaseModel):
    place_name: str
    district: Optional[str] = None
    language: str = "ta"  # "ta" for Tamil, "en" for English


class ResearchResponse(BaseModel):
    status: str  # success | ambiguous | error | not_found
    query: str
    language: str = "ta"
    is_ambiguous: bool = False
    candidates: List[AmbiguityCandidate] = []
    message: Optional[str] = None
    place: Optional[PlaceDetail] = None
    report: Optional[HistoricalReport] = None
    raw_markdown: Optional[str] = None
    source_type: str = "local_database"  # database_verified | cached_research | live_research | ambiguous_resolution
    ai_generated: bool = False


# --- Ask AI ---
class AskRequest(BaseModel):
    question: str
    district: Optional[str] = None
    language: str = "ta"  # "ta" for Tamil, "en" for English


class AskResponse(BaseModel):
    answer: str
    sources_used: List[SourceOut] = []
    passages_used: List[DocumentPassageOut] = []
    places_found: List[PlaceSummary] = []
    evidence_classification: Optional[EvidenceClassificationOut] = None
    ai_generated: bool = False
    fallback: bool = False
    identified_place: Optional[str] = None
    evidence_status: Optional[str] = None
    is_uncertain: Optional[bool] = False


# --- Graph ---
class GraphNode(BaseModel):
    id: str
    label: str
    type: str  # place | historical_name | event | source
    data: dict = {}


class GraphEdge(BaseModel):
    id: str
    source: str
    target: str
    label: str  # HAS_HISTORICAL_NAME | CHANGED_ON | SUPPORTED_BY


class GraphData(BaseModel):
    nodes: List[GraphNode]
    edges: List[GraphEdge]


# --- Health ---
class HealthResponse(BaseModel):
    status: str
    database: str
    gemini_available: bool
    version: str


# --- Historical Maps & Comparison Observations ---
class MapObservationOut(BaseModel):
    id: Optional[int] = None
    map_id: int
    place_name: str
    category: str
    title: str
    title_tamil: Optional[str] = None
    observation_text: str
    observation_text_tamil: Optional[str] = None
    evidence_type: str = "verified_archival_finding"
    historical_year_ref: Optional[str] = None
    modern_comparison: Optional[str] = None
    modern_comparison_tamil: Optional[str] = None
    source_citation: Optional[str] = None
    source_url: Optional[str] = None
    coordinates_json: Optional[str] = None
    verification_status: str = "verified"

    class Config:
        from_attributes = True


class HistoricalMapOut(BaseModel):
    id: int
    title: str
    title_tamil: Optional[str] = None
    place_name: str
    place_name_tamil: Optional[str] = None
    district: str
    district_tamil: Optional[str] = None
    historical_period: Optional[str] = None
    year_start: Optional[int] = None
    year_end: Optional[int] = None
    creator: Optional[str] = None
    creator_tamil: Optional[str] = None
    source_name: Optional[str] = None
    source_url: Optional[str] = None
    image_url: str
    map_service_url: Optional[str] = None
    license_info: Optional[str] = None
    georeferencing_status: str = "georeferenced"
    bounds_json: Optional[str] = None
    center_lat: float = 13.0827
    center_lng: float = 80.2707
    default_zoom: int = 13
    scale: Optional[str] = None
    description: Optional[str] = None
    description_tamil: Optional[str] = None
    limitations: Optional[str] = None
    limitations_tamil: Optional[str] = None
    verification_status: str = "verified"
    observations_count: Optional[int] = 0

    class Config:
        from_attributes = True


class HistoricalMapDetailOut(HistoricalMapOut):
    observations: List[MapObservationOut] = []


