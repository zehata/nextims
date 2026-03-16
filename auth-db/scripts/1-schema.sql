CREATE TABLE users (
    hashed_username TEXT PRIMARY KEY
    hashed_password TEXT NOT NULL
    user_role TEXT NOT NULL
);

CREATE TABLE apps (
    hashed_client_id TEXT PRIMARY KEY
    hashed_client_secret TEXT NOT NULL
);