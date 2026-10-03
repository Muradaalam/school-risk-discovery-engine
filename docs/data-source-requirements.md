# Data Source Requirements

## 1. Purpose

The School Risk Discovery Engine collects school-related information from
multiple public sources. Each source contributes different types of evidence
that can be linked to schools, issues, events, inspections, and repair
activities.

The purpose of this document is to define what information is required from
each source before implementing the data acquisition pipeline.

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

## 3. Primary Sources

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
- Provide additional school-level evidence

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
- Track the repair lifecycle
- Compare repair/tender activity with reported school issues

Important:

A tender or award must not be treated as proof that the corresponding
repair was completed.


### 3.4 Rajasthan Council of School Education

Required information:

- School-related records
- Infrastructure/work information
- Inspection or monitoring information, when publicly available
- Notices or reports relevant to school conditions
- Dates
- Supporting document URLs

Purpose:

- Provide institutional evidence
- Support infrastructure, inspection, and repair-related analysis

## 4. Supporting Sources

### 4.1 Jan Soochna Rajasthan

Use where school-level or locality-level information relevant to the project
is publicly available.

Potential information:

- Public service/facility information
- Administrative information
- Other school-relevant public records

### 4.2 Rajasthan Sampark

Use where publicly accessible complaint-related information can be reliably
associated with a school.

Potential information:

- Complaint/reference identifier
- Complaint subject
- Date
- Status, when available
- School/location information
- Source URL


### 4.3 Public News / Web Reports

Selected public reports may provide evidence of:

- Infrastructure problems
- School incidents
- Complaints
- Repair delays
- Other publicly reported school-level issues

Required information:

- School name
- Location, when available
- Claim/report text
- Publication date
- Publisher/source
- URL

News reports must not automatically be treated as independent evidence.
Reports derived from the same underlying source should be identified where
possible.

## 5. Common Fields

Where applicable, the acquisition pipeline should preserve:

- Original source name
- Original school name
- UDISE code
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
transformation.

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

A source does not need to provide all required information. Different sources
are expected to complement each other.


## 7. Data Acquisition Principle

The system should distinguish between:

- Data successfully retrieved
- Data successfully retrieved with no matching records
- Partial retrieval
- Retrieval failure
- Information not provided by the source

A retrieval failure must never be interpreted as absence of evidence.
