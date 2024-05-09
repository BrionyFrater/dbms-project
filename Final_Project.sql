CREATE DATABASE IF NOT EXISTS Project;
USE Project;

CREATE TABLE Account (
    uid INT PRIMARY KEY,
	fname VARCHAR(50),
    lname VARCHAR(50),
    phoneNum VARCHAR(15),
    address VARCHAR(255),
    user_role VARCHAR(50),
    adminid INT,
    accountpassword VARCHAR(100)
);

CREATE TABLE Admin (
	uid INT,
    adminid INT PRIMARY KEY,
    dateCreated DATETIME,
    foreign key (uid) REFERENCES Account(uid)
);

CREATE TABLE CreateCrse (
    adminid INT,
    cid INT PRIMARY KEY,
    dateCreated DATE,
    FOREIGN KEY (adminid) REFERENCES Admin(adminid)
);

CREATE TABLE Course (
    cid CHAR(8) PRIMARY KEY,
    cname VARCHAR(255),
    dateCreated DATETIME
);

CREATE TABLE Student (
    stud_id INT PRIMARY KEY,
    uid INT,
    address VARCHAR(255),
    password CHAR(16),
    foreign key (uid) REFERENCES Account(uid)
);

CREATE TABLE Enrol (
    cid CHAR(8),
    uid INT,
    grade INT,
    PRIMARY KEY (cid, uid),
    FOREIGN KEY (cid) REFERENCES Course(cid),
    FOREIGN KEY (uid) REFERENCES Student(uid)
);

CREATE TABLE Lecturer (
    lec_id INT PRIMARY KEY,
    uid INT,
    department VARCHAR(255),
    lecpassword char(10),
    foreign key (uid) REFERENCES Account(uid)
);

CREATE TABLE Component (
    comp_id INT,
    cid CHAR(8),
    compType VARCHAR(30),
    PRIMARY KEY (comp_id, cid),
    FOREIGN KEY (cid) REFERENCES Course(cid)
);

CREATE TABLE Event (
    eid INT PRIMARY KEY,
    cid CHAR(8),
    comp_id INT,
    name VARCHAR(255),
    description TEXT,
    dateCreated DATE,
    dueDate DATE,
    FOREIGN KEY (cid) REFERENCES Course(cid),
    foreign key (comp_id, cid) references Component(comp_id, cid)
);

CREATE TABLE Forum (
    fid INT PRIMARY KEY,
    cid CHAR(8),
    comp_id INT,
    name VARCHAR(255),
    dateCreated DATE,
    FOREIGN KEY (cid) REFERENCES Course(cid),
    foreign key (comp_id, cid) references Component(comp_id, cid)
);

CREATE TABLE Thread (
    tid INT PRIMARY KEY,
    fid INT,
    title VARCHAR(255),
    content TEXT,
    FOREIGN KEY (fid) REFERENCES Forum(fid)
);

CREATE TABLE Section (
    comp_id INT,
    cid CHAR(8),
    secName VARCHAR(255),
    PRIMARY KEY (comp_id, cid),
    FOREIGN KEY (comp_id, cid) REFERENCES Component(comp_id, cid)
);

CREATE TABLE Assignment (
    comp_id INT,
    cid CHAR(8),
    dueDate DATE,
    assignmentName VARCHAR(50),
    description TEXT,
    instructionsFile VARCHAR(50),
    PRIMARY KEY (comp_id, cid),
    FOREIGN KEY (comp_id, cid) REFERENCES Component(comp_id, cid)
);

CREATE TABLE Submit (
    comp_id INT,
    cid CHAR(8),
    uid INT,
    grade FLOAT,
    assignmentFile VARCHAR(50),
    PRIMARY KEY (comp_id, cid, uid),
    FOREIGN KEY (comp_id, cid) REFERENCES Component(comp_id, cid),
    FOREIGN KEY (uid) REFERENCES Student(uid)
);

CREATE TABLE Member (
    uid INT PRIMARY KEY,
    type CHAR
);

CREATE TABLE Assigned (
    cid CHAR(8),
    uid INT,
    FOREIGN KEY (cid) REFERENCES Course(cid),
    FOREIGN KEY (uid) REFERENCES Member(uid)
);

CREATE TABLE ModifySection (
    uid INT,
    comp_id INT,
    cid CHAR(8),
    FOREIGN KEY (uid) REFERENCES Member(uid),
    FOREIGN KEY (comp_id, cid) REFERENCES Section(comp_id, cid)
);

CREATE TABLE SectionItems (
    item_id INT PRIMARY KEY,
    name VARCHAR(255),
    type VARCHAR(255),
    comp_id INT,
    FOREIGN KEY (comp_id) REFERENCES Component(comp_id)
);
