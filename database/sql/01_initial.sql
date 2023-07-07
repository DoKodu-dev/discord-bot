create table tokens (
    id integer primary key unique,
    token varchar(255) unique,
    course varchar(255),
    used boolean,
    used_by varchar(255),
    used_date date
);