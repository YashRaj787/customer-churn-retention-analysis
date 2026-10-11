SELECT
    payment_method,
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

GROUP BY payment_method

ORDER BY churn_rate_pct DESC;
