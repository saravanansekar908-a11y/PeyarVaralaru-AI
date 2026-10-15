"""
PeyarVaralaru AI — Research-Data Ingestion Service
Handles ingestion of:
1. Tamil Nadu District Gazetteers
2. Official Archaeological Publications & Epigraphia Indica / South Indian Inscriptions
3. Government Records and Gazette Notifications (G.O.s)
4. Census of India Village and Town Directories
Extracts searchable text from PDF and text sources with OCR fallback for scanned pages.
Stores title, author/issuing authority, publication year, URL, page number, extracted text, and access date.
"""
import os
import re
import datetime
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy.orm import Session

from app.database import Document, DocumentPassage, SessionLocal
from app.services.place_resolver import TN_DISTRICTS, clean_place_query

# Optional pypdf import
try:
    from pypdf import PdfReader
    _pypdf_available = True
except ImportError:
    _pypdf_available = False

# Optional pytesseract for OCR of scanned pages
try:
    import pytesseract
    from PIL import Image
    _ocr_available = True
except ImportError:
    _ocr_available = False


def extract_text_from_pdf(pdf_path: str) -> List[Dict[str, Any]]:
    """
    Extracts text page-by-page from a PDF file.
    If a page has no selectable text (scanned document), attempts OCR fallback.
    """
    if not _pypdf_available:
        raise RuntimeError("pypdf is not installed. Please install pypdf to process PDF files.")

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    reader = PdfReader(pdf_path)
    extracted_pages = []

    for idx, page in enumerate(reader.pages):
        page_num = f"p. {idx + 1}"
        text = page.extract_text() or ""
        text = text.strip()

        # Check if the page is scanned (empty or minimal text)
        is_scanned = len(text) < 20
        if is_scanned and _ocr_available:
            try:
                # Attempt OCR on images inside the page if any
                ocr_text = []
                for img_obj in page.images:
                    img_bytes = img_obj.data
                    import io
                    pil_img = Image.open(io.BytesIO(img_bytes))
                    t = pytesseract.image_to_string(pil_img)
                    if t.strip():
                        ocr_text.append(t.strip())
                if ocr_text:
                    text = "\n".join(ocr_text)
                    is_scanned = False
            except Exception:
                pass

        if is_scanned and not text:
            text = f"[Scanned Page {idx + 1} — Historical Archival Document]"

        extracted_pages.append({
            "page_number": page_num,
            "text": text,
            "is_scanned": is_scanned
        })

    return extracted_pages


def extract_text_from_file(file_path: str) -> List[Dict[str, Any]]:
    """Extracts text from PDF, TXT, or Markdown documents."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext in [".txt", ".md", ".json"]:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        
        # Split into logical sections/pages by markdown headers or page delimiters
        chunks = re.split(r'\n(?=#{1,3}\s+|---|\f|Page\s+\d+)', content)
        pages = []
        for i, chunk in enumerate(chunks):
            if chunk.strip():
                pages.append({
                    "page_number": f"Section {i + 1}",
                    "text": chunk.strip(),
                    "is_scanned": False
                })
        return pages if pages else [{"page_number": "p. 1", "text": content.strip(), "is_scanned": False}]
    else:
        raise ValueError(f"Unsupported file format: {ext}")


def detect_evidence_level(text: str) -> str:
    """
    Classifies the passage text into the 4 strict evidence tiers:
    1. documented_fact: Epigraphy, stone inscriptions, copper plates, G.O., gazetteer records
    2. scholarly_hypothesis: Linguistic derivations, academic theories, etymology proposals
    3. traditional_explanation: Sthala puranas, folk legends, oral traditions
    4. unknown_origin: Explicitly uncertain, disputed, or lack of records
    """
    t_lower = text.lower()
    
    # 4. Unknown / Uncertain
    if any(k in t_lower for k in [
        "uncertain", "unknown origin", "not documented", "obscure", "no record",
        "நிச்சயமற்ற", "சான்றுகள் இல்லை", "தெரியவில்லை", "தெளிவற்ற"
    ]):
        return "unknown_origin"
    
    # 3. Traditional / Folk
    if any(k in t_lower for k in [
        "legend", "mythology", "tradition", "folklore", "oral tradition", "purana", "sthala purana",
        "வாய்வழி மரபு", "செவிவழி", "புராண", "ஐதீகம்", "தலபுராணம்"
    ]):
        return "traditional_explanation"
        
    # 2. Scholarly Hypothesis
    if any(k in t_lower for k in [
        "hypothesis", "linguist", "theorized", "suggested by", "etymologist", "derived perhaps",
        "அறிஞர்கள் கருதுகின்றனர்", "கோட்பாடு", "கருதுகோள்", "மொழி ஆய்வாளர்"
    ]):
        return "scholarly_hypothesis"
        
    # 1. Documented Fact (default for gazetteers and inscriptions)
    return "documented_fact"


def ingest_document(
    db: Session,
    title: str,
    title_tamil: Optional[str] = None,
    author_or_authority: Optional[str] = None,
    publication_year: Optional[str] = None,
    source_url: Optional[str] = None,
    document_type: str = "gazetteer",
    access_date: Optional[str] = None,
    file_path: Optional[str] = None,
    raw_text: Optional[str] = None,
    passages_list: Optional[List[Dict[str, Any]]] = None,
) -> Tuple[Document, int]:
    """
    Persists document metadata and extracted searchable passages in SQLite.
    Allows continuous additions of new documents without retraining.
    """
    if not access_date:
        access_date = datetime.date.today().isoformat()

    # Check if document already exists
    doc = db.query(Document).filter(Document.title == title).first()
    if not doc:
        doc = Document(
            title=title,
            title_tamil=title_tamil,
            author_or_authority=author_or_authority,
            publication_year=str(publication_year) if publication_year else None,
            source_url=source_url,
            document_type=document_type,
            access_date=access_date,
            file_path=file_path,
            full_text=raw_text or "",
            total_pages=1,
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)
    else:
        # Update metadata if existing
        if title_tamil: doc.title_tamil = title_tamil
        if author_or_authority: doc.author_or_authority = author_or_authority
        if publication_year: doc.publication_year = str(publication_year)
        if source_url: doc.source_url = source_url
        if access_date: doc.access_date = access_date
        db.commit()

    total_passages_added = 0

    # Case A: Explicit structured passages provided
    if passages_list:
        for p in passages_list:
            p_text = p.get("passage_text", "").strip()
            if not p_text:
                continue
            
            # Auto-detect evidence level if not specified
            e_level = p.get("evidence_level") or detect_evidence_level(p_text)
            
            # Check for existing duplicate passage in this document
            existing_p = db.query(DocumentPassage).filter(
                DocumentPassage.document_id == doc.id,
                DocumentPassage.page_number == p.get("page_number"),
                DocumentPassage.place_name == p.get("place_name")
            ).first()

            if not existing_p:
                dp = DocumentPassage(
                    document_id=doc.id,
                    page_number=p.get("page_number", "p. 1"),
                    passage_text=p_text,
                    passage_text_tamil=p.get("passage_text_tamil"),
                    place_name=p.get("place_name"),
                    district=p.get("district"),
                    taluk=p.get("taluk"),
                    topic=p.get("topic", "name_origin"),
                    evidence_level=e_level,
                )
                db.add(dp)
                total_passages_added += 1
            else:
                # Update existing passage
                existing_p.passage_text = p_text
                if p.get("passage_text_tamil"):
                    existing_p.passage_text_tamil = p.get("passage_text_tamil")
                existing_p.evidence_level = e_level
                total_passages_added += 1

    # Case B: File path provided (PDF, TXT, MD)
    elif file_path and os.path.exists(file_path):
        extracted_pages = extract_text_from_file(file_path)
        doc.total_pages = len(extracted_pages)
        db.commit()

        for page in extracted_pages:
            p_text = page.get("text", "").strip()
            if not p_text:
                continue
                
            e_level = detect_evidence_level(p_text)
            dp = DocumentPassage(
                document_id=doc.id,
                page_number=page.get("page_number", "p. 1"),
                passage_text=p_text,
                evidence_level=e_level,
                topic="gazetteer_excerpt"
            )
            db.add(dp)
            total_passages_added += 1

    # Case C: Raw text provided directly
    elif raw_text:
        dp = DocumentPassage(
            document_id=doc.id,
            page_number="p. 1",
            passage_text=raw_text.strip(),
            evidence_level=detect_evidence_level(raw_text),
            topic="general_record"
        )
        db.add(dp)
        total_passages_added += 1

    db.commit()
    return doc, total_passages_added
