use hackerrank;

select state, sum(population) / count(*) median
from
( select @counter := 0, @prevstate := '' ) init
inner join
(
	select
    @counter := if(state != @prevstate collate utf8_swedish_ci, 1, @counter + 1) upcounter,
    scount + 1 - @counter downcounter,
    @prevstate := state,
    state, population, scount
    from
    (
        select 
        uscities.state, uscities.population, scount
        from
        uscities
        inner join
        (
            select state, count(*) scount
            from uscities
            group by state
        ) scount
        on scount.state = uscities.state
        order by state
    ) b
) c
where abs(upcounter - downcounter) < 2
group by state
;
