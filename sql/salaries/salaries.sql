use test;

-- top 3 salaries for each job title

select s1.*
from
        salaries s1
inner join
        salaries s2
on s1.salary <= s2.salary
and s2.title = s1.title
group by s1.title, s1.salary
having count(*) <=3
;
