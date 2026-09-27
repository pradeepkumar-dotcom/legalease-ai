"""
test_scenarios.py - Automated Scenario Testing & Sample Export Generator
Validates 3 core business legal document scenarios:
1. Employment Contract (Apex Software Solutions & Alex Morgan)
2. Non-Disclosure Agreement (NovaTech Labs & John Doe)
3. Residential Lease Agreement (Greenstone Properties & Jane Smith)

Generates full Markdown, DOCX, PDF, and TXT files in output_samples/ with timing metrics.
"""
import os
import sys
import time
from pathlib import Path

# Set workspace root
ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR))

from config import DOCUMENT_TYPES, LEGAL_TONES
from ai_core.gemini_generator import GeminiLegalGenerator
from ai_core.generator import DocumentExporter

# Ensure output directory exists
OUTPUT_DIR = ROOT_DIR / "output_samples"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def run_scenario_tests():
    print("=" * 70)
    print("    LegalEase: Automated Scenario Testing & Export Generator     ")
    print("=" * 70)
    print(f"[*] Target Output Directory: {OUTPUT_DIR}\n")

    generator = GeminiLegalGenerator()

    scenarios = [
        {
            "id": "scenario_1",
            "name": "Scenario 1: Employment Contract",
            "doc_type": "Employment Agreement",
            "parties": {
                "employer_name": "Apex Software Solutions Pvt Ltd",
                "employee_name": "Alex Morgan",
            },
            "dates": "November 1, 2026",
            "jurisdiction": "State of California, USA",
            "tone": LEGAL_TONES[0],  # Strict & Comprehensive
            "specific_terms": {
                "job_title": "Lead AI Engineer",
                "salary_details": "$140,000 USD paid monthly",
                "pto_days": "20 days annual paid time off",
                "probation_period": "6-month probation period",
                "termination_notice_days": "30",
            },
            "custom_clauses": [
                "Strict Intellectual Property (IP) assignment to Employer for all works and patents.",
                "Non-compete obligation restricting direct competitor engagements for 1 year post-termination.",
                "Strict confidentiality covering proprietary AI models and algorithmic weights."
            ],
            "file_prefix": "employment_contract"
        },
        {
            "id": "scenario_2",
            "name": "Scenario 2: Non-Disclosure Agreement (NDA)",
            "doc_type": "Non-Disclosure Agreement (NDA)",
            "parties": {
                "disclosing_party": "NovaTech Labs",
                "receiving_party": "John Doe",
            },
            "dates": "October 15, 2026",
            "jurisdiction": "State of Delaware, USA",
            "tone": LEGAL_TONES[1],  # Balanced & Standard Commercial
            "specific_terms": {
                "purpose": "Confidential evaluation of proprietary LLM quantization algorithms.",
                "term_years": "3 years",
            },
            "custom_clauses": [
                "Non-disclosure term shall last three (3) years from the Effective Date.",
                "Excludes publicly known information, rightfully received third-party data, or legally compelled disclosures.",
                "Mandatory immediate return or certified destruction of confidential materials within 14 days upon written request."
            ],
            "file_prefix": "nda"
        },
        {
            "id": "scenario_3",
            "name": "Scenario 3: Residential Lease Agreement",
            "doc_type": "Residential / Commercial Lease Agreement",
            "parties": {
                "landlord_name": "Greenstone Properties",
                "tenant_name": "Jane Smith",
            },
            "dates": "December 1, 2026",
            "jurisdiction": "State of Texas, USA",
            "tone": LEGAL_TONES[1],  # Balanced & Standard Commercial
            "specific_terms": {
                "property_address": "Suite 4B, 742 Evergreen Terrace, Austin, TX 78701",
                "lease_term_months": "12 months",
                "monthly_rent": "$2,200 USD due on the 1st of each calendar month",
                "security_deposit": "$3,000 USD held in an escrow account",
                "pet_deposit": "$300 USD refundable pet deposit",
            },
            "custom_clauses": [
                "No subletting or short-term vacation renting without express prior written consent of the Landlord.",
                "Domestic pets allowed subject to a $300 pet deposit and compliance with community pet guidelines.",
                "Landlord shall provide at least 24 hours written notice prior to non-emergency property inspections."
            ],
            "file_prefix": "lease_agreement"
        }
    ]

    total_start_time = time.time()
    results_summary = []

    for idx, sc in enumerate(scenarios, 1):
        print(f"[{idx}/3] Executing {sc['name']}...")
        start_time = time.time()

        # 1. Generate Legal Document
        doc_res = generator.generate_document(
            doc_type=sc["doc_type"],
            parties=sc["parties"],
            jurisdiction=sc["jurisdiction"],
            custom_clauses=sc["custom_clauses"],
            tone=sc["tone"],
            specific_terms=sc["specific_terms"],
            effective_date=sc["dates"]
        )

        md_content = doc_res.get("content_markdown", "")
        assert len(md_content) > 150, f"Document content too short for {sc['name']}"
        word_count = len(md_content.split())

        # 2. Export to TXT
        txt_path = OUTPUT_DIR / f"{sc['file_prefix']}.txt"
        txt_bytes = DocumentExporter.to_txt(md_content)
        txt_path.write_bytes(txt_bytes)

        # 3. Export to HTML Preview
        html_path = OUTPUT_DIR / f"{sc['file_prefix']}.html"
        html_str = DocumentExporter.to_html(md_content)
        html_path.write_text(html_str, encoding="utf-8")

        # 4. Export to DOCX
        docx_path = OUTPUT_DIR / f"{sc['file_prefix']}.docx"
        docx_bytes = DocumentExporter.to_docx(md_content, title=sc["doc_type"])
        docx_path.write_bytes(docx_bytes)

        # 5. Export to PDF
        pdf_path = OUTPUT_DIR / f"{sc['file_prefix']}.pdf"
        pdf_bytes = DocumentExporter.to_pdf(md_content, title=sc["doc_type"])
        pdf_path.write_bytes(pdf_bytes)

        elapsed = time.time() - start_time
        print(f"    [+] Generated: {word_count} words in {elapsed:.2f}s")
        print(f"    [+] Saved: {txt_path.name} ({len(txt_bytes)} bytes)")
        print(f"    [+] Saved: {html_path.name} ({len(html_str)} chars)")
        print(f"    [+] Saved: {docx_path.name} ({len(docx_bytes)} bytes)")
        print(f"    [+] Saved: {pdf_path.name} ({len(pdf_bytes)} bytes)")
        print(f"    [OK] Scenario assertions verified.\n")

        results_summary.append({
            "scenario": sc["name"],
            "words": word_count,
            "duration": f"{elapsed:.2f}s",
            "files": [txt_path.name, html_path.name, docx_path.name, pdf_path.name]
        })

    total_duration = time.time() - total_start_time
    print("=" * 70)
    print("                   TEST EXECUTION SUMMARY                         ")
    print("=" * 70)
    for r in results_summary:
        print(f" - {r['scenario']}: {r['words']} words | Time: {r['duration']}")
        print(f"   Files: {', '.join(r['files'])}")
    print(f"\n[OK] Total Execution Time: {total_duration:.2f}s across 3 scenarios (12 files generated).")
    print("=" * 70)


if __name__ == "__main__":
    run_scenario_tests()
