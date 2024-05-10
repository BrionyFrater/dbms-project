
-- Total number of students
SELECT COUNT(DISTINCT uid) AS total_students
FROM Student;

-- Total number of Courses
SELECT COUNT(*) AS total_courses
FROM Course;

-- Check number of members for each course
SELECT c.cid, c.cname, COUNT(DISTINCT m.uid) AS num_members
FROM Course c
LEFT JOIN Assigned a ON c.cid = a.cid
LEFT JOIN Enrol e ON c.cid = e.cid
LEFT JOIN Member m ON (a.uid = m.uid OR e.uid = m.uid)
GROUP BY c.cid, c.cname;

-- Check if All Students have courses with a maximum of 6 courses
SELECT uid, COUNT(*) AS num_classes
FROM Enrol
GROUP BY uid
HAVING COUNT(*) > 6;

-- Check if All Students have minimum 3 courses
SELECT s.uid, COUNT(e.cid) AS num_courses
FROM Student s
LEFT JOIN Enrol e ON s.uid = e.uid
GROUP BY s.uid
HAVING COUNT(e.cid) < 3;

-- Check if All Lecturers/Course Maintainers teach at least 1 course
SELECT L.uid
FROM Lecturer L
LEFT JOIN Assigned A ON L.uid = A.uid
GROUP BY L.uid
HAVING COUNT(A.cid) = 0;

-- Check if All Lecturers/Course Maintainers teach max 5 courses
SELECT l.uid, COUNT(c.cid) AS num_courses
FROM Lecturer l
JOIN Assigned a ON l.uid = a.uid
JOIN Course c ON a.cid = c.cid
GROUP BY l.uid
HAVING num_courses > 5;