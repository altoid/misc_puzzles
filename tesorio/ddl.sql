\W

use tesorio;

create table if not exists
user
(
		id int not null primary key,
		login varchar(64) not null unique key,
		json mediumtext character set utf8 collate utf8_general_ci
) engine=innodb default charset=utf8 collate=utf8_general_ci
;


create table if not exists
repo
(
owner_id int not null,
id int not null primary key,
url varchar(1024) not null,
json mediumtext
) engine=innodb
;
