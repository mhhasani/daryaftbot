CREATE TABLE Student (
    chat_id INTEGER PRIMARY KEY,
    username VARCHAR(255),
    name VARCHAR(255),
    paye INTEGER,
    reshte VARCHAR(100),
    phone VARCHAR(20),
    message_id INTEGER,
    day DATE
);

CREATE TABLE Report (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER NOT NULL,
    lname VARCHAR(255),
    topic VARCHAR(255),
    start_time DATETIME,
    end_time DATETIME,
    FOREIGN KEY (chat_id) REFERENCES Student(chat_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Admin (
    chat_id INTEGER NOT NULL,
    FOREIGN KEY (chat_id) REFERENCES Student(chat_id) ON DELETE CASCADE ON UPDATE CASCADE
);