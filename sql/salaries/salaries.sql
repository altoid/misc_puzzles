use test;

select *
from
        salaries s1
inner join
        salaries s2
on s2.salary >= s1.salary
and s2.title = s1.title
-- group by s1.title, s1.salary
-- having count(*) <=3
;
