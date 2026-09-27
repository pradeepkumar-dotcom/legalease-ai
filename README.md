<div align="center">

# ⚖️ LegalEase: AI-Powered Legal Document Generator

**Enterprise-Grade Legal Synthesis • Statutory Compliance • Multi-Format Courtroom Exports**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.33+-FF4B4B.svg?style=flat&logo=Streamlit&logoColor=white)](https://streamlit.io)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-1.5%20Pro-4285F4.svg?style=flat&logo=google&logoColor=white)](https://ai.google.dev)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

</div>

---

## 📖 1. Project Overview & Problem Statement

Drafting legally enforceable commercial agreements traditionally demands substantial time, specialist attorney fees, and extensive compliance verifications across changing jurisdictions.

**LegalEase** is an end-to-end AI software suite engineered to automate the creation of jurisdiction-aware, binding legal contracts in seconds. By synthesizing large language model intelligence (**Google Gemini 1.5 Pro**) with rigorous legal prompt hierarchies and multi-format document formatting engines, LegalEase generates structured agreements ready for execution.

---

## 🏛️ 2. Architectural Flow Diagram

```
+-----------------------------------------------------------------------------------+
|                                  USER / CLIENT                                    |
+-----------------------------------------+-----------------------------------------+
                                          |
                   +----------------------+----------------------+
                   |                                             |
                   v                                             v
     +---------------------------+                 +---------------------------+
     |     Streamlit Web UI      |                 |    FastAPI REST Backend   |
     |        (Port 8501)        |                 |        (Port 8000)        |
     | - Document Builder Tab    |                 | - POST /api/v1/generate   |
     | - Live HTML Preview Tab   |                 | - POST /api/v1/export     |
     | - Inline Editor Tab       |                 | - GET  /api/v1/templates  |
     | - Clause Library Booster  |                 | - GET  /health            |
     +-------------+-------------+                 +-------------+-------------+
                   |                                             |
                   +----------------------+----------------------+
                                          |
                                          v
                   +---------------------------------------------+
                   |              LegalEase AI Core              |
                   +----------------------+----------------------+
                                          |
                   +----------------------+----------------------+
                   |                                             |
                   v                                             v
     +---------------------------+                 +---------------------------+
     |    Gemini Legal Engine    |                 |   Document Export Suite   |
     |  (System Rules + Gemini   |                 |  - PDF (ReportLab Canvas) |
     |   API & Fallback Engine)  |                 |  - DOCX (python-docx)     |
     |  - Jurisdiction Reasoning |                 |  - Plain Text (.txt)      |
     |  - Custom Stipulations    |                 |  - Styled HTML Preview    |
     +---------------------------+                 +---------------------------+
```

---

## ✨ 3. Key Capabilities & Features

- **10+ Pre-Configured Commercial Templates**:
  - Non-Disclosure Agreements (NDAs), Executive Employment Contracts, Residential/Commercial Leases, SaaS Terms of Service, GDPR/CCPA Privacy Policies, Independent Contractor Agreements, Partnership Agreements, Cease & Desist Notices, Promissory Notes, and Power of Attorney.
- **Jurisdiction-Aware Drafting**:
  - Automatically incorporates governing law provisions, severability rules, dispute resolution forums, and local statutory standards.
- **Live Markdown & Inline Legal Editor**:
  - Modify clauses, adjust indemnities, or add bespoke terms with live re-rendering and dynamic word count metrics.
- **Multi-Format Courtroom-Grade Exports**:
  - **PDF (.pdf)**: Built with ReportLab using two-pass `Page X of Y` footers, formal running headers, and legal table grids.
  - **Word (.docx)**: Built with `python-docx` using standardized 1-inch margins, typography styles, and signature blocks.
  - **Plaintext (.txt) & HTML (.html)**: Clean, sanitized text exports for corporate archiving and web embeds.
- **Institutional Clause Repository & Booster**:
  - Instant one-click injection of institutional clauses: AAA Binding Arbitration, Blue-Pencil Severability, Mutual Indemnification, Force Majeure, and 12-Month Non-Solicitation.
- **Offline Fallback Guarantee**:
  - Built-in deterministic legal rule engine generates comprehensive, fully formatted fallback agreements when working offline or without an active Gemini API key.

---

## 🛠️ 4. Technology Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend UI** | Streamlit 1.33+ | Responsive interactive web application with dark/light theme support |
| **API Framework** | FastAPI 0.110+ / Uvicorn | High-performance async REST API microservice |
| **AI LLM Engine** | Google Gemini 1.5 Pro | Deep legal reasoning, clause formulation, and tone modulation |
| **PDF Generation** | ReportLab 4.1+ | Flowables, numbered canvas, and exact typography |
| **Word Processing** | python-docx 1.1+ | Standardized OpenXML Word Document styling |
| **Containerization**| Docker & Docker Compose | Containerized multi-service deployment |

---

## 🚀 5. Step-by-Step Local Setup & Run

### Prerequisites
- Python 3.10, 3.11, or 3.12 installed.
- (Optional) Google Gemini API Key from [Google AI Studio](https://aistudio.google.com/).

### 1. Clone & Setup Environment
```bash
git clone https://github.com/yourusername/legalease.git
cd legalease

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Edit `.env` or set your API key:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-pro-latest
API_HOST=127.0.0.1
API_PORT=8000
```

### 3. Launch the Application
- **Windows**:
  ```cmd
  run.bat
  ```
- **Linux / macOS**:
  ```bash
  chmod +x run.sh
  ./run.sh
  ```
- **Manual Launch**:
  ```bash
  # Terminal 1: Start FastAPI Backend
  python -m uvicorn legalEaseAPI.main:app --host 127.0.0.1 --port 8000 --reload

  # Terminal 2: Start Streamlit Frontend
  python -m streamlit run frontend/app.py --server.port 8501
  ```

Access the Web UI at **`http://localhost:8501`** and the API documentation at **`http://localhost:8000/docs`**.

---

## 🐳 6. Docker Deployment (`docker-compose`)

Build and deploy both frontend and backend microservices with a single command:

```bash
docker-compose up --build -d
```

Check running services:
```bash
docker-compose ps
```

- **Streamlit Web Application**: `http://localhost:8501`
- **FastAPI REST API**: `http://localhost:8000`
- **Interactive Swagger Docs**: `http://localhost:8000/docs`

To stop services:
```bash
docker-compose down
```

---

## 📡 7. API Reference

### `POST /api/v1/generate`
Synthesizes a full-text legal instrument in Markdown with metadata.

**Request Body:**
```json
{
  "document_type": "Employment Agreement",
  "parties": {
    "employer_name": "Apex Software Solutions Pvt Ltd",
    "employee_name": "Alex Morgan"
  },
  "jurisdiction": "State of California, USA",
  "tone": "Strict & Comprehensive (Maximum Protection)",
  "specific_terms": {
    "job_title": "Lead AI Engineer",
    "salary_details": "$140,000 USD per annum"
  },
  "custom_clauses": [
    "Strict IP assignment to employer.",
    "1-year post-termination non-compete."
  ],
  "effective_date": "November 1, 2026"
}
```

**Response Body:**
```json
{
  "status": "success",
  "source": "gemini_api",
  "model": "gemini-1.5-pro-latest",
  "document_type": "Employment Agreement",
  "jurisdiction": "State of California, USA",
  "generated_at": "2026-11-01T10:00:00.000000",
  "content_markdown": "# EXECUTIVE EMPLOYMENT AGREEMENT\n\n...",
  "word_count": 842,
  "clause_count": 9
}
```

### `POST /api/v1/export`
Streams file binary for `.pdf`, `.docx`, `.txt`, or `.html`.

**Request Body:**
```json
{
  "markdown_content": "# NON-DISCLOSURE AGREEMENT\n\n...",
  "document_title": "NDA_NovaTech_JohnDoe",
  "export_format": "pdf"
}
```

---

## 🧪 8. Test Execution Guide

Run the end-to-end automated scenario suite that generates real sample files into `output_samples/`:

```bash
python test_scenarios.py
```

This verifies:
1. **Scenario 1**: Apex Software Solutions & Alex Morgan (Employment Contract)
2. **Scenario 2**: NovaTech Labs & John Doe (Non-Disclosure Agreement)
3. **Scenario 3**: Greenstone Properties & Jane Smith (Residential Lease)

Run internal component tests:
```bash
python test_suite.py
```

---

## ⚖️ 9. Legal Disclaimer
*LegalEase is an AI-powered legal document generation and assistance system. Generated documents do not constitute formal legal counsel. Users should have all drafted agreements reviewed by a qualified attorney licensed in the relevant jurisdiction prior to execution.*

---
<div align="center">
  <b>LegalEase AI • Empowering Modern Commercial Contracting</b>
</div>
