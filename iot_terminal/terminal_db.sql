#'DB IoT Terminal'
CREATE DATABASE terminal;

USE terminal;

CREATE TABLE fingerprint(
ID_fingerprint int not null AUTO_INCREMENT,
ID_employee int not null,
ID_sensor_index int,
primary key (ID_fingerprint)
);

CREATE TABLE attendance(
ID_attendance int not null AUTO_INCREMENT,
ID_employee int not null,
`timestamp` timestamp not null,
primary key (ID_attendance)
);
