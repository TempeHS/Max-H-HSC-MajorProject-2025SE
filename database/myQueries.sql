-- database: database.db


--INSERT INTO users (username, password) VALUES ('admin', 'admin123');

CREATE TABLE secure_users_9f (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    totp_secret TEXT,
    twoFA_enabled INTEGER DEFAULT 0
);

ALTER TABLE secure_users_9f
ADD COLUMN email TEXT;

INSERT INTO secure_users_9f (username, password, totp_secret, twoFA_enabled, location)
VALUES ('admin', 'admin123', 'JBSWY3DPEHPK3PXP', 1, 'Sydney');