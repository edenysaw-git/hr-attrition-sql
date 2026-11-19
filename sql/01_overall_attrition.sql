-- Q1. What is the company's overall attrition rate?
SELECT
    COUNT(*)                                   AS headcount,
    SUM(left_company)::INT                          AS leavers,
    ROUND(100.0 * AVG(left_company), 1)        AS attrition_pct
FROM employees;
