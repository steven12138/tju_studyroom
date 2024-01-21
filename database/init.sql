GRANT ALL PRIVILEGES ON *.* TO 'studyroom'@'%';
FLUSH PRIVILEGES;

create table studyroom.building
(
    id          bigint auto_increment
        primary key,
    campus_id   bigint       null,
    name        varchar(255) not null,
    mapped_name varchar(255) null,
    constraint UK_oyx9p4qp0ot5mw2vdn1qgax00
        unique (name)
);

create table studyroom.campus
(
    id   bigint auto_increment
        primary key,
    name varchar(255) not null,
    constraint UK_81rhu9trr93hw9082igcywgl8
        unique (name)
);

create table studyroom.room
(
    id          bigint auto_increment
        primary key,
    building_id varchar(255) null,
    name        varchar(255) not null,
    mapped_name varchar(255) null,
    constraint UK_4l8mm4fqoos6fcbx76rvqxer
        unique (name)
);

create table studyroom.status
(
    id            bigint auto_increment
        primary key,
    date          date   null,
    room_id       bigint null,
    session_index int    null
);


