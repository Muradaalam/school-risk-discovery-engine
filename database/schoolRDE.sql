CREATE DATABASE schoolRDE;
use schoolRDE;

#1. school : has the datails of school#
CREATE TABLE school(
id int NOT NULL AUTO_INCREMENT,
school_id varchar(50) NOT NULL,
udise_code varchar(20) ,
school_name varchar(100) NOT NULL,
state varchar(30),
district varchar(50),
block varchar(50),
latitude decimal(10,7),
longitude decimal(10,7),
school_type varchar(50) ,
management_type varchar(50),
created_on timestamp DEFAULT CURRENT_TIMESTAMP,
created_by varchar(50) DEFAULT (current_user()),
updated_on timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
updated_by varchar(50) DEFAULT (current_user()),
PRIMARY KEY (id),
UNIQUE KEY school_id (school_id))
ENGINE=InnoDB
AUTO_INCREMENT=1000000
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO school (school_id, udise_code, school_name, state, district, block,latitude, longitude, school_type, management_type) VALUES
('SCH-11234501', '08050502511', 'adarsh govt sr sec school', 'Rajasthan', 'Churu', 'Churu', NULL, NULL, 'Senior Secondary', 'Private aided'),
('SCH-12030002', '08050212702', 'Seth Ramvilas Government School', 'Rajasthan', 'Sikar', 'Fatehpur', NULL, NULL, 'Senior Secondary', 'Government'),
('SCH-15143003', '08050213408', 'Govt Bagla Senior Secondary School', 'Rajasthan', 'Bikaner', 'Nokha', NULL, NULL, 'Senior Secondary', 'Government');

#---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---#

#2 issue tables
#2.1 A master table containing issue types

CREATE TABLE issue_type(
id int NOT NULL AUTO_INCREMENT,
issue_type varchar(30) NOT NULL,
description varchar(100) DEFAULT NULL,
PRIMARY KEY (id),
UNIQUE KEY issue_type (issue_type))
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


INSERT INTO issue_type (id, issue_type, description) VALUES
(1, 'BUILDING', 'Structural damage to the school building'),
(2, 'CLASSROOM', 'Classroom damage or maintenance issues'),
(3, 'BOUNDARY_WALL', 'Damaged or missing boundary wall'),
(4, 'DRINKING_WATER', 'Drinking water availability or quality issues'),
(5, 'ELECTRICITY', 'Electrical supply or wiring problems'),
(6, 'TOILET', 'Toilet or sanitation problems'),
(7, 'ROOF', 'Roof damage or leakage'),
(8, 'ROAD_ACCESS', 'Problems accessing the school by road'),
(9, 'MID_DAY_MEAL_AVAILABILITY', 'Issues related to dry ration availability and distribution'),
(10, 'MID_DAY_MEAL_QUALITY_SAFETY', 'Issues related to food quality, nutrition and kitchen hygiene'),
(11, 'MID_DAY_MEAL_MANAGEMENT', 'Issues related to kitchen infrastructure, cooking staff'),
(12, 'OTHER', 'Other infrastructure problems');


#2.2 A master table containing issue statuses
CREATE TABLE issue_status( 
id int NOT NULL AUTO_INCREMENT,
status varchar(30) NOT NULL,
description VARCHAR(100),
PRIMARY KEY (id),
UNIQUE KEY status (status)) 
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO issue_status (id, status, description) VALUES
(1, 'ACTIVE', 'Issue exists and requires attention'),
(2, 'UNDER_REPAIR', 'Repair work is currently in progress'),
(3, 'RESOLVED', 'Issue is reported as resolved but verification is pending'),
(4, 'VERIFIED', 'Issue resolution has been verified using reliable evidence'),
(5, 'UNKNOWN', 'Insufficient evidence to determine the current issue status');

#2.3 issue : contains actual issue details related to schools
CREATE TABLE issue(
id int NOT NULL AUTO_INCREMENT,
school_id int NOT NULL,
issue_type_id int NOT NULL,
status_id int NOT NULL,
first_detected date,
last_updated datetime,
resolved_at datetime,
created_on timestamp NULL DEFAULT CURRENT_TIMESTAMP,
created_by varchar(50) DEFAULT (current_user()),
updated_on timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
updated_by varchar(50) DEFAULT (current_user()),
PRIMARY KEY (id),
KEY school_id (school_id),
KEY issue_type_id (issue_type_id),
KEY status_id (status_id),
CONSTRAINT issue_ibfk_1 FOREIGN KEY (school_id) REFERENCES school (id),
CONSTRAINT issue_ibfk_2 FOREIGN KEY (issue_type_id) REFERENCES issue_type (id),
CONSTRAINT issue_ibfk_3 FOREIGN KEY (status_id) REFERENCES issue_status (id))
ENGINE=InnoDB
AUTO_INCREMENT=2000000
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO issue (school_id, issue_type_id, status_id, first_detected, last_updated, resolved_at) VALUES
(1000000, 1, 1, '2025-07-15', '2025-08-10 10:30:00', NULL),
(1000001, 2, 2, '2025-08-01', '2025-08-20 12:00:00', NULL),
(1000002, 3, 5, '2025-09-05', '2025-09-12 11:00:00', NULL),
(1000002, 4, 1, '2025-09-05', '2025-09-12 11:00:00', NULL);
#---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---#

#3 Event
#3.1 even_type : contains master data related to event types
CREATE TABLE event_type (
id int NOT NULL AUTO_INCREMENT,
event_type varchar(30) NOT NULL,
description varchar(100) DEFAULT NULL,
PRIMARY KEY (id),
UNIQUE KEY event_type (event_type))
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO event_type (id, event_type, description) VALUES
(1, 'INFRASTRUCTURE_REVIEW', 'Review of school infrastructure and facilities'),
(2, 'ENVIRONMENT', 'Environmental activities such as tree plantation'),
(3, 'SPORTS', 'Sports activities and competitions'),
(4, 'HEALTH', 'Health checkups and health awareness programmes'),
(5, 'OTHER', 'Other school-related events');

#3.2 event : conatains event related data
CREATE TABLE event (
id int NOT NULL AUTO_INCREMENT,
school_id int NOT NULL,
event_type_id int NOT NULL,
detailed_description varchar(150),
event_date date DEFAULT NULL,
location varchar(50) DEFAULT NULL,
created_on timestamp NULL DEFAULT CURRENT_TIMESTAMP,
created_by varchar(50) DEFAULT (current_user()),
updated_on timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
updated_by varchar(50) DEFAULT (current_user()),
PRIMARY KEY (id),
KEY idx_event_school_id (school_id),
KEY idx_event_type_id (event_type_id),
CONSTRAINT fk_event_school FOREIGN KEY (school_id) REFERENCES school (id),
CONSTRAINT fk_event_type FOREIGN KEY (event_type_id) REFERENCES event_type (id))
ENGINE=InnoDB  
AUTO_INCREMENT=3000000
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO event (school_id, event_type_id, detailed_description, event_date, location) VALUES
(1000000, 1, 'Inspection of school building and infrastructure facilities', '2026-10-05', 'School Campus'),
(1000000, 2, 'Tree plantation drive organized by students and teachers', '2026-07-15', 'School Garden'),
(1000001, 3, 'Annual sports competition for school students', '2026-08-20', 'School Playground'),
(1000001, 4, 'Health checkup and health awareness programme for students', '2026-09-10', 'School Campus'),
(1000002, 1, 'Review of classroom conditions and drinking water facilities', '2026-09-18', 'School Campus'),
(1000002, 5, 'School community meeting to discuss development activities', '2026-10-10', 'School Hall');
#---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---#

