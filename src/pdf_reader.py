from pathlib import Path

from fastapi import HTTPException
ROOT = Path(__file__).resolve().parent.parent
def extract_pdf_text(raw: bytes) -> str:
    """Extract text from a text-based PDF. OCR is intentionally unsupported."""
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise HTTPException(
            status_code=500,
            detail="PDF extraction requires pypdf. Install dependencies with python3 -m pip install -r requirements.txt.",
        ) from exc

    temp_path = ROOT / "outputs" / "_uploaded_temp.pdf"
    try:
        temp_path.write_bytes(raw)
        reader = PdfReader(str(temp_path))
        text_parts = [(page.extract_text() or "") for page in reader.pages]
    finally:
        if temp_path.exists():
            temp_path.unlink()
    extracted = "\n\n".join(part.strip() for part in text_parts if part.strip()).strip()
    if not extracted:
        raise HTTPException(
            status_code=400,
            detail="No extractable text found. PDF support works for text-based PDFs only; scanned image PDFs are not supported.",
        )
    return extracted