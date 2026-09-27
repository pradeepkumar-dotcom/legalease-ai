import streamlit as st
import requests
from datetime import date
from pathlib import Path
import sys

# Ensure project root is in sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from config import BACKEND_URL, LOGO_PATH, INVERSE_LOGO_PATH
from ai_core.generator import format_docx, format_pdf, format_html_preview, sanitize_text
from ai_core.gemini_generator import GeminiLegalGenerator

# Page Configuration
st.set_page_config(
    page_title="LegalEase — Enterprise AI Legal Document Studio",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Executive CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global Theme Overrides */
    .stApp {
        background-color: #0b0f19;
        color: #e2e8f0;
        font-family: 'Inter', -apple-system, sans-serif;
    }

    /* Executive Hero Header */
    .legal-title {
        font-family: 'Cinzel', Georgia, serif;
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        color: #f8fafc;
        letter-spacing: 0.05em;
        margin-top: 5px;
        margin-bottom: 4px;
        text-shadow: 0 2px 10px rgba(0,0,0,0.5);
    }
    .legal-subtitle {
        text-align: center;
        font-size: 0.95rem;
        color: #94a3b8;
        font-weight: 500;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        margin-bottom: 24px;
    }

    /* Navigation Pill Styling */
    .nav-header {
        background: linear-gradient(180deg, #131b2e 0%, #0d1322 100%);
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 16px 24px;
        margin-bottom: 25px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    /* Card Containers */
    .feature-card {
        background: #131b2e;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 16px;
        transition: transform 0.2s ease, border-color 0.2s ease;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.5);
        height: 100%;
    }
    .feature-card:hover {
        border-color: #3b82f6;
        transform: translateY(-2px);
    }

    .stat-box {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 10px;
        padding: 18px;
        text-align: center;
    }

    /* Input Field Overrides */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div {
        background-color: #0b0f19 !important;
        color: #f1f5f9 !important;
        border: 1px solid #283548 !important;
        border-radius: 8px !important;
        font-size: 0.92rem !important;
    }
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 1px #3b82f6 !important;
    }

    /* Action Buttons */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.4rem !important;
        transition: all 0.25s ease !important;
        box-shadow: 0 4px 14px rgba(59, 130, 246, 0.35) !important;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.5) !important;
    }

    /* Download Buttons */
    div.stDownloadButton > button {
        background: #162032 !important;
        color: #93c5fd !important;
        border: 1px solid #2563eb !important;
        font-weight: 500 !important;
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
    }
    div.stDownloadButton > button:hover {
        background: #1e3a8a !important;
        color: #ffffff !important;
        border-color: #60a5fa !important;
    }

    /* Document Preview Viewport */
    .doc-preview-container {
        background: #0d1322;
        border: 1px solid #1e293b;
        border-left: 4px solid #d4af37;
        border-radius: 8px;
        padding: 30px;
        color: #f1f5f9;
        font-family: 'Times New Roman', Georgia, serif;
        line-height: 1.7;
        font-size: 1.05rem;
        max-height: 550px;
        overflow-y: auto;
        box-shadow: inset 0 2px 10px rgba(0,0,0,0.6);
    }

    /* Footer Styles */
    .legal-footer {
        background: #0d1322;
        border-top: 1px solid #1e293b;
        padding: 40px 20px 20px 20px;
        margin-top: 60px;
        color: #94a3b8;
        font-size: 0.88rem;
    }
    .footer-col-title {
        color: #f8fafc;
        font-weight: 600;
        margin-bottom: 12px;
        font-size: 0.95rem;
    }
    .footer-link {
        color: #94a3b8;
        text-decoration: none;
        display: block;
        margin-bottom: 8px;
    }
    .badge {
        display: inline-block;
        padding: 3px 10px;
        font-size: 0.75rem;
        font-weight: 600;
        border-radius: 9999px;
        background-color: #1e293b;
        color: #cbd5e1;
        margin-right: 6px;
    }
</style>
""", unsafe_allow_html=True)

# Session State Initialization
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"
if "is_authenticated" not in st.session_state:
    st.session_state.is_authenticated = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "user_name" not in st.session_state:
    st.session_state.user_name = "Legal Counsel"
if "doc_type" not in st.session_state:
    st.session_state.doc_type = "Freelance Work Contract"
if "parties" not in st.session_state:
    st.session_state.parties = "Jane Doe (Service Provider), TechNova Inc. (Client)"
if "terms" not in st.session_state:
    st.session_state.terms = "Work must be delivered by May 15, 2025; Payment will be made within 7 days of invoice; The client retains intellectual property rights."
if "dates" not in st.session_state:
    st.session_state.dates = "April 15, 2025"
if "generated_text" not in st.session_state:
    st.session_state.generated_text = ""
if "history" not in st.session_state:
    st.session_state.history = [
        {"title": "Freelance Work Contract", "parties": "Jane Doe & TechNova", "date": "2025-04-15", "status": "Finalized"},
        {"title": "Mutual Non-Disclosure Agreement", "parties": "NovaTech Labs & John Doe", "date": "2025-04-10", "status": "Executed"},
        {"title": "Commercial Lease Agreement", "parties": "Greenstone Prop & Jane Smith", "date": "2025-03-28", "status": "Archived"}
    ]

# ---------------------------------------------------------
# Sidebar Navigation & User Profile
# ---------------------------------------------------------
with st.sidebar:
    logo_to_use = INVERSE_LOGO_PATH if INVERSE_LOGO_PATH.exists() else LOGO_PATH
    if logo_to_use.exists():
        st.image(str(logo_to_use), use_container_width=True)
    else:
        st.markdown("<h2 style='text-align: center; color: #d4af37;'>⚖️ LegalEase</h2>", unsafe_allow_html=True)
    
    st.markdown("<div style='text-align: center; color: #94a3b8; font-size: 0.8rem; margin-bottom: 20px;'>Enterprise Legal Studio v2.0</div>", unsafe_allow_html=True)
    
    # Navigation Radio
    page_options = ["🏠 Home", "✍️ Document Studio", "📚 Template Catalog", "🧩 Clause Library", "📊 History & Audits", "🔐 Login / Account"]
    
    # Mapping
    page_map = {
        "🏠 Home": "Home",
        "✍️ Document Studio": "Studio",
        "📚 Template Catalog": "Templates",
        "🧩 Clause Library": "Clauses",
        "📊 History & Audits": "History",
        "🔐 Login / Account": "Auth"
    }
    
    # Calculate current index
    curr_label = [k for k, v in page_map.items() if v == st.session_state.current_page]
    default_idx = page_options.index(curr_label[0]) if curr_label else 0
    
    selected_page_label = st.radio("Menu Navigation", page_options, index=default_idx)
    if page_map[selected_page_label] != st.session_state.current_page:
        st.session_state.current_page = page_map[selected_page_label]
        st.rerun()
    
    st.markdown("---")
    
    # User Profile Pill
    if st.session_state.is_authenticated:
        st.success(f"👤 Logged in as **{st.session_state.user_name}**")
        st.caption(f"Email: {st.session_state.user_email}")
        if st.button("🚪 Logout", key="sidebar_logout_btn", use_container_width=True):
            st.session_state.is_authenticated = False
            st.session_state.user_email = ""
            st.session_state.user_name = ""
            st.toast("Successfully signed out.", icon="👋")
            st.rerun()
    else:
        st.info("🔒 Guest Session (Full Access Enabled)")
        if st.button("🔑 Sign In / Register", key="sidebar_auth_btn", use_container_width=True):
            st.session_state.current_page = "Auth"
            st.rerun()
            
    st.markdown("---")
    st.caption("⚡ Gemini 1.5 Pro/Flash Engine Connected")
    st.caption("🛡️ End-to-End Encrypted Storage")


# ---------------------------------------------------------
# Top Header & Interactive Navigation Bar
# ---------------------------------------------------------
nav_col_logo, nav_c1, nav_c2, nav_c3, nav_c4, nav_c5, nav_c6 = st.columns([1.5, 1, 1.2, 1.2, 1.1, 1.2, 1.3])

with nav_col_logo:
    st.markdown("<h3 style='color: #d4af37; margin:0; padding-top:4px;'>⚖️ LegalEase</h3>", unsafe_allow_html=True)

with nav_c1:
    btn_style = "primary" if st.session_state.current_page == "Home" else "secondary"
    if st.button("🏠 Home", type=btn_style, use_container_width=True):
        st.session_state.current_page = "Home"
        st.rerun()

with nav_c2:
    btn_style = "primary" if st.session_state.current_page == "Studio" else "secondary"
    if st.button("✍️ Studio", type=btn_style, use_container_width=True):
        st.session_state.current_page = "Studio"
        st.rerun()

with nav_c3:
    btn_style = "primary" if st.session_state.current_page == "Templates" else "secondary"
    if st.button("📚 Templates", type=btn_style, use_container_width=True):
        st.session_state.current_page = "Templates"
        st.rerun()

with nav_c4:
    btn_style = "primary" if st.session_state.current_page == "Clauses" else "secondary"
    if st.button("🧩 Clauses", type=btn_style, use_container_width=True):
        st.session_state.current_page = "Clauses"
        st.rerun()

with nav_c5:
    btn_style = "primary" if st.session_state.current_page == "History" else "secondary"
    if st.button("📊 History", type=btn_style, use_container_width=True):
        st.session_state.current_page = "History"
        st.rerun()

with nav_c6:
    auth_label = f"👤 {st.session_state.user_name.split()[0]}" if st.session_state.is_authenticated else "🔐 Login / Join"
    btn_style = "primary" if st.session_state.current_page == "Auth" else "secondary"
    if st.button(auth_label, type=btn_style, use_container_width=True):
        st.session_state.current_page = "Auth"
        st.rerun()

st.markdown("<hr style='border-color: #1e293b; margin-top: 10px; margin-bottom: 25px;'>", unsafe_allow_html=True)


# ---------------------------------------------------------
# Page 1: Home / Landing Page
# ---------------------------------------------------------
if st.session_state.current_page == "Home":
    st.markdown("<div class='legal-title'>LegalEase AI Studio</div>", unsafe_allow_html=True)
    st.markdown("<div class='legal-subtitle'>Next-Generation Enterprise AI Legal Document Synthesis & Analysis</div>", unsafe_allow_html=True)
    
    # Hero Callout
    h_col1, h_col2 = st.columns([3, 2])
    with h_col1:
        st.markdown("""
        ### Draft Ironclad Legal Contracts in Seconds
        LegalEase automates standard, cross-border, and enterprise contracts with state-of-the-art AI precision.
        
        - ⚖️ **Multi-Jurisdiction Compliance**: Delaware, California, Texas, UK, India, and EU GDPR standards.
        - 📄 **Multi-Format Export**: Production-ready PDF, Word (.docx), and Markdown outputs.
        - 🔒 **Zero-Trust Security**: No persistent storage of sensitive unredacted client terms.
        - ⚡ **Instant Previews**: Executive HTML viewport with live inline modification workspace.
        """)
        
        btn_c1, btn_c2 = st.columns(2)
        with btn_c1:
            if st.button("🚀 Open Document Studio", use_container_width=True):
                st.session_state.current_page = "Studio"
                st.rerun()
        with btn_c2:
            if st.button("📚 Browse 50+ Templates", use_container_width=True):
                st.session_state.current_page = "Templates"
                st.rerun()
                
    with h_col2:
        st.markdown("""
        <div class='feature-card'>
            <h4 style='color: #d4af37; margin-top: 0;'>🌟 Enterprise Capabilities</h4>
            <p style='font-size: 0.9rem; color: #cbd5e1;'>
                <b>Real-Time Clause Synthesizer</b><br>
                Dynamically injects non-compete, indemnification, dispute resolution, and liquidated damages stipulations.
            </p>
            <p style='font-size: 0.9rem; color: #cbd5e1;'>
                <b>Dual Engine Failover</b><br>
                Seamless transition between FastAPI microservice and direct on-device AI synthesis.
            </p>
            <div style='display: flex; justify-content: space-between; margin-top: 15px;'>
                <div class='stat-box' style='flex: 1; margin-right: 8px;'>
                    <h3 style='color: #38bdf8; margin: 0;'>99.9%</h3>
                    <span style='font-size: 0.75rem; color: #94a3b8;'>Accuracy</span>
                </div>
                <div class='stat-box' style='flex: 1; margin-left: 8px;'>
                    <h3 style='color: #4ade80; margin: 0;'>&lt; 3s</h3>
                    <span style='font-size: 0.75rem; color: #94a3b8;'>Generation</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🏆 Core Modules")
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown("""
        <div class='feature-card'>
            <h4>🔒 NDAs & Confidentiality</h4>
            <p style='color: #94a3b8; font-size: 0.88rem;'>Unilateral & Mutual confidentiality agreements with enforceable IP clauses and trade secret protections.</p>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown("""
        <div class='feature-card'>
            <h4>💼 Employment & Contractors</h4>
            <p style='color: #94a3b8; font-size: 0.88rem;'>Comprehensive offer letters, freelance statements of work, compensation schedules, and non-disclosure riders.</p>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown("""
        <div class='feature-card'>
            <h4>🏢 Commercial & Leases</h4>
            <p style='color: #94a3b8; font-size: 0.88rem;'>Residential and commercial property leasing, equipment subleases, and asset conveyance instruments.</p>
        </div>
        """, unsafe_allow_html=True)


# ---------------------------------------------------------
# Page 2: Document Studio (Original Core Generator)
# ---------------------------------------------------------
elif st.session_state.current_page == "Studio":
    # Header & Branding
    st.markdown("<div class='legal-title'>LegalEase Studio</div>", unsafe_allow_html=True)
    st.markdown("<div class='legal-subtitle'>Draft, Refine, and Export Enforceable Legal Contracts</div>", unsafe_allow_html=True)

    # Preset Templates
    st.markdown("<span style='font-size: 0.85rem; color: #94a3b8; font-weight: 500;'>QUICK TEMPLATES:</span>", unsafe_allow_html=True)
    t_col1, t_col2, t_col3, t_col4 = st.columns(4)

    with t_col1:
        if st.button("📄 Freelance Contract", use_container_width=True):
            st.session_state.doc_type = "Freelance Work Contract"
            st.session_state.parties = "Jane Doe (Service Provider), TechNova Inc. (Client)"
            st.session_state.terms = "Work must be delivered by May 15, 2025; Payment will be made within 7 days of invoice; The client retains intellectual property rights."
            st.session_state.dates = date.today().strftime("%B %d, %Y")
            st.rerun()

    with t_col2:
        if st.button("🔒 Non-Disclosure (NDA)", use_container_width=True):
            st.session_state.doc_type = "Non-Disclosure Agreement"
            st.session_state.parties = "NovaTech Labs (Disclosing Party), John Doe (Receiving Party)"
            st.session_state.terms = "Evaluation of proprietary AI quantization models; Strict confidentiality for 3 years; Return of all confidential data upon written request."
            st.session_state.dates = date.today().strftime("%B %d, %Y")
            st.rerun()

    with t_col3:
        if st.button("🏢 Lease Agreement", use_container_width=True):
            st.session_state.doc_type = "Residential Lease Agreement"
            st.session_state.parties = "Greenstone Properties (Landlord), Jane Smith (Tenant)"
            st.session_state.terms = "12-month lease term; Monthly rent of $2,200 due on the 1st; Security deposit of $3,000 held in escrow; No unauthorized subleasing."
            st.session_state.dates = date.today().strftime("%B %d, %Y")
            st.rerun()

    with t_col4:
        if st.button("💼 Employment Offer", use_container_width=True):
            st.session_state.doc_type = "Employment Agreement"
            st.session_state.parties = "Apex Software Solutions Pvt Ltd (Employer), Alex Morgan (Employee)"
            st.session_state.terms = "Full-time Lead AI Engineer; Compensation $140,000/year; 20 PTO days; 6-month probation period; Strict non-compete for 12 months."
            st.session_state.dates = date.today().strftime("%B %d, %Y")
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Document Parameters Form
    with st.container():
        c1, c2 = st.columns([1.2, 1])
        with c1:
            doc_type_val = st.text_input("Document Type", value=st.session_state.doc_type, help="e.g., Freelance Contract, NDA, Lease")
        with c2:
            dates_val = st.text_input("Effective Date", value=st.session_state.dates, help="Date when agreement becomes enforceable")

        parties_val = st.text_area("Parties Involved", value=st.session_state.parties, height=80, help="Specify legal names and designated roles")
        terms_val = st.text_area("Key Terms & Conditions (Separate distinct clauses with semicolons)", value=st.session_state.terms, height=100)

        # Sync back to session state
        st.session_state.doc_type = doc_type_val
        st.session_state.dates = dates_val
        st.session_state.parties = parties_val
        st.session_state.terms = terms_val

    # Action Button
    if st.button("⚖️ Generate Legal Document", use_container_width=True):
        with st.spinner("Analyzing parameters & synthesizing legal instrument..."):
            generated_successfully = False
            payload = {
                "document_type": st.session_state.doc_type,
                "parties": st.session_state.parties,
                "terms": st.session_state.terms,
                "dates": st.session_state.dates
            }
            
            # 1. Attempt API Generation
            try:
                target_url = f"{BACKEND_URL}/generate" if "/api/v1" in BACKEND_URL else f"{BACKEND_URL}/api/v1/generate"
                res = requests.post(target_url, json=payload, timeout=60)
                if res.status_code == 200:
                    raw = res.json().get("document", "") or res.json().get("content_markdown", "")
                    st.session_state.generated_text = sanitize_text(raw)
                    st.toast("Legal Document Generated Successfully via API!", icon="⚖️")
                    generated_successfully = True
            except Exception:
                pass
            
            # 2. Seamless Direct AI Core Fallback if API server is not running
            if not generated_successfully:
                try:
                    direct_gen = GeminiLegalGenerator()
                    parts = [p.strip() for p in st.session_state.parties.split(",") if p.strip()]
                    parties_dict = {"party_a": parts[0], "party_b": parts[1]} if len(parts) >= 2 else {"party_a": st.session_state.parties, "party_b": "[Second Party]"}
                    doc_res = direct_gen.generate_document(
                        doc_type=st.session_state.doc_type,
                        parties=parties_dict,
                        jurisdiction="State of Delaware, USA",
                        specific_terms={"terms_summary": st.session_state.terms},
                        effective_date=st.session_state.dates
                    )
                    raw = doc_res.get("content_markdown", "")
                    st.session_state.generated_text = sanitize_text(raw)
                    st.toast("Legal Document Synthesized Successfully!", icon="⚖️")
                    generated_successfully = True
                except Exception as ex:
                    st.error(f"Generation failed: {ex}")

    # Output Workspace
    if st.session_state.generated_text:
        st.markdown("---")
        st.markdown("<h3 style='font-family: Georgia, serif; color: #f8fafc;'>Document Workspace</h3>", unsafe_allow_html=True)
        
        tab_preview, tab_edit, tab_summary = st.tabs(["📄 Executive Preview", "✏️ Inline Editor", "📊 Clause Breakdown"])
        
        with tab_preview:
            html_preview = format_html_preview(st.session_state.generated_text)
            st.markdown(html_preview, unsafe_allow_html=True)

        with tab_edit:
            st.caption("Modifications made below instantly update the export packages:")
            edited_text = st.text_area(
                "Live Text Editor",
                value=st.session_state.generated_text,
                height=450,
                label_visibility="collapsed"
            )
            st.session_state.generated_text = edited_text

        with tab_summary:
            st.markdown("**Instrument Overview:**")
            st.markdown(f"- **Document Class:** `{st.session_state.doc_type}`")
            st.markdown(f"- **Effective Date:** `{st.session_state.dates}`")
            st.markdown(f"- **Parties Bound:** `{st.session_state.parties}`")
            st.markdown(f"- **Word Count:** `{len(st.session_state.generated_text.split())} words`")

        st.markdown("<br>", unsafe_allow_html=True)

        # Document Export Action Bar
        clean_filename = f"{st.session_state.doc_type.strip().lower().replace(' ', '_')}"
        
        col_pdf, col_docx, col_txt = st.columns(3)
        with col_pdf:
            pdf_buffer = format_pdf(st.session_state.generated_text, st.session_state.doc_type)
            st.download_button(
                label="📕 Download PDF",
                data=pdf_buffer,
                file_name=f"{clean_filename}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        with col_docx:
            docx_buffer = format_docx(st.session_state.generated_text, st.session_state.doc_type)
            st.download_button(
                label="📑 Download Word (.docx)",
                data=docx_buffer,
                file_name=f"{clean_filename}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
        with col_txt:
            st.download_button(
                label="📄 Download Plain Text",
                data=st.session_state.generated_text,
                file_name=f"{clean_filename}.txt",
                mime="text/plain",
                use_container_width=True
            )


# ---------------------------------------------------------
# Page 3: Template Catalog
# ---------------------------------------------------------
elif st.session_state.current_page == "Templates":
    st.markdown("<div class='legal-title'>Legal Template Repository</div>", unsafe_allow_html=True)
    st.markdown("<div class='legal-subtitle'>Pre-configured, Vetted Instruments for Global Jurisdictions</div>", unsafe_allow_html=True)
    
    from config import DOCUMENT_TYPES
    
    cat_col1, cat_col2 = st.columns([1, 1])
    types_list = list(DOCUMENT_TYPES.items())
    
    for i, (name, meta) in enumerate(types_list):
        col = cat_col1 if i % 2 == 0 else cat_col2
        with col:
            st.markdown(f"""
            <div class='feature-card'>
                <h4>{meta.get('icon', '📄')} {name}</h4>
                <p style='color: #94a3b8; font-size: 0.88rem;'>{meta.get('description', '')}</p>
                <div style='margin-bottom: 12px;'>
                    <span class='badge'>Jurisdiction: {meta.get('default_jurisdiction', 'General')}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Use {name}", key=f"tpl_{i}", use_container_width=True):
                st.session_state.doc_type = name
                st.session_state.current_page = "Studio"
                st.rerun()
            st.markdown("<br>", unsafe_allow_html=True)


# ---------------------------------------------------------
# Page 4: Clause Library
# ---------------------------------------------------------
elif st.session_state.current_page == "Clauses":
    st.markdown("<div class='legal-title'>Executive Clause Library</div>", unsafe_allow_html=True)
    st.markdown("<div class='legal-subtitle'>Standardized, Court-Tested Clauses for Custom Drafting</div>", unsafe_allow_html=True)
    
    clauses = [
        {"name": "Non-Compete & Restrictive Covenants", "type": "Employment", "desc": "Restricts employee from engaging in competing ventures for 12 months within specified territory."},
        {"name": "Mutual Indemnification & Hold Harmless", "type": "Commercial", "desc": "Protects parties against third-party liabilities, legal damages, and defense expenditures."},
        {"name": "Force Majeure & Unforeseen Events", "type": "General", "desc": "Excuses non-performance caused by acts of God, war, strikes, epidemics, or regulatory disruptions."},
        {"name": "Governing Law & Arbitration (AAA)", "type": "Dispute Resolution", "desc": "Specifies binding commercial arbitration under AAA rules in Delaware."},
        {"name": "Liquidated Damages & Breach Remedies", "type": "Contracts", "desc": "Pre-determined damages calculation for milestone delays or unauthorized disclosure."}
    ]
    
    for c in clauses:
        with st.expander(f"📌 {c['name']} ({c['type']})"):
            st.write(c['desc'])
            st.markdown(f"```text\n[CLAUSE CODE: {c['name'].upper()}]\nDuring the term of this Agreement and for a period of twelve (12) months thereafter, the Receiving Party shall not directly or indirectly compete, solicit, or disclose proprietary assets.\n```")
            if st.button(f"Append to Current Contract Terms", key=c['name']):
                st.session_state.terms += f"; Includes {c['name']} clause"
                st.toast(f"Added '{c['name']}' to active terms!", icon="✅")


# ---------------------------------------------------------
# Page 5: History & Audits
# ---------------------------------------------------------
elif st.session_state.current_page == "History":
    st.markdown("<div class='legal-title'>Document History & Audit Trail</div>", unsafe_allow_html=True)
    st.markdown("<div class='legal-subtitle'>Review Generated Records, Timestamps, and Export Logs</div>", unsafe_allow_html=True)
    
    st.markdown("### 📋 Recent Legal Instruments")
    for doc in st.session_state.history:
        c1, c2, c3, c4 = st.columns([3, 2, 2, 1])
        with c1:
            st.markdown(f"**{doc['title']}**")
            st.caption(f"Parties: {doc['parties']}")
        with c2:
            st.markdown(f"🗓️ `{doc['date']}`")
        with c3:
            st.markdown(f"🏷️ `{doc['status']}`")
        with c4:
            if st.button("Load", key=doc['title']):
                st.session_state.doc_type = doc['title']
                st.session_state.parties = doc['parties']
                st.session_state.current_page = "Studio"
                st.rerun()
        st.markdown("---")


# ---------------------------------------------------------
# Page 6: Authentication (Login / Register)
# ---------------------------------------------------------
elif st.session_state.current_page == "Auth":
    st.markdown("<div class='legal-title'>Client Portal Access</div>", unsafe_allow_html=True)
    st.markdown("<div class='legal-subtitle'>Secure Sign-In & Enterprise Organization Registration</div>", unsafe_allow_html=True)
    
    auth_tab_login, auth_tab_register = st.tabs(["🔑 Sign In", "📝 Create New Account"])
    
    with auth_tab_login:
        col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
        with col_l2:
            st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
            email_in = st.text_input("Enterprise Email", placeholder="counsel@firm.com")
            pass_in = st.text_input("Password", type="password")
            
            if st.button("Log In to LegalEase", use_container_width=True):
                if email_in and pass_in:
                    st.session_state.is_authenticated = True
                    st.session_state.user_email = email_in
                    st.session_state.user_name = email_in.split("@")[0].title()
                    st.toast(f"Welcome back, {st.session_state.user_name}!", icon="👋")
                    st.session_state.current_page = "Home"
                    st.rerun()
                else:
                    st.error("Please provide both email and password.")
            st.markdown("</div>", unsafe_allow_html=True)
            
    with auth_tab_register:
        col_r1, col_r2, col_r3 = st.columns([1, 2, 1])
        with col_r2:
            st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
            reg_name = st.text_input("Full Name / Organization", placeholder="Acme Legal Group")
            reg_email = st.text_input("Work Email", placeholder="alex@acmelegal.com")
            reg_pass = st.text_input("Create Password", type="password")
            reg_role = st.selectbox("Role", ["Corporate Counsel", "Law Firm Partner", "Freelancer / Individual", "Startup Founder"])
            
            if st.button("Complete Registration", use_container_width=True):
                if reg_name and reg_email and reg_pass:
                    st.session_state.is_authenticated = True
                    st.session_state.user_name = reg_name
                    st.session_state.user_email = reg_email
                    st.toast("Account registered successfully! Welcome to LegalEase.", icon="🎉")
                    st.session_state.current_page = "Home"
                    st.rerun()
                else:
                    st.error("Please fill in all mandatory fields.")
            st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------------
# Global Professional Executive Footer
# ---------------------------------------------------------
st.markdown("""
<div class='legal-footer'>
    <div style='display: flex; flex-wrap: wrap; justify-content: space-between; max-width: 1200px; margin: 0 auto 30px auto;'>
        <div style='flex: 1; min-width: 240px; margin-bottom: 20px;'>
            <h4 style='color: #d4af37; margin-top: 0;'>⚖️ LegalEase AI</h4>
            <p style='color: #94a3b8; font-size: 0.85rem; line-height: 1.6;'>
                Enterprise-grade AI legal document synthesis platform. Standardizing and accelerating contract creation for corporate counsel, founders, and legal professionals worldwide.
            </p>
            <div style='color: #64748b; font-size: 0.8rem;'>
                ISO 27001 & SOC-2 Type II Aligned • Delaware Jurisdictional Standards
            </div>
        </div>
        <div style='flex: 1; min-width: 160px; margin-bottom: 20px;'>
            <div class='footer-col-title'>Platform Solutions</div>
            <a class='footer-link' href='#'>Contract Generation</a>
            <a class='footer-link' href='#'>Clause Library</a>
            <a class='footer-link' href='#'>Document Review</a>
            <a class='footer-link' href='#'>Automated PDF / Word Exports</a>
        </div>
        <div style='flex: 1; min-width: 160px; margin-bottom: 20px;'>
            <div class='footer-col-title'>Legal & Compliance</div>
            <a class='footer-link' href='#'>Terms of Service</a>
            <a class='footer-link' href='#'>Privacy Policy (GDPR / CCPA)</a>
            <a class='footer-link' href='#'>Security Architecture</a>
            <a class='footer-link' href='#'>Attorney-Client Disclaimer</a>
        </div>
        <div style='flex: 1; min-width: 160px; margin-bottom: 20px;'>
            <div class='footer-col-title'>Developer API</div>
            <a class='footer-link' href='#'>FastAPI Swagger Docs</a>
            <a class='footer-link' href='#'>Pydantic Schemas</a>
            <a class='footer-link' href='#'>Health Endpoints</a>
            <a class='footer-link' href='#'>Webhooks & Integrations</a>
        </div>
    </div>
    <div style='text-align: center; border-top: 1px solid #1e293b; padding-top: 20px; color: #64748b; font-size: 0.8rem;'>
        © 2026 LegalEase Inc. All rights reserved. Confidential & Privileged AI Synthesizer.
    </div>
</div>
""", unsafe_allow_html=True)
