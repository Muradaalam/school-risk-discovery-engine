from dataclasses import dataclass
from enum import Enum

from data_pipeline.normalization.school_name import normalize_school_name
from data_pipeline.normalization.udise_code import normalize_udise_code


class MatchStatus(str, Enum):
    CONFIRMED = "CONFIRMED"
    POSSIBLE = "POSSIBLE"
    NO_MATCH = "NO_MATCH"
    UNRESOLVED = "UNRESOLVED"


@dataclass
class SchoolCandidate:
    name: str
    district: str | None = None
    block: str | None = None
    udise_code: str | None = None


@dataclass
class MatchResult:
    status: MatchStatus
    reason: str


def normalize_optional(value: str | None) -> str | None:
    if value is None or not value.strip():
        return None

    return normalize_school_name(value)


def match_schools(first: SchoolCandidate, second: SchoolCandidate) -> MatchResult:
    code1 = normalize_udise_code(first.udise_code) if first.udise_code else None
    code2 = normalize_udise_code(second.udise_code) if second.udise_code else None

    district1 = normalize_optional(first.district)
    district2 = normalize_optional(second.district)
    block1 = normalize_optional(first.block)
    block2 = normalize_optional(second.block)

    if code1 and code2 and code1 != code2:
        return MatchResult(MatchStatus.NO_MATCH, "Different UDISE codes")

    if district1 and district2 and district1 != district2:
        return MatchResult(MatchStatus.NO_MATCH, "Conflicting districts")

    if block1 and block2 and block1 != block2:
        return MatchResult(MatchStatus.NO_MATCH, "Conflicting blocks")

    if code1 and code2:
        return MatchResult(MatchStatus.CONFIRMED, "Matching UDISE codes")

    name1 = normalize_school_name(first.name)
    name2 = normalize_school_name(second.name)

    if name1 == name2 and district1 and district2 and block1 and block2:
        return MatchResult(MatchStatus.POSSIBLE, "Matching name and location; manual verification required")

    return MatchResult(MatchStatus.UNRESOLVED, "Insufficient evidence to confirm school identity")
