-- CyberShield Database Schema
-- MySQL 8.0+

CREATE DATABASE IF NOT EXISTS cybershield;
USE cybershield;

-- Users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    role VARCHAR(20) DEFAULT 'student',
    avatar VARCHAR(255) DEFAULT 'default_avatar.png',
    bio TEXT,
    organization VARCHAR(150),
    country VARCHAR(50) DEFAULT 'India',
    is_active BOOLEAN DEFAULT TRUE,
    is_email_verified BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME NULL,
    password_reset_token VARCHAR(255),
    password_reset_expires DATETIME,
    INDEX idx_username (username),
    INDEX idx_email (email)
);

-- Courses table
CREATE TABLE courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    description TEXT NOT NULL,
    level VARCHAR(20) NOT NULL,
    category VARCHAR(50) NOT NULL,
    thumbnail VARCHAR(255) DEFAULT 'default_course.png',
    duration_minutes INT DEFAULT 30,
    lessons_count INT DEFAULT 5,
    instructor_id INT,
    is_published BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_level (level),
    INDEX idx_category (category),
    INDEX idx_published (is_published)
);

-- Course progress table
CREATE TABLE course_progress (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    course_id INT NOT NULL,
    current_lesson INT DEFAULT 1,
    total_lessons INT DEFAULT 5,
    is_completed BOOLEAN DEFAULT FALSE,
    points INT DEFAULT 0,
    started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME NULL,
    last_accessed DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_course (user_id, course_id)
);

-- Quiz questions table
CREATE TABLE quiz_questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question TEXT NOT NULL,
    option_a VARCHAR(200) NOT NULL,
    option_b VARCHAR(200) NOT NULL,
    option_c VARCHAR(200) NOT NULL,
    option_d VARCHAR(200) NOT NULL,
    correct_option VARCHAR(1) NOT NULL,
    difficulty VARCHAR(20) NOT NULL,
    category VARCHAR(50) NOT NULL,
    explanation TEXT,
    points INT DEFAULT 10,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_difficulty (difficulty),
    INDEX idx_category (category),
    INDEX idx_active (is_active)
);

-- Quiz scores table
CREATE TABLE quiz_scores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    question_id INT NOT NULL,
    selected_option VARCHAR(1) NOT NULL,
    is_correct BOOLEAN NOT NULL,
    points INT DEFAULT 0,
    time_taken_seconds INT,
    submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES quiz_questions(id) ON DELETE CASCADE,
    INDEX idx_user (user_id),
    INDEX idx_submitted (submitted_at)
);

-- Phishing cases table
CREATE TABLE phishing_cases (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    email_content TEXT,
    email_sender VARCHAR(200),
    email_subject VARCHAR(255),
    url_detected VARCHAR(500),
    is_phishing BOOLEAN NOT NULL,
    risk_score FLOAT NOT NULL,
    detection_reasons TEXT,
    user_triggered BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user (user_id),
    INDEX idx_phishing (is_phishing),
    INDEX idx_created (created_at)
);

-- Certificates table
CREATE TABLE certificates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    certificate_type VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    course_id INT,
    quiz_score_id INT,
    score FLOAT,
    points INT DEFAULT 0,
    certificate_number VARCHAR(50) UNIQUE NOT NULL,
    file_path VARCHAR(255),
    issued_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    expires_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE SET NULL,
    INDEX idx_user (user_id),
    INDEX idx_issued (issued_at)
);

-- Reports table
CREATE TABLE reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    report_type VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    file_path VARCHAR(255),
    generated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user (user_id),
    INDEX idx_generated (generated_at)
);

-- Insert sample courses
INSERT INTO courses (title, description, level, category, duration_minutes, lessons_count) VALUES
('Phishing Email Detection', 'Learn to identify and detect phishing emails with advanced techniques', 'beginner', 'phishing', 30, 5),
('Password Security Fundamentals', 'Master password strength, encryption, and security best practices', 'beginner', 'password', 25, 4),
('Network Security Basics', 'Understanding TCP/IP, DNS, and network protocols', 'beginner', 'network', 40, 6),
('Advanced Phishing Attack Prevention', 'Deep dive into sophisticated phishing attacks and prevention', 'intermediate', 'phishing', 50, 8),
('Password Cracking & Defense', 'Learn how passwords are cracked and how to defend against it', 'intermediate', 'password', 45, 7),
('Malware Analysis Essentials', 'Introduction to malware types, detection, and analysis', 'intermediate', 'malware', 55, 9),
('Enterprise Security Architecture', 'Designing secure systems for large organizations', 'advanced', 'general', 60, 10),
('Zero-Day Vulnerability Research', 'Advanced techniques in vulnerability discovery', 'advanced', 'malware', 70, 12);

-- Insert sample quiz questions
INSERT INTO quiz_questions (question, option_a, option_b, option_c, option_d, correct_option, difficulty, category, points, explanation) VALUES
('What is the primary indicator of a phishing email?', 'Professional logo', 'Request for sensitive information urgently', 'Clear subject line', 'From a known company'),
('Which password is strongest?', 'password123', 'John1990', 'Tr0ub4dor&3', 'abc123'),
('What does DNS stand for?', 'Digital Name System', 'Domain Name System', 'Data Network Service', 'Direct Name Server'),
('What is the first step in TCP 3-way handshake?', 'ACK', 'FIN', 'SYN', 'SYN-ACK'),
('Which HTTP status code indicates success?', '404', '500', '200', '403');

-- Create admin user (password: admin123)
INSERT INTO users (username, email, password_hash, first_name, last_name, role, is_email_verified) VALUES
('admin', 'admin@cybershield.platform', 'QiYy9sQPmPFkKLvN8rT2wX6zB4cD0eF1gH3iJ5kL7mN9oP', 'Admin', 'User', 'admin', TRUE);

-- Commit
COMMIT;