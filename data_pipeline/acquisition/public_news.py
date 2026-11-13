 # note:  this code is written using AI

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

FEEDS = {
    "AKASHVANI": "https://newsonair.gov.in/hi/rss-feeds/",
    "PIB": "https://pib.gov.in/RssMain.aspx?ModId=6&Lang=1&Regid=1",
}

SEED_URLS = {
    "AKASHVANI": "https://newsonair.gov.in/school-tragedy-in-rajasthan-building-collapse-in-jhalawar-leaves-5-dead-20-injured/",
    "PIB": "https://www.pib.gov.in/PressReleaseIframePage.aspx?PRID=2148897&lang=2&reg=48"
}

HOSTS = {
    "AKASHVANI": "newsonair.gov.in",
    "PIB": "pib.gov.in",
}

SCHOOL_TERMS = ("school", "विद्यालय", "स्कूल", "विद्यालयों", "शाळा")

ISSUE_TERMS = (
    "collapse", "collapsed", "roof", "ceiling", "dilapidated",
    "unsafe", "repair", "crack", "damaged", "building", "wall",
    "injur", "construction", "demolish", "जर्जर", "छत",
    "गिर", "मरम्मत", "भवन", "दीवार", "घायल", "ढह"
)


def allowed_url(url: str, source: str) -> bool:
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    domain = HOSTS[source]
    return parsed.scheme == "https" and host in (domain, f"www.{domain}")


def relevant(text: str) -> bool:
    text = text.casefold()
    return (any(word in text for word in SCHOOL_TERMS)
            and any(word in text for word in ISSUE_TERMS))


def iso_date(value: str) -> str:
    if not value:
        return ""

    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).date().isoformat()
    except ValueError:
        try:
            return parsedate_to_datetime(value).date().isoformat()
        except (ValueError, TypeError, IndexError):
            return ""


def feed_entries(xml: str, source: str) -> list[dict]:
    soup = BeautifulSoup(xml, "xml")
    output = []

    for item in soup.select("item"):
        link = item.find("link")
        title = item.find("title")
        description = item.find("description")
        date = item.find("pubDate")
        url = link.get_text(strip=True) if link else ""

        if not allowed_url(url, source):
            continue

        summary = ""
        if description:
            summary = BeautifulSoup(
                description.get_text(" ", strip=True), "html.parser"
            ).get_text(" ", strip=True)

        output.append({
            "url": url,
            "title": title.get_text(" ", strip=True) if title else "",
            "summary": summary,
            "published_date": iso_date(date.get_text(strip=True)) if date else ""
        })

    return output


def article_details(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    title_tag = soup.find("h1")
    meta_title = soup.find("meta", property="og:title")

    title = title_tag.get_text(" ", strip=True) if title_tag else (
        meta_title.get("content", "") if meta_title else ""
    )

    published = ""
    for attrs in (
        {"property": "article:published_time"},
        {"itemprop": "datePublished"},
        {"name": "date"}
    ):
        tag = soup.find("meta", attrs=attrs)
        if tag:
            published = iso_date(tag.get("content", ""))
            if published:
                break

    if not published:
        tag = soup.find("time", datetime=True)
        published = iso_date(tag.get("datetime", "")) if tag else ""

    body = None
    for selector in (
        "article", "[itemprop='articleBody']", ".entry-content",
        ".article-body", ".td-post-content", "main"
    ):
        body = soup.select_one(selector)
        if body:
            break

    paragraphs = body.find_all("p") if body else soup.find_all("p")
    content = " ".join(p.get_text(" ", strip=True) for p in paragraphs)
    content = re.sub(r"\s+", " ", content).strip()

    return {
        "title": title,
        "published_date": published,
        "excerpt": content[:320]
    }


def collect(output_path: str | Path, max_items: int = 40,
            include_seed: bool = False, session=None) -> dict:
    if max_items < 1:
        raise ValueError("max_items must be positive")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    seen = set()
    if output_path.exists():
        with output_path.open(encoding="utf-8") as file:
            for line in file:
                if line.strip():
                    seen.add(json.loads(line)["url"])

    client = session if session is not None else requests.Session()
    if session is None:
        client.headers.update({
            "User-Agent": "SRDE-AcademicResearch/0.1 (public-report-review)"
        })

    sources = ["AKASHVANI", "PIB"]

    result = {
        "discovered": 0,
        "new_reports": 0,
        "already_seen": 0,
        "feed_errors": {},
        "article_errors": 0,
        "output": str(output_path)
    }

    with output_path.open("a", encoding="utf-8") as file:
        for source in sources:
            candidates = []

            try:
                response = client.get(FEEDS[source], timeout=20)
                response.raise_for_status()

                if not allowed_url(response.url, source):
                    raise ValueError("Feed redirected outside the approved host")

                candidates = feed_entries(response.text, source)[:max_items]

            except (requests.RequestException, ValueError) as error:
                result["feed_errors"][source] = str(error)[:180]

            if include_seed and source in SEED_URLS:
                candidates.insert(0, {
                    "url": SEED_URLS[source],
                    "title": "",
                    "summary": "",
                    "published_date": ""
                })

            for entry in candidates:
                url = entry["url"]

                if not allowed_url(url, source):
                    continue

                is_seed = include_seed and url == SEED_URLS.get(source)

                if not is_seed and not relevant(entry["title"] + " " + entry["summary"]):
                    continue

                result["discovered"] += 1

                if url in seen:
                    result["already_seen"] += 1
                    continue

                try:
                    response = client.get(url, timeout=20)
                    response.raise_for_status()

                    if not allowed_url(response.url, source):
                        raise ValueError("Article redirected outside the approved host")

                    details = article_details(response.text)

                except (requests.RequestException, ValueError):
                    result["article_errors"] += 1
                    continue

                title = details["title"] or entry["title"]

                if not relevant(title + " " + details["excerpt"] + " " + entry["summary"]):
                    continue

                record = {
                    "report_id": "WEB:" + hashlib.sha256(url.encode()).hexdigest()[:16],
                    "source": source,
                    "url": url,
                    "title": title,
                    "published_date": details["published_date"] or entry["published_date"],
                    "excerpt": details["excerpt"],
                    "retrieved_at": datetime.now(timezone.utc).isoformat(),
                    "review_status": "NEEDS_SCHOOL_IDENTITY_AND_CLAIM_REVIEW"
                }

                file.write(json.dumps(record, ensure_ascii=False) + "\n")
                file.flush()
                seen.add(url)
                result["new_reports"] += 1

                if session is None:
                    time.sleep(1)

    return result


def main():
    parser = argparse.ArgumentParser(description="Collect public school-infrastructure news")
    parser.add_argument("output")
    parser.add_argument("--max-items", type=int, default=40)
    parser.add_argument("--seed", action="store_true")
    args = parser.parse_args()

    print(json.dumps(
        collect(args.output, args.max_items, args.seed),
        indent=2
    ))


if __name__ == "__main__":
    main()
