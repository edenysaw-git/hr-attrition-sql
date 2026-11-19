-- Q10. How many current employees fit a high-risk profile, and what would losing them cost?
-- High risk = 2+ of: overtime, job satisfaction <= 2, paid below role/level median, under 2 yrs tenure.
-- Replacement cost assumption: 50% of annual salary (a common HR rule of thumb; change to test).
WITH flags AS (
    SELECT *,
           (CASE WHEN overtime = 'Yes' THEN 1 ELSE 0 END)
         + (CASE WHEN job_satisfaction <= 2 THEN 1 ELSE 0 END)
         + (CASE WHEN monthly_income < MEDIAN(monthly_income)
                      OVER (PARTITION BY job_role, job_level) THEN 1 ELSE 0 END)
         + (CASE WHEN years_at_company < 2 THEN 1 ELSE 0 END)   AS risk_flags
    FROM employees
)
SELECT
    CASE WHEN risk_flags >= 2 THEN 'High risk (2+ flags)' ELSE 'Lower risk' END AS segment,
    COUNT(*)                                                     AS headcount,
    ROUND(100.0 * AVG(left_company), 1)                          AS historical_attrition_pct,
    SUM(CASE WHEN left_company = 0 THEN 1 ELSE 0 END)::INT       AS still_employed,
    ROUND(SUM(CASE WHEN left_company = 0 THEN annual_income * 0.5 END)
          * AVG(left_company), 0)::BIGINT                              AS expected_replacement_cost_usd
FROM flags
GROUP BY segment
ORDER BY historical_attrition_pct DESC;
