use leetcode;

\W

select ranked_scores.rank, s.score
from
(
    select score, rank
    from
    (select @counter := 0) init
    inner join
    (
    	  select @counter := @counter + 1 rank, score
    	  from
    	  (
    		select distinct scores.score
    		from scores
    		order by score desc
    	  ) sc
    ) rest
) ranked_scores
inner join scores s on s.score = ranked_scores.score
order by ranked_scores.rank
;
