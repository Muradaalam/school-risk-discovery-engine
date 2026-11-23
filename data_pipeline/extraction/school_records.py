
import hashlib
import re

SCHOOL_CODE = re.compile(r"(?<![0-9])([0-9]{10,11})(?![0-9])")
SERIAL = re.compile(r"^\s*([0-9]{1,7})\s{2,}")
SCHOOL_TYPE = re.compile(r"^(GG?PS|GG?UPS|GG?SSS|GG?SS|PS|UPS|SS|SSS|MGGS)\b", re.I)
SCHOOL_TERMS = re.compile(r"school|विद्यालय|स्कूल|पाठशाला|(?:^|\s)(?:GPS|GUPS|GSSS|GGPS|GGUPS)\b", re.I)
ISSUES = {
    "BUILDING_DILAPIDATED": re.compile(r"dilapidated|जर्जर|unsafe building|structurally unsafe|क्षतिग्रस्त", re.I),
    "BUILDING_COLLAPSE": re.compile(r"(?:roof|building|wall|ceiling).{0,35}collaps|collaps.{0,35}(?:school|roof|building|wall)|(?:छत|दीवार|भवन).{0,30}(?:ढह|गिर(?:ा|ी|े|ने))", re.I),
    "MAJOR_REPAIR": re.compile(r"major\s+repairs?|repairing|school\s+repairs?|मेजर\s+रिपेयर|मरम्मत|मरम्मती", re.I),
    "BUILDING_REQUIREMENT": re.compile(r"new\s+building\s+requirement|building\s+construction|नवीन\s+भवन|भवन\s+निर्माण", re.I),
}


def clean(value):
    return re.sub(r"\s+", " ", value or "").strip()


def record_id(*parts):
    return hashlib.sha256("\x1f".join(str(x) for x in parts).encode("utf-8")).hexdigest()[:24]


def issue_type(text):
    for category, pattern in ISSUES.items():
        if pattern.search(text or ""):
            return category
    return ""


def _name_type_conflict(name, school_type):
    prefix = re.match(r"^(GPS|GUPS|GSSS|GGPS|GGUPS|GGSSS)\b", name, re.I)
    return bool(prefix and school_type and prefix.group(1).upper() != school_type.upper())


def parse_school_table_row(line, *, section, meta):

    match = SERIAL.match(line)
    if not match:
        return None
    code = SCHOOL_CODE.search(line, match.end())
    if not code:
        return None
    before = [clean(p) for p in re.split(r"\s{2,}", line[:code.start()].strip()) if clean(p)]
    after = line[code.end():].strip()
    if len(before) < 4 or before[0] != match.group(1):
        return None
    district, block, name = before[1], before[-2], before[-1]
    if not district or not block or not name or name.isdigit():
        return None
    kind = SCHOOL_TYPE.match(after)
    school_type = kind.group(1).upper() if kind else ""
    remainder = after[kind.end():].strip() if kind else after
    cols = re.split(r"\s{2,}", remainder) if remainder else []
    cells = [c.strip() for c in cols if c.strip()]
    
    dilapidated = next((v.upper() for v in cells if v.upper() in ("YES", "NO")), "")
    title = meta.get("title", "")
    context_issue = issue_type(title)
    if dilapidated == "YES" and not context_issue:
        context_issue = "BUILDING_CONDITION_REPORTED"
    if dilapidated == "NO":
        context_issue = ""  
    identity_note = "VALID_FORMAT_UNVERIFIED_IDENTITY" if len(code.group(1)) == 11 else "REQUIRES_VERIFICATION_10_DIGIT"
    row = {
        "record_id": record_id(meta["sha256"], section.get("page_number"), match.group(1), line),
        "source": meta.get("source", "UNKNOWN"), "source_url": meta.get("source_url", ""),
        "source_sha256": meta["sha256"], "document_title": title,
        "document_format": meta.get("format", ""),
        "page_number": section.get("page_number"), "serial": int(match.group(1)),
        "district": district, "block": block, "school_name": name,
        "school_code_raw": code.group(1), "udise_raw": code.group(1),
        "udise_code": code.group(1) if len(code.group(1)) == 11 else "",
        "identity_status": identity_note, "school_type": school_type,
        "dilapidated_reported": dilapidated, "evidence_type": context_issue,
        "evidence_snippet": clean(line)[:500],
        "inspection_status": "NOT_ASSESSED", "repair_completion_status": "UNVERIFIED",
    }
    if _name_type_conflict(name, school_type):
        row["review_flag"] = "SCHOOL_NAME_TYPE_MISMATCH"
    
    if len(cells) >= 3 and cells[0].isdigit() and cells[1].isdigit():
        row["enrollment_raw"] = cells[0]
        row["repair_classrooms_raw"] = cells[1]
        row["repair_amount_raw"] = cells[2]
    return row


def extract_school_evidence(sections, meta, *, max_narrative=200):
    schools, evidence, review = [], [], []
    seen_records = set()
    seen_serials = set()
    table_row_candidates = 0
    unparsed_table_rows = 0
    narratives = 0
    for section in sections:
        text = section.get("text", "")
        
        for line_number, line in enumerate(text.splitlines(), 1):
            looks_like_table = bool(SERIAL.match(line) and len(re.split(r"\s{2,}", line.strip())) >= 4)
            table_row_candidates += int(looks_like_table)
            row = parse_school_table_row(line, section=section, meta=meta)
            if row:
                if row["record_id"] in seen_records:
                    continue
                seen_records.add(row["record_id"])
                schools.append(row)
                if row["serial"] in seen_serials:
                    review.append({"reason": "POSSIBLE_DUPLICATE_SERIAL", "serial": row["serial"],
                                   "page_number": section.get("page_number"), "record_id": row["record_id"]})
                seen_serials.add(row["serial"])
                if row.get("review_flag"):
                    review.append({"reason": row["review_flag"], "record_id": row["record_id"],
                                   "page_number": section.get("page_number"), "text": clean(line)[:300]})
                if row["evidence_type"]:
                    evidence.append({
                        "evidence_id": record_id("ev", row["record_id"]),
                        "source": row["source"], "source_url": row["source_url"],
                        "source_sha256": row["source_sha256"], "page_number": row["page_number"],
                        "school_record_id": row["record_id"], "school_name": row["school_name"],
                        "identity_status": row["identity_status"], "evidence_type": row["evidence_type"],
                        "snippet": row["evidence_snippet"], "status": "REQUIRES_REVIEW",
                    })
                continue
            if looks_like_table:
                unparsed_table_rows += 1
                review.append({"reason": "UNPARSED_POSSIBLE_TABLE_ROW",
                               "page_number": section.get("page_number"),
                               "text": clean(line)[:350], "source_sha256": meta["sha256"]})
                continue
            if narratives >= max_narrative:
                continue
            line = clean(line)
            if len(line) < 20 or not SCHOOL_TERMS.search(line):
                continue
            kind = issue_type(line)
            if not kind:
                continue
            narratives += 1
            evidence.append({
                "evidence_id": record_id("narrative", meta["sha256"], section.get("page_number"), line_number, line),
                "source": meta.get("source", "UNKNOWN"),
                "source_url": section.get("entry_url") or meta.get("source_url", ""),
                "source_sha256": meta["sha256"], "page_number": section.get("page_number"),
                "school_record_id": "", "school_name": "",
                "identity_status": "UNRESOLVED", "evidence_type": kind,
                "snippet": line[:700], "status": "REQUIRES_SCHOOL_MATCHING_AND_CLAIM_REVIEW",
            })
    serials = {row["serial"] for row in schools}
    if len(serials) >= 3:
        first, last = min(serials), max(serials)
        missing_serials = [number for number in range(first, min(last + 1, first + 100000)) if number not in serials]
    else:
        missing_serials = []
    audit = {"table_row_candidates": table_row_candidates,
             "parsed_table_rows": len(schools), "unparsed_table_rows": unparsed_table_rows,
             "unique_serials": len(serials), "min_serial": min(serials) if serials else None,
             "max_serial": max(serials) if serials else None,
             "missing_serial_count": len(missing_serials),
             "missing_serial_sample": missing_serials[:30]}
    if not schools:
        review.append({"reason": "NO_STRUCTURED_SCHOOL_ROWS", "source_sha256": meta["sha256"],
                       "note": "Narrative evidence (if any) is preserved separately; no school identity inferred"})
    return {"schools": schools, "evidence": evidence, "review": review, "audit": audit}
