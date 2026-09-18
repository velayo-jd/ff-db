CREATE DATABASE IF NOT EXISTS ff_db;
USE ff_db;

CREATE TABLE characters (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    arcane VARCHAR(100),
    nationality VARCHAR(50),
    physical_description TEXT
);

CREATE TABLE terminologies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    term VARCHAR(100) NOT NULL,
    term_type VARCHAR(100),
    term_definition TEXT
);