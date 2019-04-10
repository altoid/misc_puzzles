\W

use hackerrank;

-- median population from whole corpus

select sum(median) / count(*) median
from
(
select population median
from 
( select @rowid := 0 ) init
join
( select @rowid := @rowid + 1 as rowid,
  population
  from uscities order by population
) x
join ( select count(*) c from uscities ) cnt
where abs((c - rowid + 1) - rowid) <= 1
) y
;

/*
if the count is even, then we have take the mean of the sum of 2 values.
in this case the mininum difference in row ids is 1.

if the count is odd, then we just have one value.  we can still take the mean of the sum of 1 value.
in this case the minimum difference in row ids is 0.
*/
