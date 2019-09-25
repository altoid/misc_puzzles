use leetcode;


select d.name Department, e.name Employee, e.salary Salary from
(
    select t1.salary, t1.departmentid
    from 
    (select distinct salary, departmentid from employee) t1
    inner join
    (select distinct salary, departmentid from employee) t2
    on t1.DepartmentId = t2.DepartmentId and t1.salary <= t2.salary
    group by t1.departmentid, t1.salary 
    having count(*) <= 3
) top3
inner join department d on d.id = top3.departmentid
inner join employee e on e.salary = top3.salary and e.departmentid = top3.departmentid
;


