----- exploratory work to learn about different tables -----
select student_lookup, school_year, grade, graduation_date, district_withdraw_date, withdraw_reason 
from clean.all_snapshots 
where grade = 9 and (school_year + 4) <= 2015;

select distinct right(school_year,4) from clean.intervention i;

SELECT *
FROM information_schema.role_table_grants

--JOIN all_grades to all snapshots on student_lookup, grade and school_year
select * from clean.all_grades
where student_lookup = 46 and
		term = 'Final';

select 

--These two districts provide non letter grades for some classes
select distinct mark from clean.all_grades
where --grade in (6,7,8) and 
--length(mark) < 4 and 
district not in ('Coshocton','Maysville');

--isolating number marks
select * from clean.all_grades
where 
--district in ('Coshocton','Maysville') THESE ARE THE CULPRITS, mixed grades, some letter some scores between 0-100
term = 'Final' and
--only taking marks that start with an integer
left((mark),1) in ('0','1','2','3','4','5','6','7','8','9','.') and
--class called 'Music 3' gives marks of '3' or '4'
length(mark) != 1;
--mapping https://en.wikipedia.org/wiki/Academic_grading_in_the_United_States



--isolating 'letter grade' marks
select distinct mark from clean.all_grades
where term = 'Final' and
--only taking letter grades
mark in ('A+','A','A-','B+','B','B-','C+','C','C-','D+','D','D-','F');
--maps to (4,4,3.7,3.3,3,2.7,2.3,2,1.7,1.3,1,0.7,0)
--source: https://education.ohio.gov/getattachment/Topics/What-s-Happening-with-Ohio-s-Graduation-Requiremen/Graduation-Requirements-2014-2017/Alternative-Pathway-for-Diploma/Board-GPA-Calculation-Chart.pdf.aspx

select * from clean.all_grades ag

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

	
select count(grade_points) from sketch.gpa
where grade in (6,7,8)
	
	
	
	
	

	left outer join
		(select student_lookup,grade,school_year,mark from clean.all_grades
		where mark not in ('A+','A','A-','B+','B','B-','C+','C','C-','D+','D','D-','F') or
		left((mark),1) not in ('0','1','2','3','4','5','6','7','8','9','.')) o
		using (student_lookup,grade,school_year);



--intervention count, by student-year
select student_lookup, right(school_year,4) as school_year,
	count(student_lookup) as intervention_count
	from clean.intervention
	group by student_lookup, school_year;

--eigth grade test scores, only one score per student-grade
select student_lookup, 
	8 as grade, 
	eighth_math_ss, 
	eighth_read_ss
from clean.oaaogt
where student_lookup = 2727;

--high school gpa
select student_lookup, school_year, gpa from clean.high_school_gpa

select * from clean.high_school_gpa hsg;



----create a view from a single
create or replace view test as 
select 
	snap.student_lookup, 
	snap.grade as grade, 
	cast(snap.school_year as int) as school_year, 
	snap.days_absent as days_absent, 
	snap.graduation_date as graduation_date,
	snap.discipline_incidents,
	snap.withdraw_reason,
	snap.district_withdraw_date,
	snap.ethnicity,
	snap.school_name,
	coalesce(inter.intervention_count,0) as intervention_count,
	test.eighth_math_ss,
	test.eighth_read_ss,
	gpa.gpa
from 
	clean.all_snapshots as snap
	left outer join 
	(select student_lookup, cast(right(school_year,4) as int) as school_year, count(student_lookup) as intervention_count
	from clean.intervention group by student_lookup, school_year) as inter
	on (snap.student_lookup = inter.student_lookup and snap.school_year = inter.school_year)
	left outer join
	clean.oaaogt as test 
	on (snap.student_lookup = test.student_lookup)
	left outer join
	clean.high_school_gpa as gpa
	on ((snap.student_lookup = gpa.student_lookup and snap.school_year = gpa.school_year));
	
