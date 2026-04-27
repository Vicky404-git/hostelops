-- =========================================================================
-- HostelOps Database Schema
-- Focus: Event-Driven Institutional Operations Accountability
-- =========================================================================

-- Create and select the database
CREATE DATABASE IF NOT EXISTS hostelops_db;
USE hostelops_db;

-- -------------------------------------------------------------------------
-- 1. Core Issues Table (Replaces issues.json)
-- Purpose: Stores the current state and metadata of every reported problem.
-- -------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS issues (
    issue_id VARCHAR(20) PRIMARY KEY,       -- e.g., 'ISSUE1', 'ISSUE2'
    student_id VARCHAR(50) NOT NULL,        -- Identifier for the student
    block VARCHAR(50) NOT NULL,             -- e.g., 'Block A (Boys)'
    room VARCHAR(20) NOT NULL,              -- Actual room number or 'Classified'
    issue_type VARCHAR(50) NOT NULL,        -- Category: Water, Electricity, Food, etc.
    description TEXT,                       -- Detailed explanation of the problem
    current_status VARCHAR(50) NOT NULL DEFAULT 'Reported', 
    created_at DATETIME NOT NULL            -- Time the issue was first logged
);

-- -------------------------------------------------------------------------
-- 2. Append-Only Events Table (Replaces events.json)
-- Purpose: The Accountability Layer. Records every status change immutably.
-- -------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS events (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    issue_id VARCHAR(20) NOT NULL,          -- Links directly to the parent issue
    event_desc TEXT NOT NULL,               -- e.g., 'Assigned to Plumber Ram'
    event_time DATETIME NOT NULL,           -- Exact timestamp of the action
    image_path VARCHAR(255) DEFAULT NULL,   -- Local path to uploaded visual proof
    
    -- Constraint: Referential Integrity. 
    -- If an issue is somehow deleted, clear its history to prevent orphaned data.
    CONSTRAINT fk_issue
        FOREIGN KEY (issue_id) 
        REFERENCES issues(issue_id) 
        ON DELETE CASCADE
);

-- -------------------------------------------------------------------------
-- 3. (Optional / Bonus) Users Table
-- Purpose: For DBMS requirements, adding a users table shows proper RBAC
-- (Role-Based Access Control) instead of hardcoded passwords in app.py.
-- -------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    user_id VARCHAR(50) PRIMARY KEY,        -- Student ID or Staff ID
    user_role ENUM('Student', 'Admin', 'Staff') NOT NULL,
    password_hash VARCHAR(255) NOT NULL,    -- Secure password storage
    full_name VARCHAR(100) NOT NULL
);

-- =========================================================================
-- Initial Seed Data (Optional: Run this to test your views before connecting UI)
-- =========================================================================
/*
INSERT INTO issues (issue_id, student_id, block, room, issue_type, description, current_status, created_at)
VALUES 
('ISSUE1', 'STU101', 'Block A (Boys)', '104', 'Electricity', 'Fan is making weird noises', 'Reported', NOW());

INSERT INTO events (issue_id, event_desc, event_time, image_path)
VALUES
('ISSUE1', 'Reported', NOW(), NULL);
*/
