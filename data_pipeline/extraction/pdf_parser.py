
from pathlib import Path
import subprocess


def parse_pdf(path):
    path = Path(path)
    with path.open("rb") as f:
        signature = f.read(5)
    if signature != b"%PDF-":
        raise ValueError("Not a PDF: missing %PDF- signature")
    try:
        result = subprocess.run(
            ["pdftotext", "-layout", "-enc", "UTF-8", str(path), "-"],
            capture_output=True, timeout=240, check=False,
        )
    except FileNotFoundError:
        return _parse_with_pymupdf(path)
    except subprocess.TimeoutExpired as error:
        raise ValueError("PDF text extraction timed out") from error
    if result.returncode:
        raise ValueError(f"pdftotext failed: {result.stderr.decode('utf-8', 'replace')[:220]}")
    pages = result.stdout.decode("utf-8", "replace").split("\f")
    if pages and not pages[-1].strip():
        pages.pop()
    return [{"page_number": i, "text": content, "kind": "pdf_page"}
            for i, content in enumerate(pages, 1)]


def _parse_with_pymupdf(path):
    try:
        import fitz
    except ImportError as error:
        raise RuntimeError("Install poppler-utils (pdftotext) or pymupdf") from error
    with fitz.open(str(path)) as doc:
        return [{"page_number": i + 1, "text": page.get_text(sort=True), "kind": "pdf_page"}
                for i, page in enumerate(doc)]
