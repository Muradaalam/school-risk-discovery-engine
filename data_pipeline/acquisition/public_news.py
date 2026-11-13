# This code is AI generated

import argparse
import hashlib
import json
import re
import time
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

HOSTS = {"AKASHVANI": "newsonair.gov.in", "PIB": "pib.gov.in"}
FEEDS = {
    "AKASHVANI": "https://newsonair.gov.in/hi/rss-feeds/",
    "PIB": "https://pib.gov.in/RssMain.aspx?ModId=6&Lang=1&Regid=1"
}
SEED_URLS = {
    "AKASHVANI": "https://newsonair.gov.in/school-tragedy-in-rajasthan-building-collapse-in-jhalawar-leaves-5-dead-20-injured/",
    "PIB": "https://www.pib.gov.in/PressReleaseIframePage.aspx?PRID=2148897&lang=2&reg=48"
}
SCHOOL_TERMS = ("school", "विद्यालय", "स्कूल")
ISSUE_TERMS = (
    "collapse", "roof", "ceiling", "dilapidated", "unsafe", "repair",
    "crack", "damaged", "building", "wall", "injur", "construction",
    "जर्जर", "छत", "गिर", "मरम्मत", "भवन", "दीवार", "घायल", "ढह"
)


def source_for_url(url):
    parsed = urlparse(url)
    host = (parsed.hostname or "").casefold()
    if parsed.scheme != "https":
        return ""
    for source, domain in HOSTS.items():
        if host == domain or host == f"www.{domain}":
            return source
    return ""


def allowed_url(url, source):
    return source_for_url(url) == source


def relevant(text):
    text = (text or "").casefold()
    return any(t in text for t in SCHOOL_TERMS) and any(t in text for t in ISSUE_TERMS)


def iso_date(text):
    if not text:
        return ""
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00")).date().isoformat()
    except ValueError:
        try:
            return parsedate_to_datetime(text).date().isoformat()
        except (ValueError, TypeError, IndexError):
            pass
    for fmt in ("%B %d, %Y", "%b %d, %Y", "%d %B %Y", "%d %b %Y"):
        match = re.search(
            r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December|"
            r"Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4}\b|"
            r"\b\d{1,2}\s+[A-Za-z]+\s+\d{4}\b", text, flags=re.I
        )
        if match:
            try:
                return datetime.strptime(match.group(0), fmt).date().isoformat()
            except ValueError:
                continue
    return ""


def feed_entries(xml, source):
    soup = BeautifulSoup(xml, "xml")
    if not soup.find("rss") and not soup.find("feed"):
        raise ValueError("Endpoint returned a page, not RSS/Atom XML")
    entries = []
    for item in soup.find_all(["item", "entry"]):
        link = item.find("link")
        url = link.get("href", "") if link and link.get("href") else (
            link.get_text(strip=True) if link else ""
        )
        if not allowed_url(url, source):
            continue
        title = item.find("title")
        summary = item.find("description") or item.find("summary")
        date = item.find("pubDate") or item.find("published") or item.find("updated")
        summary_text = BeautifulSoup(summary.get_text(" ", strip=True), "html.parser").get_text(" ", strip=True) if summary else ""
        entries.append({
            "url": url,
            "title": title.get_text(" ", strip=True) if title else "",
            "summary": summary_text,
            "published_date": iso_date(date.get_text(strip=True)) if date else ""
        })
    return entries


def article_details(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    title = ""
    for attrs in ({"property": "og:title"}, {"name": "twitter:title"}):
        tag = soup.find("meta", attrs=attrs)
        if tag and tag.get("content", "").strip():
            title = tag["content"].strip()
            break
    if not title:
        heading = soup.find("h1") or soup.find("title")
        title = heading.get_text(" ", strip=True) if heading else ""

    published = ""
    for attrs in (
        {"property": "article:published_time"}, {"itemprop": "datePublished"},
        {"name": "date"}, {"name": "pubdate"}, {"name": "publish-date"}
    ):
        tag = soup.find("meta", attrs=attrs)
        if tag:
            published = iso_date(tag.get("content", ""))
            if published:
                break
    if not published:
        tag = soup.find("time", datetime=True)
        if tag:
            published = iso_date(tag.get("datetime", ""))
    if not published:
        published = iso_date(soup.get_text(" ", strip=True)[:800])

    body = next((soup.select_one(selector) for selector in (
        "article", "[itemprop='articleBody']", ".entry-content", ".article-body",
        ".td-post-content", "main"
    ) if soup.select_one(selector)), None)
    paragraphs = body.find_all("p") if body else soup.find_all("p")
    content = re.sub(r"\s+", " ", " ".join(p.get_text(" ", strip=True) for p in paragraphs)).strip()
    if not content and body:
        content = body.get_text(" ", strip=True)
    if not title and content:
        title = content[:110]
    return {"title": title, "published_date": published, "excerpt": content[:500]}


def collect(output_path, max_items=40, include_seed=False, session=None,
            skip_feeds=False, urls_file=None):
    if max_items < 1:
        raise ValueError("max_items must be positive")
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    seen = set()
    if path.exists():
        with path.open(encoding="utf-8") as file:
            for line in file:
                if line.strip():
                    seen.add(json.loads(line)["url"])

    client = session if session is not None else requests.Session()
    if session is None:
        client.headers.update({"User-Agent": "SRDE-AcademicPrototype/0.1 (public-source article review)"})

    result = {"new_reports": 0, "already_seen": 0, "skipped_irrelevant": 0,
              "article_errors": 0, "feed_errors": {}, "unsupported_urls": 0,
              "output": str(path)}
    candidates = []

    if urls_file:
        for line in Path(urls_file).read_text(encoding="utf-8").splitlines():
            url = line.strip()
            if url and not url.startswith("#"):
                if source_for_url(url):
                    candidates.append({"url": url, "title": "", "summary": "", "published_date": ""})
                else:
                    result["unsupported_urls"] += 1

    if include_seed:
        candidates.extend({"url": url, "title": "", "summary": "", "published_date": ""}
                          for url in SEED_URLS.values())

    if not skip_feeds:
        for source, feed in FEEDS.items():
            try:
                response = client.get(feed, timeout=12)
                response.raise_for_status()
                if not allowed_url(response.url, source):
                    raise ValueError("Feed redirected off-site")
                entries = feed_entries(response.text, source)
                candidates.extend(e for e in entries[:max_items]
                                  if relevant(e["title"] + " " + e["summary"]))
            except (requests.RequestException, ValueError) as error:
                result["feed_errors"][source] = str(error)[:180]

    attempted = set()
    with path.open("a", encoding="utf-8") as file:
        for entry in candidates:
            url = entry["url"]
            source = source_for_url(url)
            if not source or url in attempted:
                continue
            attempted.add(url)
            if url in seen:
                result["already_seen"] += 1
                continue
            try:
                response = client.get(url, timeout=20)
                response.raise_for_status()
                if not allowed_url(response.url, source):
                    raise ValueError("Article redirected off-site")
                details = article_details(response.text)
            except (requests.RequestException, ValueError):
                result["article_errors"] += 1
                continue
            title = details["title"] or entry["title"]
            if not relevant(" ".join((title, details["excerpt"], entry["summary"]))):
                result["skipped_irrelevant"] += 1
                continue
            record = {
                "report_id": "WEB:" + hashlib.sha256(url.encode()).hexdigest()[:16],
                "source": source, "url": url, "title": title,
                "published_date": details["published_date"] or entry["published_date"],
                "excerpt": details["excerpt"],
                "retrieved_at": datetime.now(timezone.utc).isoformat(),
                "identity_status": "UNVERIFIED"
            }
            file.write(json.dumps(record, ensure_ascii=False) + "\n")
            file.flush()
            seen.add(url)
            result["new_reports"] += 1
            if session is None:
                time.sleep(1)
    return result


def main():
    parser = argparse.ArgumentParser(description="Extract public school-infrastructure articles")
    parser.add_argument("output")
    parser.add_argument("--max-items", type=int, default=40)
    parser.add_argument("--seed", action="store_true")
    parser.add_argument("--urls-file", help="Text file with one Akashvani/PIB HTTPS URL per line")
    parser.add_argument("--skip-feeds", action="store_true", help="Use seeds / URL file only; don't wait for RSS")
    args = parser.parse_args()
    print(json.dumps(collect(args.output, args.max_items, args.seed,
                             skip_feeds=args.skip_feeds, urls_file=args.urls_file), indent=2))


if __name__ == "__main__":
    main()
