WITH status_summary AS (
    SELECT
        churn,
        COUNT(*) AS total_customers,
        SUM(monthly_charges) AS total_monthly_charges,
        AVG(monthly_charges) AS avg_monthly_charges,
        AVG(total_charges) AS avg_total_charges
    FROM public.telco_customer_churn
    GROUP BY churn
)
SELECT
    churn,
    total_customers,
    ROUND(total_monthly_charges, 2) AS sum_monthly_charges,
    ROUND(100.0 * total_monthly_charges / NULLIF(SUM(total_monthly_charges) OVER (), 0), 2) AS share_of_monthly_charges_pct,
    ROUND(avg_monthly_charges, 2) AS avg_monthly_charges,
    ROUND(avg_total_charges, 2) AS avg_total_charges
FROM status_summary
ORDER BY CASE churn WHEN 'Yes' THEN 1 WHEN 'No' THEN 2 ELSE 3 END;
