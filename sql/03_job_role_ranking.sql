-- Q3. Rank job roles by attrition rate (roles with 20+ people only).
WITH role_stats AS (
    SELECT
        job_role,
        department,
        COUNT(*)                               AS headcount,
        SUM(left_company)::INT                      AS leavers,
        AVG(left_company)                      AS attrition_rate
    FROM employees
    GROUP BY job_role, department
    HAVING COUNT(*) >= 20
)
SELECT
    RANK() OVER (ORDER BY attrition_rate DESC) AS risk_rank,
    job_role,
    department,
    headcount,
    leavers,
    ROUND(100.0 * attrition_rate, 1)           AS attrition_pct
FROM role_stats
ORDER BY risk_rank;
