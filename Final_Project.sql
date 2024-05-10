CREATE DATABASE IF NOT EXISTS Project;
-- CREATE USER 'project_user'@'localhost' IDENTIFIED BY '123';
GRANT ALL PRIVILEGES ON Project.* TO 'project_user'@'localhost';

USE Project;

--NEW STUFF---

CREATE TABLE Account (
    uid INT PRIMARY KEY,
	fname VARCHAR(50),
    lname VARCHAR(50),
    phoneNum VARCHAR(15),
    user_role VARCHAR(50),
    password VARCHAR(100)
);

CREATE TABLE Student (
    uid INT PRIMARY KEY,
    address VARCHAR(255),
    FOREIGN KEY (uid) REFERENCES Account(uid)
);

CREATE TABLE Admin (
	uid INT,
    dateCreated DATETIME,
    FOREIGN KEY (uid) REFERENCES Account(uid)
);

CREATE TABLE Lecturer (
    uid INT PRIMARY KEY,
    department VARCHAR(255)
    FOREIGN KEY (uid) REFERENCES Account(uid)
);

CREATE TABLE Course (
    cid CHAR(8) PRIMARY KEY,
    cname VARCHAR(255),
    dateCreated DATETIME
);

CREATE TABLE CreateCrse (
    --cid INT PRIMARY KEY,
    cid CHAR(8) PRIMARY KEY,
    uid INT,
    dateCreated DATE,
    FOREIGN KEY (uid) REFERENCES Admin(uid)
);

CREATE TABLE Enrol (
    cid CHAR(8),
    uid INT,
    grade INT,
    PRIMARY KEY (cid, uid),
    FOREIGN KEY (cid) REFERENCES Course(cid),
    FOREIGN KEY (uid) REFERENCES Student(uid)
);

CREATE TABLE Member (
    uid INT PRIMARY KEY,
    type CHAR

    --possibly remove
    FOREIGN KEY (uid) REFERENCES Account(uid)
);

CREATE TABLE Assigned (
    cid CHAR(8),
    uid INT,

    --new attriutes
    semester INT,
    year INT

    PRIMARY KEY (cid, uid, semester, year)
    FOREIGN KEY (cid) REFERENCES Course(cid),
    FOREIGN KEY (uid) REFERENCES Member(uid)
);


CREATE TABLE Component (
    comp_id INT,
    cid CHAR(8),
    compType VARCHAR(30),
    PRIMARY KEY (comp_id, cid),

    --possible remove cascade delete
    FOREIGN KEY (cid) REFERENCES Course(cid) ON DELETE CASCADE
);

CREATE TABLE Event (
    --eid INT PRIMARY KEY,
    cid CHAR(8),
    comp_id INT,
    name VARCHAR(255),
    description TEXT,
    dateCreated DATE,
    dueDate DATE,

    PRIMARY KEY (comp_id, cid)
    FOREIGN KEY (comp_id, cid) REFERENCES Component(comp_id, cid)
);

CREATE TABLE Forum (
    --fid INT PRIMARY KEY,
    cid CHAR(8),
    comp_id INT,
    name VARCHAR(255),
    dateCreated DATE,

    --added new primary
    PRIMARY KEY (comp_id, cid)
    FOREIGN KEY (comp_id, cid) REFERENCES Component(comp_id, cid)
);

CREATE TABLE Thread (
    tid INT AUTO_INCREMENT PRIMARY KEY,
    parent INT,
    title VARCHAR(255),
    content TEXT,
    dateCreated DATE,
    FOREIGN KEY (parent) REFERENCES Forum(comp_id) ON DELETE CASCADE
);

CREATE TABLE Reply (
    reply_id INT AUTO_INCREMENT PRIMARY KEY,
    parent INT,
    author VARCHAR(255),
    content TEXT,
    dateCreated DATE,
    FOREIGN KEY (parent) REFERENCES Thread(tid)
);

CREATE TABLE Section (
    comp_id INT,
    cid CHAR(8),
    secName VARCHAR(255),
    PRIMARY KEY (comp_id, cid),
    FOREIGN KEY (comp_id, cid) REFERENCES Component(comp_id, cid)
);

CREATE TABLE ModifySection (
    uid INT,
    comp_id INT,
    cid CHAR(8),
    FOREIGN KEY (uid) REFERENCES Account(uid),
    FOREIGN KEY (comp_id, cid) REFERENCES Section(comp_id, cid)
);

CREATE TABLE ModifyItem (
    uid INT,
    comp_id INT,
    cid CHAR(8),
    FOREIGN KEY (uid) REFERENCES Account(uid),
    FOREIGN KEY (comp_id, cid) REFERENCES Section(comp_id, cid)
);

CREATE TABLE SectionItems (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(255),
    item_type VARCHAR(255),
    contentPath VARCHAR(255),
    parent_id INT,
    parent_cid CHAR(8),
    FOREIGN KEY (parent_id, parent_cid) REFERENCES Section(comp_id, cid)
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
    grade INT,
    assignmentFile VARCHAR(50),
    PRIMARY KEY (comp_id, cid, uid),
    FOREIGN KEY (comp_id, cid) REFERENCES Component(comp_id, cid),
    FOREIGN KEY (uid) REFERENCES Student(uid)
);




