-- Create the database
CREATE DATABASE irs;

-- Switch to the database
USE irs;

-- Create the userid table
CREATE TABLE userid (
    userid VARCHAR(50) NOT NULL PRIMARY KEY,
    uname VARCHAR(50) NOT NULL,
    gender ENUM('M', 'F'),
    contactno VARCHAR(10),
    address VARCHAR(100),
    passhash CHAR(64)  -- Storing hashed passwords (SHA-256 produces a 64-character hash)
);

-- Create the issue table
CREATE TABLE issue (
    issue_id VARCHAR(10) NOT NULL PRIMARY KEY,
    userid VARCHAR(50) NOT NULL,
    title VARCHAR(100) NOT NULL,
    description_ TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status_ ENUM('Open', 'Closed') NOT NULL,
    FOREIGN KEY (userid) REFERENCES userid(userid)
);
