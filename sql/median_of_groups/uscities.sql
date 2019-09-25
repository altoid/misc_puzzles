\W

-- https://simplemaps.com/data/us-cities

use hackerrank;

drop table if exists uscities;

create table uscities 
(
city varchar(33),
city_ascii varchar(33),
state_id varchar(2),
state_name varchar(33),
county_fips int,
county_name varchar(33),
lat float,
lng float,
population int,
population_proper varchar(33),
density float,
`source` varchar(33),
incorporated varchar(33),
timezone varchar(33),
zips varchar(1024),
id int
) engine=innodb;
