CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    password TEXT
);

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

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    exercise_id INTEGER REFERENCES exercises,
    comment TEXT
);

CREATE TABLE relations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    friend_id INTEGER REFERENCES users
);

CREATE TABLE requests (
    id SERIAL PRIMARY KEY,
    requestor INTEGER REFERENCES users,
    receiver INTEGER REFERENCES users
);