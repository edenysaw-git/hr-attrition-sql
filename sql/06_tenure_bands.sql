-- Q6. When in their tenure do people leave? Running share of all leavers by tenure band.
WITH by_band AS (
    SELECT
        tenure_band,
        MIN(years_at_company)                  AS sort_key,
        COUNT(*)                               AS headcount,
        SUM(left_company)::INT                      AS leavers,
        AVG(left_company)                      AS attrition_rate
    FROM employees
    GROUP BY tenure_band
)
SELECT
    tenure_band,
    headcount,
    leavers,
    ROUND(100.0 * attrition_rate, 1)           AS attrition_pct,
    ROUND(100.0 * SUM(leavers) OVER (ORDER BY sort_key) / SUM(leavers) OVER (), 1)
                                               AS cumulative_share_of_leavers_pct
FROM by_band
ORDER BY sort_key;
