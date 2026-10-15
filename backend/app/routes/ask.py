"""
AI Question Answering route.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import AskRequest, AskResponse, SourceOut, PlaceSummary, HistoricalNameOut
from app.services.ai_service import ask_question

router = APIRouter(prefix="/api", tags=["ai"])


@router.post("/ask", response_model=AskResponse)
def ask_ai(req: AskRequest, db: Session = Depends(get_db)):
    """Ask a historical question. Uses Gemini + database evidence or fallback."""
    result = ask_question(db, req.question, req.language)

    return AskResponse(
        answer=result["answer"],
        sources_used=[SourceOut.model_validate(s) for s in result["sources_used"]],
        places_found=[
            PlaceSummary(
                id=p.id,
                current_name=p.current_name,
                current_name_tamil=p.current_name_tamil,
                district=p.district,
                description=p.description,
                description_tamil=p.description_tamil,
                historical_names=[
                    HistoricalNameOut.model_validate(hn) for hn in p.historical_names
                ],
            )
            for p in result["places_found"]
        ],
        ai_generated=result["ai_generated"],
        fallback=result["fallback"],
    )
