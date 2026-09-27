"""
Gemini API Integration and Legal Prompt Builder Engine
"""
import os
import re
import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

# Setup logger
logger = logging.getLogger("LegalEase.Gemini")
logging.basicConfig(level=logging.INFO)

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    logger.warning("google-generativeai is not installed. Running in mock/template mode.")

from config import GEMINI_API_KEY, GEMINI_MODEL, DOCUMENT_TYPES, LEGAL_TONES


class LegalPromptEngine:
    """
    Constructs rigorous, jurisdiction-aware, and clause-rich legal system prompts.
    """

    SYSTEM_INSTRUCTION = """You are a senior partner and expert legal drafting counsel with 25+ years of specialized corporate and commercial law experience.
Your duty is to generate airtight, legally sound, enforceable, and crystal-clear contracts and legal instruments.

CRITICAL DRAFTING RULES:
1. STRUCTURE & ORGANIZATION:
   - Use standard professional contract structure: Title, Preamble (Parties & Effective Date), Recitals (WHEREAS clauses), Numbered Operational Articles/Clauses, Boilerplate Provisions (Severability, Entire Agreement, Governing Law, Force Majeure, Notices), and formal Signature Blocks.
2. JURISDICTION & GOVERNING LAW:
   - Explicitly weave in statutory nuances and compliance for the requested jurisdiction.
3. CLEAR PLACEHOLDERS:
   - Where dynamic inputs are missing, use clear bracketed identifiers like `[INSERT SPECIFIC DETAILS]` or `[OPTIONAL CLAUSE]`.
4. FORMATTING:
   - Format output in clean Markdown with clear headings (`#`, `##`, `###`), bold terms, structured bullet/numbered sub-clauses, and clean separation.
5. NO CONVERSATIONAL FILLER:
   - Return ONLY the exact legal document text. Do NOT include preambles like 'Here is your contract' or post-document chit-chat.
"""

    @classmethod
    def build_prompt(
        cls,
        doc_type: str,
        parties: Dict[str, str],
        jurisdiction: str,
        custom_clauses: List[str],
        tone: str,
        specific_terms: Dict[str, Any],
        effective_date: Optional[str] = None,
    ) -> str:
        date_str = effective_date or datetime.now().strftime("%B %d, %Y")
        doc_meta = DOCUMENT_TYPES.get(doc_type, {})
        
        parties_formatted = "\n".join([f"  - **{k.replace('_', ' ').title()}**: {v}" for k, v in parties.items() if v])
        terms_formatted = "\n".join([f"  - **{k.replace('_', ' ').title()}**: {v}" for k, v in specific_terms.items() if v])
        custom_clauses_formatted = "\n".join([f"  - {c}" for c in custom_clauses if c.strip()]) if custom_clauses else "  - Standard commercial protections applicable to this instrument."

        prompt = f"""Generate an exhaustive, professional, and binding **{doc_type}**.

### DOCUMENT PARAMETERS:
- **Instrument Type**: {doc_type}
- **Effective Date**: {date_str}
- **Governing Jurisdiction**: {jurisdiction}
- **Drafting Tone & Posture**: {tone}

### IDENTIFIED PARTIES:
{parties_formatted if parties_formatted else "  - [Standard First Party] and [Standard Second Party]"}

### KEY COMMERCIAL & OPERATIONAL TERMS:
{terms_formatted if terms_formatted else "  - Standard covenants, representations, and warranties."}

### REQUIRED SPECIAL CLAUSES & STIPULATIONS:
{custom_clauses_formatted}

### DRAFTING REQUIREMENTS:
1. Ensure full compliance with laws of {jurisdiction}.
2. Include precise definition sections, term & termination, liability caps, indemnification, dispute resolution (mediation/arbitration), and complete signature execution blocks for all parties.
3. Produce the entire finalized text ready for execution.
"""
        return prompt


class GeminiLegalGenerator:
    """
    Coordinates legal document synthesis with Google Gemini API and high-fidelity fallback templates.
    """

    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        self.api_key = api_key or GEMINI_API_KEY or os.getenv("GEMINI_API_KEY", "")
        self.model_name = model_name or GEMINI_MODEL or "gemini-1.5-pro-latest"
        self.is_configured = False

        if GENAI_AVAILABLE and self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.is_configured = True
                logger.info("Gemini AI successfully configured.")
            except Exception as e:
                logger.error(f"Failed to configure Gemini client: {e}")
                self.is_configured = False
        else:
            logger.info("Running in fallback/offline mode (No valid GEMINI_API_KEY provided).")

    def generate_document(
        self,
        doc_type: str,
        parties: Dict[str, str],
        jurisdiction: str,
        custom_clauses: Optional[List[str]] = None,
        tone: Optional[str] = None,
        specific_terms: Optional[Dict[str, Any]] = None,
        effective_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Generates document markdown content with metadata.
        """
        custom_clauses = custom_clauses or []
        tone = tone or LEGAL_TONES[1]
        specific_terms = specific_terms or {}
        
        prompt = LegalPromptEngine.build_prompt(
            doc_type=doc_type,
            parties=parties,
            jurisdiction=jurisdiction,
            custom_clauses=custom_clauses,
            tone=tone,
            specific_terms=specific_terms,
            effective_date=effective_date,
        )

        if self.is_configured and GENAI_AVAILABLE:
            try:
                model = genai.GenerativeModel(
                    model_name=self.model_name,
                    system_instruction=LegalPromptEngine.SYSTEM_INSTRUCTION
                )
                response = model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.2, # Low temperature for accurate legal drafting
                        top_p=0.95,
                        max_output_tokens=8192
                    )
                )
                generated_text = response.text.strip()
                return {
                    "status": "success",
                    "source": "gemini_api",
                    "model": self.model_name,
                    "document_type": doc_type,
                    "jurisdiction": jurisdiction,
                    "generated_at": datetime.now().isoformat(),
                    "content_markdown": generated_text,
                }
            except Exception as e:
                logger.error(f"Gemini API error during generation: {e}. Falling back to legal template engine.")
                return self._generate_fallback_template(
                    doc_type, parties, jurisdiction, custom_clauses, tone, specific_terms, effective_date, error_note=str(e)
                )
        else:
            return self._generate_fallback_template(
                doc_type, parties, jurisdiction, custom_clauses, tone, specific_terms, effective_date
            )

    def _generate_fallback_template(
        self,
        doc_type: str,
        parties: Dict[str, str],
        jurisdiction: str,
        custom_clauses: List[str],
        tone: str,
        specific_terms: Dict[str, Any],
        effective_date: Optional[str] = None,
        error_note: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Provides comprehensive, ready-to-sign fallback legal agreements when offline or without API key.
        """
        date_str = effective_date or datetime.now().strftime("%B %d, %Y")
        p1 = parties.get("disclosing_party") or parties.get("employer_name") or parties.get("landlord_name") or parties.get("client_name") or parties.get("lender_name") or parties.get("party_a") or "Party A Corp."
        p2 = parties.get("receiving_party") or parties.get("employee_name") or parties.get("tenant_name") or parties.get("contractor_name") or parties.get("borrower_name") or parties.get("party_b") or "Party B Ltd."

        # Template library
        if "Non-Disclosure" in doc_type or "NDA" in doc_type:
            content = f"""# MUTUAL NON-DISCLOSURE AND CONFIDENTIALITY AGREEMENT

**THIS MUTUAL NON-DISCLOSURE AGREEMENT** (the "Agreement") is entered into as of **{date_str}** (the "Effective Date"), by and between:

- **{p1}**, having its principal place of business at `[Address of {p1}]` ("Disclosing Party"), and
- **{p2}**, having its principal place of business at `[Address of {p2}]` ("Receiving Party").

Disclosing Party and Receiving Party are collectively referred to as the **"Parties"** or individually as a **"Party"**.

---

### RECITALS
**WHEREAS**, the Parties wish to explore and engage in discussions regarding a potential business relationship or transaction (the "**Purpose**"); and  
**WHEREAS**, in connection with such discussions, each Party may disclose to the other certain proprietary and non-public information;

**NOW, THEREFORE**, in consideration of the mutual promises and covenants herein contained, the Parties agree as follows:

---

### 1. DEFINITION OF CONFIDENTIAL INFORMATION
"**Confidential Information**" refers to any proprietary information, technical data, trade secrets, know-how, software code, product plans, customer lists, business strategies, and financial records disclosed by one Party to the other, whether orally, electronically, or in writing, designated as confidential or which reasonably should be understood to be confidential.

### 2. EXCLUSIONS FROM CONFIDENTIALITY
Confidential Information does not include information that:
- (a) Is or becomes publicly known through no breach of this Agreement;
- (b) Was already in the rightful possession of the Receiving Party prior to disclosure;
- (c) Is independently developed by the Receiving Party without reference to or reliance upon the Disclosing Party's information; or
- (d) Is rightfully received from a third party without duty of confidentiality.

### 3. OBLIGATIONS OF RECEIVING PARTY
The Receiving Party agrees to:
- (a) Hold the Disclosing Party’s Confidential Information in strict confidence using at least the same degree of care it uses for its own sensitive data, but no less than reasonable care;
- (b) Restrict disclosure solely to employees, officers, and legal/financial advisors with a legitimate need-to-know who are bound by confidentiality obligations at least as restrictive as those herein;
- (c) Not use the Confidential Information for any purpose other than the defined Purpose without prior written authorization.

### 4. TERM AND SURVIVAL
This Agreement shall govern disclosures for a period of **two (2) years** from the Effective Date. The duty of confidentiality regarding trade secrets shall survive perpetually, and for all other information, for **three (3) years** following expiration or termination.

### 5. RETURN OR DESTRUCTION OF MATERIALS
Upon written request by the Disclosing Party, the Receiving Party shall promptly return or certify the permanent destruction of all copies, extracts, and summaries of Confidential Information.

### 6. REMEDIES AND INJUNCTIVE RELIEF
The Parties acknowledge that any breach of this Agreement may cause irreparable harm for which monetary damages alone would be inadequate. Accordingly, the Disclosing Party shall be entitled to seek injunctive relief in addition to all other remedies available at law or equity.

### 7. GOVERNING LAW AND DISPUTE RESOLUTION
This Agreement shall be governed by, and construed in accordance with, the laws of the **{jurisdiction}**, without giving effect to conflict of laws principles. Any legal suit, action, or proceeding arising out of this Agreement shall be instituted exclusively in the competent courts located in **{jurisdiction}**.

### 8. MISCELLANEOUS
- **Entire Agreement**: This document constitutes the entire agreement between the Parties regarding confidentiality and supersedes all prior understandings.
- **Severability**: If any provision is found invalid or unenforceable, the remaining provisions shall remain in full force and effect.
- **Amendments**: No amendment or waiver shall be binding unless executed in writing by both Parties.

---

### IN WITNESS WHEREOF, the Parties have executed this Non-Disclosure Agreement as of the Effective Date.

| For: **{p1}** | For: **{p2}** |
| :--- | :--- |
| **Signature**: ___________________________ | **Signature**: ___________________________ |
| **Name**: `[Authorized Officer Name]` | **Name**: `[Authorized Officer Name]` |
| **Title**: `[Title / Position]` | **Title**: `[Title / Position]` |
| **Date**: `{date_str}` | **Date**: `{date_str}` |
"""
        elif "Employment" in doc_type:
            content = f"""# EXECUTIVE EMPLOYMENT AGREEMENT

**THIS EMPLOYMENT AGREEMENT** (the "Agreement") is made and entered into this **{date_str}**, by and between:

- **{p1}** ("Employer" or "Company"), and
- **{p2}** ("Employee").

---

### 1. POSITION AND DUTIES
The Employer hereby employs the Employee in the position of **`{specific_terms.get('job_title', 'Senior Associate')}`**. The Employee shall faithfully and diligently perform all duties customary to such role and follow lawful directives of the Company.

### 2. COMPENSATION AND BENEFITS
- **Base Salary**: The Company shall pay Employee a base salary of **`{specific_terms.get('salary_details', '$120,000 per annum')}`**, payable in accordance with the Company's standard payroll schedule.
- **Benefits**: Employee shall be eligible for participation in standard medical, dental, retirement, and paid leave benefits.

### 3. CONFIDENTIALITY AND INTELLECTUAL PROPERTY
- (a) **Proprietary Information**: Employee agrees not to disclose or use any trade secrets, customer records, or proprietary software belonging to Company.
- (b) **Work for Hire**: All inventions, code, designs, and works of authorship created by Employee during the course of employment shall be deemed "works made for hire" and remain the sole property of Company.

### 4. NON-SOLICITATION AND RESTRICTIVE COVENANTS
During the employment term and for a period of **twelve (12) months** following termination, Employee shall not directly or indirectly solicit any clients, employees, or contractors of Employer.

### 5. TERMINATION
Either party may terminate this agreement at-will upon providing **`{specific_terms.get('termination_notice_days', '30')}` days** prior written notice, or immediately for Cause (including fraud, gross negligence, or criminal conviction).

### 6. GOVERNING LAW
This Agreement shall be governed by, and interpreted in accordance with, the laws of **{jurisdiction}**.

---

### SIGNATURES

| **EMPLOYER**: {p1} | **EMPLOYEE**: {p2} |
| :--- | :--- |
| **By**: ___________________________ | **By**: ___________________________ |
| **Title**: Authorized Signatory | **Title**: Employee |
| **Date**: {date_str} | **Date**: {date_str} |
"""
        else:
            # Generic High-Standard Commercial Contract
            content = f"""# {doc_type.upper()}

**THIS {doc_type.upper()}** (the "Agreement") is dated **{date_str}**, by and between **{p1}** ("First Party") and **{p2}** ("Second Party").

---

### 1. PURPOSE & APPOINTMENT
The Parties enter into this Agreement to define rights, liabilities, and obligations regarding `{doc_type}` within the jurisdiction of **{jurisdiction}**.

### 2. SCOPE OF OBLIGATIONS
Each Party covenants and agrees to perform their respective obligations with high commercial diligence and standard industry care.

### 3. TERM & TERMINATION
This Agreement commences on the Effective Date and shall continue until completed or terminated by mutual written agreement or written notice in accordance with statutory standards.

### 4. LIMITATION OF LIABILITY
Neither Party shall be liable for indirect, incidental, punitive, or consequential damages arising out of or related to this Agreement. Total liability shall not exceed the aggregate fees paid under this Agreement during the preceding 12-month period.

### 5. GOVERNING LAW & JURISDICTION
This Agreement and any claims arising out of it shall be governed by the laws of **{jurisdiction}**.

---

### EXECUTION

| For: **{p1}** | For: **{p2}** |
| :--- | :--- |
| Signature: _______________________ | Signature: _______________________ |
| Date: {date_str} | Date: {date_str} |
"""

        return {
            "status": "success",
            "source": "fallback_engine" if not error_note else f"fallback_engine (API Fallback: {error_note})",
            "model": "legal-rules-engine-v1",
            "document_type": doc_type,
            "jurisdiction": jurisdiction,
            "generated_at": datetime.now().isoformat(),
            "content_markdown": content.strip(),
        }
