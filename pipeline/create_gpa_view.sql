--create view of grade points by course---
--only counting grade points when 'mark' report as letter grade (A,B+, etc.) or numerical grade (1-100..)
--includes 'mark' column, which shows the original datapoint in the all_grades table, need to make sure this works
create or replace view gpa as 
select a.student_lookup, 
	a.grade, 
	a.school_year, 
	a.clean_term, 
	a.course_name,
	a.mark,
	a.percent_of_year,
	coalesce(a.number_gpa,a.letter_gpa,null) as grade_points
from
	(select ag.student_lookup, ag.grade, ag.school_year, ag.clean_term, ag.course_name, ag.mark, ag.percent_of_year,
		case
			when n.mark isnull then null
			when n.mark >= 93 then 4
			when n.mark >= 90 then 3.67
			when n.mark >= 87 then 3.33
			when n.mark >= 83 then 3
			when n.mark >= 80 then 2.67
			when n.mark >= 77 then 2.33
			when n.mark >= 73 then 2
			when n.mark >= 70 then 1.67
			when n.mark >= 67 then 1.33
			when n.mark >= 63 then 1
			when n.mark >= 60 then 0.67
			else 0
		end as number_gpa, 
		case
			when l.mark isnull then null
			when l.mark = 'A+' then 4
			when l.mark = 'A' then 4
			when l.mark = 'A-' then 3.67
			when l.mark = 'B+' then 3.33
			when l.mark = 'B' then 3
			when l.mark = 'B-' then 2.67
			when l.mark = 'C+' then 2.33
			when l.mark = 'C' then 2
			when l.mark = 'C-' then 1.67
			when l.mark = 'D+' then 1.33
			when l.mark = 'D' then 1
			when l.mark = 'D-' then 0.67
			else 0
		end as letter_gpa
	from clean.all_grades ag
		left outer join
			(select student_lookup,grade,course_code,school_year,cast(mark as float) as mark,clean_term from clean.all_grades
			where left((mark),1) in ('0','1','2','3','4','5','6','7','8','9','.') and length(mark) != 1) n
			using (student_lookup,course_code,grade,school_year,clean_term)
		left outer join
			(select student_lookup,grade,course_code,school_year,mark,clean_term from clean.all_grades
			where mark in ('A+','A','A-','B+','B','B-','C+','C','C-','D+','D','D-','F')) l
			using (student_lookup,course_code,grade,school_year,clean_term)
	) a;