CREATE TABLE exercises (
    id SERIAL PRIMARY KEY,
    type TEXT, 
    date DATE, 
    hours INTEGER, 
    minutes INTEGER, 
    visible INTEGER,
    creator_id INTEGER REFERENCES users,
    created_at TIMESTAMP
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    password TEXT
);
