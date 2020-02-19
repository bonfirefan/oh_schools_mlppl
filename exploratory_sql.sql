select status, description, grade, inv_group, count(*) from clean.intervention 
group by status, description, grade, inv_group
order by count(*) desc;

select description, count(*)
from clean.intervention
group by description
order by count(*) desc;