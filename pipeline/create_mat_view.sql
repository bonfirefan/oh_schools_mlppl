
----create a view for next steps ---
CREATE MATERIALIZED VIEW sketch.train_data AS 
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
	gpa.gpa,
	new_gpa.new_gpa
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
		on ((snap.student_lookup = gpa.student_lookup and snap.school_year = gpa.school_year))
	left outer join
		(select student_lookup,school_year, 
		sum(grade_points*percent_of_year)/sum(percent_of_year) as new_gpa
		from sketch.gpa
		where clean_term != 'final'
		group by (student_lookup,school_year)) as new_gpa
		on ((snap.student_lookup = new_gpa.student_lookup and snap.school_year = new_gpa.school_year));