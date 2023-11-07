-- Create Database --
DROP DATABASE IF EXISTS PlanT;
CREATE DATABASE PlanT;
USE PlanT;

-- Create Tables --
SET FOREIGN_KEY_CHECKS = 0;
SET AUTOCOMMIT = 0;

-- Users --
DROP TABLE IF EXISTS Users;
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    display_id VARCHAR(100),
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    phone CHAR(12) NOT NULL,
    username VARCHAR(50) NOT NULL,
    password CHAR(255) NOT NULL
);

-- Events --
DROP TABLE IF EXISTS Events;
CREATE TABLE Events (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    event_name VARCHAR(100),
    event_desc VARCHAR(255),
    date DATE NOT NULL,
    time TIME NOT NULL,
    user_id INT NOT NULL,
    CONSTRAINT Events_ibfk_1
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- Friends --
DROP TABLE IF EXISTS Friends;
CREATE TABLE Friends (
    friend1_id INT,
    friend2_id INT,
    CONSTRAINT Friends_ibfk_1
    FOREIGN KEY (friend1_id) REFERENCES Users(user_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT Friends_ibfk_2
    FOREIGN KEY (friend2_id) REFERENCES Users(user_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);