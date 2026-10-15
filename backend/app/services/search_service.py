"""
Backward compatibility layer for search_service.
Redirects to local_search.
"""
from app.services.local_search import (
    normalize_text,
    search_local_places as search_places,
    get_place_by_id
)

__all__ = ["normalize_text", "search_places", "get_place_by_id"]
