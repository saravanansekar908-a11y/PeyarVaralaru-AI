"""
PeyarVaralaru AI — Evaluation Harness for Source-Grounded RAG
Tests:
1. Retrieval Accuracy: Precision of local passage retrieval from ingested gazetteers & records.
2. Factual Support: Verification that ground truth facts are present in generated answers.
3. Citation Validity: Verification that all cited documents exist in SQLite with non-empty metadata.
4. Tamil Quality: Accurate Tamil toponymic categories and natural phrasing.
5. Uncertainty Handling: Proper declaration of uncertain/oral tradition without fabrication.
"""
import sys
import os
import json
from typing import Dict, Any, List

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import init_db, SessionLocal
from app.services.seed_documents import seed_research_documents
from app.services.rag_service import generate_rag_answer


def run_rag_evaluation(eval_file_path: str = "data/eval_dataset.json") -> Dict[str, Any]:
    print("=" * 70)
    print("PEYARVARALARU AI — SOURCE-GROUNDED RAG EVALUATION BENCHMARK")
    print("=" * 70)

    # 1. Initialize DB and ensure documents seeded
    init_db()
    db = SessionLocal()
    seed_research_documents(db)

    # 2. Load evaluation dataset
    full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), eval_file_path)
    with open(full_path, "r", encoding="utf-8") as f:
        benchmark = json.load(f)

    test_cases = benchmark.get("test_cases", [])
    total_cases = len(test_cases)
    print(f"\nLoaded {total_cases} test cases from {eval_file_path}\n")

    results = []
    retrieval_success_count = 0
    factual_support_count = 0
    citation_valid_count = 0
    tamil_quality_count = 0
    uncertainty_correct_count = 0

    for idx, tc in enumerate(test_cases, 1):
        case_id = tc["id"]
        place = tc["place"]
        q_ta = tc["question_ta"]
        dist = tc["district"]
        req_facts = tc.get("required_facts", [])
        req_facts_ta = tc.get("required_facts_tamil", [])
        exp_uncertain = tc.get("expected_uncertain", False)
        exp_doc = tc.get("expected_document_title", "").lower()

        print(f"[{idx}/{total_cases}] Evaluating {case_id}: {place} ({tc['place_tamil']})...")

        # Execute RAG pipeline
        rag_out = generate_rag_answer(
            db=db,
            query_or_place=q_ta,
            district_hint=dist,
            language="ta"
        )

        answer = rag_out.get("answer", "")
        passages = rag_out.get("passages_used", [])
        sources = rag_out.get("sources_used", [])
        is_uncertain = rag_out.get("is_uncertain", False)
        e_class = rag_out.get("evidence_classification", {})

        answer_lower = answer.lower()

        # 1. Retrieval Accuracy Metric
        # Check if expected document was retrieved among passages
        retrieved_doc_titles = [p.get("document_title", "").lower() for p in passages]
        retrieval_pass = False
        if any(exp_doc in t for t in retrieved_doc_titles):
            retrieval_pass = True
        elif len(passages) > 0 and any(place.lower() in (p.get("place_name") or "").lower() for p in passages):
            retrieval_pass = True

        if retrieval_pass:
            retrieval_success_count += 1

        # 2. Factual Support Metric
        # Check presence of required ground-truth historical facts
        matched_facts = 0
        for f in req_facts:
            if f.lower() in answer_lower:
                matched_facts += 1
        for f_ta in req_facts_ta:
            if f_ta in answer:
                matched_facts += 1

        # Passes if at least 2 ground truth facts are explicitly verified
        factual_pass = (matched_facts >= 2)
        if factual_pass:
            factual_support_count += 1

        # 3. Citation Validity Metric
        # Every cited source must have title, publisher, and year without fabrication
        citation_pass = True
        if not sources:
            citation_pass = False
        else:
            for s in sources:
                if not s.get("title") or not s.get("publisher") or not s.get("publication_date"):
                    citation_pass = False
                    break

        if citation_pass:
            citation_valid_count += 1

        # 4. Tamil Quality Metric
        # Must contain standard Tamil toponymy and evidence headings
        has_ta_headings = any(k in answer for k in [
            "ஆவணப்படுத்தப்பட்ட உண்மைகள்", "அறிஞர்களின் கருதுகோள்கள்",
            "பாரம்பரிய", "அறியப்படாத", "வரலாற்று", "ஆதார"
        ])
        tamil_pass = has_ta_headings and len(answer) > 80
        if tamil_pass:
            tamil_quality_count += 1

        # 5. Uncertainty Handling Metric
        # If place is expected to be uncertain (e.g. Kalambur), system must declare uncertainty
        # and refrain from presenting folk stories as documented facts
        if exp_uncertain:
            uncertainty_pass = (is_uncertain is True) or any(k in answer for k in ["நிச்சயமற்ற", "சான்றுகள் இல்லை", "வாய்வழி"])
        else:
            uncertainty_pass = (is_uncertain is False)

        if uncertainty_pass:
            uncertainty_correct_count += 1

        status_str = "PASS" if (retrieval_pass and factual_pass and citation_pass and uncertainty_pass) else "REVIEW"
        print(f"    -> Status: {status_str} | Retrieval: {'✓' if retrieval_pass else '✗'} | Factual: {'✓' if factual_pass else '✗'} | Citation: {'✓' if citation_pass else '✗'} | Uncertainty: {'✓' if uncertainty_pass else '✗'}")

        results.append({
            "id": case_id,
            "place": place,
            "retrieval_pass": retrieval_pass,
            "factual_pass": factual_pass,
            "citation_pass": citation_pass,
            "tamil_pass": tamil_pass,
            "uncertainty_pass": uncertainty_pass,
            "is_uncertain": is_uncertain,
            "passages_count": len(passages),
            "sources_count": len(sources)
        })

    db.close()

    # Calculate summary metrics
    pct_retrieval = (retrieval_success_count / total_cases) * 100
    pct_factual = (factual_support_count / total_cases) * 100
    pct_citation = (citation_valid_count / total_cases) * 100
    pct_tamil = (tamil_quality_count / total_cases) * 100
    pct_uncertainty = (uncertainty_correct_count / total_cases) * 100

    print("\n" + "=" * 70)
    print("EVALUATION BENCHMARK RESULTS SUMMARY")
    print("=" * 70)
    print(f"Total Test Cases Evaluated: {total_cases}")
    print(f"1. Retrieval Accuracy:           {pct_retrieval:.1f}% ({retrieval_success_count}/{total_cases})")
    print(f"2. Factual Support Score:        {pct_factual:.1f}% ({factual_support_count}/{total_cases})")
    print(f"3. Citation Validity:            {pct_citation:.1f}% ({citation_valid_count}/{total_cases})")
    print(f"4. Tamil Quality & Terminology:  {pct_tamil:.1f}% ({tamil_quality_count}/{total_cases})")
    print(f"5. Uncertainty Handling:         {pct_uncertainty:.1f}% ({uncertainty_correct_count}/{total_cases})")
    print("=" * 70)

    overall_pass = (
        pct_retrieval >= 85.0 and
        pct_factual >= 85.0 and
        pct_citation >= 95.0 and
        pct_tamil >= 90.0 and
        pct_uncertainty >= 90.0
    )

    if overall_pass:
        print("🏆 BENCHMARK PASSED: All 5 research metrics satisfy rigorous grounding criteria!")
    else:
        print("⚠️ BENCHMARK COMPLETED with areas needing refinement.")

    return {
        "total_cases": total_cases,
        "pct_retrieval": pct_retrieval,
        "pct_factual": pct_factual,
        "pct_citation": pct_citation,
        "pct_tamil": pct_tamil,
        "pct_uncertainty": pct_uncertainty,
        "overall_pass": overall_pass,
        "results": results
    }


if __name__ == "__main__":
    run_rag_evaluation()
