WITH service_groups AS (
    SELECT 'Multiple Lines'::text AS service, multiple_lines::text AS service_status, churn
    FROM public.telco_customer_churn

    UNION ALL
    SELECT 'Online Security', online_security, churn
    FROM public.telco_customer_churn

    UNION ALL
    SELECT 'Online Backup', online_backup, churn
    FROM public.telco_customer_churn

    UNION ALL
    SELECT 'Device Protection', device_protection, churn
    FROM public.telco_customer_churn

    UNION ALL
    SELECT 'Tech Support', tech_support, churn
    FROM public.telco_customer_churn

    UNION ALL
    SELECT 'Streaming TV', streaming_tv, churn
    FROM public.telco_customer_churn

    UNION ALL
    SELECT 'Streaming Movies', streaming_movies, churn
    FROM public.telco_customer_churn
)
SELECT
    service,
    service_status,
    COUNT(*) AS total_customers,
    COUNT(*) FILTER (WHERE churn = 'Yes') AS churned_customers,
    COUNT(*) FILTER (WHERE churn = 'No') AS retained_customers,
    ROUND(100.0 * COUNT(*) FILTER (WHERE churn = 'Yes') / NULLIF(COUNT(*), 0), 2) AS churn_rate_pct
FROM service_groups
GROUP BY service, service_status
ORDER BY service, churn_rate_pct DESC, service_status;
