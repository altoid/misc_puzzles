\W

use hackerrank;

select x.state, population, state_count, nn, state_count + 1 - nn rev
from
( select @prev := '' collate utf8_swedish_ci, @n := 0) init
join
(
select
@n := if(`state` != @prev collate utf8_swedish_ci, 1, @n + 1) as nn,
@prev := `state`,
`state`,
population
from uscities
where `state` in ('VI', 'RI')
order by `state`, population
) x
inner join
(
select state, count(*) state_count
from uscities
group by state
) state_counts
on state_counts.state = x.state

where abs( (state_count + 1 - nn) - nn) <= 1
;
