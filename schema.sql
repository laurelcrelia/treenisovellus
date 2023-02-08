CREATE TABLE exercises (
    id SERIAL PRIMARY KEY,
    type TEXT, 
    date DATE, 
    hours INTEGER, 
    minutes INTEGER, 
    visible INTEGER,
    creator_id INTEGER REFERENCES users
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    password TEXT
);
