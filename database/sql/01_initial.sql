create table tokens (
    id unique integer,
    token unique varchar(255),
    course varchar(255)
    used boolean,
    used_by varchar(255),
    used_date date
);