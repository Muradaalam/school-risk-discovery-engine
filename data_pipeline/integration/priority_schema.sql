
CREATE TABLE IF NOT EXISTS srde_report_priorities (
    entity_id VARCHAR(50) NOT NULL,
    school_fk INT NOT NULL,
    priority_rank INT NOT NULL,
    priority_score TINYINT UNSIGNED NOT NULL,
    priority_level VARCHAR(10) NOT NULL,
    identity_status VARCHAR(50) NOT NULL,
    issue_state VARCHAR(50) NOT NULL,
    incident_groups INT NOT NULL DEFAULT 0,
    evidence_events INT NOT NULL DEFAULT 0,
    latest_evidence_date DATE DEFAULT NULL,
    evidence_references JSON NOT NULL,
    explanation TEXT NOT NULL,
    calculated_at DATETIME DEFAULT NULL,
    active TINYINT(1) NOT NULL DEFAULT 1,
    imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (entity_id),
    KEY idx_srde_report_queue (active, priority_rank),
    KEY idx_srde_report_school (school_fk),
    CONSTRAINT fk_srde_report_school FOREIGN KEY (school_fk) REFERENCES school(id),
    CONSTRAINT chk_srde_priority_score CHECK (priority_score BETWEEN 0 AND 100)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
