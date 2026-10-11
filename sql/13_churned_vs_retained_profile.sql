SELECT
    churn,
    COUNT(*) AS total_customers,
    ROUND(AVG(tenure)::numeric, 2) AS avg_tenure_months,
    ROUND((PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY tenure))::numeric, 2) AS median_tenure_months,
    ROUND(AVG(monthly_charges), 2) AS avg_monthly_charges,
    ROUND((PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY monthly_charges))::numeric, 2) AS median_monthly_charges,
    COUNT(total_charges) AS customers_with_total_charges,
    ROUND(AVG(total_charges), 2) AS avg_total_charges
FROM public.telco_customer_churn
GROUP BY churn
ORDER BY CASE churn WHEN 'Yes' THEN 1 WHEN 'No' THEN 2 ELSE 3 END;
