use hackerrank;

-- give me the median population by state, among cities with > 0 population

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
    	from
	(
		select state, population
		from uscities
		where population > 0
	) nonzero_pop
    	order by state, population
    ) main
    inner join
    (
    	select state, count(*) cnt
    	from uscities
	where population > 0
    	group by state
    ) statecount
    on statecount.state = main.state
) wrap1
where selector < 2
group by state
;

-- median population by county

select
state, county_name, avg(population) county_median
from
(
    select
	main.state,
	main.county_name,
    	population,
    	main.rowid upcount,
    	cty_count.cnt - main.rowid + 1 downcount,
       	abs(main.rowid - (cty_count.cnt - main.rowid + 1)) selector
    from
    (select @prev_state := null, @prev_county := null, @rowid := 0) init
    inner join
    (
    	select state, county_name, population,
    	@rowid := if (state = @prev_state and county_name = @prev_county, @rowid + 1, 1) rowid,
    	@prev_state := state,
    	@prev_county := county_name
    	from
    	(
    		select state, county_name, population
    		from uscities
    		where population > 0
    	) nonzero_pop
    	order by state, county_name, population
    ) main
    inner join
    (
    	select state, county_name, count(*) cnt
    	from uscities
    	where population > 0
    	group by state, county_name
    ) cty_count
    on cty_count.state = main.state and cty_count.county_name = main.county_name
) wrap
where selector < 2
group by state, county_name
;
