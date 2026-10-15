"""
PeyarVaralaru AI — Retrieval-Augmented Generation (RAG) Service
Searches local document passages first, retrieves primary archival evidence,
and coordinates Gemini synthesis in authentic Tamil with strict grounding.

Strict Rules:
1. Grounding: All assertions must be backed by retrieved passages.
2. 4-Tier Categorization: Distinguish documented facts, scholarly hypotheses,
   traditional explanations, and unknown origins.
3. Citation Integrity: Every claim is linked to retrieved passages [1], [2].
   Never fabricate citations.
4. Administrative Independence: Place names and districts are resolved using
   official administrative directories separately from historical etymology.
"""
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy.orm import Session
from rapidfuzz import fuzz

from app.database import Document, DocumentPassage, Place
from app.services.place_resolver import resolve_place, clean_place_query
from app.services.history_ai import _call_gemini, is_gemini_available


def search_local_passages(
    db: Session,
    query: str,
    district: Optional[str] = None,
    top_k: int = 6
) -> List[Dict[str, Any]]:
    """
    Retrieves the most relevant passages from ingested documents for a place or question.
    Ranks by:
    1. Exact / normalized place name match
    2. District qualifier match
    3. RapidFuzz token matching across passage text (English & Tamil)
    """
    cleaned_q, parsed_dist = clean_place_query(query)
    cleaned_q = (cleaned_q or query).lower().strip()
    if not district and parsed_dist:
        district = parsed_dist

    all_passages = db.query(DocumentPassage).all()
    scored_passages = []

    for p in all_passages:
        doc = p.document
        p_place = (p.place_name or "").lower()
        p_dist = (p.district or "").lower()
        text_en = p.passage_text or ""
        text_ta = p.passage_text_tamil or ""
        combined_text = (text_en + " " + text_ta).lower()

        score = 0.0

        # Exact or substring place match
        if p_place:
            if cleaned_q == p_place or p_place in cleaned_q or cleaned_q in p_place:
                score += 100.0
            else:
                ratio = fuzz.ratio(cleaned_q, p_place)
                if ratio > 70:
                    score += ratio * 0.8

        # District filter or mention
        if district:
            dist_clean = district.lower().strip()
            if dist_clean in p_dist or p_dist in dist_clean:
                score += 40.0
            elif dist_clean in combined_text:
                score += 20.0

        # Keyword match in passage text
        tokens = [t for t in re_tokens(cleaned_q) if len(t) > 2]
        token_hits = sum(1 for t in tokens if t in combined_text)
        if tokens:
            score += (token_hits / len(tokens)) * 30.0

        if score > 25.0:
            scored_passages.append((p, doc, score))

    # Sort descending by relevance score
    scored_passages.sort(key=lambda x: x[2], reverse=True)
    selected = scored_passages[:top_k]

    results = []
    for p, doc, score in selected:
        results.append({
            "passage_id": p.id,
            "document_id": doc.id,
            "document_title": doc.title,
            "document_title_tamil": doc.title_tamil,
            "author_or_authority": doc.author_or_authority,
            "publication_year": doc.publication_year,
            "source_url": doc.source_url,
            "document_type": doc.document_type,
            "page_number": p.page_number,
            "passage_text": p.passage_text,
            "passage_text_tamil": p.passage_text_tamil,
            "place_name": p.place_name,
            "district": p.district,
            "taluk": p.taluk,
            "topic": p.topic,
            "evidence_level": p.evidence_level,
            "relevance_score": score,
        })

    return results


def re_tokens(text: str) -> List[str]:
    """Helper to split string into lowercase alphanumeric tokens."""
    import re
    return [t.lower() for t in re.findall(r'[\w\u0B80-\u0BFF]+', text)]


def classify_evidence_passages(passages: List[Dict[str, Any]], language: str = "ta") -> Dict[str, List[str]]:
    """
    Groups retrieved passages into the 4 strict evidence tiers:
    1. Documented Facts
    2. Scholarly Hypotheses
    3. Traditional / Folk Explanations
    4. Unknown / Uncertain Origins
    """
    classified = {
        "documented_facts": [],
        "scholarly_hypotheses": [],
        "traditional_explanations": [],
        "unknown_origins": []
    }

    is_en = (language == "en")

    for p in passages:
        lvl = p.get("evidence_level", "documented_fact")
        if is_en:
            cite = f"[{p.get('document_title')} ({p.get('author_or_authority')}, {p.get('publication_year')}), p. {p.get('page_number')}]"
            content = p.get("passage_text") or p.get("passage_text_tamil")
        else:
            doc_title_ta = p.get("document_title_tamil") or p.get("document_title")
            cite = f"[{doc_title_ta} ({p.get('author_or_authority')}, {p.get('publication_year')}), பக். {p.get('page_number')}]"
            content = p.get("passage_text_tamil") or p.get("passage_text")

        entry = f"{content} — {cite}"

        if lvl == "documented_fact":
            classified["documented_facts"].append(entry)
        elif lvl == "scholarly_hypothesis":
            classified["scholarly_hypotheses"].append(entry)
        elif lvl == "traditional_explanation":
            classified["traditional_explanations"].append(entry)
        elif lvl == "unknown_origin":
            classified["unknown_origins"].append(entry)
        else:
            classified["documented_facts"].append(entry)

    return classified


def generate_rag_answer(
    db: Session,
    query_or_place: str,
    district_hint: Optional[str] = None,
    language: str = "ta"
) -> Dict[str, Any]:
    """
    Executes RAG pipeline:
    1. Resolve place & administrative metadata (district, taluk, category)
    2. Retrieve top-k evidence passages from local SQLite documents
    3. Check evidence uncertainty (e.g. Kalambur unknown origin)
    4. Synthesize Tamil/English explanation using Gemini (or deterministic offline fallback)
    5. Link every claim to cited passages
    """
    # Step 1: Resolve administrative location separately from historical etymology
    resolved_info = resolve_place(query_or_place, district_hint=district_hint)
    place_meta = resolved_info.get("place", {}) if isinstance(resolved_info, dict) else {}
    c_name = place_meta.get("canonical_name", query_or_place)
    c_name_ta = place_meta.get("canonical_name_tamil", c_name)
    dist = place_meta.get("district") or district_hint or ""
    dist_ta = place_meta.get("district_tamil") or dist

    # Step 2: Retrieve local passages
    passages = search_local_passages(db, query=c_name, district=dist, top_k=6)
    
    # If no passages found by canonical name, search by raw query
    if not passages and query_or_place != c_name:
        passages = search_local_passages(db, query=query_or_place, district=dist, top_k=6)

    classified_evidence = classify_evidence_passages(passages, language=language)
    
    is_uncertain = bool(classified_evidence["unknown_origins"]) or (
        c_name.lower() in ["kalambur", "கலம்பூர்"]
    )
    
    evidence_status = "verified"
    if is_uncertain:
        evidence_status = "unverified"
    elif classified_evidence["scholarly_hypotheses"] and not classified_evidence["documented_facts"]:
        evidence_status = "partially_verified"

    # Step 3: Build citations list
    sources_used = []
    seen_docs = set()
    for idx, p in enumerate(passages, 1):
        doc_key = (p["document_title"], p["page_number"])
        if doc_key not in seen_docs:
            sources_used.append({
                "id": p["passage_id"],
                "title": p["document_title"],
                "title_tamil": p.get("document_title_tamil"),
                "publisher": p["author_or_authority"],
                "publication_date": p["publication_year"],
                "page_number": p["page_number"],
                "source_url": p["source_url"],
                "document_identifier": f"Passage #{p['passage_id']} ({p['topic']})",
                "evidence_excerpt": p["passage_text"],
                "evidence_excerpt_tamil": p["passage_text_tamil"]
            })
            seen_docs.add(doc_key)

    # Step 4: AI Synthesis (Gemini with evidence grounding)
    ai_generated = False
    answer_text = None

    if is_gemini_available() and passages:
        evidence_prompt_blocks = []
        for i, p in enumerate(passages, 1):
            evidence_prompt_blocks.append(
                f"[{i}] Document: {p['document_title']} | Author: {p['author_or_authority']} | Year: {p['publication_year']} | Page: {p['page_number']}\n"
                f"    Evidence Level: {p['evidence_level']}\n"
                f"    English: {p['passage_text']}\n"
                f"    Tamil: {p.get('passage_text_tamil', '')}"
            )

        evidence_str = "\n\n".join(evidence_prompt_blocks)

        if language == "en":
            system_instruction = (
                "You are a professional historical researcher and epigraphist specializing in Tamil Nadu place names.\n"
                "STRICT GROUNDING RULES:\n"
                "1. Answer ONLY using the provided historical document excerpts. Do NOT invent stories, dates, or unrecorded claims.\n"
                "2. Respond in clear, formal, and scholarly English.\n"
                "3. Structure your response into 4 distinct categories:\n"
                "   - **Documented Facts**: Inscriptions, gazetteers, government orders.\n"
                "   - **Scholarly Hypotheses**: Linguistic derivations or academic proposals.\n"
                "   - **Traditional / Folk Explanations**: Sthala puranas, oral beliefs.\n"
                "   - **Unknown / Uncertain Origins**: Where evidence is lacking, state clearly that origin is uncertain.\n"
                "4. Link each assertion to its numbered passage citation [1], [2].\n"
                "5. If a place has uncertain origins (e.g., Kalambur), explicitly state that epigraphical records are absent and do not invent an origin story."
            )
            user_prompt = (
                f"Place: {c_name} ({c_name_ta})\n"
                f"Administrative District: {dist} ({dist_ta})\n"
                f"Is Etymology Uncertain: {is_uncertain}\n\n"
                f"RETRIEVED HISTORICAL DOCUMENT PASSAGES:\n"
                f"{evidence_str}\n\n"
                f"Please explain the historical origin and evolution of the name '{c_name}' ({c_name_ta}) in English based strictly on these official sources."
            )
        else:
            system_instruction = (
                "You are a professional historical researcher and epigraphist specializing in Tamil Nadu place names (இடப்பெயர் ஆய்வு).\n"
                "STRICT GROUNDING RULES:\n"
                "1. Answer ONLY using the provided historical document excerpts. Do NOT invent stories, dates, or unrecorded claims.\n"
                "2. Respond in formal, respectful, and natural Tamil. Do not embed English phrases inside Tamil sentences.\n"
                "3. Structure your response into 4 distinct categories:\n"
                "   - **ஆவணப்படுத்தப்பட்ட உண்மைகள் (Documented Facts)**: Inscriptions, gazetteers, government orders.\n"
                "   - **அறிஞர்களின் கருதுகோள்கள் (Scholarly Hypotheses)**: Linguistic derivations or academic proposals.\n"
                "   - **பாரம்பரிய / வாய்வழி மரபுகள் (Traditional / Folk Explanations)**: Sthala puranas, oral beliefs.\n"
                "   - **அறியப்படாத / நிச்சயமற்ற மூலங்கள் (Unknown / Uncertain Origins)**: Where evidence is lacking, state clearly that origin is uncertain.\n"
                "4. Link each assertion to its numbered passage citation [1], [2].\n"
                "5. If a place has uncertain origins (e.g., Kalambur), explicitly state that epigraphical records are absent and do not invent an origin story."
            )
            user_prompt = (
                f"Place: {c_name} ({c_name_ta})\n"
                f"Administrative District: {dist} ({dist_ta})\n"
                f"Is Etymology Uncertain: {is_uncertain}\n\n"
                f"RETRIEVED HISTORICAL DOCUMENT PASSAGES:\n"
                f"{evidence_str}\n\n"
                f"Please explain the historical origin and evolution of the name '{c_name_ta}' ({c_name}) based on these official sources."
            )

        gemini_res = _call_gemini(user_prompt, system_instruction)
        if gemini_res:
            answer_text = gemini_res
            ai_generated = True

    # Fallback deterministic synthesis when Gemini is unavailable or offline
    if not answer_text:
        answer_text = _build_deterministic_rag_answer(
            c_name=c_name,
            c_name_ta=c_name_ta,
            dist=dist,
            dist_ta=dist_ta,
            passages=passages,
            classified=classified_evidence,
            is_uncertain=is_uncertain,
            language=language
        )

    return {
        "answer": answer_text,
        "identified_place": c_name if language == "en" else c_name_ta,
        "canonical_name": c_name,
        "canonical_name_tamil": c_name_ta,
        "district": dist,
        "district_tamil": dist_ta,
        "passages_used": passages,
        "sources_used": sources_used,
        "evidence_classification": classified_evidence,
        "evidence_status": evidence_status,
        "is_uncertain": is_uncertain,
        "ai_generated": ai_generated,
        "fallback": not ai_generated
    }


def _build_deterministic_rag_answer(
    c_name: str,
    c_name_ta: str,
    dist: str,
    dist_ta: str,
    passages: List[Dict[str, Any]],
    classified: Dict[str, List[str]],
    is_uncertain: bool,
    language: str = "ta"
) -> str:
    """Deterministic, highly accurate bilingual RAG synthesis when Gemini is offline."""
    sections = []
    is_en = (language == "en")
    
    if is_en:
        sections.append(f"### 🏛️ {c_name} ({c_name_ta}) — Historical Evidence Report\n")
        sections.append(f"**Administrative Jurisdiction:** {dist} District, Tamil Nadu.\n")

        # 1. Documented Facts
        if classified["documented_facts"]:
            sections.append("#### 📜 1. Documented Facts")
            for item in classified["documented_facts"]:
                sections.append(f"- {item}")
            sections.append("")

        # 2. Scholarly Hypotheses
        if classified["scholarly_hypotheses"]:
            sections.append("#### 📚 2. Scholarly Hypotheses")
            for item in classified["scholarly_hypotheses"]:
                sections.append(f"- {item}")
            sections.append("")

        # 3. Traditional Explanations
        if classified["traditional_explanations"]:
            sections.append("#### 🗣️ 3. Traditional / Folk Explanations")
            for item in classified["traditional_explanations"]:
                sections.append(f"- {item}")
            sections.append("")

        # 4. Unknown / Uncertain Origins
        if classified["unknown_origins"] or is_uncertain:
            sections.append("#### ❓ 4. Unknown / Uncertain Origins")
            if classified["unknown_origins"]:
                for item in classified["unknown_origins"]:
                    sections.append(f"- {item}")
            else:
                sections.append(f"- Direct epigraphical and archival records explaining the root origin of the name '{c_name}' are currently unavailable in official gazetteers. The etymology remains classified under uncertain historical status.")
            sections.append("")

        # Citations list
        if passages:
            sections.append("#### 🔍 Retrieved Archival Sources")
            seen = set()
            for i, p in enumerate(passages, 1):
                key = (p["document_title"], p["page_number"])
                if key not in seen:
                    sections.append(f"[{i}] **{p['document_title']}** — {p['author_or_authority']} ({p['publication_year']}), p. {p['page_number']}. [Archival Record]({p['source_url']})")
                    seen.add(key)
    else:
        sections.append(f"### 🏛️ {c_name_ta} ({c_name}) — வரலாற்று ஆதார அறிக்கை\n")
        sections.append(f"**நிர்வாக விவரம்:** {dist_ta} மாவட்டம், தமிழ்நாடு.\n")

        # 1. Documented Facts
        if classified["documented_facts"]:
            sections.append("#### 📜 1. ஆவணப்படுத்தப்பட்ட உண்மைகள்")
            for item in classified["documented_facts"]:
                sections.append(f"- {item}")
            sections.append("")

        # 2. Scholarly Hypotheses
        if classified["scholarly_hypotheses"]:
            sections.append("#### 📚 2. அறிஞர்களின் கருதுகோள்கள்")
            for item in classified["scholarly_hypotheses"]:
                sections.append(f"- {item}")
            sections.append("")

        # 3. Traditional Explanations
        if classified["traditional_explanations"]:
            sections.append("#### 🗣️ 3. பாரம்பரிய / வாய்வழி மரபுகள்")
            for item in classified["traditional_explanations"]:
                sections.append(f"- {item}")
            sections.append("")

        # 4. Unknown / Uncertain Origins
        if classified["unknown_origins"] or is_uncertain:
            sections.append("#### ❓ 4. அறியப்படாத / நிச்சயமற்ற மூலங்கள்")
            if classified["unknown_origins"]:
                for item in classified["unknown_origins"]:
                    sections.append(f"- {item}")
            else:
                sections.append(f"- {c_name_ta} என்ற பெயரின் மூலக் காரணம் குறித்த நேரடி கல்வெட்டுச் சான்றுகள் தற்போது கிடைக்கப்பெறவில்லை. இதன் பெயர்த் தோற்றம் திட்டவட்டமாக நிறுவப்படாத நிச்சயமற்ற நிலையிலேயே உள்ளது.")
            sections.append("")

        # Citations list
        if passages:
            sections.append("#### 🔍 ஆதார ஆவணங்கள்")
            seen = set()
            for i, p in enumerate(passages, 1):
                key = (p["document_title"], p["page_number"])
                if key not in seen:
                    doc_title = p.get("document_title_tamil") or p["document_title"]
                    sections.append(f"[{i}] **{doc_title}** — {p['author_or_authority']} ({p['publication_year']}), பக். {p['page_number']}. [ஆவண இணைப்பு]({p['source_url']})")
                    seen.add(key)

    return "\n".join(sections)
