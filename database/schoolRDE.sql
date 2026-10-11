CREATE TABLE school (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    school_id VARCHAR(50) NOT NULL UNIQUE,
    udise_code VARCHAR(20),
    school_name VARCHAR(100) NOT NULL,
    state VARCHAR(30),
    district VARCHAR(50),
    block VARCHAR(100),
    latitude DECIMAL(10, 7),
    longitude DECIMAL(10, 7),
    school_type VARCHAR(50),
    management_type VARCHAR(100),
    created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    createdBy VARCHAR(100) DEFAULT (CURRENT_USER()),
    updated_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    updatedBy VARCHAR(100) DEFAULT (CURRENT_USER())
);

INSERT INTO school (school_id, udise_code, school_name, state, district, block,latitude, longitude, school_type, management_type)
VALUES
('SCH-11234501', '08050502511', 'adarsh govt sr sec school', 'Rajasthan', 'Churu', 'Churu', NULL, NULL, 'Senior Secondary', 'Private aided'),
('SCH-12030002', '08050212702', 'Seth Ramvilas Government School', 'Rajasthan', 'Sikar', 'Fatehpur', NULL, NULL, 'Senior Secondary', 'Government'),
('SCH-15143003', '08050213408', 'Govt Bagla Senior Secondary School', 'Rajasthan', 'Bikaner', 'Nokha', NULL, NULL, 'Senior Secondary', 'Government');