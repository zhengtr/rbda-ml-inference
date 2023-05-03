SELECT q.year, avg(c.cWord_ans_sum) as avg_ans_w_cWord_sum 
FROM ques q 
INNER JOIN (SELECT q.postId, count(*) as cWord_ans_sum 
            FROM ques q JOIN ans a 
            ON q.postId = a.parentId 
            WHERE q.cWord > 0 AND a.cWord > 0 
            GROUP BY q.postId) c 
ON q.postId = c.postId 
GROUP BY q.year 
ORDER BY q.year; 
