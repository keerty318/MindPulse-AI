


CREATE DATABASE IF NOT EXISTS mindpulseai;

USE mindpulseai;

-- Drop tables if they already exist

DROP TABLE IF EXISTS assessments;
DROP TABLE IF EXISTS users;


-- Users Table


CREATE TABLE users (

    id INT AUTO_INCREMENT PRIMARY KEY,

    full_name VARCHAR(100) NOT NULL,

    username VARCHAR(50) UNIQUE NOT NULL,

    email VARCHAR(100) UNIQUE NOT NULL,

    password VARCHAR(255) NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);


-- Assessments Table


CREATE TABLE assessments (

    assessment_id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NOT NULL,

    age INT,

    gender TINYINT,

    study_hours FLOAT,

    assignments_completed INT,

    attendance_percentage FLOAT,

    final_grade INT,

    sleep_hours FLOAT,

    stress FLOAT,

    focus FLOAT,

    phone_usage_hours FLOAT,

    social_media FLOAT,

    youtube FLOAT,

    gaming FLOAT,

    breaks_per_day INT,

    exercise_minutes INT,

    coffee INT,

    productivity_score FLOAT,

    productivity_status VARCHAR(20),

    wellness_score INT,

    burnout_risk INT,

    burnout_status VARCHAR(20),

    distraction_index INT,

    distraction_status VARCHAR(30),

    focus_leakage INT,

    digital_profile VARCHAR(50),

    top_source VARCHAR(30),

    potential_gain INT,

    potential_productivity INT,

    strongest_attribute VARCHAR(50),

    assessment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE

);

