# Data Source Requirements

## 1. Purpose

The School Risk Discovery Engine collects school-related information from
public sources. Each source may provide different information about schools,
reported problems, and repair activities.

This document lists the sources we studied, the information we need from
them, and the sources used in our data pipeline.

## 2. Core Requirements

A useful source should provide one or more of the following:

- School identity information
- School location or administrative information
- Infrastructure or facility information
- Inspection information
- Complaints or reported issues
- Repair or construction information
- Tender or procurement information
- Dates associated with events or records
- Publicly accessible supporting documents or URLs

Where possible, the original source record and its URL should be preserved.

## 3. Sources Studied

### 3.1 UDISE+

Required information:

- UDISE code
- School name
- State
- District
- Block
- School type
- Management type
- Available infrastructure/facility indicators
- Relevant reporting year

Purpose:

- Establish school identity
- Provide baseline school and infrastructure information
- Support comparison of infrastructure conditions across reporting periods

Access status:

UDISE+ is useful for identifying schools and checking infrastructure data.
However, the relevant access flow involved OTP verification, so we did not
implement automated extraction from UDISE+. We also did not attempt to
bypass the access controls.

### 3.2 Rajasthan ShalaDarpan

Required information:

- School identity
- School name
- UDISE code, when available
- District
- Block
- Available school/facility information
- Relevant dates or reporting periods

Purpose:

- Provide Rajasthan-specific school information
- Support school entity resolution
- Provide additional school-level information

Access status:

We explored publicly accessible school information and the available API
surface. A complete, tested ShalaDarpan collection and integration workflow
was not included in the final data pipeline.

### 3.3 Rajasthan eProcurement

Required information:

- Tender/work reference
- Work description
- School name or location, when available
- Tender publication date
- Award date, when available
- Work/start date, when available
- Completion information, when available
- Estimated/contract value, when available
- Contractor, when available
- Source document URL

Purpose:

- Identify proposed and awarded repair/construction work
- Track available repair-related information
- Compare tender activity with reported school issues

Access status:

We tested a small tender-linking pilot, but did not build a complete
automated eProcurement collection and school-matching workflow.
Tender information is difficult to link to a particular school when the
school name or identifier is missing or inconsistent.

Important:

A tender or award must not be treated as proof that the corresponding
repair was completed.

## 4. Sources Used in the Pipeline

### 4.1 Public School Repair List (Rajasthan Gyan Sankalp PDF)

Required information:

- School name and location
- School identifier, when available
- Reported repair-related information
- Source document and reporting period

Purpose:

- Extract and study school-level repair records
- Test PDF extraction and data-quality checks
- Identify records that require manual verification

Implementation:

We processed a 508-page public repair list. The extraction produced
46,743 parsed records and 4,295 rows flagged for review. These results
belong to our earlier PDF-processing work; they are not automatically
used as the input for the final public-report priority queue.

### 4.2 Akashvani News

Required information:

- School name, when mentioned
- District or location, when available
- Article title and report text
- Publication date, when available
- Article URL

Purpose:

- Identify publicly reported school infrastructure incidents
- Link reports to school candidates
- Retain the source URL as supporting evidence

Implementation:

We implemented article collection for known Akashvani News URLs using
Python and Beautiful Soup. New article discovery and periodic collection
are not automated in the final prototype.

### 4.3 Press Information Bureau (PIB)

Required information:

- School name or incident location, when available
- Notice or article text
- Publication date, when available
- Article URL

Purpose:

- Collect relevant public announcements and reports
- Link additional information to already identified school incidents
- Preserve official source references

Implementation:

We implemented collection for known PIB article URLs. Some PIB material
may not name one particular school, so it is linked only when the school
can be identified through an unambiguous report or incident-group match.
Otherwise, it is left for review.

## 5. Common Fields

Where applicable, the acquisition pipeline should preserve:

- Original source name
- Original school name
- UDISE code, when available
- District
- Block
- Location
- Record/document title
- Source URL
- Publication date
- Event date
- Retrieved date
- Raw source data
- Document/content identifier

The pipeline should preserve original values before normalization or
transformation. Not every source provides all these fields.

## 6. Source Selection Principles

Sources should be prioritized based on:

1. Relevance to school-level analysis
2. Availability of school identifiers
3. Availability of historical information
4. Availability of dates
5. Public accessibility
6. Reliability and provenance
7. Ability to retrieve information programmatically
8. Ability to link records to an individual school

A source does not need to provide all required information. Different
sources are expected to complement each other.

For the final report-first prototype, the article collector uses Akashvani
News and PIB. The earlier repair-PDF extraction and tender-linking pilot
are separate parts of our data collection work.

## 7. Data Acquisition Principle

The system should distinguish between:

- Data successfully retrieved
- Data successfully retrieved with no matching records
- Partial retrieval
- Retrieval failure
- Information not provided by the source

A retrieval failure must never be interpreted as absence of evidence.

School names and identifiers found in public reports may be incomplete.
If a record cannot be linked confidently to one school, it should be kept
for review rather than assigned to a school by guessing.
