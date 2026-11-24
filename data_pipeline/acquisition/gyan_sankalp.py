

import argparse
import hashlib
import json
import os
import sqlite3
import tempfile
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse, urlunparse

import requests
from bs4 import BeautifulSoup

HOST = "gyansankalp.rajasthan.gov.in"
PAGES = (
    f"https://{HOST}/Home/HomePage.aspx",
    f"https://{HOST}/home/ViewDocument.aspx",
)

TERMS = (
    "जर्जर", "मरम्मत", "रिपेयर", "भौतिक विकास", "भवन", "निर्माण",
    "major repair", "repairing", "raiparing", "dilapidated", "unsafe",
    "new building", "newbuidlidng", "school building", "construction",
    "infrastructure", "classroom", "structural", "renovation",
)
DOC_ROOT = Path("data_pipeline/raw/gyan_sankalp")
DB_PATH = Path("data_pipeline/state/gyan_sankalp.sqlite")


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def approved(url):
    parsed = urlparse(url)
    return parsed.scheme == "https" and (parsed.hostname or "").lower() == HOST and not parsed.username and not parsed.password and parsed.port in (None, 443)


def canonical(url):
    parsed = urlparse(url)
    return urlunparse((parsed.scheme.lower(), parsed.netloc.lower(), parsed.path, "", parsed.query, ""))


def pdf_link(page_url, raw):
    raw = (raw or "").strip()
    if not raw or raw.startswith(("#", "javascript:", "mailto:", "data:")):
        return ""
    url = canonical(urljoin(page_url, raw))
    return url if approved(url) and urlparse(url).path.casefold().endswith(".pdf") else ""


def extract_candidates(html, page_url):
   
    soup = BeautifulSoup(html, "html.parser")
    output = {}
    for a in soup.select("a[href]"):
        url = pdf_link(page_url, a.get("href"))
        if not url:
            continue
        label = a.get_text(" ", strip=True)
        parent = a.parent.get_text(" ", strip=True) if a.parent else ""
        
        context = parent if len(parent) <= 240 else label
        name = unquote(urlparse(url).path.rsplit("/", 1)[-1])
        searchable = " ".join((label, a.get("title", ""), context, name)).casefold()
        if not any(word in searchable for word in TERMS):
            continue
        title = context if len(context) > len(label) and len(context) <= 160 else label
        if len(title) < 6 or title.casefold() in ("pdf", "view", "click here", "click here to view pdf"):
            title = name
        output[url] = {"url": url, "title": title[:220], "discovered_from": page_url}
    return list(output.values())


def init_db(conn):
    conn.execute("""CREATE TABLE IF NOT EXISTS documents (
        url TEXT PRIMARY KEY, title TEXT NOT NULL, discovered_from TEXT NOT NULL,
        first_seen TEXT NOT NULL, last_seen TEXT NOT NULL, last_checked TEXT,
        etag TEXT, last_modified TEXT, sha256 TEXT, saved_path TEXT,
        size_bytes INTEGER
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS versions (
        url TEXT NOT NULL, sha256 TEXT NOT NULL, saved_path TEXT NOT NULL,
        downloaded_at TEXT NOT NULL, size_bytes INTEGER NOT NULL,
        PRIMARY KEY (url, sha256)
    )""")
    conn.commit()


def get_response(session, url, *, headers=None, stream=False, timeout=20):
    
    for _ in range(4):
        if not approved(url):
            raise ValueError(f"Off-site/non-HTTPS URL: {url}")
        response = session.get(url, headers=headers or {}, timeout=timeout,
                               allow_redirects=False, stream=stream)
        if response.status_code in (301, 302, 303, 307, 308):
            target = urljoin(url, response.headers.get("Location", ""))
            response.close()
            if not approved(target):
                raise ValueError(f"Redirect outside approved host: {target}")
            url = target
            continue
        response.raise_for_status()
        return response
    raise ValueError("More than 3 redirects")


def record_event(log_path, event):
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def download_pdf(session, entry, old, output_dir, *, max_bytes, timeout):
   
    headers = {"Accept": "application/pdf,application/octet-stream;q=0.8,*/*;q=0.1"}
    if old and old["etag"] and old["saved_path"] and Path(old["saved_path"]).exists():
        headers["If-None-Match"] = old["etag"]
    if old and old["last_modified"] and old["saved_path"] and Path(old["saved_path"]).exists():
        headers["If-Modified-Since"] = old["last_modified"]

    response = get_response(session, entry["url"], headers=headers, stream=True, timeout=timeout)
    if response.status_code == 304:
        response.close()
        return {"status": "unchanged", "etag": old["etag"],
                "last_modified": old["last_modified"]}
    temporary = None
    try:
        if response.status_code == 206:
            raise ValueError("Server returned partial PDF (HTTP 206), not a complete file")
        size_header = response.headers.get("Content-Length", "")
        if size_header.isdigit() and int(size_header) > max_bytes:
            raise ValueError(f"PDF exceeds {max_bytes} byte limit")
        # MIME is advisory; PDF magic bytes are checked below.
        if "text/html" in response.headers.get("Content-Type", "").lower():
            raise ValueError("Returned HTML (possibly error/login page), not a PDF")
        sha = hashlib.sha256()
        total, prefix = 0, b""
        with tempfile.NamedTemporaryFile(mode="wb", prefix=".gyan_", suffix=".part",
                                         dir=output_dir, delete=False) as f:
            temporary = Path(f.name)
            for chunk in response.iter_content(chunk_size=65536):
                if not chunk:
                    continue
                total += len(chunk)
                if total > max_bytes:
                    raise ValueError(f"PDF exceeds {max_bytes} byte limit")
                if len(prefix) < 5:
                    prefix += chunk[:5 - len(prefix)]
                sha.update(chunk)
                f.write(chunk)
        if prefix != b"%PDF-":
            raise ValueError("Missing %PDF- signature")
        if size_header.isdigit() and int(size_header) != total:
            raise ValueError("Incomplete PDF: Content-Length does not match bytes received")
        with temporary.open("rb") as pdf_file:
            pdf_file.seek(max(0, total - 2048))
            if b"%%EOF" not in pdf_file.read():
                raise ValueError("Incomplete PDF: missing %%EOF marker")
        digest = sha.hexdigest()
        metadata = {"etag": response.headers.get("ETag", ""),
                    "last_modified": response.headers.get("Last-Modified", "")}
        if old and digest == old["sha256"] and old["saved_path"] and Path(old["saved_path"]).exists():
            temporary.unlink()
            return {"status": "unchanged", **metadata}
        final = output_dir / f"{hashlib.sha256(entry['url'].encode()).hexdigest()[:16]}_{digest[:16]}.pdf"
        os.replace(temporary, final)
        temporary = None
        return {"status": "updated" if old and old["sha256"] else "downloaded",
                "sha256": digest, "saved_path": str(final), "size_bytes": total, **metadata}
    finally:
        response.close()
        if temporary and temporary.exists():
            temporary.unlink()


def collect(output_dir=DOC_ROOT, state_db=DB_PATH, *, limit=10, recheck_hours=24,
            max_pdf_mb=60, delay=1.0, timeout=20, pages=PAGES, session=None):
    
    if limit < 1 or recheck_hours < 0 or max_pdf_mb < 1 or delay < 0:
        raise ValueError("Invalid limit, recheck interval, size limit, or delay")
    output_dir, state_db = Path(output_dir), Path(state_db)
    output_dir.mkdir(parents=True, exist_ok=True)
    state_db.parent.mkdir(parents=True, exist_ok=True)
    own_session = session is None
    client = session or requests.Session()
    if own_session:
        client.headers.update({"User-Agent": "SRDE-AcademicResearch/0.2 (public-document-monitor)"})
    report = {"source": "GYAN_SANKALP", "pages_ok": 0, "page_errors": {},
              "discovered": 0, "new_urls": 0, "downloaded": 0, "updated": 0,
              "unchanged": 0, "deferred": 0, "download_errors": {},
              "output_dir": str(output_dir), "state_db": str(state_db)}
    conn = sqlite3.connect(state_db)
    conn.row_factory = sqlite3.Row
    init_db(conn)
    try:
        candidates = {}
        for page in pages:
            try:
                if not approved(page):
                    raise ValueError("Listing URL outside approved host")
                response = get_response(client, page, timeout=timeout)
                try:
                    if "text/html" not in response.headers.get("Content-Type", "").lower():
                        raise ValueError("Listing did not return HTML")
                    items = extract_candidates(response.content, response.url)
                    candidates.update((row["url"], row) for row in items)
                    report["pages_ok"] += 1
                finally:
                    response.close()
            except (requests.RequestException, ValueError) as ex:
                report["page_errors"][page] = str(ex)[:200]
            if own_session and delay:
                time.sleep(delay)
        report["discovered"] = len(candidates)
        stamp = now()
        pending = []
        cutoff = datetime.now(timezone.utc) - timedelta(hours=recheck_hours)
        for entry in candidates.values():
            old = conn.execute("SELECT * FROM documents WHERE url=?", (entry["url"],)).fetchone()
            if old is None:
                conn.execute("""INSERT INTO documents
                    (url,title,discovered_from,first_seen,last_seen)
                    VALUES (?,?,?,?,?)""", (entry["url"], entry["title"], entry["discovered_from"], stamp, stamp))
                report["new_urls"] += 1
                pending.append((entry, None))
            else:
                conn.execute("""UPDATE documents SET title=?,discovered_from=?,last_seen=?
                    WHERE url=?""", (entry["title"], entry["discovered_from"], stamp, entry["url"]))
                last_checked = datetime.fromisoformat(old["last_checked"]) if old["last_checked"] else None
                # Retry downloads that previously failed or files that went missing.
                if (not old["sha256"] or not old["saved_path"] or
                        not Path(old["saved_path"]).exists() or
                        not last_checked or last_checked <= cutoff):
                    pending.append((entry, old))
        conn.commit()
        report["deferred"] = max(0, len(pending) - limit)
        for entry, old in pending[:limit]:
            url = entry["url"]
            try:
                result = download_pdf(client, entry, old, output_dir,
                                      max_bytes=max_pdf_mb * 1024 * 1024, timeout=timeout)
                date = now()
                if result["status"] == "unchanged":
                    report["unchanged"] += 1
                    conn.execute("""UPDATE documents SET last_checked=?,etag=?,last_modified=?
                        WHERE url=?""", (date, result["etag"], result["last_modified"], url))
                else:
                    report[result["status"]] += 1
                    conn.execute("""UPDATE documents SET last_checked=?,etag=?,last_modified=?,
                        sha256=?,saved_path=?,size_bytes=? WHERE url=?""",
                        (date, result["etag"], result["last_modified"], result["sha256"],
                         result["saved_path"], result["size_bytes"], url))
                    conn.execute("""INSERT OR IGNORE INTO versions
                        (url,sha256,saved_path,downloaded_at,size_bytes) VALUES (?,?,?,?,?)""",
                        (url, result["sha256"], result["saved_path"], date, result["size_bytes"]))
                    record_event(output_dir / "acquired_documents.jsonl", {
                        "source": "GYAN_SANKALP", "url": url, "title": entry["title"],
                        "discovered_from": entry["discovered_from"], "sha256": result["sha256"],
                        "saved_path": result["saved_path"], "size_bytes": result["size_bytes"],
                        "retrieved_at": date, "change_type": result["status"],
                        "review_status": "UNVERIFIED_SCHOOL_AND_REPAIR_STATUS"})
                conn.commit()
            except (requests.RequestException, ValueError, OSError) as ex:
                report["download_errors"][url] = str(ex)[:200]
            if own_session and delay:
                time.sleep(delay)
    finally:
        conn.close()
        if own_session:
            client.close()
    report["status"] = ("FAILED" if report["pages_ok"] == 0 else
                        "PARTIAL" if report["page_errors"] or report["download_errors"] else "OK")
    return report


def main():
    parser = argparse.ArgumentParser(description="Incrementally collect Gyan Sankalp public school-infrastructure PDFs")
    parser.add_argument("--output-dir", type=Path, default=DOC_ROOT)
    parser.add_argument("--state-db", type=Path, default=DB_PATH)
    parser.add_argument("--limit", type=int, default=10, help="Max PDF requests per run")
    parser.add_argument("--recheck-hours", type=float, default=24,
                        help="Check previously collected PDFs again after this many hours; 0 = every run")
    parser.add_argument("--max-pdf-mb", type=int, default=60)
    parser.add_argument("--delay", type=float, default=1.0)
    args = parser.parse_args()
    print(json.dumps(collect(args.output_dir, args.state_db, limit=args.limit,
                             recheck_hours=args.recheck_hours, max_pdf_mb=args.max_pdf_mb,
                             delay=args.delay), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
