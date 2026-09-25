# School Risk Discovery Engine — Priority Model

## 1. Purpose

The priority model determines the current inspection priority of a school
based on the available public evidence associated with its current issues.

The model is designed to be:

- deterministic
- explainable
- evidence-driven
- time-dependent
- auditable
- resistant to duplicate or dependent evidence


Every priority result must be explainable through the underlying:

    School
       ↓
    Issue
       ↓
    Event
       ↓
    Evidence
       ↓
    Document
       ↓
    Source


# 2. Priority Calculation Flow

The priority calculation follows this pipeline:

    Evidence
        ↓
    Events
        ↓
    Issue State
        ↓
    Issue Priority
        ↓
    School Priority


Evidence is first associated with events and issues.

The current state of each issue is then determined from the available
historical evidence.

The priority of each current issue is calculated using the priority factors.

The school's current priority is derived from its current issues.



# 3. Important Design Principles

## 3.1 Deterministic Model

The current version of the system calculates inspection priority using predefined rules and evidence-based factors. This provides a transparent and explainable baseline for evaluating school priority.

The current implementation does not use a machine-learning model to directly predict inspection priority.

As a planned extension, the system will support a machine-learning-based priority prediction model. A set of school-issue cases will be annotated with priority labels, relevant features will be extracted from the collected evidence, and classical machine-learning models will be trained to predict priority levels.

The ML-based predictions will subsequently be compared with the deterministic priority results to evaluate differences in predictions, consistency, and performance. This will allow the system to retain an interpretable rule-based baseline while providing a path toward data-driven priority prediction.


ML/NLP components will be used elsewhere in the pipeline for tasks such as:

- entity matching
- information extraction
- issue classification
- duplicate detection
- claim extraction

However, these components do not directly determine the final priority.


## 3.2 Priority Is Time-Dependent

Priority is not a permanent property of a school.

A school's priority may change when:

- new evidence is discovered
- an issue is resolved
- a repair progresses
- a new issue appears
- contradictory evidence appears
- older evidence becomes stale

Historical priority snapshots must therefore be retained.


## 3.3 Priority Is Issue-First

Priority is calculated primarily at the issue level.

For example:

    School A
        |
        +-- Roof damage       → HIGH
        |
        +-- Broken toilet     → LOW
        |
        +-- Old boundary wall → MEDIUM

The school's current priority is derived from its current issues.

The system does not simply add the scores of all historical issues.


## 3.4 Historical Issues Do Not Permanently Increase Priority

A school should not remain HIGH merely because it had serious problems
in the past.

For example:

    2024  Roof damaged
    2025  Repair completed
    2026  Repair verified

The historical issue remains visible in the timeline.

However, the resolved issue contributes no current priority unless newer
evidence contradicts the resolution.


# 4. Issue Priority Factors

Each current issue receives a score using six factors:

    1. Severity
    2. Current Status
    3. Recency
    4. Independent Corroboration
    5. Repair Lifecycle
    6. Inspection Context


Maximum score:

    27


The formula is:

    Issue Priority Score =
        Severity
        + Current Status
        + Recency
        + Corroboration
        + Repair Lifecycle
        + Inspection Context


# 5. Factor 1 — Severity

Severity represents the nature and potential significance of the issue.

It does NOT represent the number of reports about the issue.

| Severity | Meaning |
|----------|---------|
| 1        | Minor |
| 2        | Moderate |
| 3        | Significant |
| 4        | Serious |
| 5        | Critical |

Examples:

    Roof/building structural damage      → 4–5
    Major building damage                → 4–5
    Drinking water problem               → 3
    Toilet/sanitation problem            → 3
    Electricity problem                  → 3–4
    Boundary wall damage                 → 2–3
    Minor maintenance issue              → 1


Severity must be assigned according to the issue type and documented
characteristics.

A large number of reports cannot increase the inherent severity of an issue.


# 6. Factor 2 — Current Status

Current status represents the latest supported state of the issue.

| Issue Status | Score |
|--------------|------ |
| VERIFIED     |   0   |
| RESOLVED     |   0   |
| UNDER_REPAIR |   2   |
| UNKNOWN      |   3   |
| CONFLICTED   |   3   |
| ACTIVE       |   5   |

### Important rules

A VERIFIED or RESOLVED issue contributes zero current status points when
there is no newer contradictory evidence.

An UNDER_REPAIR issue remains relevant but receives less weight than an
ACTIVE unresolved issue.

UNKNOWN means that the available evidence does not establish the current
state.

CONFLICTED means that available evidence contains unresolved contradictions
about the current state.

# 7. Factor 3 — Recency

Recency represents how recently the available evidence supports the current
state of the issue.

| Latest Relevant Evidence | Score |
|--------------------------|-------|
| ≤ 6 months               |   5   |
| > 6 and ≤ 18 months      |   4   |
| > 18 and ≤ 36 months     |   2   |
| > 36 months              |   1   |

The relevant date should normally be the date of the underlying event or
observation.

The system must distinguish:

    event_date
    published_at
    retrieved_at
    extracted_at

These dates must not be substituted for one another.

### Persistence rule

Old evidence should not automatically make a currently persistent issue
stale.

For example:

    2023  Roof damage reported
    2026  Roof damage still reported

The 2026 evidence establishes current persistence and therefore receives
the appropriate recent-evidence score.


# 8. Factor 4 — Independent Corroboration

Corroboration measures the number of genuinely independent observations
supporting the current issue.

| Independent supporting observations | Score |
|-------------------------------------|-------|
|                   0                 |   0   |
|                   1                 |   2   |
|                   2                 |   4   |
|               3 or more             |   5   |

Only independent observations contribute to this factor.

The system must NOT count:

- copied news articles
- duplicate documents
- syndicated reports
- evidence derived from the same original report

as independent observations.

For example:

    Government inspection report
    Independent complaint
    Independent public report

may represent three independent observations.

However:

    Original report
    News article quoting original report
    Another article copying the same report

may represent only one independent observation.


# 9. Factor 5 — Repair Lifecycle

Repair lifecycle represents the available evidence about corrective action
associated with the issue.

| Repair State                                                    | Score |
|-----------------------------------------------------------------|-------|
| Verified completed                                              |   0   |
| Work in progress                                                |   1   |
| Recently proposed/awarded                                       |   2   |
| Awarded but long overdue / no completion evidence               |   4   |
| No repair response evidence where source coverage is sufficient |   5   |

### Important rules

A tender being issued does not mean that repair has started.

A tender being awarded does not mean that repair has been completed.

Completion requires separate supporting evidence.

The system must also distinguish:

    No completion evidence found

from:

    Repair was not completed


A source retrieval failure must never be treated as evidence that no repair
completion record exists.

# 10. Factor 6 — Inspection Context

Inspection context provides a small additional factor related to the
availability and recency of public inspection information.

| Inspection Context                                | Score |
|---------------------------------------------------|-------|
| Recent documented inspection addressing the issue |   0   |
| Older documented inspection                       |   1   |
| No recent public inspection record identified     |   2   |

This factor is intentionally small.

The absence of a public inspection record does NOT mean that an inspection
never occurred.

The system should use wording such as:

    "No recent public inspection record was identified
     in the searched sources."

It must not state:

    "The school has not been inspected."

# 11. Maximum Score

The maximum possible issue score is:

    Severity              5
    Current Status        5
    Recency               5
    Corroboration         5
    Repair Lifecycle      5
    Inspection Context    2
                        
    Maximum              27


# 12. Priority Classification

The initial priority thresholds are:

| Score | Priority |
|------:|----------|
| 0–7   | LOW      |
| 8–14  | MEDIUM   |
| 15–27 | HIGH     |

These thresholds are the initial version of the model and may be calibrated
after testing against real project data.

They should not be presented as universally optimal or scientifically
validated thresholds.


# 13. HIGH Priority Severity Constraint

A score of 15 or above is not sufficient by itself to produce HIGH priority.

An issue must also have:

    Severity >= 3

to receive HIGH priority.

Therefore:

    Severity 1 or 2
          ↓
    Maximum priority = MEDIUM


This prevents a minor issue from becoming HIGH merely because it has:

- many reports
- recent observations
- multiple duplicate sources
- a long repair history


Example:

    Severity = 1
    Status = 5
    Recency = 5
    Corroboration = 5
    Repair = 5
    Inspection = 2

    Raw score = 23

The final priority is still:

    MEDIUM

because the underlying issue is minor.


# 14. Hard Rules

The following rules override or constrain the numerical score.

## Rule 1 — Verified Resolution

If an issue is VERIFIED or RESOLVED and there is no newer contradictory
evidence:

    Current priority contribution = 0


The historical issue remains visible.


## Rule 2 — Stale Evidence

Old evidence alone cannot establish that an issue is currently unresolved.

A serious issue supported only by old evidence may therefore receive
MEDIUM rather than HIGH priority.


## Rule 3 — Recent Persistence

Recent evidence showing that an old issue is still present can restore
current priority.

Example:

    2023 → Roof damage reported
    2026 → Roof damage still reported

The 2026 evidence is used for current priority calculation.


## Rule 4 — Evidence Independence

Duplicate or derived evidence must not increase independent corroboration.

Evidence relationships must be represented explicitly through
EvidenceRelation.


## Rule 5 — Contradictory Evidence

Contradictory evidence must be preserved.

The system must not silently select one source as correct.

An issue may therefore receive:

    CONFLICTED

status.

Conflicting evidence may justify further verification.


## Rule 6 — Retrieval Failure

A failed scraper or unavailable source must not be interpreted as
absence of evidence.

For example:

    SourceRetrieval = FAILED

does NOT mean:

    No repair evidence exists.


## Rule 7 — Missing Public Inspection Record

No public inspection record must never be interpreted as proof that no
inspection occurred.


## Rule 8 — Evidence Coverage

Evidence coverage must remain separate from priority.

Low evidence coverage does not automatically reduce priority.

High evidence coverage does not automatically increase priority.


## Rule 9 — Scope of Evidence

Only evidence that can be reliably associated with a school should directly
contribute to that school's priority.

Evidence at:

    SCHOOL_LEVEL

may directly contribute.

Evidence at:

    BLOCK_LEVEL
    DISTRICT_LEVEL
    STATE_LEVEL

may be retained as contextual information but should not automatically
increase an individual school's priority.

# 15. School-Level Priority

A school may have multiple active issues at the same time.

For example:

School A

Roof damage          → MEDIUM
Drinking water       → MEDIUM
Electricity          → MEDIUM
Boundary wall        → LOW

The school-level priority should therefore not be determined simply by taking the highest individual issue priority.

Multiple concurrent issues may indicate a broader problem at the school level. The system will therefore analyze the combined issue profile of each school.

The analysis may consider factors such as:

individual issue scores
number of active issues
severity of issues
recency of evidence
independent supporting evidence
recurrence of issues
repair or resolution status
evidence coverage
combinations of different issue types

The system will analyze the collected dataset to determine how these factors and combinations of issues relate to the overall school-level priority. The aggregation approach and its thresholds will be determined based on this analysis rather than by assuming a fixed rule such as "two MEDIUM issues automatically become HIGH."

The objective is to ensure that:

multiple substantial issues can collectively increase school priority;
numerous minor issues do not automatically result in HIGH priority;
the reasoning behind the school-level priority remains explainable.

The resulting school-level priority will be supported by the underlying issues and evidence so that users can understand why the school received that priority.

As a later extension, a machine-learning-based priority model may be developed using the collected and labeled data. Its predictions can then be compared with the school-level priorities obtained from the initial data-driven aggregation approach.

# 16. Priority Explanation

Every priority result must be explainable.

For example:

    HIGH — Issue Priority Score: 21/27

    Primary issue:
        Roof damage

    Contributing factors:
        Severity:             5/5
        Current status:       5/5
        Recency:              5/5
        Corroboration:        2/5
        Repair lifecycle:     3/5
        Inspection context:   1/2

    Supporting evidence:
        - Government record
        - Public complaint
        - Repair/tender record

    Explanation:
        Recent evidence indicates a serious unresolved roof issue.
        Independent public records support the issue, while available
        repair information does not establish verified completion.


The user should be able to navigate from the priority result to the
underlying evidence and original sources.


# 17. Evidence Coverage

Evidence coverage is stored separately from priority.

Possible values:

    LOW
    MEDIUM
    HIGH


Evidence coverage describes how much relevant public information was
available to the system.

It does NOT describe the actual physical condition of the school.

Example:

    School A
        HIGH evidence coverage
        Multiple recent records

    School B
        LOW evidence coverage
        Very little public information


The system must NOT conclude:

    School B is safer.


Low information availability may simply mean that the public record is
limited.


# 18. Example Calculations

## Example A — Recent Serious Roof Damage

    Severity             = 5
    Current Status       = 5
    Recency              = 5
    Corroboration        = 2
    Repair Lifecycle     = 4
    Inspection Context   = 1

    Total = 22

    Priority = HIGH


Reason:

Recent evidence indicates a serious unresolved issue with supporting
evidence and incomplete/overdue repair information.


## Example B — Serious Issue Verified Repaired

    Severity             = 5
    Current Status       = 0
    Recency              = 5
    ...

However:

    VERIFIED + no newer contradictory evidence
            ↓
    Current priority contribution = 0

    Priority = LOW


The historical issue remains available in the timeline.

## Example C — Old Serious Issue

    Severity             = 5
    Current Status       = 5
    Recency              = 1
    Corroboration        = 0
    Repair Lifecycle     = 0
    Inspection Context   = 1

    Total = 12

    Priority = MEDIUM


Reason:

The historical issue is serious, but there is insufficient recent evidence
to establish that it remains unresolved.

## Example D — Minor Issue With Many Reports

    Severity             = 1
    Current Status       = 5
    Recency              = 5
    Corroboration        = 5
    Repair Lifecycle     = 5
    Inspection Context   = 2

    Raw Total = 23

But:

    Severity < 3

Therefore:

    Final Priority = MEDIUM


The issue cannot become HIGH solely because of the amount of evidence.

## Example E — Moderate Issue Under Repair

    Severity             = 3
    Current Status       = 2
    Recency              = 5
    Corroboration        = 2
    Repair Lifecycle     = 1
    Inspection Context   = 1

    Total = 14

    Priority = MEDIUM


The issue is current and significant, but corrective action is underway.

## Example F — Old Issue With Recent Persistence Evidence

    Severity             = 5
    Current Status       = 5
    Recency              = 5
    Corroboration        = 4
    Repair Lifecycle     = 2
    Inspection Context   = 1

    Total = 22

    Priority = HIGH


The original issue is old, but recent evidence establishes persistence.


## Example G — Conflicting Recent Records

Example:

    Record A:
        Repair completed

    Record B:
        Roof still leaking


The records are preserved separately.

The issue may be marked:

    CONFLICTED


Possible calculation:

    Severity             = 5
    Current Status       = 3
    Recency              = 5
    Corroboration        = 2
    Repair Lifecycle     = 2
    Inspection Context   = 1

    Total = 18

    Priority = HIGH


The explanation should explicitly state:

    "Conflicting recent public records were identified.
     Further verification may be warranted."


# 19. Source Failure Example

Suppose the Rajasthan eProcurement scraper fails.

The system records:

    SourceRetrieval
        status = FAILED


No repair completion information should be inferred from this failure.

The system must NOT convert:

    FAILED

into:

    "No repair completion evidence exists."


This distinction is essential for preventing false conclusions.

# 20. Duplicate Evidence Example

Suppose an original government report is reproduced by five news websites.

The system may contain:

    Document A → Original report
    Document B → News article
    Document C → News article
    Document D → News article
    Document E → News article


If B–E are derived from A:

    A = independent observation

    B–E = derived/duplicate evidence


Therefore the system must not treat five documents as five independent
observations.

EvidenceRelation should represent the relationships.

# 21. Priority Snapshot

Each calculated priority should be stored as a PrioritySnapshot.

A snapshot contains:

    priority_id
    school_id
    priority_level
    calculated_at
    reason_summary
    evidence_coverage


Priority snapshots allow the system to preserve changes over time.

Example:

    2025-01-10 → MEDIUM
    2025-06-20 → HIGH
    2026-01-15 → LOW


The historical snapshots explain how the school's priority changed as
new evidence appeared or issues were resolved.

# 22. Priority Recalculation

Priority should be recalculated when material evidence changes.

Examples:

- new issue evidence is discovered
- new inspection record is discovered
- repair status changes
- new corroborating evidence is linked
- contradictory evidence is discovered
- issue is verified as resolved
- recent persistence evidence is discovered

The calculation should use the latest available evidence while retaining
previous PrioritySnapshot records.

# 23. Acceptance Tests

The implementation must satisfy the following tests.

### Test 1 — Recent serious unresolved issue

Expected:

    HIGH


### Test 2 — Serious issue verified repaired

Expected:

    LOW current priority

Historical record remains.


### Test 3 — Old serious issue without recent confirmation

Expected:

    Not automatically HIGH


### Test 4 — Minor issue with many reports

Expected:

    Never HIGH


### Test 5 — Duplicate reports

Expected:

    Do not increase independent corroboration


### Test 6 — Independent evidence

Expected:

    Independent observations increase corroboration


### Test 7 — Conflicting evidence

Expected:

    Evidence preserved
    Issue may become CONFLICTED
    Explanation mentions conflict


### Test 8 — Failed scraper

Expected:

    No evidence-of-absence conclusion


### Test 9 — Recent persistence of old issue

Expected:

    Recent evidence affects current priority


### Test 10 — Resolved historical issues

Expected:

    Historical issues remain visible
    Current priority is not permanently increased


### Test 11 — No public inspection record

Expected:

    May contribute inspection-context points

But the system must NOT state:

    "No inspection occurred."


### Test 12 — Low evidence coverage

Expected:

    Does not automatically reduce priority


### Test 13 — High evidence coverage

Expected:

    Does not automatically increase priority


### Test 14 — School with multiple issues

Expected:

    Highest current issue determines primary school priority

The system should not simply sum all issue scores.


### Test 15 — Retrieval failure

Expected:

    FAILED source retrieval is not treated as absence of evidence.

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

This priority model is the initial version (v1).

The thresholds and factor weights are design parameters rather than
universally validated values.

After implementation, the model should be tested against real data from
the selected Rajasthan sources.

Any later adjustment should be documented as model calibration rather than
silently changing the rules.

# 26. Final Formula

For a current issue:

    Issue Priority Score =
        Severity
        + Current Status
        + Recency
        + Independent Corroboration
        + Repair Lifecycle
        + Inspection Context


Maximum: 27


Classification:

    0–7     → LOW
    8–14    → MEDIUM
    15–27   → HIGH


Additional constraint:

    HIGH requires Severity >= 3


The final priority must always remain:

    explainable
    traceable
    time-dependent
    evidence-based