use test;

create table if not exists salaries
( title varchar(16) not null,
  salary int not null )
engine=innodb;

insert into salaries values
( 'president', 1000000),
( 'director' ,  500000),
( 'director' ,  400000),
( 'director' ,  454000),
( 'director' ,  300000),
( 'director' ,  350000),
( 'director' ,  200000),
( 'coder'    ,   32233),
( 'coder'    ,   32456),
( 'coder'    ,   25646),
( 'coder'    ,   10000),
( 'coder'    ,   20000)
;


