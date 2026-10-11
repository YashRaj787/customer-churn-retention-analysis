WITH customer_addons AS (
    SELECT
        customer_id,
        churn,
        (CASE WHEN online_security = 'Yes' THEN 1 ELSE 0 END
       + CASE WHEN online_backup = 'Yes' THEN 1 ELSE 0 END
       + CASE WHEN device_protection = 'Yes' THEN 1 ELSE 0 END
       + CASE WHEN tech_support = 'Yes' THEN 1 ELSE 0 END
       + CASE WHEN streaming_tv = 'Yes' THEN 1 ELSE 0 END
       + CASE WHEN streaming_movies = 'Yes' THEN 1 ELSE 0 END) AS addon_count
    FROM public.telco_customer_churn
)
SELECT
    addon_count,
    COUNT(*) AS total_customers,
    COUNT(*) FILTER (WHERE churn = 'Yes') AS churned_customers,
    COUNT(*) FILTER (WHERE churn = 'No') AS retained_customers,
    ROUND(100.0 * COUNT(*) FILTER (WHERE churn = 'Yes') / NULLIF(COUNT(*), 0), 2) AS churn_rate_pct
FROM customer_addons
GROUP BY addon_count
ORDER BY addon_count;
