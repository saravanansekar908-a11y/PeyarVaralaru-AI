"""
PeyarVaralaru AI — Documents & Ingestion API Routes
Allows adding new historical documents (Gazetteers, Inscriptions, G.O.s, Census directories)
and immediately searching them without model retraining.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db, Document, DocumentPassage
from app.schemas import (
    DocumentOut,
    DocumentPassageOut,
    DocumentIngestRequest,
    DocumentIngestResponse
)
from app.services.ingestion_service import ingest_document
from app.services.rag_service import search_local_passages

router = APIRouter(prefix="/api/documents", tags=["documents"])


@router.get("", response_model=List[DocumentOut])
def list_documents(db: Session = Depends(get_db)):
    """List all ingested historical research documents with metadata."""
    docs = db.query(Document).order_by(Document.id.desc()).all()
    results = []
    for d in docs:
        results.append(
            DocumentOut(
                id=d.id,
                title=d.title,
                title_tamil=d.title_tamil,
                author_or_authority=d.author_or_authority,
                publication_year=d.publication_year,
                source_url=d.source_url,
                document_type=d.document_type,
                access_date=d.access_date,
                total_pages=d.total_pages or 1,
                passages_count=len(d.passages),
                passages=[]  # keep list light; fetch passages via detailed endpoint
            )
        )
    return results


@router.get("/search/passages", response_model=List[DocumentPassageOut])
def search_passages(
    q: str = Query(..., description="Place name or search query"),
    district: Optional[str] = Query(None, description="Optional district filter"),
    db: Session = Depends(get_db)
):
    """Search passages directly using RAG local collection search."""
    passages = search_local_passages(db, query=q, district=district, top_k=10)
    return [
        DocumentPassageOut(
            id=p["passage_id"],
            document_id=p["document_id"],
            document_title=p["document_title"],
            author_or_authority=p["author_or_authority"],
            publication_year=p["publication_year"],
            page_number=p["page_number"],
            passage_text=p["passage_text"],
            passage_text_tamil=p["passage_text_tamil"],
            place_name=p["place_name"],
            district=p["district"],
            taluk=p["taluk"],
            topic=p["topic"],
            evidence_level=p["evidence_level"],
        )
        for p in passages
    ]


@router.get("/{document_id}/passages", response_model=List[DocumentPassageOut])
def get_document_passages(document_id: int, db: Session = Depends(get_db)):
    """Retrieve all extracted passage chunks for a specific document."""
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    return [
        DocumentPassageOut(
            id=p.id,
            document_id=doc.id,
            document_title=doc.title,
            author_or_authority=doc.author_or_authority,
            publication_year=doc.publication_year,
            page_number=p.page_number,
            passage_text=p.passage_text,
            passage_text_tamil=p.passage_text_tamil,
            place_name=p.place_name,
            district=p.district,
            taluk=p.taluk,
            topic=p.topic,
            evidence_level=p.evidence_level,
        )
        for p in doc.passages
    ]


@router.post("/ingest", response_model=DocumentIngestResponse)
def ingest_new_document(req: DocumentIngestRequest, db: Session = Depends(get_db)):
    """
    Ingest a new historical document into SQLite.
    Allows zero-retraining real-time additions to the research system.
    """
    passages_payload = None
    if req.passages:
        passages_payload = [p.model_dump() for p in req.passages]

    doc, total_added = ingest_document(
        db=db,
        title=req.title,
        title_tamil=req.title_tamil,
        author_or_authority=req.author_or_authority,
        publication_year=req.publication_year,
        source_url=req.source_url,
        document_type=req.document_type or "gazetteer",
        access_date=req.access_date,
        raw_text=req.raw_text,
        passages_list=passages_payload
    )

    return DocumentIngestResponse(
        status="success",
        document_id=doc.id,
        title=doc.title,
        total_passages=total_added,
        message=f"Document '{doc.title}' successfully ingested with {total_added} searchable passages."
    )
