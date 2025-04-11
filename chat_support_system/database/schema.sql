-- Admins table
CREATE TABLE admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL
);

-- Agents table
CREATE TABLE agents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    is_available BOOLEAN DEFAULT TRUE
);

-- Messages table (for future persistent storage)
CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sender VARCHAR(100) NOT NULL,
    receiver VARCHAR(100),
    content TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
