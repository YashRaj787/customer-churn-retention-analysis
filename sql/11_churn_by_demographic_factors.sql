WITH factor_groups AS (
    SELECT 'Gender'::text AS factor, gender::text AS category, churn
    FROM public.telco_customer_churn

    UNION ALL
    SELECT 'Senior Citizen',
           CASE WHEN senior_citizen = 1 THEN 'Senior citizen' ELSE 'Not senior citizen' END,
           churn
    FROM public.telco_customer_churn

    UNION ALL
    SELECT 'Partner', partner, churn
    FROM public.telco_customer_churn

    UNION ALL
    SELECT 'Dependents', dependents, churn
    FROM public.telco_customer_churn

    UNION ALL
    SELECT 'Paperless Billing', paperless_billing, churn
    FROM public.telco_customer_churn
)
SELECT
    factor,
    category,
    COUNT(*) AS total_customers,
    COUNT(*) FILTER (WHERE churn = 'Yes') AS churned_customers,
    COUNT(*) FILTER (WHERE churn = 'No') AS retained_customers,
    ROUND(100.0 * COUNT(*) FILTER (WHERE churn = 'Yes') / NULLIF(COUNT(*), 0), 2) AS churn_rate_pct
FROM factor_groups
GROUP BY factor, category
ORDER BY factor, churn_rate_pct DESC, category;
