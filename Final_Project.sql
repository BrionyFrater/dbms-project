CREATE DATABASE IF NOT EXISTS Project;
USE Project;

CREATE TABLE Admin (
    adminid INT PRIMARY KEY,
    fname VARCHAR(50),
    lname VARCHAR(50)
);

CREATE TABLE Account (
    uid INT PRIMARY KEY,
    adminid INT,
    password VARCHAR(100),
    FOREIGN KEY (adminid) REFERENCES Admin(adminid)
);

CREATE TABLE User (
    uid INT PRIMARY KEY,
    fname VARCHAR(50),
    name VARCHAR(50),
    phoneNum VARCHAR(15),
    address VARCHAR(255)
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
    uid INT PRIMARY KEY,
    password CHAR(16)
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
    uid INT PRIMARY KEY,
    password CHAR(16)
);

CREATE TABLE Event (
    eid INT PRIMARY KEY,
    cid CHAR(8),
    name VARCHAR(255),
    description TEXT,
    dateCreated DATE,
    dueDate DATE,
    FOREIGN KEY (cid) REFERENCES Course(cid)
);

CREATE TABLE Forum (
    fid INT PRIMARY KEY,
    cid CHAR(8),
    name VARCHAR(255),
    dateCreated DATE,
    FOREIGN KEY (cid) REFERENCES Course(cid)
);

CREATE TABLE Thread (
    tid INT PRIMARY KEY,
    fid INT,
    title VARCHAR(255),
    content TEXT,
    FOREIGN KEY (fid) REFERENCES Forum(fid)
);

CREATE TABLE Component (
    comp_id INT,
    cid CHAR(8),
    compType VARCHAR(30),
    PRIMARY KEY (comp_id, cid),
    FOREIGN KEY (cid) REFERENCES Course(cid)
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
