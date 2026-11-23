SchoolRDE Database Schema

Database Name: schoolRDE
Database: MySQL

Tables
school – Stores school details, identification, location, school type and management information
columns : id, school_id, udise_code, school_name, state, district, block, latitude, longitude, school_type, management_type, created_on, created_by, updated_on, updated_by

issue_type – Stores master categories of school infrastructure issues
type : BUILDING, CLASSROOM, BOUNDARY_WALL, DRINKING_WATER, ELECTRICITY, TOILET, ROOF, ROAD_ACCESS, MID_DAY_MEAL_AVAILABILITY, MID_DAY_MEAL_QUALITY_SAFETY, MID_DAY_MEAL_MANAGEMENT, OTHER

issue_status – Stores statuses of reported issues
status : ACTIVE, UNDER_REPAIR, RESOLVED, VERIFIED, UNKNOWN

issue – Stores infrastructure issues associated with schools, including issue type, status and detection dates
columns : id, school_id, issue_type_id, status_id, first_detected, last_updated, resolved_at, created_on, created_by, updated_on, updated_by

event_type – Stores categories of school-related events
types : INFRASTRUCTURE_REVIEW, ENVIRONMENT, SPORTS, HEALTH, OTHER

event – Stores school events and related details
columns : id, school_id, event_type_id, detailed_description, event_date, location, created_on, created_by, updated_on, updated_by

project – Stores repair and new construction project details, costs, status and timelines
columns : id, issue_id, project_type, project_description, project_status, estimated_cost, actual_cost, start_date, expected_completion_date, actual_completion_date, remarks, created_on, created_by, updated_on, updated_by

tender_status – Stores master tender statuses
status : DRAFT, PUBLISHED, OPEN, CLOSED, UNDER_EVALUATION, AWARDED, CANCELLED, COMPLETED, OTHER

tender – Stores tender details associated with infrastructure projects and contractor information
columns : id, project_id, tender_number, tender_title, tender_description, tender_status_id, estimated_amount, awarded_amount, publication_date, submission_deadline, award_date, contractor_name, contract_start_date, contract_end_date, created_on, created_by, updated_on, updated_by

inspection – Stores school inspection details and inspector information
columns : id, school_id, inspection_date, inspection_type, remarks, inspector_name, created_on, created_by, updated_on, updated_by

source_name – Stores categories of information sources
names : UDISE_PLUS, SCHOOL_INSPECTION, NEWSPAPER, SCHOOL_RECORD, OTHER

source – Stores information for documents, URLs associated with schools
columns : id, school_id, source_name_id, source_url, publication_date, created_on, created_by, updated_on, updated_by

priority_snapshot – Stores historical school priority scores and issue statistics
columns : id, school_id, snapshot_date, priority_score, active_issues, under_resol_issues, resolved_issues, created_on, created_by, updated_on, updated_by

object_category – Stores categories of entities associated with documents
objectName : SCHOOL, ISSUE, EVENT, PROJECT, TENDER, INSPECTION

document – Stores document metadata, file paths, these documents are evidence associated with schools, issues, events, projects, tenders and inspections
(all these six entities are treated as objectId in document table)
columns : id, object_id, object_category_id, source_id, document_name, doc_path, description, created_on, created_by, updated_on, updated_by 

Relationships
school -> issue (One-to-Many)
issue -> issue_type (Many-to-One)
issue -> issue_status (Many-to-One)
school -> event (One-to-Many)
event -> event_type (Many-to-One)
issue -> project (One-to-Many)
project -> tender (One-to-Many)
tender -> tender_status (Many-to-One)
school -> inspection (One-to-Many)
school -> source (One-to-Many)
source -> source_name (Many-to-One)
school -> priority_snapshot (One-to-Many)
document -> object_category  (Many-to-One)
document -> source (Many-to-One)
document -> school (Many-to-One)
document -> issue (Many-to-One)
document -> event (Many-to-One)
document -> project (Many-to-One)
document -> tender (Many-to-One)
document -> inspection (Many-to-One)

Refer to /database/schoolRDE.sql for the complete database creation scripts, table definitions, constraints, master data and sample records.
