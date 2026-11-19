-- Q7. Attrition by job satisfaction x work-life balance (1 = low, 4 = high).
SELECT
    job_satisfaction,
    work_life_balance,
    COUNT(*)                                   AS headcount,
    ROUND(100.0 * AVG(left_company), 1)        AS attrition_pct
FROM employees
GROUP BY job_satisfaction, work_life_balance
HAVING COUNT(*) >= 15
ORDER BY attrition_pct DESC
LIMIT 10;
