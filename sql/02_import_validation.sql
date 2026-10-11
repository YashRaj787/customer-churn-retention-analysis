SELECT
    COUNT(*) AS total_records,
    COUNT(DISTINCT customer_id) AS unique_customer_ids,
    COUNT(*) FILTER (
        WHERE churn = 'Yes'
    ) AS churned_customers,
    COUNT(*) FILTER (
        WHERE churn = 'No'
    ) AS retained_customers,
    COUNT(*) FILTER (
        WHERE total_charges IS NULL
    ) AS missing_total_charges
FROM public.telco_customer_churn;