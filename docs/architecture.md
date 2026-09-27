# LegalEase: System Architecture & Technical Specification

## 1. Executive Summary
**LegalEase** is an enterprise-grade AI-powered legal document generation platform designed to synthesize jurisdiction-compliant, contractually binding, and tailored commercial agreements. The platform bridges large language model reasoning (via Google Gemini) with deterministic document formatting engines to produce courtroom-ready `.pdf`, `.docx`, and `.txt` instruments.

---

## 2. High-Level Architecture

```
                                    +----------------------------+
                                    |     User / Web Client      |
                                    +--------------+-------------+
                                                   |
                        +--------------------------+--------------------------+
                        |                                                     |
                        v                                                     v
          +-----------------------------+                       +-----------------------------+
          |  Streamlit Frontend (8501)  |                       |   FastAPI REST API (8000)   |
          |  (Interactive UI / Editor)  |                       |   (Headless & Microservice) |
          +--------------+--------------+                       +--------------+--------------+
                         |                                                     |
                         +--------------------------+--------------------------+
                                                    |
                                                    v
                                    +-------------------------------+
                                    |       LegalEase AI Core       |
                                    +---------------+---------------+
                                                    |
                         +--------------------------+--------------------------+
                         |                                                     |
                         v                                                     v
          +-----------------------------+                       +-----------------------------+
          |    Gemini Legal Engine      |                       |    Document Exporter        |
          |  (Dynamic Prompt Synthesis  |                       |  - PDF (ReportLab Canvas)   |
          |   & Offline Rule Engine)    |                       |  - DOCX (python-docx)       |
          +-----------------------------+                       |  - HTML & TXT Formatter     |
                                                                +-----------------------------+
```

---

## 3. Directory Layout & Module Responsibilities

```text
LEGALEASE/
│
├── ai_core/
│   ├── __init__.py
│   ├── gemini_generator.py      # Gemini API integration, prompt builder, and fallback rules engine
│   └── generator.py             # Multi-format export engine (.docx, .pdf, .txt) & HTML previewer
│
├── docs/
│   └── architecture.md          # Architecture and technical specification document
│
├── frontend/
│   └── app.py                   # Streamlit web UI with live preview, inline editor, and downloads
│
├── Image/
│   ├── Logo.png                 # Primary legal logo
│   └── inverseLogo.png          # Inverted/dark legal logo
│
├── legalEaseAPI/
│   ├── __init__.py
│   ├── main.py                  # FastAPI application entry point, CORS, root health check
│   └── routes.py                # Pydantic schemas and POST /generate endpoint
│
├── .env                         # Environment variables (GEMINI_API_KEY)
├── config.py                    # Global constants, paths, and configurations
├── requirements.txt             # Production dependency list
├── setup_assets.py              # Auto-bootstrap script for brand logos
├── run.bat                      # Windows launcher
└── run.sh                       # Linux/macOS launcher
```

---

## 4. API Endpoints Specification

### Base URL: `http://127.0.0.1:8000`

| Method | Path | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Root service status and documentation links |
| `GET` | `/health` | Service uptime and health verification |
| `GET` | `/api/v1/templates` | Returns supported document types, schemas, and default jurisdictions |
| `POST` | `/api/v1/generate` | Generates full-text legal document in Markdown format with metadata |
| `POST` | `/api/v1/export` | Converts Markdown legal text to `.pdf`, `.docx`, `.txt`, or `.html` binary stream |
| `POST` | `/api/v1/preview-html` | Generates rich styled HTML embed code for web renderers |

---

## 5. Security & Legal Disclaimer
- **Data Privacy**: Documents generated locally or via Gemini API adhere to zero-data-retention prompts where applicable.
- **Legal Advisory**: Generated materials represent initial drafts and must be reviewed by accredited legal counsel prior to formal execution.
