-- Q4. Do employees who work overtime leave more often? Split by department.
SELECT
    department,
    ROUND(100.0 * AVG(CASE WHEN overtime = 'Yes' THEN left_company END), 1) AS overtime_attrition_pct,
    ROUND(100.0 * AVG(CASE WHEN overtime = 'No'  THEN left_company END), 1) AS no_overtime_attrition_pct,
    ROUND(
        AVG(CASE WHEN overtime = 'Yes' THEN left_company END)
      / NULLIF(AVG(CASE WHEN overtime = 'No' THEN left_company END), 0), 1
    )                                                                       AS overtime_risk_multiple
FROM employees
GROUP BY department
ORDER BY overtime_risk_multiple DESC;
