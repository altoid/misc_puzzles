use hackerrank;

/*
select *
from
(select @counter := 0, @prev := '') init
inner join
(
select @counter := if(state != @prev, 1, @counter + 1) cc,
@prev := state,
state, population
from uscities
where state in ('RI', 'DE')
order by state, population
) x
inner join
(
select state, count(*) scount
from uscities
group by state
) statecount
on x.state = statecount.state
;
*/

select state, sum(population) / count(*)
from
(
    select
    -- upcounter, downcounter, population, 
    state, population
    from
    (select @counter := 0, @prev := '') init
    inner join
    (
        select
        @counter := if(state != @prev collate utf8_swedish_ci, 1, @counter + 1) upcounter,
        @prev := state,
        population,
    	scount,
    	scount + 1 - @counter downcounter,
    	state
        from (
            select 
            uscities.state, uscities.population, scount
            from uscities
            inner join
            (
            select state, count(*) scount
            from uscities
            group by state
            ) statecount
            on uscities.state = statecount.state
            order by state, population
        ) a
    ) statecount
    where abs(upcounter - downcounter) < 2
) b
group by state
;
