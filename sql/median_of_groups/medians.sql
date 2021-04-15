use hackerrank;

-- give me the median population by state

select
    state, avg(population)
from
(
    select
    	main.state,
    	main.population,
    	main.rowid upcount,
    	statecount.cnt - main.rowid + 1 downcount,
    	abs(main.rowid - (statecount.cnt - main.rowid + 1)) selector
    from
    (select @prev_state := null, @rowid := 0) init
    inner join
    (
    	select state, population,
    	@rowid := if (state = @prev_state, @rowid + 1, 1) rowid,
    	@prev_state := state
    	from uscities
    	order by state, population
    ) main
    inner join
    (
    	select state, count(*) cnt
    	from uscities
    	group by state
    ) statecount
    on statecount.state = main.state
) wrap1
where selector <= 1
group by state
;
