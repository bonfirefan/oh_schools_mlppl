select has_grad, yrs_dist, count(*)
from
(select case when grad is null then 0 else 1 end as has_grad,
case when grad is null then 0 else 1 end as has_grad,
yr, yr-admit as yrs_dist, admit, avg(count), count(*) total
from 
(SELECT student_lookup, 
max(graduation_date) as grad, max(school_year) as yr, min(CAST(to_char(district_admit_date, 'yyyy') as NUMERIC)) as admit, count(*)
FROM clean.all_snapshots
group by student_lookup) gs
group by grad, yr, admit) ot 
group by has_grad, yrs_dist