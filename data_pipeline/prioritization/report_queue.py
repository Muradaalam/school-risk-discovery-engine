#this code is AI generated

import argparse
import csv
import hashlib
import json
import re
import unicodedata
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from data_pipeline.prioritization.ranking import FIELDS

REVIEW_FIELDS = ["url", "source", "title", "reason", "school_name", "district", "incident_group", "approved"]
SEVERE_TERMS = ("collapse", "collapsed", "death", "died", "killed", "injur", "ढह", "गिर", "मृत्यु", "घायल")
ISSUE_TERMS = SEVERE_TERMS + ("roof", "wall", "crack", "unsafe", "damaged", "dilapidated", "repair", "building", "छत", "दीवार", "जर्जर", "मरम्मत", "भवन")
DISTRICTS = (
    "Ajmer", "Alwar", "Anupgarh", "Balotra", "Banswara", "Baran", "Barmer",
    "Beawar", "Bharatpur", "Bhilwara", "Bikaner", "Bundi", "Chittorgarh",
    "Churu", "Dausa", "Deeg", "Dholpur", "Didwana Kuchaman", "Dudu",
    "Dungarpur", "Gangapur City", "Hanumangarh", "Jaipur", "Jaisalmer",
    "Jalore", "Jhalawar", "Jhunjhunu", "Jodhpur", "Karauli", "Kekri",
    "Khairthal Tijara", "Kota", "Kotputli Behror", "Nagaur", "Neem Ka Thana",
    "Pali", "Phalodi", "Pratapgarh", "Rajsamand", "Salumbar", "Sanchore",
    "Sawai Madhopur", "Shahpura", "Sikar", "Sirohi", "Sri Ganganagar",
    "Tonk", "Udaipur"
)
SCHOOL_PATTERN = re.compile(
    r"\b((?i:Government|Govt\.?)\s+"
    r"(?:(?i:Girls?|Upper|Senior|Secondary|Primary|Higher|Middle|High|Model|Composite)\s+){1,5}"
    r"(?i:School))\s+(?:(?i:at|in|of)\s+)?"
    r"([A-Z][A-Za-z'-]+(?:\s+[A-Z][A-Za-z'-]+){0,3})\b"
)
SHORT_PATTERN = re.compile(r"\b(GPS|GUPS|GSSS|GGSSS)\s+([A-Z][A-Za-z'-]+(?:\s+[A-Z][A-Za-z'-]+){0,2})\b")
SHORT_TYPES = {"GPS": "Government Primary School", "GUPS": "Government Upper Primary School", "GSSS": "Government Senior Secondary School", "GGSSS": "Government Girls Senior Secondary School"}


def norm(value):
    value = unicodedata.normalize("NFKC", str(value or "")).casefold()
    return re.sub(r"[^\w]+", " ", value, flags=re.UNICODE).strip()


def canonical_url(url):
    try:
        p = urlsplit((url or "").strip())
        if p.scheme.lower() != "https" or not p.hostname:
            return ""
        params = sorted((k, v) for k, v in parse_qsl(p.query, keep_blank_values=True)
                        if not k.lower().startswith("utm_"))
        host = p.hostname.casefold().removeprefix("www.")
        return urlunsplit(("https", host, p.path.rstrip("/") or "/", urlencode(params), ""))
    except ValueError:
        return ""


def read_csv(path):
    path = Path(path)
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8-sig") as file:
        return list(csv.DictReader(file))


def read_jsonl(path):
    path = Path(path)
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as file:
        return [json.loads(line) for line in file if line.strip()]


def write_csv(path, rows, fields):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def identity_key(name, district, block=""):
    return (norm(district), norm(name), norm(block))


def article_school(text, known_schools):
    """Find one explicit school and district; return (key, reason, display).

    A successfully extracted name is still provisional, not verified.
    """
    text_norm = " " + norm(text) + " "
    known = set()
    for key, record in known_schools.items():
        name = " " + norm(record["school_name"]) + " "
        district = " " + norm(record["district"]) + " "
        if name in text_norm and district in text_norm:
            known.add(key)
    if len(known) == 1:
        return next(iter(known)), "KNOWN_NAME_IN_ARTICLE", None
    if len(known) > 1:
        return None, "AMBIGUOUS_KNOWN_SCHOOLS", None

    districts = sorted(set(DISTRICTS) | {r["district"] for r in known_schools.values()},
                       key=len, reverse=True)
    matches = [d for d in districts if re.search(r"(?<!\w)" + re.escape(d) + r"(?!\w)", text, re.I)]
    matches = list({norm(d): d for d in matches}.values())
    if len(matches) != 1:
        return None, "DISTRICT_MISSING_OR_AMBIGUOUS", None
    district = matches[0]

    if not any(term in text_norm for term in ISSUE_TERMS):
        return None, "NO_INFRASTRUCTURE_INCIDENT_TERMS", None

    names = set()
    for match in SCHOOL_PATTERN.finditer(text):
        prefix, place = match.groups()
        if norm(place).endswith(norm(district)):
            place = place[:-len(district)].strip()
        if place:
            names.add(f"{prefix} {place}")
    for match in SHORT_PATTERN.finditer(text):
        prefix, place = match.groups()
        if norm(place).endswith(norm(district)):
            place = place[:-len(district)].strip()
        if place:
            names.add(f"{SHORT_TYPES[prefix]} {place}")

    if len(names) != 1:
        return None, "SCHOOL_NAME_MISSING_OR_AMBIGUOUS", None
    name = next(iter(names))
    return identity_key(name, district), "AUTO_EXTRACTED_NAME_UNVERIFIED", (name, district)


def build_report_queue(curated_csv, scraped_jsonl, review_csv, all_csv, top_csv, limit=50):
    if limit < 1:
        raise ValueError("limit must be positive")
    outputs = [Path(p).resolve() for p in (review_csv, all_csv, top_csv)]
    if len(set(outputs)) != 3:
        raise ValueError("Output paths must be different")

    curated = read_csv(curated_csv)
    if not Path(curated_csv).exists():
        raise FileNotFoundError(curated_csv)
    scraped = read_jsonl(scraped_jsonl)

    # Optional previously approved overrides stay usable, but are not required.
    approvals = {}
    for row in read_csv(review_csv):
        if row.get("approved", "").strip().casefold() in ("yes", "true", "1"):
            url = canonical_url(row.get("url"))
            if url and row.get("school_name", "").strip() and row.get("district", "").strip():
                approvals[url] = row

    schools = {}
    group_to_schools = defaultdict(set)
    curated_by_url = defaultdict(list)
    evidence = defaultdict(dict)
    unresolved = []
    scraped_links = {"by_url_or_group": 0, "by_name": 0, "unresolved": 0, "already_in_curated": 0}

    def ensure_school(key, name, district, block, status):
        if key not in schools:
            schools[key] = {
                "school_name": name.strip(), "district": district.strip(),
                "block": block.strip(), "identity_status": status
            }
        elif status == "CURATED_NAME_UNVERIFIED":
            schools[key]["identity_status"] = status

    def add_evidence(key, report, match_method):
        url = canonical_url(report.get("url"))
        if not url:
            return False
        record = dict(report)
        record["match_method"] = match_method
        old = evidence[key].get(url)
        if old:
            # A scraped article supplements curated data but isn't a second report.
            if not old.get("claim") and record.get("claim"):
                old["claim"] = record["claim"]
            if not old.get("date") and record.get("date"):
                old["date"] = record["date"]
            return False
        evidence[key][url] = record
        return True

    # First pass: create the named school registry, including more than six rows.
    for row in curated:
        name, district = row.get("school_name", "").strip(), row.get("district", "").strip()
        if not name or not district:
            continue
        key = identity_key(name, district, row.get("block", ""))
        ensure_school(key, name, district, row.get("block", ""), "CURATED_NAME_UNVERIFIED")
        group = norm(row.get("incident_group", ""))
        if group:
            group_to_schools[group].add(key)

    # Second pass: attach curated rows by explicit school name, or by a unique
    # incident-group link to a named school. This includes unnamed PIB notices.
    for row in curated:
        url = canonical_url(row.get("source_url"))
        if not url:
            continue
        group = norm(row.get("incident_group", ""))
        name, district = row.get("school_name", "").strip(), row.get("district", "").strip()
        curated_by_url[url].append(row)
        key = identity_key(name, district, row.get("block", "")) if name and district else None
        method = "CURATED_NAMED_SCHOOL"
        if key is None and group and len(group_to_schools[group]) == 1:
            key = next(iter(group_to_schools[group]))
            method = "CURATED_INCIDENT_GROUP_LINK"
        if key is None:
            unresolved.append({
                "url": row.get("source_url", ""), "source": row.get("publisher", "CURATED"),
                "title": row.get("claim_summary", ""), "reason": "UNNAMED_OR_AMBIGUOUS_CURATED_SCHOOL",
                "school_name": "", "district": district, "incident_group": row.get("incident_group", ""), "approved": ""
            })
            continue
        add_evidence(key, {
            "url": row["source_url"],
            "group": group or url,
            "date": row.get("event_date") or row.get("published_date") or "",
            "claim": " ".join((row.get("event_type", ""), row.get("claim_summary", ""))),
            "source": row.get("publisher", "CURATED")
        }, method)

    # Third pass: import scraped pages automatically when their identity can be
    # linked to curated evidence, or when the article explicitly names one school.
    scraped_seen = set()
    for article in scraped:
        url = canonical_url(article.get("url"))
        if not url or url in scraped_seen:
            continue
        scraped_seen.add(url)
        text = " ".join((article.get("title", ""), article.get("excerpt", "")))
        matched_key, method, group = None, "", url

        if url in curated_by_url:
            scraped_links["already_in_curated"] += 1
            matching = curated_by_url[url]
            possible = set()
            for row in matching:
                name, district = row.get("school_name", "").strip(), row.get("district", "").strip()
                incident_group = norm(row.get("incident_group", ""))
                if name and district:
                    possible.add(identity_key(name, district, row.get("block", "")))
                elif incident_group and len(group_to_schools[incident_group]) == 1:
                    possible |= group_to_schools[incident_group]
            if len(possible) == 1:
                matched_key = next(iter(possible))
                group = norm(matching[0].get("incident_group", "")) or url
                method = "CURATED_URL_OR_GROUP"
        else:
            override = approvals.get(url)
            if override:
                name, district = override["school_name"].strip(), override["district"].strip()
                matched_key = identity_key(name, district)
                ensure_school(matched_key, name, district, "", "MANUALLY_REVIEWED_NAME")
                group = norm(override.get("incident_group", "")) or url
                method = "PREVIOUSLY_APPROVED"
            else:
                matched_key, method, extracted = article_school(text, schools)
                if matched_key and matched_key not in schools and extracted:
                    name, district = extracted
                    ensure_school(matched_key, name, district, "", "AUTO_EXTRACTED_NAME_UNVERIFIED")

        if matched_key is None:
            scraped_links["unresolved"] += 1
            unresolved.append({
                "url": article.get("url", ""), "source": article.get("source", ""),
                "title": article.get("title", ""), "reason": method or "NO_UNAMBIGUOUS_SCHOOL_LINK",
                "school_name": "", "district": "", "incident_group": "", "approved": ""
            })
            continue

        added = add_evidence(matched_key, {
            "url": article["url"], "group": group,
            "date": article.get("published_date", ""), "claim": text,
            "source": article.get("source", "")
        }, method)
        if method == "CURATED_URL_OR_GROUP":
            scraped_links["by_url_or_group"] += 1
        elif added:
            scraped_links["by_name"] += 1

    now = datetime.now(timezone.utc).isoformat()
    ranked = []
    for key, school in schools.items():
        reports = list(evidence[key].values())
        if not reports:
            continue
        groups = {r["group"] for r in reports}
        severe = any(any(term in norm(r.get("claim")) for term in SEVERE_TERMS) for r in reports)
        score = min(100, 40 + 15 * min(len(groups), 3) + (15 if severe else 0))
        dates = [r["date"] for r in reports if re.fullmatch(r"\d{4}-\d{2}-\d{2}", r.get("date", ""))]
        school_id = "REPORT:" + hashlib.sha256("|".join(key).encode()).hexdigest()[:16]
        urls = [r["url"] for r in reports]
        group_linked = sum(r["match_method"] == "CURATED_INCIDENT_GROUP_LINK" for r in reports)
        ranked.append({
            "rank": "", "entity_id": school_id,
            "school_name": school["school_name"], "district": school["district"],
            "block": school["block"], "identity_status": school["identity_status"],
            "issue_state": "CURRENT_CONDITION_UNKNOWN", "eligible": True,
            "priority_score": score, "priority_level": "HIGH" if score >= 60 else "MEDIUM",
            "repair_classrooms": 0, "incident_groups": len(groups),
            "evidence_events": len(reports), "latest_evidence_date": max(dates, default=""),
            "evidence_references": json.dumps(urls, ensure_ascii=False),
            "explanation": (
                f"{len(groups)} reported incident group(s) across {len(reports)} source URL(s); "
                + ("serious incident terms reported; " if severe else "")
                + (f"{group_linked} source(s) linked by curated incident group; " if group_linked else "")
                + "school identity and current condition not independently verified"
            ),
            "generated_at": now
        })

    ranked.sort(key=lambda r: (r["entity_id"]))
    ranked.sort(key=lambda r: r["latest_evidence_date"], reverse=True)
    ranked.sort(key=lambda r: r["priority_score"], reverse=True)
    for index, row in enumerate(ranked, 1):
        row["rank"] = index

    # Keep previously approved overrides; unresolved entries are a non-blocking audit.
    approved_review = [{field: ("MANUAL_OVERRIDE_RETAINED" if field == "reason" else row.get(field, ""))
                        for field in REVIEW_FIELDS} for row in approvals.values()]
    write_csv(review_csv, approved_review + unresolved, REVIEW_FIELDS)
    write_csv(all_csv, ranked, FIELDS)
    write_csv(top_csv, ranked[:limit], FIELDS)

    return {
        "curated_reports": len(curated), "scraped_articles": len(scraped),
        "scraped_linked_by_url_or_group": scraped_links["by_url_or_group"],
        "scraped_linked_by_name": scraped_links["by_name"],
        "scraped_unresolved": scraped_links["unresolved"],
        "unresolved_records_total": len(unresolved),
        "ranked_school_candidates": len(ranked), "top_count": min(limit, len(ranked)),
        "review_output": str(review_csv), "all_output": str(all_csv), "top_output": str(top_csv)
    }


def main():
    parser = argparse.ArgumentParser(description="Public-report-first school inspection suggestions")
    parser.add_argument("curated_csv")
    parser.add_argument("scraped_jsonl")
    parser.add_argument("review_csv")
    parser.add_argument("all_csv")
    parser.add_argument("top_csv")
    parser.add_argument("--limit", type=int, default=50)
    args = parser.parse_args()
    print(json.dumps(build_report_queue(
        args.curated_csv, args.scraped_jsonl, args.review_csv,
        args.all_csv, args.top_csv, args.limit
    ), indent=2))


if __name__ == "__main__":
    main()
