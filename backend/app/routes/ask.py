"""
AI Question Answering route using universal place research pipeline.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import (
    AskRequest, 
    AskResponse, 
    SourceOut, 
    DocumentPassageOut,
    EvidenceClassificationOut,
    PlaceSummary, 
    HistoricalNameOut
)
from app.services.history_research import ask_place_question

router = APIRouter(prefix="/api", tags=["ai"])


@router.post("/ask", response_model=AskResponse)
def ask_ai(req: AskRequest, db: Session = Depends(get_db)):
    """
    Ask a historical place question using source-grounded RAG.
    Workflow:
    User Question -> Place & District Resolution -> Local Document Passages Search ->
    4-Tier Evidence Classification -> Gemini AI Synthesis in Tamil ->
    Cited Passage Footnotes.
    """
    result = ask_place_question(
        db=db,
        question=req.question,
        district_hint=req.district,
        language=req.language
    )

    sources_out = []
    for s in result.get("sources_used", []):
        sources_out.append(SourceOut.model_validate(s))

    passages_out = []
    for p in result.get("passages_used", []):
        passages_out.append(
            DocumentPassageOut(
                id=p.get("passage_id") or p.get("id"),
                document_id=p.get("document_id"),
                document_title=p.get("document_title"),
                author_or_authority=p.get("author_or_authority"),
                publication_year=p.get("publication_year"),
                page_number=p.get("page_number"),
                passage_text=p.get("passage_text", ""),
                passage_text_tamil=p.get("passage_text_tamil"),
                place_name=p.get("place_name"),
                district=p.get("district"),
                taluk=p.get("taluk"),
                topic=p.get("topic"),
                evidence_level=p.get("evidence_level", "documented_fact"),
            )
        )

    e_class = None
    if result.get("evidence_classification"):
        e_class = EvidenceClassificationOut(**result["evidence_classification"])

    places_out = []
    for p in result.get("places_found", []):
        places_out.append(
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
        )

    return AskResponse(
        answer=result.get("answer", ""),
        sources_used=sources_out,
        passages_used=passages_out,
        places_found=places_out,
        evidence_classification=e_class,
        ai_generated=result.get("ai_generated", False),
        fallback=result.get("fallback", False),
        identified_place=result.get("identified_place"),
        evidence_status=result.get("evidence_status"),
        is_uncertain=result.get("is_uncertain", False)
    )
