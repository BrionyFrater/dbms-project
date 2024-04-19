USE Project;
-- Generate 100,000 students with random names
INSERT INTO Student (uid, fname, lname, password)
SELECT (100000 + ROW_NUMBER() OVER (ORDER BY (SELECT NULL))),
       CONCAT('Student', FLOOR(RAND() * 10000) + 1), 
       CONCAT('Lastname', FLOOR(RAND() * 10000) + 1), 
       'password'
FROM information_schema.tables t1, information_schema.tables t2
LIMIT 100000;

-- Generate 200 courses with random names
INSERT INTO Course (cid, cname, dateCreated)
SELECT (200 + ROW_NUMBER() OVER (ORDER BY (SELECT NULL))),
       CONCAT('Course', FLOOR(RAND() * 10000) + 1), 
       NOW()
FROM information_schema.tables t1, information_schema.tables t2
LIMIT 200;

-- Randomly assign students to courses (3 to 6 courses per student)
INSERT INTO Enrol (cid, uid, grade)
SELECT DISTINCT c.cid, s.uid, FLOOR(RAND() * 100) + 40 
FROM Student s
JOIN Course c
WHERE NOT EXISTS (
    SELECT 1 FROM Enrol WHERE Enrol.uid = s.uid AND Enrol.cid = c.cid
)
AND RAND() < 0.7; 

-- Ensure each course has at least 10 members
UPDATE Course c
SET c.members = (
    SELECT COUNT(*) FROM Enrol e WHERE e.cid = c.cid
)
WHERE (SELECT COUNT(*) FROM Enrol e WHERE e.cid = c.cid) < 10;

-- Assign courses to lecturers (1 to 5 courses per lecturer)
INSERT INTO Assigned (cid, uid)
SELECT DISTINCT c.cid, l.uid
FROM Course c
JOIN Lecturer l
WHERE NOT EXISTS (
    SELECT 1 FROM Assigned WHERE Assigned.uid = l.uid AND Assigned.cid = c.cid
)
AND RAND() < 0.6 
GROUP BY l.uid
HAVING COUNT(*) <= 5;
