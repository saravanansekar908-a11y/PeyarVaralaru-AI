"""
AI service — Gemini-powered historical Q&A with evidence grounding.
Falls back to database-only answers when API is unavailable.
"""
import os
from typing import List, Optional
from sqlalchemy.orm import Session
from app.database import Place, HistoricalName, Event, Source, event_sources
from app.services.search_service import normalize_text, search_places

# Try importing Gemini SDK
_gemini_available = False
_gemini_client = None

try:
    from google import genai
    api_key = os.getenv("GEMINI_API_KEY", "")
    if api_key:
        _gemini_client = genai.Client(api_key=api_key)
        _gemini_available = True
except Exception:
    pass


def is_gemini_available() -> bool:
    return _gemini_available


def _build_context(places: List[Place], db: Session) -> str:
    """Build evidence context from database records."""
    context_parts = []
    for place in places:
        lines = [f"Place: {place.current_name} ({place.current_name_tamil or ''})"]
        if place.district:
            lines.append(f"  District: {place.district}")
        if place.description:
            lines.append(f"  Description: {place.description}")

        # Historical names
        for hn in place.historical_names:
            lines.append(f"  Historical Name: {hn.name} (Language: {hn.language}, Type: {hn.name_type}, From: {hn.valid_from or 'Unknown'}, To: {hn.valid_to or 'Unknown'})")

        # Events and sources
        for evt in place.events:
            lines.append(f"  Event: {evt.event_type} — {evt.description}")
            lines.append(f"    Date: {evt.event_date or 'Unknown'} (Precision: {evt.date_precision})")
            lines.append(f"    Evidence Status: {evt.evidence_status}")
            for src in evt.sources:
                lines.append(f"    Source: {src.title}")
                if src.document_identifier:
                    lines.append(f"      Document: {src.document_identifier}")
                if src.source_url:
                    lines.append(f"      URL: {src.source_url}")
                if src.evidence_excerpt:
                    lines.append(f"      Excerpt: {src.evidence_excerpt}")

        context_parts.append("\n".join(lines))
    return "\n\n---\n\n".join(context_parts)


def _build_fallback_answer(places: List[Place], question: str, language: str) -> str:
    """Build a structured answer from database records without AI."""
    if not places:
        if language == "ta":
            return "மன்னிக்கவும், உங்கள் கேள்விக்கு தொடர்புடைய இடங்கள் தரவுத்தளத்தில் காணப்படவில்லை. வேறு பெயர் அல்லது சொல்லைக் கொண்டு தேடவும்."
        return "Sorry, no relevant places were found in the database for your question. Please try searching with a different name or keyword."

    parts = []
    for place in places:
        if language == "ta":
            parts.append(f"📍 **{place.current_name_tamil or place.current_name}** ({place.current_name})")
        else:
            parts.append(f"📍 **{place.current_name}**" + (f" ({place.current_name_tamil})" if place.current_name_tamil else ""))

        if place.district:
            parts.append(f"  {'மாவட்டம்' if language == 'ta' else 'District'}: {place.district}")
        if language == "ta" and place.description_tamil:
            parts.append(f"  {place.description_tamil}")
        elif place.description:
            parts.append(f"  {place.description}")

        for hn in place.historical_names:
            type_label = {
                "official_renaming": "அதிகாரப்பூர்வ மறுபெயரிடுதல்" if language == "ta" else "Official Renaming",
                "historical_variant": "வரலாற்றுப் பெயர்" if language == "ta" else "Historical Variant",
                "transliteration": "ஒலிபெயர்ப்பு" if language == "ta" else "Transliteration",
                "uncertain": "நிச்சயமற்றது" if language == "ta" else "Uncertain",
            }.get(hn.name_type, hn.name_type or "")
            period = ""
            if hn.valid_from or hn.valid_to:
                period = f" ({hn.valid_from or '?'} – {hn.valid_to or '?'})"
            parts.append(f"  • {hn.name} [{type_label}]{period}")

        for evt in place.events:
            desc = evt.description_tamil if (language == "ta" and evt.description_tamil) else evt.description
            status = evt.evidence_status
            date_str = evt.event_date or ("தேதி தெரியவில்லை" if language == "ta" else "Date unknown")
            parts.append(f"  📅 {date_str}: {desc} [{'நிலை' if language == 'ta' else 'Status'}: {status}]")
            for src in evt.sources:
                parts.append(f"    📄 {src.title}" + (f" — {src.document_identifier}" if src.document_identifier else ""))

        parts.append("")

    if language == "ta":
        parts.append("⚠️ இது தரவுத்தளத்தில் உள்ள ஆவணங்களின் அடிப்படையிலான பதில். AI உருவாக்கிய பதில் அல்ல.")
    else:
        parts.append("⚠️ This answer is based on database records only. AI-generated answer is not available.")
    return "\n".join(parts)


def ask_question(db: Session, question: str, language: str = "ta") -> dict:
    """
    Answer a historical question using database evidence + optional Gemini AI.
    Returns dict with answer, sources_used, places_found, ai_generated, fallback.
    """
    # Extract keywords and search
    q_norm = normalize_text(question)
    search_results = search_places(db, q_norm, limit=5)

    # Also try individual words for broader matching
    words = q_norm.split()
    seen_ids = {r[0].id for r in search_results}
    for word in words:
        if len(word) >= 3:
            word_results = search_places(db, word, limit=3)
            for place, reason in word_results:
                if place.id not in seen_ids:
                    search_results.append((place, reason))
                    seen_ids.add(place.id)

    places = [r[0] for r in search_results]

    # Collect all sources
    all_sources = []
    source_ids = set()
    for place in places:
        for evt in place.events:
            for src in evt.sources:
                if src.id not in source_ids:
                    all_sources.append(src)
                    source_ids.add(src.id)

    # Try Gemini
    if _gemini_available and places:
        try:
            context = _build_context(places, db)
            lang_instruction = "Tamil (தமிழ்)" if language == "ta" else "English"
            system_prompt = f"""You are PeyarVaralaru AI, a historical Tamil place name research assistant.
Answer ONLY based on the provided evidence. Do NOT invent facts, dates, page numbers, or source URLs.
If the evidence is insufficient, say so clearly.
Keep source citations, historical names, and document identifiers in their original form.
Respond in {lang_instruction}.

Evidence from database:
{context}"""

            response = _gemini_client.models.generate_content(
                model="gemini-2.0-flash",
                contents=question,
                config={
                    "system_instruction": system_prompt,
                    "temperature": 0.3,
                    "max_output_tokens": 1500,
                }
            )
            answer = response.text
            return {
                "answer": answer,
                "sources_used": all_sources,
                "places_found": places,
                "ai_generated": True,
                "fallback": False,
            }
        except Exception as e:
            # Fall through to fallback
            pass

    # Fallback: database-only answer
    answer = _build_fallback_answer(places, question, language)
    return {
        "answer": answer,
        "sources_used": all_sources,
        "places_found": places,
        "ai_generated": False,
        "fallback": True,
    }
