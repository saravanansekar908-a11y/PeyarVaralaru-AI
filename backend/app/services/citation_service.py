"""
PeyarVaralaru AI — Citation Service
Validates, deduplicates, and formats historical source references and citations.
Ensures source ground truth and accurate evidence status.
"""
from typing import List, Dict, Any, Optional


def classify_evidence_status(
    has_go_or_gazette: bool = False,
    has_inscription: bool = False,
    has_secondary_gazetteer: bool = False,
    is_oral_tradition: bool = False,
    has_conflicting_claims: bool = False
) -> str:
    """
    Classifies evidence status based on historical methodology:
    - verified: Documented by confirmed Government Order, Gazette, or primary published Inscription.
    - partially_verified: Documented in district gazetteer, colonial manual, or academic publication without primary legislative/epigraphical proof.
    - unverified: Oral tradition, popular folklore, or plausible hypothesis without primary archive document.
    - disputed: Competing claims or contradictory historical origins.
    """
    if has_conflicting_claims:
        return "disputed"
    if has_go_or_gazette or has_inscription:
        return "verified"
    if has_secondary_gazetteer:
        return "partially_verified"
    return "unverified"


def validate_and_clean_source(src: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validates source dictionary structure, assigns default fields if missing,
    and strips spurious whitespace.
    """
    title = (src.get("title") or "Historical Archive Document").strip()
    title_ta = (src.get("title_tamil") or title).strip()
    publisher = (src.get("publisher") or "Tamil Nadu Archives / Government Records").strip()
    doc_id = src.get("document_identifier")
    if doc_id:
        doc_id = str(doc_id).strip()

    pub_date = src.get("publication_date")
    if pub_date:
        pub_date = str(pub_date).strip()

    page_no = src.get("page_number")
    if page_no:
        page_no = str(page_no).strip()

    source_url = src.get("source_url")
    if source_url:
        source_url = str(source_url).strip()

    excerpt = src.get("evidence_excerpt")
    if excerpt:
        excerpt = str(excerpt).strip()

    excerpt_ta = src.get("evidence_excerpt_tamil")
    if excerpt_ta:
        excerpt_ta = str(excerpt_ta).strip()

    return {
        "title": title,
        "title_tamil": title_ta,
        "publisher": publisher,
        "source_url": source_url,
        "document_identifier": doc_id,
        "publication_date": pub_date,
        "page_number": page_no,
        "evidence_excerpt": excerpt,
        "evidence_excerpt_tamil": excerpt_ta,
    }


def format_citation_tamil(src: Dict[str, Any]) -> str:
    """Format single source reference into natural academic Tamil bibliography string."""
    parts = []
    title = src.get("title_tamil") or src.get("title")
    parts.append(f"**{title}**")

    meta = []
    if src.get("publisher"):
        meta.append(src["publisher"])
    if src.get("publication_date"):
        meta.append(f"வெளியீடு: {src['publication_date']}")
    if src.get("document_identifier"):
        meta.append(f"ஆவண எண்: {src['document_identifier']}")
    if src.get("page_number"):
        meta.append(f"பக்கம்: {src['page_number']}")

    if meta:
        parts.append(f"({', '.join(meta)})")

    if src.get("source_url"):
        parts.append(f"[ஆவண இணைப்பு]({src['source_url']})")

    if src.get("evidence_excerpt_tamil") or src.get("evidence_excerpt"):
        excerpt = src.get("evidence_excerpt_tamil") or src.get("evidence_excerpt")
        parts.append(f"\n> சான்றுப் பகுதி: *\"{excerpt}\"*")

    return " ".join(parts)


def format_citation_english(src: Dict[str, Any]) -> str:
    """Format single source reference into academic English bibliography string."""
    parts = []
    title = src.get("title") or src.get("title_tamil")
    parts.append(f"**{title}**")

    meta = []
    if src.get("publisher"):
        meta.append(src["publisher"])
    if src.get("publication_date"):
        meta.append(f"Pub: {src['publication_date']}")
    if src.get("document_identifier"):
        meta.append(f"Doc ID: {src['document_identifier']}")
    if src.get("page_number"):
        meta.append(f"p. {src['page_number']}")

    if meta:
        parts.append(f"({', '.join(meta)})")

    if src.get("source_url"):
        parts.append(f"[Source Link]({src['source_url']})")

    if src.get("evidence_excerpt"):
        parts.append(f"\n> Excerpt: *\"{src['evidence_excerpt']}\"*")

    return " ".join(parts)
