use leetcode;

-- select count(*), nn, num
select num
from

(select @prev := 0, @n := 0 ) init
join
(
		select @n := if(num != @prev, @n + 1, @n) as nn,
		@prev := num,
		c.*
		from consecutive c
		order by id
) x
group by nn, num
having count(*) > 2
;

