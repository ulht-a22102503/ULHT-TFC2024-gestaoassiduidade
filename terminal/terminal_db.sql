-- 'DB IoT Terminal'
-- 1. database creation
CREATE DATABASE terminal;

USE terminal;

CREATE TABLE shift(
    ID_shift int not null AUTO_INCREMENT,
    time_begin TIME(4) not null, -- HH:MM
    break_begin TIME(4),
    break_end TIME(4),
    time_end TIME(4) not null,
    primary key (ID_shift)
);

CREATE TABLE job_role(
    ID_role char(4) not null,
    descript char(50) not null,
    primary key (ID_role)
);

CREATE TABLE workcode(
    ID_workcode char(4) not null,
    code_type BOOL not null, -- 1 present, 0 missing
    descript char(30) not null,
    primary key (ID_workcode)
);

CREATE TABLE employee(
ID_employee int not null AUTO_INCREMENT,
ID_role char(4) not null,
`name` varchar(200) not null,
primary key (ID_employee),
CONSTRAINT fk_employee_job_role FOREIGN KEY (ID_role) REFERENCES job_role(ID_role)
);

CREATE TABLE credentials(
ID_fingerprint int not null AUTO_INCREMENT,
ID_employee int not null UNIQUE,
ID_sensor_index_main int,
ID_sensor_index_sec int,
pincode char(64),
primary key (ID_fingerprint),
CONSTRAINT fk_credentials_employee FOREIGN KEY (ID_employee) REFERENCES employee(ID_employee)
);

CREATE TABLE attendance(
ID_attendance int not null AUTO_INCREMENT,
ID_employee int not null,
`timestamp` timestamp not null,
primary key (ID_attendance),
CONSTRAINT fk_attendance_fingerprint FOREIGN KEY (ID_employee) REFERENCES employee(ID_employee)
);

CREATE TABLE schedule(
    ID_schedule int not null AUTO_INCREMENT,
    valid_on date not null,
    ID_workcode char(4) not null,
    ID_shift int,
    ID_employee int not null,
    primary key (ID_schedule),
    CONSTRAINT fk_schedule_workcode FOREIGN KEY (ID_workcode) REFERENCES workcode(ID_workcode),
    CONSTRAINT fk_schedule_shift FOREIGN KEY (ID_shift) REFERENCES shift(ID_shift),
    CONSTRAINT fk_schedule_employee FOREIGN KEY (ID_employee) REFERENCES employee(ID_employee)
);

-- 2. user creation
GRANT ALL PRIVILEGES ON terminal.* TO 'assiduidade'@'localhost' IDENTIFIED BY 'password';
FLUSH PRIVILEGES;
