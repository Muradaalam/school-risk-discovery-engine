# SchoolRDE Database Schema

**Database Name:** `schoolRDE`  
**Database:** MySQL

## Tables

### 1. school
Stores school details, identification, location, school type and management information.

**Columns:**  
`id`, `school_id`, `udise_code`, `school_name`, `state`, `district`, `block`, `latitude`, `longitude`, `school_type`, `management_type`, `created_on`, `created_by`, `updated_on`, `updated_by`

### 2. issue_type
Stores master categories of school infrastructure issues.

**Types values:**  
`BUILDING`, `CLASSROOM`, `BOUNDARY_WALL`, `DRINKING_WATER`, `ELECTRICITY`, `TOILET`, `ROOF`, `ROAD_ACCESS`, `MID_DAY_MEAL_AVAILABILITY`, `MID_DAY_MEAL_QUALITY_SAFETY`, `MID_DAY_MEAL_MANAGEMENT`, `OTHER`

### 3. issue_status
Stores statuses of reported issues.

**Status values:**  
`ACTIVE`, `UNDER_REPAIR`, `RESOLVED`, `VERIFIED`, `UNKNOWN`

### 4. issue
Stores infrastructure issues associated with schools, including issue type, status and detection dates.

**Columns:**  
`id`, `school_id`, `issue_type_id`, `status_id`, `first_detected`, `last_updated`, `resolved_at`, `created_on`, `created_by`, `updated_on`, `updated_by`

### 5. event_type
Stores categories of school-related events.

**event Type values:**  
`INFRASTRUCTURE_REVIEW`, `ENVIRONMENT`, `SPORTS`, `HEALTH`, `OTHER`

### 6. event
Stores school events and related details.

**Columns:**  
`id`, `school_id`, `event_type_id`, `detailed_description`, `event_date`, `location`, `created_on`, `created_by`, `updated_on`, `updated_by`

### 7. project
Stores repair and new construction project details, costs, status and timelines.

**Columns:**  
`id`, `issue_id`, `project_type`, `project_description`, `project_status`, `estimated_cost`, `actual_cost`, `start_date`, `expected_completion_date`, `actual_completion_date`, `remarks`, `created_on`, `created_by`, `updated_on`, `updated_by`

### 8. tender_status
Stores master tender statuses.

**Status values:**  
`DRAFT`, `PUBLISHED`, `OPEN`, `CLOSED`, `UNDER_EVALUATION`, `AWARDED`, `CANCELLED`, `COMPLETED`, `OTHER`

### 9. tender
Stores tender details associated with infrastructure projects and contractor information.

**Columns:**  
`id`, `project_id`, `tender_number`, `tender_title`, `tender_description`, `tender_status_id`, `estimated_amount`, `awarded_amount`, `publication_date`, `submission_deadline`, `award_date`, `contractor_name`, `contract_start_date`, `contract_end_date`, `created_on`, `created_by`, `updated_on`, `updated_by`

### 10. inspection
Stores school inspection details and inspector information.

**Columns:**  
`id`, `school_id`, `inspection_date`, `inspection_type`, `remarks`, `inspector_name`, `created_on`, `created_by`, `updated_on`, `updated_by`

### 11. source_name
Stores categories of information sources.

**Source Names values:**  
`UDISE_PLUS`, `SCHOOL_INSPECTION`, `NEWSPAPER`, `SCHOOL_RECORD`, `OTHER`

### 12. source
Stores information for documents, URLs associated with schools.

**Columns:**  
`id`, `school_id`, `source_name_id`, `source_url`, `publication_date`, `created_on`, `created_by`, `updated_on`, `updated_by`

### 13. priority_snapshot
Stores historical school priority scores and issue statistics.

**Columns:**  
`id`, `school_id`, `snapshot_date`, `priority_score`, `active_issues`, `under_resol_issues`, `resolved_issues`, `created_on`, `created_by`, `updated_on`, `updated_by`

### 14. object_category
Stores categories of entities associated with documents.

**Object Names:**  
`SCHOOL`, `ISSUE`, `EVENT`, `PROJECT`, `TENDER`, `INSPECTION`

### 15. document
Stores document metadata, file paths. These documents are evidence associated with schools, issues, events, projects, tenders and inspections.

All these six entities are treated as `objectId` in the document table.

**Columns:**  
`id`, `object_id`, `object_category_id`, `source_id`, `document_name`, `doc_path`, `description`, `created_on`, `created_by`, `updated_on`, `updated_by`

## Relationships

- school -> issue (One-to-Many)
- issue -> issue_type (Many-to-One)
- issue -> issue_status (Many-to-One)
- school -> event (One-to-Many)
- event -> event_type (Many-to-One)
- issue -> project (One-to-Many)
- project -> tender (One-to-Many)
- tender -> tender_status (Many-to-One)
- school -> inspection (One-to-Many)
- school -> source (One-to-Many)
- source -> source_name (Many-to-One)
- school -> priority_snapshot (One-to-Many)
- document -> object_category (Many-to-One)
- document -> source (Many-to-One)
- document -> school (Many-to-One)
- document -> issue (Many-to-One)
- document -> event (Many-to-One)
- document -> project (Many-to-One)
- document -> tender (Many-to-One)
- document -> inspection (Many-to-One)


## Database Creation Script

Refer to `/database/schoolRDE.sql` for the complete database creation scripts, table definitions, constraints, master data and sample records.
