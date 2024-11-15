#'DB IoT Terminal'
CREATE DATABASE terminal;

USE terminal;

CREATE TABLE fingerprints(
ID_employee int not null,
ID_fingerprint int not null,
primary key (ID_employee, ID_fingerprint)
);

CREATE TABLE attendance(
ID_employee int not null,
[timestamp] timestamp not null,
primary key (ID_employee, timestamp)
);