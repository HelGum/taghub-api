CREATE DATABASE taghub_task;
\c taghub_task;

CREATE TABLE users(
    id SERIAL NOT NULL, 
    username VARCHAR(50),
    email VARCHAR(100),
    password VARCHAR(100),
    UNIQUE(username),
    UNIQUE(email),
    PRIMARY KEY(id)
);