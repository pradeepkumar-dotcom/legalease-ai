"""
LegalEase Global Configuration & Constants
"""
import os
from pathlib import Path
try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False

# Base Directory Paths
BASE_DIR = Path(__file__).resolve().parent
AI_CORE_DIR = BASE_DIR / "ai_core"
FRONTEND_DIR = BASE_DIR / "frontend"
IMAGE_DIR = BASE_DIR / "Image"
API_DIR = BASE_DIR / "legalEaseAPI"
DOCS_DIR = BASE_DIR / "docs"

# Ensure directories exist
for directory in [AI_CORE_DIR, FRONTEND_DIR, IMAGE_DIR, API_DIR, DOCS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Load environment variables
if DOTENV_AVAILABLE:
    load_dotenv(dotenv_path=BASE_DIR / ".env")

# API & Model Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("API_PORT", 8000))
API_BASE_URL = f"http://{API_HOST}:{API_PORT}"
BACKEND_URL = os.getenv("BACKEND_URL", f"{API_BASE_URL}/api/v1")

# Brand Assets
LOGO_PATH = IMAGE_DIR / "Logo.png"
INVERSE_LOGO_PATH = IMAGE_DIR / "inverseLogo.png"

# Supported Legal Document Types & Categories
DOCUMENT_TYPES = {
    "Non-Disclosure Agreement (NDA)": {
        "description": "Mutual or unilateral confidentiality agreement protecting trade secrets and proprietary data.",
        "icon": "🔒",
        "default_jurisdiction": "State of Delaware, USA",
        "key_fields": ["disclosing_party", "receiving_party", "purpose", "term_years", "confidential_scope", "governing_law"],
    },
    "Employment Agreement": {
        "description": "Comprehensive full-time or part-time employment contract with IP assignment, non-compete, and benefits.",
        "icon": "💼",
        "default_jurisdiction": "State of California, USA",
        "key_fields": ["employer_name", "employee_name", "job_title", "salary_details", "start_date", "termination_notice_days", "governing_law"],
    },
    "Independent Contractor / Freelance Agreement": {
        "description": "Service-for-hire contract clarifying independent contractor status, deliverables, IP ownership, and payment milestones.",
        "icon": "🤝",
        "default_jurisdiction": "State of New York, USA",
        "key_fields": ["client_name", "contractor_name", "scope_of_work", "payment_rate", "milestones", "ip_assignment", "governing_law"],
    },
    "Residential / Commercial Lease Agreement": {
        "description": "Lease contract detailing rental property terms, security deposits, maintenance obligations, and tenant rules.",
        "icon": "🏢",
        "default_jurisdiction": "State of Texas, USA",
        "key_fields": ["landlord_name", "tenant_name", "property_address", "monthly_rent", "security_deposit", "lease_term_months", "governing_law"],
    },
    "Software as a Service (SaaS) Terms of Service": {
        "description": "Online customer agreement covering user licenses, data security, uptime SLA, warranties, and liability caps.",
        "icon": "☁️",
        "default_jurisdiction": "State of Delaware, USA",
        "key_fields": ["company_name", "product_name", "acceptable_use_summary", "subscription_fees", "liability_cap_amount", "governing_law"],
    },
    "Privacy Policy (GDPR / CCPA Compliant)": {
        "description": "Comprehensive data privacy policy informing users regarding data collection, cookies, GDPR/CCPA rights, and contact details.",
        "icon": "🛡️",
        "default_jurisdiction": "European Union / California, USA",
        "key_fields": ["company_name", "website_url", "data_collected", "cookies_used", "dpo_contact_email", "governing_law"],
    },
    "Partnership / Operating Agreement": {
        "description": "Co-founder or LLC operating contract covering equity split, voting rights, capital contributions, and buyout provisions.",
        "icon": "👥",
        "default_jurisdiction": "State of Delaware, USA",
        "key_fields": ["partnership_name", "partner_names", "ownership_percentages", "capital_contributions", "profit_distribution", "governing_law"],
    },
    "Cease & Desist Letter": {
        "description": "Formal legal notice demanding immediate cessation of trademark infringement, copyright violation, defamation, or breach.",
        "icon": "⚠️",
        "default_jurisdiction": "United States Federal Jurisdiction",
        "key_fields": ["sender_name", "recipient_name", "infringing_act", "evidence_summary", "compliance_deadline_days", "legal_basis"],
    },
    "Power of Attorney (General / Limited)": {
        "description": "Legal authorization appointing an attorney-in-fact to manage financial, business, or legal affairs.",
        "icon": "📜",
        "default_jurisdiction": "State of Florida, USA",
        "key_fields": ["principal_name", "agent_name", "scope_of_powers", "effective_date", "revocation_terms", "governing_law"],
    },
    "Promissory Note & Loan Agreement": {
        "description": "Legally binding debt agreement outlining principal loan amount, interest rates, repayment schedule, and default penalties.",
        "icon": "💵",
        "default_jurisdiction": "State of Illinois, USA",
        "key_fields": ["lender_name", "borrower_name", "principal_amount", "interest_rate", "repayment_schedule", "maturity_date", "governing_law"],
    }
}

# Legal Tones
LEGAL_TONES = [
    "Strict & Comprehensive (Maximum Protection)",
    "Balanced & Standard Commercial",
    "Plain-Language / Friendly (Startups & Modern Businesses)",
    "Aggressive Enforcement (Cease & Desist / Litigation Preparation)"
]
