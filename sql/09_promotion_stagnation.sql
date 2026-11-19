-- Q9. Does waiting longer for a promotion raise attrition? By job level.
SELECT
    job_level,
    CASE
        WHEN years_since_last_promotion = 0 THEN 'Promoted this year'
        WHEN years_since_last_promotion <= 2 THEN '1-2 yrs'
        ELSE '3+ yrs'
    END                                        AS time_since_promotion,
    COUNT(*)                                   AS headcount,
    ROUND(100.0 * AVG(left_company), 1)        AS attrition_pct
FROM employees
GROUP BY job_level, time_since_promotion
ORDER BY job_level, MIN(years_since_last_promotion);
