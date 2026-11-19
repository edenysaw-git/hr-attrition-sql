-- Q8. Are people paid below the median for their role and level more likely to leave?
WITH peer_pay AS (
    SELECT *,
           MEDIAN(monthly_income) OVER (PARTITION BY job_role, job_level) AS peer_median_income
    FROM employees
)
SELECT
    CASE WHEN monthly_income < peer_median_income
         THEN 'Below peer median' ELSE 'At or above peer median' END     AS pay_position,
    COUNT(*)                                   AS headcount,
    ROUND(100.0 * AVG(left_company), 1)        AS attrition_pct,
    ROUND(AVG(monthly_income / peer_median_income) * 100, 1)              AS avg_pay_vs_peers_pct
FROM peer_pay
GROUP BY pay_position
ORDER BY attrition_pct DESC;
