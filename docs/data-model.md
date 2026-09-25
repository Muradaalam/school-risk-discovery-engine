

# Data Model

## 1. Purpose

The data model defines how the School Risk Discovery Engine represents schools,
public sources, documents, evidence, issues, events, inspections, repair/tender
activities, and inspection-priority history.

The model is designed around four principles:

1. Every important conclusion must be traceable to public evidence.
2. Historical information must not be overwritten.
3. Missing public information must not be interpreted as proof of absence.
4. Evidence from copied or dependent sources must not be counted as independent
   corroboration.

The system is an evidence-discovery and inspection-prioritization system.
It does not determine whether a school is objectively safe/unsafe and does not
replace an official inspection.


# 2. High-Level Model

The main entities are:

1. School
2. Source
3. Document
4. Evidence
5. EvidenceRelation
6. Issue
7. Event
8. Inspection
9. RepairTender
10. PrioritySnapshot

An additional operational entity is:

11. SourceRetrieval

The high-level relationship is:

    Source
       |
       v
    Document
       |
       v
    Evidence -----> EvidenceRelation
       |
       v
     Event
       |
       v
     Issue
       |
       +--------> Inspection
       |
       +--------> RepairTender

    School
       |
       +-------- Issue
       +-------- Event
       +-------- Evidence
       +-------- Inspection
       +-------- RepairTender
       +-------- PrioritySnapshot


# 3. Design Principles

## 3.1 Internal IDs

Every major entity receives an internal system-generated ID.

Examples:

    SCH_RJ_000123
    DOC_000456
    EVD_000789
    EVT_000234
    ISS_000321

External identifiers such as UDISE codes or tender references are stored
separately and must not be assumed to be permanent internal primary keys.


## 3.2 Preserve Original Data

The system must preserve important source values.

For example, if three sources use:

    Government Senior Secondary School Sanganer
    GSSS Sanganer
    Govt. Sr. Sec. School, Sanganer

the original names must remain available.

A normalized name may additionally be stored for matching.


## 3.3 Historical Data Is Append-Oriented

Important historical events should not normally be overwritten.

For example:

    2024  Roof damage reported
    2025  Repair tender issued
    2025  Tender awarded
    2026  Completion evidence found

These remain separate records.

The current state can be derived from the historical record.


# 4. Entity: School

Represents the physical educational institution.

## Fields

    school_id
        Internal permanent identifier.

    udise_code
        External UDISE identifier when available.

    school_name
        Official/source-provided school name.

    normalized_name
        Normalized representation used for matching.

    state
        State in which the school is located.

    district
        District.

    block
        Administrative block.

    latitude
        Geographic latitude when available.

    longitude
        Geographic longitude when available.

    school_type
        Example: primary, secondary, senior secondary.

    management_type
        Example: government, aided, etc.

    created_at
        System record creation timestamp.

    updated_at
        Last system update timestamp.

## Important rules

- `school_id` is the system's internal identity.
- `udise_code` is an external identifier.
- UDISE code should be preferred for exact entity matching when available.
- A school may exist in the system even when a UDISE code is unavailable.
- Original source names must not be discarded.


# 5. Entity: Source

Represents an organization, portal, or information system publishing
information.

Examples:

    UDISE+
    Rajasthan ShalaDarpan
    Rajasthan eProcurement
    Rajasthan Council of School Education
    Jan Soochna Rajasthan
    Rajasthan Sampark
    Public news source

## Fields

    source_id
        Internal identifier.

    source_name
        Human-readable source name.

    source_type
        Example:
            GOVERNMENT
            INSTITUTIONAL
            NEWS
            PUBLIC_REPORT

    source_tier
        Evidence provenance category:

            TIER_1_OFFICIAL
            TIER_2_INSTITUTIONAL
            TIER_3_PUBLIC_REPORTING

    base_url
        Main source URL.

    created_at
        Record creation timestamp.

## Important rule

`source_tier` describes provenance and origin.

It is NOT a direct numerical truth score.


# 6. Entity: Document

Represents an individual webpage, PDF, notice, tender document,
report, dataset record, or other retrievable source artifact.

## Fields

    document_id
        Internal identifier.

    source_id
        Source that published the document.

    title
        Document/page title.

    url
        Original URL.

    document_type
        Example:

            WEB_PAGE
            PDF
            TENDER
            INSPECTION_REPORT
            NOTICE
            DATASET_RECORD
            NEWS_ARTICLE
            OTHER

    published_at
        Publication date when available.

    retrieved_at
        Time at which the system retrieved the document.

    content_hash
        Hash used to identify duplicate versions/content.

    created_at
        System record creation timestamp.

## Important rules

- One document may contain information about multiple schools.
- One document may support multiple evidence records.
- Documents should not be duplicated merely because they support multiple
  schools or issues.
- `content_hash` can help identify copied or duplicate documents.


# 7. Entity: Evidence

Evidence represents a specific extracted claim or observation from a document.

Examples:

    "Roof damage reported at the school."

    "Repair tender awarded on 12 June 2025."

    "Inspection conducted on 10 January 2026."

Evidence is the fundamental traceable unit used by the intelligence layer.

## Fields

    evidence_id
        Internal identifier.

    school_id
        School associated with the evidence when confidently resolved.

    event_id
        Event supported by this evidence.

    document_id
        Document from which the evidence was obtained.

    evidence_group_id
        Optional identifier used to group evidence records that refer to
        the same underlying claim or event.

        Evidence grouping must not merge genuinely independent observations.
        Independent evidence remains represented as separate Evidence records.

        Relationships between individual evidence records are represented
        through EvidenceRelation.

    independence_type
        Classification of the relationship of this evidence to other evidence:

            INDEPENDENT
            DERIVED
            DUPLICATE
            UNKNOWN

    claim
        Extracted factual statement.

    event_date
        Date associated with the underlying event, when available.

    extracted_at
        Timestamp when the system extracted the evidence.

    confidence
        Confidence of the extraction/entity association.

## Important rules

- Evidence must retain its document provenance.
- Evidence is not the same thing as a document.
- Multiple evidence records may come from the same document.
- Multiple independent evidence records may support the same event.
- Copied reports must not automatically count as independent evidence.
- `confidence` describes system confidence in extraction/matching; it does not
  mean that the underlying claim is objectively true.


# 8. Entity: EvidenceRelation

Represents a relationship between two evidence records.

This is necessary because multiple sources may discuss the same underlying
event without representing independent observations.

## Fields

    evidence_relation_id
        Internal identifier.

    evidence_id
        First evidence record.

    related_evidence_id
        Related evidence record.

    relation_type
        Possible values:

            DUPLICATES
            DERIVED_FROM
            CORROBORATES
            CONTRADICTS

    created_at
        Timestamp when the relationship was created.

## Examples

If two websites copy the same original report:

    Article B
        DERIVED_FROM
    Article A

If an independent inspection report supports a news report:

    Inspection Evidence
        CORROBORATES
    News Evidence

If two records disagree:

    Evidence A
        CONTRADICTS
    Evidence B

## Important rule

Independent evidence should remain as separate evidence records.

Evidence grouping must never collapse independent observations into one record.


# 9. Entity: Issue

Represents a specific school-level problem or condition.

Examples:

    Roof damage
    Broken toilets
    Lack of drinking water
    Damaged boundary wall

## Fields

    issue_id
        Internal identifier.

    school_id
        School experiencing the issue.

    issue_type
        Controlled category.

    description
        Human-readable description.

    status
        Possible values:

            ACTIVE
            UNDER_REPAIR
            RESOLVED
            VERIFIED
            UNKNOWN
            CONFLICTED

    first_detected_at
        Earliest known date.

    last_updated_at
        Most recent known update.

    resolved_at
        Resolution date when supported by evidence.

## Issue types

    ROOF
    BUILDING
    CLASSROOM
    TOILET
    DRINKING_WATER
    ELECTRICITY
    BOUNDARY_WALL
    ROAD_ACCESS
    OTHER

## Important rules

- An issue represents a problem/condition, not an individual report.
- Multiple events may belong to one issue.
- If the same type of issue occurs again after being resolved, it should
  normally be represented as a new issue instance rather than overwriting
  the historical issue.
- `UNKNOWN` must be used when available evidence does not establish the
  current status.


# 10. Entity: Event

Represents something that happened regarding a school or issue.

Examples:

    Issue reported
    Inspection conducted
    Tender issued
    Tender awarded
    Repair completed

## Fields

    event_id
        Internal identifier.

    school_id
        School associated with the event.

    issue_id
        Related issue when applicable.

    event_type
        Controlled event category.

    event_date
        Date on which the event occurred.

    description
        Description of the event.

    created_at
        System record creation timestamp.

## Event types

    ISSUE_REPORTED
    INSPECTION_CONDUCTED
    REPAIR_PROPOSED
    TENDER_ISSUED
    TENDER_AWARDED
    REPAIR_STARTED
    REPAIR_COMPLETED
    ISSUE_VERIFIED
    COMPLAINT_REPORTED
    INCIDENT_REPORTED
    STATUS_UPDATED
    OTHER

## Important rules

- Events are historical facts/claims supported by evidence.
- One event can have multiple evidence records.
- An event should not be created solely because the system failed to find
  evidence for something.
- "No completion evidence found" is not itself a `REPAIR_COMPLETED` or
  `REPAIR_NOT_COMPLETED` event.


# 11. Entity: Inspection

Represents a publicly identifiable inspection record.

## Fields

    inspection_id
        Internal identifier.

    school_id
        School inspected.

    inspection_date
        Date of inspection.

    inspection_type
        Type of inspection when available.

    status
        Status of the inspection record.

    document_id
        Supporting public document.

    created_at
        System record creation timestamp.

## Important rules

- Absence of an inspection record does NOT mean that no inspection occurred.
- Only publicly identifiable inspection information should be represented
  as an inspection record.
- Inspection history is retained even after newer inspections occur.


# 12. Entity: RepairTender

Represents a repair/construction tender or work lifecycle associated
with a school.

## Fields

    repair_id
        Internal identifier.

    school_id
        School associated with the work.

    issue_id
        Related issue when known.

    tender_reference
        External tender/work reference.

    work_description
        Description of the work.

    tender_date
        Tender publication date.

    award_date
        Award date when available.

    start_date
        Work start date when available.

    completion_date
        Completion date when supported.

    status
        Possible values:

            PROPOSED
            TENDERED
            AWARDED
            IN_PROGRESS
            COMPLETED
            UNKNOWN

    estimated_value
        Estimated/contract value when available.

    contractor
        Contractor name when available.

    document_id
        Primary supporting document.

    created_at
        System record creation timestamp.

## Important rule

A tender or award does NOT imply that the repair was completed.

Completion requires separate supporting evidence.


# 13. Entity: PrioritySnapshot

Represents the inspection priority calculated for a school at a particular
point in time.

## Fields

    priority_id
        Internal identifier.

    school_id
        School being evaluated.

    priority_level
        Possible values:

            LOW
            MEDIUM
            HIGH

    calculated_at
        Timestamp at which the priority was calculated.

    reason_summary
        Human-readable explanation of the major factors contributing
        to the priority.

    evidence_coverage
        Optional coverage classification:

            LOW
            MEDIUM
            HIGH

## Important rules

- Priority is time-dependent.
- Priority must not be stored as a permanent property of a school.
- Historical priority snapshots must be retained.
- A priority result must be explainable through underlying evidence/events.
- Evidence coverage must not be interpreted as risk.
- A low evidence coverage value does not imply low inspection priority.


# 14. Entity: SourceRetrieval

Operational entity used to record scraper/retrieval activity.

## Fields

    retrieval_id
        Internal identifier.

    source_id
        Source being retrieved.

    retrieved_at
        Retrieval timestamp.

    status
        Possible values:

            SUCCESS
            PARTIAL
            FAILED

    record_count
        Number of records successfully retrieved.

    error
        Error information when applicable.

## Important distinction

These two situations are different:

    SUCCESS + record_count = 0

means:

    "The source was successfully searched and no matching records
     were found."

Whereas:

    FAILED

means:

    "The source could not be successfully searched."

The system must never convert a retrieval failure into "no evidence found."


# 15. Entity Relationships

## School → Issue

One school can have many issues.

    School 1 ---- N Issue


## School → Event

One school can have many events.

    School 1 ---- N Event


## Issue → Event

One issue can have many events.

    Issue 1 ---- N Event

Example:

    Roof issue
        |
        +-- ISSUE_REPORTED
        +-- REPAIR_PROPOSED
        +-- TENDER_AWARDED
        +-- REPAIR_STARTED
        +-- REPAIR_COMPLETED


## Event → Evidence

One event can have multiple supporting evidence records.

    Event 1 ---- N Evidence


## Document → Evidence

One document can support multiple evidence records.

    Document 1 ---- N Evidence


## Source → Document

One source can publish many documents.

    Source 1 ---- N Document


## Evidence ↔ Evidence

Evidence records can have relationships through EvidenceRelation.

    Evidence N ---- N Evidence

Possible relationships:

    DUPLICATES
    DERIVED_FROM
    CORROBORATES
    CONTRADICTS


## School → Inspection

    School 1 ---- N Inspection


## School → RepairTender

    School 1 ---- N RepairTender


## School → PrioritySnapshot

    School 1 ---- N PrioritySnapshot


# 16. Entity Resolution

Entity resolution is responsible for determining whether a source record
belongs to an existing school.

Matching should follow approximately this hierarchy:

    1. Exact UDISE code
    2. Strong identifier + geographic agreement
    3. Strong name + district/block/location agreement
    4. Entity matching algorithm
    5. Manual/controlled review when necessary

Every resolved record should retain:

    match_method
    match_confidence

If the system cannot confidently resolve a record:

    DO NOT force the record onto a school.

False association is more damaging than an unresolved record.


# 17. Evidence and Independence

The system must distinguish between:

## Independent evidence

Two genuinely independent observations.

Example:

    Independent complaint
    Independent inspection report

These can strengthen corroboration.

## Derived evidence

One source obtained its information from another source.

Example:

    News article quoting an earlier report.

This should not be counted as an independent observation.

## Duplicate evidence

The same document/content appears multiple times.

Duplicates should not increase corroboration.

## Unknown

The relationship cannot be reliably determined.


# 18. Contradictory Evidence

The system must preserve contradictory public records.

Example:

    Evidence A:
        "Repair completed."

    Evidence B:
        "Roof still leaking."

The system should retain both and represent:

    A CONTRADICTS B

It must not silently select one source as correct.

The UI may display:

    "Conflicting public records identified."


# 19. Missing Information

The following distinctions must be preserved:

    No evidence found
    Source unavailable
    Evidence exists but could not be linked confidently
    Public record does not contain the required information

These are not equivalent.

In particular:

    No public evidence found

does NOT mean:

    The event/problem never occurred.


# 20. Temporal Model

The system distinguishes between:

    event_date
    published_at
    retrieved_at
    extracted_at

These dates have different meanings.

Example:

    event_date
        When the underlying event occurred.

    published_at
        When the source published the document.

    retrieved_at
        When our system retrieved it.

    extracted_at
        When our pipeline extracted the evidence.

The system should never replace one with another.


# 21. Data Lineage

Every important system conclusion should be traceable:

    Priority
       ↓
    Issue/Event
       ↓
    Evidence
       ↓
    Document
       ↓
    Source

A user should therefore be able to move from:

    "HIGH inspection priority"

to:

    "Why?"

and then see the supporting events, evidence, documents, and original sources.


# 22. Current Priority vs Historical Record

The system must distinguish:

    Historical evidence
    Current issue state
    Current inspection priority

Historical information remains available even when an issue is resolved.

For example:

    2024  Roof damaged
    2025  Repair completed
    2026  Inspection verified repair

The historical record remains intact, while the current priority calculation
can reflect the latest available evidence.

# 23. Evidence Coverage

Evidence coverage describes the availability of relevant public information,
not the actual condition of a school.

Example:

    School A:
        High evidence coverage
        Several recent records

    School B:
        Low evidence coverage
        Very little public information

The system must not interpret School B as safer merely because less
information is available.


# 24. Scope of Evidence

Not all public documents can be confidently associated with an individual
school.

Evidence may be:

    SCHOOL_LEVEL
    BLOCK_LEVEL
    DISTRICT_LEVEL
    STATE_LEVEL

Only evidence that can be reliably associated with a school should directly
contribute to that school's inspection priority.

Broader-scope information may be retained as contextual information.


# 25. Priority Queue

The system will expose a current inspection-priority view.

Example:

    INSPECTION PRIORITY QUEUE

    School                     Priority
    -------------------------------------
    School A                   HIGH
    School B                   HIGH
    School C                   MEDIUM
    School D                   LOW

Users can filter by:

    District
    Block
    Issue type
    Date
    Priority

The queue represents evidence-based prioritization for further inspection.
It is not a declaration that one school is objectively unsafe or that an
inspection must literally occur in a particular order.


# 26. Core Integrity Rules

The following rules are mandatory:

1. Never treat a missing record as proof of absence.
2. Never treat a tender award as proof of repair completion.
3. Never count copied sources as independent evidence.
4. Never force uncertain school matches.
5. Never overwrite historical events.
6. Never permanently label a school as risky.
7. Never silently resolve contradictory evidence.
8. Never confuse source retrieval failure with absence of evidence.
9. Never treat evidence coverage as risk.
10. Every priority result must be explainable through underlying evidence.
11. Preserve original source information.
12. Keep event date, publication date, retrieval date, and extraction date distinct.
13. Resolved issues should remain visible historically.
14. Recurring issues should be represented as separate issue instances when appropriate.
15. Evidence should remain traceable to its original document and source.


# 27. Simplified Example

A school may ultimately have:

    SCHOOL
       |
       +-- ISSUE: Roof damage
       |      |
       |      +-- EVENT: Issue reported
       |      |      |
       |      |      +-- Evidence → News article
       |      |      +-- Evidence → Complaint
       |      |
       |      +-- EVENT: Tender awarded
       |      |      |
       |      |      +-- Evidence → Rajasthan eProcurement
       |      |
       |      +-- EVENT: Repair completed
       |             |
       |             +-- Evidence → Completion document
       |
       +-- INSPECTION
       |
       +-- PRIORITY SNAPSHOT
              |
              +-- HIGH
              +-- MEDIUM
              +-- LOW

Every priority result can therefore be traced back to the evidence that
produced it.


# 28. What This Model Does Not Store

The core model does not attempt to store:

- A permanent "risk score" for a school
- A permanent safe/unsafe classification
- Unsupported claims about a school
- Unverified assumptions that an inspection never happened
- Unverified assumptions that a repair failed
- Duplicate copies of the same evidence as independent observations

Such information would either be misleading or unnecessarily constrain the
system.