-- Schema:
-- Students (sid, name, degree, ...)
-- Courses (cid, code, term, title, ...)
-- Enrolments (sid, cid, mark, grade)
-- Sample data is available in ... / databases/uni.sql
-- All students who passed COMP9315 in 18s2 (sid, name, mark)

select s.sid, s.name, e.mark
from Students s join Enrolments e join Courses c
where c.code = 9315 and c.term = '18s2' and mark >= 50;