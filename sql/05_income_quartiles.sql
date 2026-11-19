-- Q5. How does attrition change across pay quartiles?
WITH banded AS (
    SELECT *,
           NTILE(4) OVER (ORDER BY monthly_income) AS income_quartile
    FROM employees
)
SELECT
    income_quartile,
    MIN(monthly_income)                        AS min_monthly_income,
    MAX(monthly_income)                        AS max_monthly_income,
    COUNT(*)                                   AS headcount,
    ROUND(100.0 * AVG(left_company), 1)        AS attrition_pct
FROM banded
GROUP BY income_quartile
ORDER BY income_quartile;
