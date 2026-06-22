"""Document loading utilities for Strategic Intelligence Agent."""

from pathlib import Path


def load_document(path: str | Path) -> str:
    """Load a plain-text or Markdown document from disk."""
    document_path = Path(path)
    if not document_path.exists():
        raise FileNotFoundError(f"Document not found: {document_path}")
    if document_path.suffix.lower() not in {".txt", ".md", ".markdown"}:
        raise ValueError(f"Unsupported document type: {document_path.suffix}")
    return document_path.read_text(encoding="utf-8").strip()

