
SELECT
    contract,
    COUNT(*) AS total_customers,

    COUNT(*) FILTER (
        WHERE churn = 'Yes'
    ) AS churned_customers,

    COUNT(*) FILTER (
        WHERE churn = 'No'
    ) AS retained_customers,

    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE churn = 'Yes'
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS churn_rate_pct

FROM public.telco_customer_churn

GROUP BY contract

ORDER BY
    CASE contract
        WHEN 'Month-to-month' THEN 1
        WHEN 'One year' THEN 2
        WHEN 'Two year' THEN 3
        ELSE 4
    END;
