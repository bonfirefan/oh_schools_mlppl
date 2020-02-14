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
	
