"""
LegalEase FastAPI Endpoints & Pydantic Validation Schemas
"""
import io
import re
try:
    from pydantic import BaseModel, Field
    PYDANTIC_AVAILABLE = True
except ImportError:
    PYDANTIC_AVAILABLE = False
    # Lightweight pure-Python fallback for BaseModel & Field
    class Field:
        def __init__(self, default=None, **kwargs):
            self.default = default

    class BaseModel:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
        def dict(self):
            return self.__dict__
        def json(self):
            import json
            return json.dumps(self.__dict__)

try:
    from fastapi import APIRouter, HTTPException, Query, Response, status
    from fastapi.responses import StreamingResponse
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False
    class APIRouter:
        def __init__(self, *args, **kwargs): pass
        def get(self, *args, **kwargs): return lambda f: f
        def post(self, *args, **kwargs): return lambda f: f
    class HTTPException(Exception):
        def __init__(self, status_code, detail):
            self.status_code = status_code
            self.detail = detail
    class status:
        HTTP_200_OK = 200
        HTTP_400_BAD_REQUEST = 400
        HTTP_422_UNPROCESSABLE_ENTITY = 422
        HTTP_500_INTERNAL_SERVER_ERROR = 500
    class StreamingResponse:
        def __init__(self, *args, **kwargs): pass
    Query = lambda default=None, **kw: default
    Response = None

from ai_core.gemini_generator import GeminiLegalGenerator
from ai_core.generator import DocumentExporter
from config import DOCUMENT_TYPES, LEGAL_TONES, GEMINI_MODEL

router = APIRouter(prefix="/api/v1", tags=["Legal Generation & Exports"])

# Initialize default AI engine
ai_generator = GeminiLegalGenerator()


from typing import Dict, Any, Optional, List, Union

class DocumentGenerationRequest(BaseModel):
    document_type: str = Field(..., description="Target legal document type name")
    parties: Optional[Union[Dict[str, str], str]] = Field(default_factory=dict, description="Key-value mapping or comma-separated string of involved parties")
    terms: Optional[Union[Dict[str, Any], str]] = Field(default=None, description="Commercial parameters or terms string")
    specific_terms: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Commercial parameters dict")
    dates: Optional[str] = Field(None, description="Effective date or date range string")
    effective_date: Optional[str] = Field(None, description="Optional custom effective date (e.g. 'October 1, 2026')")
    jurisdiction: str = Field("State of Delaware, USA", description="Governing law state or nation")
    custom_clauses: List[str] = Field(default_factory=list, description="List of bespoke stipulations or clauses to inject")
    tone: str = Field(LEGAL_TONES[1], description="Drafting tone style")


class DocumentGenerationResponse(BaseModel):
    status: str
    source: str
    model: str
    document_type: str
    jurisdiction: str
    generated_at: str
    content_markdown: str
    document: Optional[str] = None
    word_count: int
    clause_count: int


class ExportRequest(BaseModel):
    markdown_content: str = Field(..., description="Markdown legal text to convert into file formats")
    document_title: str = Field("LegalEase Document", description="Document filename/title")
    export_format: str = Field("pdf", description="Format type: 'pdf', 'docx', 'txt', or 'html'")


class ClauseSuggestionRequest(BaseModel):
    clause_type: str = Field(..., description="E.g. 'Non-Compete', 'Liquidated Damages', 'Indemnification'")
    context: str = Field(..., description="Context of the contract and industry")


# --- API Routes ---

@router.get("/templates", summary="Get Available Legal Document Types & Metadata")
async def get_templates():
    """
    Returns list of all supported contract templates, field specifications, and default jurisdictions.
    """
    return {
        "count": len(DOCUMENT_TYPES),
        "document_types": DOCUMENT_TYPES,
        "tones": LEGAL_TONES
    }


@router.post(
    "/generate",
    response_model=DocumentGenerationResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate Full-Text Legal Instrument"
)
async def generate_document_endpoint(payload: DocumentGenerationRequest):
    """
    Synthesizes a legally binding, jurisdiction-compliant contract based on input parameters.
    """
    try:
        # Normalize parties
        parties_dict = {}
        if isinstance(payload.parties, dict):
            parties_dict = payload.parties
        elif isinstance(payload.parties, str) and payload.parties:
            parts = [p.strip() for p in payload.parties.split(",") if p.strip()]
            if len(parts) >= 2:
                parties_dict = {"party_a": parts[0], "party_b": parts[1]}
            elif parts:
                parties_dict = {"party_a": parts[0], "party_b": "[Second Party]"}

        # Normalize terms
        terms_dict = payload.specific_terms or {}
        if isinstance(payload.terms, dict):
            terms_dict.update(payload.terms)
        elif isinstance(payload.terms, str) and payload.terms:
            terms_dict["terms_summary"] = payload.terms

        eff_date = payload.effective_date or payload.dates

        result = ai_generator.generate_document(
            doc_type=payload.document_type,
            parties=parties_dict,
            jurisdiction=payload.jurisdiction,
            custom_clauses=payload.custom_clauses,
            tone=payload.tone,
            specific_terms=terms_dict,
            effective_date=eff_date
        )

        md = result.get("content_markdown", "")
        word_count = len(md.split())
        clause_count = len(re.findall(r'###\s+\d+\.|\bSection\s+\d+\b|\bARTICLE\s+[IVXLCDM]+\b', md, re.IGNORECASE))

        return DocumentGenerationResponse(
            status=result.get("status", "success"),
            source=result.get("source", "unknown"),
            model=result.get("model", GEMINI_MODEL),
            document_type=result.get("document_type", payload.document_type),
            jurisdiction=result.get("jurisdiction", payload.jurisdiction),
            generated_at=result.get("generated_at", ""),
            content_markdown=md,
            document=md,
            word_count=word_count,
            clause_count=max(clause_count, 4)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Legal document synthesis failed: {str(e)}"
        )


@router.post("/export", summary="Convert Markdown to DOCX / PDF / TXT / HTML")
async def export_document_endpoint(payload: ExportRequest):
    """
    Streams binary or textual file outputs ready for instant download.
    """
    fmt = payload.export_format.lower().strip()
    safe_title = re.sub(r'[^a-zA-Z0-9_\- ]', '', payload.document_title).strip().replace(' ', '_') or "LegalEase_Document"

    if fmt == "pdf":
        file_bytes = DocumentExporter.to_pdf(payload.markdown_content, title=payload.document_title)
        media_type = "application/pdf"
        filename = f"{safe_title}.pdf"
    elif fmt == "docx":
        file_bytes = DocumentExporter.to_docx(payload.markdown_content, title=payload.document_title)
        media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        filename = f"{safe_title}.docx"
    elif fmt == "txt":
        file_bytes = DocumentExporter.to_txt(payload.markdown_content)
        media_type = "text/plain"
        filename = f"{safe_title}.txt"
    elif fmt == "html":
        html_str = DocumentExporter.to_html(payload.markdown_content)
        file_bytes = html_str.encode("utf-8")
        media_type = "text/html"
        filename = f"{safe_title}.html"
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported format '{fmt}'. Choose from 'pdf', 'docx', 'txt', or 'html'."
        )

    return StreamingResponse(
        io.BytesIO(file_bytes),
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )


@router.post("/preview-html", summary="Get Rich Styled HTML Preview")
async def preview_html_endpoint(
    payload: ExportRequest,
    dark_mode: bool = Query(False, description="Render in high-contrast dark theme")
):
    """
    Renders styled HTML component with custom legal typography and tables for live frontend embeds.
    """
    html_output = DocumentExporter.to_html(payload.markdown_content, dark_mode=dark_mode)
    return {"html": html_output}
