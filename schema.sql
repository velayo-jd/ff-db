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

CREATE TABLE locations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL, -- Central Nu Regional Hospital
    type VARCHAR(50), -- Hospital
    region TEXT, -- Central Nu, near The Medical Recidency
    status VARCHAR(50), -- In Operation, from Phase 1 to Phase 3
    description TEXT -- The largest hospital in Nu, and is one of the last bastions of justice in the series.
                     -- Funded by the goverment and Richoka; they're the golden standard in shifts & medical practices  
);