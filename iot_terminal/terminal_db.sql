-- 'DB IoT Terminal'
-- 1. database creation
CREATE DATABASE terminal;

USE terminal;

CREATE TABLE employee(
ID_employee int not null AUTO_INCREMENT,
`name` varchar(200) not null,
primary key (ID_employee)
);

CREATE TABLE fingerprint(
ID_fingerprint int not null AUTO_INCREMENT,
ID_employee int not null,
ID_sensor_index int,
primary key (ID_fingerprint),
CONSTRAINT fk_employee_fingerprint FOREIGN KEY (ID_employee) REFERENCES employee(ID_employee)
);

CREATE TABLE attendance(
ID_attendance int not null AUTO_INCREMENT,
ID_employee int not null,
`timestamp` timestamp not null,
primary key (ID_attendance),
CONSTRAINT fk_attendance_fingerprint FOREIGN KEY (ID_employee) REFERENCES employee(ID_employee)
);

-- 2. user creation
GRANT ALL PRIVILEGES ON terminal.* TO 'assiduidade'@'localhost' IDENTIFIED BY 'password';
FLUSH PRIVILEGES;
