create table users (
    id serial primary key,
    name varchar(512),
    registration_address varchar(512),
    last_known_location varchar(512)
);

INSERT INTO users (name, registration_address, last_known_location) VALUES
 ('Alice Smith', 'New York', 'New York'),
 ('Bob Johnson', 'Los Angeles', 'New York'),
 ('Charlie Brown', 'New York', 'Chicago'),
 ('David Williams', 'Chicago', 'New York'),
 ('Emily Davis', 'New York', 'New York'),
 ('Franklin Garcia', 'New York', 'New York'),
 ('George Harris', 'New York', 'New York'),
 ('Hannah Lee', 'New York', 'New York'),
 ('Ian Taylor', 'New York', 'New York'),
 ('Jessica White', 'New York', 'New York');