-- Q2. Which departments lose the most people, in count and in rate?
SELECT
    department,
    COUNT(*)                                   AS headcount,
    SUM(left_company)::INT                          AS leavers,
    ROUND(100.0 * AVG(left_company), 1)        AS attrition_pct,
    ROUND(100.0 * SUM(left_company)::INT / SUM(SUM(left_company)::INT) OVER (), 1)
                                               AS share_of_all_leavers_pct
FROM employees
GROUP BY department
ORDER BY attrition_pct DESC;
