\W

use deutsch;

/*
show me no more than 5 words for any character count

https://mariadb.com/kb/en/library/groupwise-max-in-mariadb/
*/

select len, word
from
( select @n := 0, @prev := 0 ) init
join
(
	select @n := if(length(word) != @prev, 1, @n + 1) as nn,
    length(word) len,
	@prev := length(word),
	word
    from word
    order by length(word), word
) x
where nn <= 5
order by length(word), word
;

