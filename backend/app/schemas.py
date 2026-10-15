"""
Pydantic schemas for request/response validation.
"""
from pydantic import BaseModel
from typing import Optional, List


# --- Source ---
class SourceOut(BaseModel):
    id: int
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
    id: int
    place_id: int
    name: str
    language: Optional[str] = None
    name_type: Optional[str] = None
    valid_from: Optional[str] = None
    valid_to: Optional[str] = None

    class Config:
        from_attributes = True


# --- Event ---
class EventOut(BaseModel):
    id: int
    place_id: int
    event_type: str
    event_date: Optional[str] = None
    date_precision: Optional[str] = None
    description: Optional[str] = None
    description_tamil: Optional[str] = None
    evidence_status: str = "unverified"
    sources: List[SourceOut] = []

    class Config:
        from_attributes = True


# --- Place ---
class PlaceSummary(BaseModel):
    id: int
    current_name: str
    current_name_tamil: Optional[str] = None
    district: Optional[str] = None
    description: Optional[str] = None
    description_tamil: Optional[str] = None
    historical_names: List[HistoricalNameOut] = []
    match_reason: Optional[str] = None  # Only in search results

    class Config:
        from_attributes = True


class PlaceDetail(BaseModel):
    id: int
    current_name: str
    current_name_tamil: Optional[str] = None
    district: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    description: Optional[str] = None
    description_tamil: Optional[str] = None
    historical_names: List[HistoricalNameOut] = []
    events: List[EventOut] = []

    class Config:
        from_attributes = True


# --- Ask AI ---
class AskRequest(BaseModel):
    question: str
    language: str = "ta"  # "ta" for Tamil, "en" for English


class AskResponse(BaseModel):
    answer: str
    sources_used: List[SourceOut] = []
    places_found: List[PlaceSummary] = []
    ai_generated: bool = False
    fallback: bool = False


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
