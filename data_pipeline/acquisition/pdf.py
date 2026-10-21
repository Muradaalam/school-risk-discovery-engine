"""Stream a public PDF to disk and record provenance metadata."""

import argparse
import hashlib
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen


MAX_PDF_BYTES = 150 * 1024 * 1024
CHUNK_SIZE = 64 * 1024


def download_pdf(url: str, output: str | Path, source_id: str = "GYAN_SANKALP", max_bytes: int = MAX_PDF_BYTES) -> dict:
    if urlparse(url).scheme not in ("http", "https") or not urlparse(url).netloc:
        raise ValueError("A valid HTTP or HTTPS URL is required")
    if max_bytes < 1:
        raise ValueError("max_bytes must be positive")

    output = Path(output)
    metadata_path = output.with_suffix(output.suffix + ".json")

    if output.exists() or metadata_path.exists():
        raise FileExistsError("Output or metadata already exists; use a new filename")

    output.parent.mkdir(parents=True, exist_ok=True)
    temp_path = None

    try:
        request = Request(url, headers={"User-Agent": "SchoolRiskDiscoveryEngine/0.1"})

        with urlopen(request, timeout=30) as response:
            with tempfile.NamedTemporaryFile(dir=output.parent, prefix=".pdf_", delete=False) as temp:
                temp_path = Path(temp.name)
                digest = hashlib.sha256()
                size = 0

                while chunk := response.read(CHUNK_SIZE):
                    if size == 0 and not chunk.startswith(b"%PDF-"):
                        raise ValueError("Response is not a PDF")

                    size += len(chunk)

                    if size > max_bytes:
                        raise ValueError("PDF exceeds the download size limit")

                    temp.write(chunk)
                    digest.update(chunk)

        if size == 0:
            raise ValueError("Empty PDF response")

        metadata = {
            "source_id": source_id,
            "source_url": url,
            "retrieved_at": datetime.now(timezone.utc).isoformat(),
            "file_path": str(output),
            "size_bytes": size,
            "sha256": digest.hexdigest()
        }

        os.replace(temp_path, output)
        temp_path = None

        metadata_path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
        return metadata

    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description="Download an accessible public PDF with provenance metadata")
    parser.add_argument("url")
    parser.add_argument("output")

    args = parser.parse_args()
    print(json.dumps(download_pdf(args.url, args.output), indent=2))


if __name__ == "__main__":
    main()