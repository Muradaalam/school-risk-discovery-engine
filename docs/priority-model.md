# School Risk Discovery Engine — Priority Model

## 1. Purpose

The priority model determines which schools should be considered for further
inspection based on the public reports that can be linked to them.

The model is designed to be:

- deterministic
- explainable
- evidence-driven
- auditable
- resistant to duplicate reports

Every priority result should be traceable to the underlying:

    School
       ↓
    Linked reports
       ↓
    Original source URLs

The score is intended for inspection screening. It does not prove that a
school is unsafe.

# 2. Priority Calculation Flow

The priority calculation follows this pipeline:

    Public reports
        ↓
    School identification
        ↓
    Evidence linking and grouping
        ↓
    School priority score
        ↓
    Ranked inspection queue

We first identify the school mentioned in a report. Curated records can be
linked using school name and district, or through a unique incident-group
link. Scraped articles can also be matched using the school name and location.

Reports that cannot be linked unambiguously are kept for review.

The score is calculated using the linked reports for each school.

# 3. Important Design Principles

## 3.1 Deterministic Model

The system calculates inspection priority using predefined rules. The same
linked evidence produces the same score.

The current priority calculation does not use a trained machine-learning
model.

## 3.2 Priority Can Change

Priority is not a permanent property of a school.

The ranking is calculated using the reports available when the pipeline runs.
New reports can change the number of incident groups, the serious-incident
indicator, and the resulting rank.

The report date is also used when scores are tied.

## 3.3 Priority Is Calculated Per School

The report queue calculates one score for each school with linked evidence.

For example:

    School A
        |
        +-- Report 1: roof damage
        |
        +-- Report 2: follow-up on the same incident
        |
        +-- Report 3: another incident

The reports are grouped before scoring, so two articles about the same
incident do not automatically count as two incidents.

## 3.4 Historical Reports Remain Evidence

Older reports are not discarded merely because newer reports appear.

A report about a past repair does not, by itself, prove the school's current
condition. The report queue therefore records:

    CURRENT_CONDITION_UNKNOWN

The score reflects linked public reports, not a confirmed current safety state.

# 4. Priority Factors

Each school with linked reports receives a score using three parts:

    1. Base score
    2. Number of incident groups
    3. Serious-incident indicator

The formula is:

    School Priority Score =
        40
        + 15 × min(Incident Groups, 3)
        + 15 if serious incident terms are present

The final score is capped at 100.

# 5. Factor 1 — Base Score

The base score is 40.

This is applied only after a school has at least one linked evidence report.

The code checks:

    reports = list(evidence[key].values())
    if not reports:
        continue

A school without linked evidence is excluded from the ranking. It does not
receive a score of 40.

# 6. Factor 2 — Incident Groups

Incident groups represent reports associated with the same reported incident.

The model counts distinct group identifiers, with a maximum contribution from
three groups.

| Distinct incident groups | Points added |
|-------------------------|-------------:|
| 1                       | 15           |
| 2                       | 30           |
| 3 or more               | 45           |

For example:

    Article A → roof incident at School X
    Article B → follow-up on the same incident

If both use the same incident-group identifier, they contribute one group.

When a curated incident group is unavailable, the source URL may be used as
the group identifier. This avoids counting the same URL twice, but does not
prove that articles at different URLs describe independent incidents.

# 7. Factor 3 — Serious Incident Terms

The model adds 15 points when a linked report contains one of the configured
serious-incident terms.

Examples include words relating to:

    building collapse
    deaths
    injuries

The code checks English and Hindi terms in the linked report claims.

The additional 15 points are applied once per school, not once per article.

For example:

    One incident group, no serious term → 40 + 15 = 55
    One incident group, serious term    → 40 + 15 + 15 = 70

The indicator is keyword-based and should not be treated as an independently
verified severity assessment.

# 8. School Identification

A report must be linked to a school before it can affect that school's score.

The pipeline first builds a school registry from curated records containing a
school name and district.

Scraped reports can then be matched by:

- a URL already present in the curated reports
- an unambiguous school name and district already in the registry
- an explicitly extracted school name and district
- a previously approved manual match

For newly extracted school names, the article-matching code also checks for
infrastructure-related terms. If the name or district is ambiguous, the report
is left for review.

A recognized school identity is still provisional until separately verified.

# 9. Report Grouping and Duplicate Handling

The model keeps evidence records by canonical source URL for each school.

The URL is normalized so that minor differences, including common tracking
parameters, do not create extra copies of the same report.

If a scraped article has a URL already present in curated evidence, it is not
counted as another report.

Reports may also be assigned a common incident-group identifier.

For example:

    Original report  → Group A
    Follow-up report → Group A

The two URLs can remain visible as supporting references, while the group is
counted once for the score.

Different URLs without a shared group may still refer to the same event, so
the incident count is based on available grouping information.

# 10. Evidence Dates and Recency

The report queue records the latest available evidence date for a school.

Dates come from the available report information, such as event dates in the
curated file or publication dates in scraped articles.

Recency does not add points to the 0–100 score.

Instead, the latest evidence date is used to break ties between schools with
the same score.

For example:

    School A → Score 70, latest evidence in 2026
    School B → Score 70, latest evidence in 2025

School A is ranked above School B.

The underlying event date and publication date are not necessarily the same.

# 11. Maximum Score

The highest score is:

    Base score                 40
    Three incident groups      45
    Serious incident terms     15

    Maximum                   100

The number of incident groups contributes at most 45 points, even if more
than three groups are linked to a school.

# 12. Priority Classification

The report queue uses these thresholds:

| Score    | Priority |
|---------:|----------|
| Below 60 | MEDIUM   |
| 60–100   | HIGH     |

Schools with no linked reports are not ranked.

With the current formula, one incident group without a serious term receives
55 (MEDIUM), and one group with a serious term receives 70 (HIGH).

The report queue does not currently assign LOW to ranked candidates.

# 13. HIGH Priority Rule

A school receives HIGH priority when its calculated score is 60 or above.

Examples:

    1 incident group + serious terms → 70 → HIGH
    2 incident groups, no serious terms → 70 → HIGH

HIGH means the reported evidence meets our screening threshold. It does not
mean the school's present condition has been verified as dangerous.

# 14. Hard Rules

These rules are applied when building the report-based queue.

## Rule 1 — Linked Evidence Required

A school without linked reports is not scored.

## Rule 2 — Valid Source Reference

Evidence without a valid HTTPS source URL is not added to the report queue.

## Rule 3 — Unambiguous School Association

Reports that cannot be linked to a single school are kept in the review file.
The system should not assign a report to a school by guessing.

## Rule 4 — Provisional Identity

A school identified from a public report remains unverified unless additional
identity evidence becomes available.

## Rule 5 — Duplicate URLs

A report URL is counted once per school. The same article appearing in the
curated and scraped inputs does not become two reports.

## Rule 6 — Incident Grouping

Reports sharing an incident-group identifier contribute one group to the
scoring formula.

## Rule 7 — Serious Incident Indicator

Serious-incident terms contribute 15 points at most once per school.

## Rule 8 — Current Condition

The report queue uses CURRENT_CONDITION_UNKNOWN. A news report does not, by
itself, establish whether an issue is currently active or resolved.

## Rule 9 — Failed Retrieval

A failed article request is not interpreted as proof that no issue exists.
The collector keeps counts of article and feed errors separately from the
successfully collected reports.

# 15. School-Level Priority

The report queue produces one ranking entry per school with linked evidence.

For example:

    School A
        |
        +-- Incident Group 1
        +-- Incident Group 2
        +-- Serious terms found

    Score = 40 + 15 × 2 + 15 = 85
    Priority = HIGH

Schools are ordered by:

    1. Priority score, descending
    2. Latest evidence date, descending
    3. Generated school entity ID, ascending

The Top-50 file contains the first 50 ranked schools, or fewer when fewer
schools have qualifying linked evidence.

# 16. Priority Explanation

Every priority result includes a human-readable explanation.

For example:

    HIGH — School Priority Score: 70/100

    Incident groups:         1
    Linked source URLs:      2
    Serious terms:           Present
    Current issue state:     CURRENT_CONDITION_UNKNOWN

    Supporting evidence:
        - Public report URL 1
        - Public report URL 2

    Explanation:
        One reported incident group is linked to two source URLs.
        Serious incident terms were found in the reported claims.
        The school's identity and present condition are not independently
        verified.

The ranking output also contains the evidence references so the supporting
articles can be checked.

# 17. Evidence Coverage

Evidence coverage and priority are different concepts.

The report queue records:

    incident_groups
    evidence_events
    evidence_references

These fields describe how many groups and linked source URLs were found.

They do not prove that all available public evidence has been collected.

A school with few public reports should not automatically be described as
safe. A school with many reports should not automatically be described as
unsafe.

# 18. Example Calculations

## Example A — One Reported Incident

    Base score                = 40
    Incident groups          = 1 × 15
    Serious terms            = 0

    Total = 55
    Priority = MEDIUM

## Example B — One Serious Incident

    Base score                = 40
    Incident groups          = 1 × 15
    Serious terms            = 15

    Total = 70
    Priority = HIGH

## Example C — Two Reported Incidents

    Base score                = 40
    Incident groups          = 2 × 15
    Serious terms            = 0

    Total = 70
    Priority = HIGH

## Example D — Two Serious Incident Groups

    Base score                = 40
    Incident groups          = 2 × 15
    Serious terms            = 15

    Total = 85
    Priority = HIGH

## Example E — Three Incident Groups With Serious Terms

    Base score                = 40
    Incident groups          = 3 × 15
    Serious terms            = 15

    Total = 100
    Priority = HIGH

## Example F — Duplicate Articles About One Incident

    Article A → Group 1
    Article B → Group 1

    Distinct incident groups = 1
    Serious terms            = 0

    Total = 55
    Priority = MEDIUM

Two URLs may provide references to the same group, but the group is counted
once in the scoring formula.

## Example G — No Linked Evidence

    Linked evidence reports = 0

The school is skipped before scoring.

    No priority score assigned
    Not included in the queue

# 19. Source Failure Example

Suppose an Akashvani or PIB article request fails.

The collector records an article error instead of creating an evidence record
for that request.

The system must not convert:

    Article retrieval failed

into:

    No infrastructure problem exists.

Only successfully collected or curated reports can be linked and ranked.

# 20. Duplicate Evidence Example

Suppose the same public report appears in the curated CSV and the scraped
article output.

The report queue uses its canonical URL to avoid counting the same article
twice for the same school.

If two different URLs are known to describe the same incident, they can share
an incident-group identifier.

For example:

    Article A → Group 1
    Article B → Group 1

They contribute one incident group to the score.

A shared group prevents inflation of the incident-group count. It does not
establish whether two sources are genuinely independent observations.

# 21. Priority Storage

The report ranking is written to:

    data_pipeline/raw/report_school_priorities.csv
    data_pipeline/raw/report_top50.csv

The current recommendations can also be imported into MySQL in the table:

    srde_report_priorities

Each row stores the school reference, rank, score, priority level, evidence
references, explanation, and the calculation timestamp.

The importer updates existing candidate records when the ranking is imported
again. This table stores the current imported ranking, not a separate
historical snapshot for every run.

# 22. Priority Recalculation

Priority is recalculated when the report-ranking pipeline is run again with
its current inputs.

For example:

- a newly supplied article is linked to a school
- another report adds an incident group
- a serious-incident term is found in a linked report
- a report is associated with a different school after review

The updated ranked CSV can then be imported into MySQL.

# 23. Acceptance Tests

The ranking rules can be checked with the following cases.

### Test 1 — No linked evidence

Expected:

    School is excluded from ranking.

### Test 2 — One incident group

Expected:

    Score = 55, MEDIUM.

### Test 3 — One serious incident group

Expected:

    Score = 70, HIGH.

### Test 4 — Two incident groups without serious terms

Expected:

    Score = 70, HIGH.

### Test 5 — Three serious incident groups

Expected:

    Score = 100, HIGH.

### Test 6 — More than three incident groups

Expected:

    Incident-group contribution remains capped at 45.

### Test 7 — Duplicate source URL

Expected:

    Same URL does not produce another evidence event for that school.

### Test 8 — Two URLs in the same incident group

Expected:

    One incident group contributes to the score.

### Test 9 — Ambiguous school name

Expected:

    Unresolved report is recorded for review.

### Test 10 — School name and district missing

Expected:

    A new school is not created by guessing.

### Test 11 — Equal scores

Expected:

    Latest evidence date breaks the tie.

### Test 12 — Ranking output

Expected:

    Up to 50 schools appear in the Top-50 CSV, ordered by rank.

# 24. Model Limitations

The priority model operates on publicly available information.

Therefore:

- public information may be incomplete
- some sources may be unavailable
- some records may be outdated
- entity matching may be uncertain
- public reports may contain errors
- different sources may contradict one another
- absence of public information does not prove absence of a problem
- a HIGH priority does not prove that a school is unsafe

The output should therefore be interpreted as:

    "Based on the available public evidence, further inspection or
     verification may be warranted."

It should not be interpreted as:

    "The school is unsafe."

# 25. Initial Model Status

The current report-ranking model uses a 0–100 score based on the linked
incident groups and serious-incident terms.

The thresholds and factor values are design choices and have not been
scientifically validated as measurements of physical risk.

The model is intended to produce an explainable inspection screening queue
from the public reports available to the system.

# 26. Final Formula

For a school with at least one linked evidence report:

    School Priority Score =
        min(100, 40 + 15 × min(Incident Groups, 3)
                  + (15 if serious terms are present else 0))

    Maximum: 100

Classification:
    score <50   → Low
    50 < Score < 60  → MEDIUM
    Score >= 60 → HIGH 

A school with no linked evidence is not scored.

The output remains:

    explainable
    traceable
    evidence-based
    specific to the reports collected
