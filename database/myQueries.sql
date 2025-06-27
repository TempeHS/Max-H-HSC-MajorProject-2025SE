

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

CREATE TABLE IF NOT EXISTS saved_recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    recipe_id TEXT NOT NULL,
    title TEXT,
    image TEXT
);

CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    recipe_id INTEGER NOT NULL,
    review TEXT NOT NULL,
    rating INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);