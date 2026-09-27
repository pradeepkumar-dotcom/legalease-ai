"""
End-to-end verification test suite for LegalEase
"""
import sys
import os
from pathlib import Path

# Add root directory to sys.path
ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR))

from config import DOCUMENT_TYPES, LEGAL_TONES
from ai_core.gemini_generator import LegalPromptEngine, GeminiLegalGenerator
from ai_core.generator import DocumentExporter

def run_tests():
    print("==================================================")
    print("      Testing LegalEase End-to-End Suite          ")
    print("==================================================")
    
    # 1. Test Prompt Engine
    print("\n[1] Testing LegalPromptEngine...")
    prompt = LegalPromptEngine.build_prompt(
        doc_type="Non-Disclosure Agreement (NDA)",
        parties={"disclosing_party": "Acme Inc.", "receiving_party": "Beta Corp."},
        jurisdiction="State of Delaware, USA",
        custom_clauses=["30-day cure period"],
        tone=LEGAL_TONES[0],
        specific_terms={"term_years": "3"}
    )
    assert "Acme Inc." in prompt
    assert "State of Delaware, USA" in prompt
    print("  [OK] Prompt Engine successfully constructed legal prompt.")

    # 2. Test GeminiLegalGenerator
    print("\n[2] Testing GeminiLegalGenerator (Fallback / Template)...")
    generator = GeminiLegalGenerator()
    doc_result = generator.generate_document(
        doc_type="Non-Disclosure Agreement (NDA)",
        parties={"disclosing_party": "Acme Inc.", "receiving_party": "Beta Corp."},
        jurisdiction="State of Delaware, USA",
        custom_clauses=["30-day cure period"],
        tone=LEGAL_TONES[0],
        specific_terms={"term_years": "3"}
    )
    assert doc_result["status"] == "success"
    md_content = doc_result["content_markdown"]
    assert len(md_content) > 100
    print(f"  [OK] Document generated successfully ({len(md_content.split())} words).")

    # 3. Test Export Engine
    print("\n[3] Testing Document Exporter (TXT, HTML, DOCX, PDF)...")
    
    # TXT
    txt_bytes = DocumentExporter.to_txt(md_content)
    assert len(txt_bytes) > 0
    print(f"  [OK] TXT Export: {len(txt_bytes)} bytes")

    # HTML
    html_str = DocumentExporter.to_html(md_content)
    assert "div style=" in html_str
    print(f"  [OK] HTML Formatter: {len(html_str)} chars")

    # DOCX
    docx_bytes = DocumentExporter.to_docx(md_content, title="Test Document")
    assert len(docx_bytes) > 0
    print(f"  [OK] DOCX Export: {len(docx_bytes)} bytes")

    # PDF
    pdf_bytes = DocumentExporter.to_pdf(md_content, title="Test Document")
    assert len(pdf_bytes) > 0
    print(f"  [OK] PDF Export: {len(pdf_bytes)} bytes")

    print("\n==================================================")
    print("  ALL TESTS PASSED SUCCESSFULLY!                  ")
    print("==================================================")

if __name__ == "__main__":
    run_tests()
