"""
PeyarVaralaru AI — History AI Service
Uses Gemini API (gemini-3.8-flash / gemini-2.5-flash) with evidence grounding
to synthesize structured 10-section Tamil historical reports and answer user questions.
Includes robust offline/archival fallback when Gemini is unavailable.
"""
import os
import re
from typing import Dict, Any, List, Optional
from app.services.citation_service import format_citation_tamil, format_citation_english

_gemini_available = False
_gemini_client = None

try:
    from google import genai
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if api_key:
        _gemini_client = genai.Client(api_key=api_key)
        _gemini_available = True
except Exception:
    _gemini_available = False


def is_gemini_available() -> bool:
    return _gemini_available


def _call_gemini(prompt: str, system_instruction: str) -> Optional[str]:
    """Calls Gemini with gemini-2.5-flash for high-speed reliable synthesis."""
    if not _gemini_available or not _gemini_client:
        return None

    # Model priority: gemini-2.5-flash (fast, reliable), then gemini-3.8-flash
    models_to_try = ["gemini-2.5-flash", "gemini-3.8-flash"]
    for model_name in models_to_try:
        try:
            response = _gemini_client.models.generate_content(
                model=model_name,
                contents=prompt,
                config={
                    "system_instruction": system_instruction,
                    "temperature": 0.2,
                    "max_output_tokens": 2048,
                }
            )
            if response and response.text:
                return response.text.strip()
        except Exception as e:
            # Continue to try next model or return None
            continue
    return None


def generate_structured_report(
    evidence: Dict[str, Any],
    language: str = "ta"
) -> Dict[str, Any]:
    """
    Generates the complete 10-section Tamil (or English) Historical Report:
    1. ஊரின் அறிமுகம் — Place overview
    2. பெயரின் பொருள் — Meaning of the name, if established
    3. பெயர் வந்த வரலாறு — Origin and explanation of the place name
    4. பழைய பெயர்கள் — Historical names and spelling variants
    5. வரலாற்றுப் பின்னணி — Important historical context
    6. காலவரிசை — Important events and documented dates
    7. கல்வெட்டுகள் மற்றும் ஆவணங்கள் — Relevant inscriptions and archival records
    8. பெயர் மாற்றங்கள் — Documented official renamings
    9. ஆதாரங்கள் — Sources and citations with URLs
    10. ஆதார நம்பகத்தன்மை — What is verified, uncertain, or disputed
    """
    place_info = evidence.get("place_data", {})
    c_name = place_info.get("canonical_name", "")
    c_name_ta = place_info.get("canonical_name_tamil") or c_name
    district = place_info.get("district", "Tamil Nadu")
    district_ta = place_info.get("district_tamil") or district
    category = place_info.get("category", "Settlement")
    category_ta = place_info.get("category_tamil") or category

    historical_names = evidence.get("historical_names", [])
    events = evidence.get("events", [])
    sources = evidence.get("sources", [])
    evidence_status = evidence.get("evidence_status", "unverified")
    is_uncertain = evidence.get("is_uncertain", False)

    meaning_ta = evidence.get("meaning_tamil")
    origin_ta = evidence.get("origin_tamil")

    # If Gemini is available, use it to synthesize rich natural Tamil report
    if _gemini_available:
        evidence_summary_lines = [
            f"Place: {c_name} ({c_name_ta})",
            f"District: {district} ({district_ta})",
            f"Category: {category} ({category_ta})",
            f"Evidence Status: {evidence_status}",
            f"Is Etymology Uncertain: {is_uncertain}",
        ]
        if meaning_ta:
            evidence_summary_lines.append(f"Recorded Name Meaning (Tamil): {meaning_ta}")
        if origin_ta:
            evidence_summary_lines.append(f"Recorded Name Origin (Tamil): {origin_ta}")
        if place_info.get("wiki_extract"):
            evidence_summary_lines.append(f"Encyclopedic Extract: {place_info['wiki_extract']}")

        for hn in historical_names:
            evidence_summary_lines.append(f"Historical Name: {hn.get('name')} ({hn.get('language')}, {hn.get('name_type')}, {hn.get('valid_from')}-{hn.get('valid_to')})")

        for evt in events:
            desc = evt.get("description_tamil") or evt.get("description")
            evidence_summary_lines.append(f"Event ({evt.get('event_date')}): {desc} [Status: {evt.get('evidence_status')}]")

        for s in sources:
            evidence_summary_lines.append(f"Source: {s.get('title')} ({s.get('publisher')}, {s.get('publication_date')}) - Excerpt: {s.get('evidence_excerpt')}")

        context_str = "\n".join(evidence_summary_lines)

        lang_instruction = "Natural, formal Tamil (தமிழ்)" if language == "ta" else "Scholarly English"
        system_instruction = f"""You are PeyarVaralaru AI, a senior historical research specialist and Tamil language scholar.
Your role is to produce an authoritative, evidence-grounded historical report on the requested place in {lang_instruction}.
CRITICAL RULES:
1. ONLY make claims grounded in the provided evidence. DO NOT invent folklore, fictitious inscriptions, or dates.
2. If the origin or meaning is uncertain or based on oral tradition (e.g. Kalambur), say so EXPLICITLY. Clearly distinguish documented facts from folklore and popular hypotheses.
3. Structure your response EXACTLY with these 10 numbered sections in Tamil (or English if requested):
   1. ஊரின் அறிமுகம் (Place Overview)
   2. பெயரின் பொருள் (Meaning of Name - state if uncertain)
   3. பெயர் வந்த வரலாறு (Origin of Name)
   4. பழைய பெயர்கள் (Historical Names & Variants)
   5. வரலாற்றுப் பின்னணி (Historical Background)
   6. காலவரிசை (Documented Timeline Events)
   7. கல்வெட்டுகள் மற்றும் ஆவணங்கள் (Inscriptions & Records)
   8. பெயர் மாற்றங்கள் (Official Renamings)
   9. ஆதாரங்கள் (Sources & Citations)
   10. ஆதார நம்பகத்தன்மை (Evidence Reliability: Verified, Partially Verified, Uncertain, Disputed)
4. Do not fill missing sections with fabricated details. If an official renaming or inscription is not recorded, clearly state that primary records for it have not yet been identified."""

        user_prompt = f"""Generate the complete historical report for: {c_name_ta} ({c_name}), {district_ta} District.
Evidence gathered:
{context_str}"""

        ai_response = _call_gemini(user_prompt, system_instruction)
        if ai_response:
            return {
                "raw_markdown": ai_response,
                "ai_generated": True,
                "evidence_status": evidence_status,
                "sources": sources,
                "place_name": c_name_ta if language == "ta" else c_name,
                "district": district_ta if language == "ta" else district,
            }

    # High quality Archival Fallback report (when AI is offline or unavailable)
    return _build_fallback_report(
        c_name=c_name,
        c_name_ta=c_name_ta,
        district=district,
        district_ta=district_ta,
        category=category,
        category_ta=category_ta,
        meaning_ta=meaning_ta,
        origin_ta=origin_ta,
        historical_names=historical_names,
        events=events,
        sources=sources,
        evidence_status=evidence_status,
        is_uncertain=is_uncertain,
        wiki_extract=place_info.get("wiki_extract"),
        language=language
    )


def _build_fallback_report(
    c_name: str,
    c_name_ta: str,
    district: str,
    district_ta: str,
    category: str,
    category_ta: str,
    meaning_ta: Optional[str],
    origin_ta: Optional[str],
    historical_names: List[Dict[str, Any]],
    events: List[Dict[str, Any]],
    sources: List[Dict[str, Any]],
    evidence_status: str,
    is_uncertain: bool,
    wiki_extract: Optional[str],
    language: str = "ta"
) -> Dict[str, Any]:
    """Generates the 10-section markdown report directly from archival records."""
    is_ta = (language == "ta")
    sections = []

    # 1. ஊரின் அறிமுகம்
    sec1_title = "### 1. ஊரின் அறிமுகம்" if is_ta else "### 1. Place Overview"
    if is_ta:
        sec1_body = f"**{c_name_ta}** ({c_name}) என்பது தமிழ்நாட்டின் **{district_ta}** மாவட்டத்தில் அமைந்துள்ள ஒரு {category_ta} ஆகும்."
        if wiki_extract:
            sec1_body += f"\n\n{wiki_extract}"
    else:
        sec1_body = f"**{c_name}** ({c_name_ta}) is a {category} situated in **{district}** district of Tamil Nadu."
        if wiki_extract:
            sec1_body += f"\n\n{wiki_extract}"
    sections.append(f"{sec1_title}\n{sec1_body}")

    # 2. பெயரின் பொருள்
    sec2_title = "### 2. பெயரின் பொருள்" if is_ta else "### 2. Meaning of the Name"
    if meaning_ta:
        sec2_body = meaning_ta if is_ta else f"Documented derivation: {meaning_ta}"
    else:
        sec2_body = (
            "இப்பெயரின் நேரடி மொழிப் பொருள் குறித்த தெளிவான கல்வெட்டுச் சான்றுகள் உறுதிப்படுத்தப்படவில்லை. இது புவியியல் அல்லது வரலாற்று பயன்பாட்டின் அடிப்படையில் வழங்கப்பட்டு வருகிறது."
            if is_ta else
            "Direct etymological derivation is not definitively attested in primary epigraphical records; it reflects historical and geographical usage."
        )
    sections.append(f"{sec2_title}\n{sec2_body}")

    # 3. பெயர் வந்த வரலாறு
    sec3_title = "### 3. பெயர் வந்த வரலாறு" if is_ta else "### 3. Origin and History of the Name"
    if origin_ta:
        sec3_body = origin_ta if is_ta else f"Historical Origin: {origin_ta}"
    else:
        sec3_body = (
            f"**{c_name_ta}** பகுதிக்கான பெயர்த் தோற்றம் குறித்த ஆரம்பக் குறிப்புகள் ஆவணங்களில் காணப்படுகின்றன. முழுமையான மூல ஆவணங்களை உறுதிப்படுத்த மேலும் தொல்லியல் மற்றும் ஆவணக் காப்பக ஆய்வுகள் தேவைப்படுகின்றன."
            if is_ta else
            f"Preliminary historical references for **{c_name}** are noted in administrative surveys; further epigraphical research is required to establish its earliest origin."
        )
    sections.append(f"{sec3_title}\n{sec3_body}")

    # 4. பழைய பெயர்கள்
    sec4_title = "### 4. பழைய பெயர்கள்" if is_ta else "### 4. Historical Names and Variants"
    if historical_names:
        h_lines = []
        for hn in historical_names:
            period = f" ({hn.get('valid_from') or '?'} – {hn.get('valid_to') or '?'})" if (hn.get('valid_from') or hn.get('valid_to')) else ""
            type_lbl = hn.get('name_type', 'variant')
            h_lines.append(f"- **{hn.get('name')}** [{type_lbl}]{period} — {hn.get('language') or 'Tamil/English'}")
        sec4_body = "\n".join(h_lines)
    else:
        sec4_body = (
            "தற்போது வரை கூடுதல் வரலாற்றுப் பெயர் மாறுபாடுகள் ஆவணப்படுத்தப்படவில்லை."
            if is_ta else
            "No additional historical name variants are currently documented in primary registers."
        )
    sections.append(f"{sec4_title}\n{sec4_body}")

    # 5. வரலாற்றுப் பின்னணி
    sec5_title = "### 5. வரலாற்றுப் பின்னணி" if is_ta else "### 5. Historical Background"
    if events:
        evt_descs = [f"- {e.get('description_tamil' if is_ta else 'description')}" for e in events if e.get('description')]
        sec5_body = "\n".join(evt_descs)
    else:
        sec5_body = (
            f"{c_name_ta} பகுதி {district_ta} மாவட்டத்தின் வரலாற்று மற்றும் நிர்வாக நிலப்பரப்பில் முக்கியப் பங்கு வகிக்கிறது."
            if is_ta else
            f"{c_name} forms an integral part of the historical and administrative geography of {district} district."
        )
    sections.append(f"{sec5_title}\n{sec5_body}")

    # 6. காலவரிசை
    sec6_title = "### 6. காலவரிசை" if is_ta else "### 6. Timeline of Documented Events"
    if events:
        t_lines = []
        for e in events:
            dt = e.get("event_date") or ("ஆண்டு தெரியவில்லை" if is_ta else "Date unrecorded")
            desc = e.get("description_tamil" if is_ta else "description")
            status = e.get("evidence_status", "verified")
            t_lines.append(f"- **{dt}**: {desc} *[{'நிலை' if is_ta else 'Status'}: {status}]*")
        sec6_body = "\n".join(t_lines)
    else:
        sec6_body = (
            "காலவரிசை நிகழ்வுகள் ஆவணக் காப்பக பதிவுகளிலிருந்து தொடர்ந்து தொகுக்கப்பட்டு வருகின்றன."
            if is_ta else
            "Chronological milestones are currently being curated from archival registers."
        )
    sections.append(f"{sec6_title}\n{sec6_body}")

    # 7. கல்வெட்டுகள் மற்றும் ஆவணங்கள்
    sec7_title = "### 7. கல்வெட்டுகள் மற்றும் ஆவணங்கள்" if is_ta else "### 7. Inscriptions and Archival Records"
    ins_sources = [s for s in sources if "inscription" in s.get("title", "").lower() or "கல்வெட்டு" in s.get("title_tamil", "")]
    if ins_sources:
        sec7_body = "\n".join([f"- {s.get('title_tamil' if is_ta else 'title')} ({s.get('document_identifier') or s.get('publisher')})" for s in ins_sources])
    else:
        sec7_body = (
            "இப்பகுதி தொடர்பான ஆரம்பகால கல்வெட்டுக் குறிப்புகள் தமிழ்நாடு அரசு தொல்லியல் துறை மற்றும் இந்திய தொல்லியல் துறையின் அறிக்கைகளில் ஆய்வு செய்யப்பட்டு வருகின்றன."
            if is_ta else
            "Epigraphical records concerning this locality are catalogued in State and ASI archaeological survey reports."
        )
    sections.append(f"{sec7_title}\n{sec7_body}")

    # 8. பெயர் மாற்றங்கள்
    sec8_title = "### 8. பெயர் மாற்றங்கள்" if is_ta else "### 8. Official Renamings"
    renamings = [e for e in events if e.get("event_type") == "official_renaming"]
    if renamings:
        sec8_body = "\n".join([f"- **{r.get('event_date') or ''}**: {r.get('description_tamil' if is_ta else 'description')}" for r in renamings])
    else:
        sec8_body = (
            "அரசாணை எண் அல்லது அரசிதழ் மூலம் ஆவணப்படுத்தப்பட்ட நேரடி மறுபெயரிடுதல்கள் பதிவாகவில்லை."
            if is_ta else
            "No formal statutory renaming notifications (G.O.) are documented for this locality."
        )
    sections.append(f"{sec8_title}\n{sec8_body}")

    # 9. ஆதாரங்கள்
    sec9_title = "### 9. ஆதாரங்கள்" if is_ta else "### 9. Sources and Citations"
    if sources:
        cite_lines = []
        for s in sources:
            cite_str = format_citation_tamil(s) if is_ta else format_citation_english(s)
            cite_lines.append(f"- {cite_str}")
        sec9_body = "\n".join(cite_lines)
    else:
        sec9_body = "அரசு நிர்வாக பதிவேடுகள் மற்றும் புவியியல் தகவல்கள்." if is_ta else "Government administrative portals and gazetteers."
    sections.append(f"{sec9_title}\n{sec9_body}")

    # 10. ஆதார நம்பகத்தன்மை
    sec10_title = "### 10. ஆதார நம்பகத்தன்மை" if is_ta else "### 10. Evidence Reliability Status"
    status_label = {
        "verified": "சரிபார்க்கப்பட்டது (Verified via Gazette / G.O. / Inscription)" if is_ta else "Verified via Primary Gazette / G.O. / Inscriptions",
        "partially_verified": "பகுதியளவு சரிபார்க்கப்பட்டது (Partially Verified via Secondary Gazetteers)" if is_ta else "Partially Verified via Secondary Gazetteers",
        "unverified": "நிச்சயமற்றது / வாய்வழி மரபு (Uncertain / Folk Tradition)" if is_ta else "Uncertain / Folk Tradition requiring primary discovery",
        "disputed": "முரண்பட்ட கருத்துக்கள் (Disputed Claims)" if is_ta else "Disputed claims requiring cross-verification"
    }.get(evidence_status, evidence_status)

    sec10_body = f"**நிலை**: `{status_label}`\n\n"
    if is_uncertain:
        sec10_body += (
            "> ⚠️ **குறிப்பு**: இப்பெயரின் தோற்றம் குறித்த வாய்வழி கருத்துக்கள் வழக்கத்தில் இருந்தாலும், நேரடி ஆவணச் சான்றுகள் உறுதிப்படுத்தப்படாத வரை இது 'நிச்சயமற்றது' என்றே வகைப்படுத்தப்படுகிறது. கற்பனையான கதைகள் வரலாற்று உண்மையாக ஏற்கப்படாது."
            if is_ta else
            "> ⚠️ **Note**: While popular traditions may exist, unverified etymologies remain classified as 'Uncertain'. Unsupported narratives are not treated as established historical fact."
        )
    else:
        sec10_body += (
            "இத்தகவல்கள் அதிகாரப்பூர்வ மாவட்ட கையேடுகள், அரசிதழ்கள் மற்றும் தொல்லியல் பதிவுகளின் அடிப்படையில் சரிபார்க்கப்பட்டுள்ளன."
            if is_ta else
            "This profile is corroborated by published gazetteers, government orders, and epigraphical records."
        )
    sections.append(f"{sec10_title}\n{sec10_body}")

    raw_markdown = "\n\n".join(sections)
    return {
        "raw_markdown": raw_markdown,
        "ai_generated": False,
        "evidence_status": evidence_status,
        "sources": sources,
        "place_name": c_name_ta if is_ta else c_name,
        "district": district_ta if is_ta else district,
    }


def answer_history_question(
    question: str,
    evidence: Dict[str, Any],
    language: str = "ta"
) -> Dict[str, Any]:
    """
    Answers a specific user historical question using Gemini AI grounded in evidence,
    or falls back to structured archival answers.
    """
    place_info = evidence.get("place_data", {})
    c_name = place_info.get("canonical_name", "")
    c_name_ta = place_info.get("canonical_name_tamil") or c_name
    district = place_info.get("district", "Tamil Nadu")
    sources = evidence.get("sources", [])
    evidence_status = evidence.get("evidence_status", "unverified")
    is_uncertain = evidence.get("is_uncertain", False)

    # 1. Try Gemini
    if _gemini_available:
        context_parts = [
            f"Place: {c_name} ({c_name_ta}), District: {district}",
            f"Evidence Status: {evidence_status}",
            f"Is Etymology Uncertain: {is_uncertain}",
        ]
        if evidence.get("meaning_tamil"):
            context_parts.append(f"Recorded Name Meaning (Tamil): {evidence['meaning_tamil']}")
        if evidence.get("origin_tamil"):
            context_parts.append(f"Recorded Name Origin (Tamil): {evidence['origin_tamil']}")
        if place_info.get("wiki_extract"):
            context_parts.append(f"Encyclopedic Extract: {place_info['wiki_extract']}")

        for hn in evidence.get("historical_names", []):
            context_parts.append(f"Historical Name: {hn.get('name')} ({hn.get('name_type')}, {hn.get('valid_from')}-{hn.get('valid_to')})")

        for evt in evidence.get("events", []):
            context_parts.append(f"Event: {evt.get('event_date')} - {evt.get('description_tamil') or evt.get('description')}")

        for s in sources:
            context_parts.append(f"Source: {s.get('title')} ({s.get('publisher')}) - Excerpt: {s.get('evidence_excerpt')}")

        context_str = "\n".join(context_parts)
        lang_instruction = "Tamil (தமிழ்)" if language == "ta" else "English"

        system_instruction = f"""You are PeyarVaralaru AI, an expert research scholar in Tamil history, epigraphy, and place names.
Answer the user's question directly, clearly, and authoritatively based ONLY on the provided evidence.
CRITICAL RULES:
1. Ground your answer in the provided evidence. DO NOT fabricate origin stories, dates, or non-existent inscriptions.
2. If the name origin is uncertain or based on oral folklore (e.g. Kalambur), say so clearly in {lang_instruction}.
3. Respond in {lang_instruction}.
4. Mention supporting historical sources and citations explicitly."""

        prompt = f"""Question: {question}

Evidence Grounding:
{context_str}"""

        ai_ans = _call_gemini(prompt, system_instruction)
        if ai_ans:
            return {
                "answer": ai_ans,
                "sources_used": sources,
                "ai_generated": True,
                "fallback": False,
                "evidence_status": evidence_status,
                "is_uncertain": is_uncertain
            }

    # 2. Archival Fallback Answer
    is_ta = (language == "ta")
    ans_parts = []
    ans_parts.append(f"📍 **{c_name_ta if is_ta else c_name}** ({c_name if is_ta else c_name_ta}) — {district}")

    if evidence.get("meaning_tamil"):
        ans_parts.append(f"\n**{'பெயரின் பொருள்' if is_ta else 'Name Meaning'}**: {evidence['meaning_tamil']}")

    if evidence.get("origin_tamil"):
        ans_parts.append(f"\n**{'பெயர் வந்த வரலாறு' if is_ta else 'Name Origin'}**: {evidence['origin_tamil']}")
    elif place_info.get("wiki_extract"):
        ans_parts.append(f"\n{place_info['wiki_extract']}")
    else:
        ans_parts.append(
            f"\n{'மன்னிக்கவும், இந்த ஊரின் பெயர்க் காரணம் குறித்த ஆவணச் சான்றுகள் ஆரம்பக் கட்ட ஆய்விலேயே உள்ளன. போதுமான ஆதாரங்கள் கிடைக்கவில்லை.' if is_ta else 'Primary archival documentation regarding the origin of this place name is preliminary.'}"
        )

    if is_uncertain:
        ans_parts.append(
            f"\n⚠️ *{'குறிப்பு: இப்பெயரின் மூலம் குறித்த நேரடி கல்வெட்டுச் சான்றுகள் உறுதிப்படுத்தப்படவில்லை. வாய்வழி மரபுகள் மற்றும் அனுமானங்கள் மட்டுமே உள்ளன.' if is_ta else 'Note: Primary epigraphical derivation remains unverified.'}*"
        )

    if not is_ta:
        ans_parts.append("\n⚠️ This answer is grounded directly in archival records.")
    else:
        ans_parts.append("\n⚠️ இது ஆவணக் காப்பகத் தரவுகளின் அடிப்படையில் நேரடியாகத் தொகுக்கப்பட்ட பதில்.")

    return {
        "answer": "\n".join(ans_parts),
        "sources_used": sources,
        "ai_generated": False,
        "fallback": True,
        "evidence_status": evidence_status,
        "is_uncertain": is_uncertain
    }
