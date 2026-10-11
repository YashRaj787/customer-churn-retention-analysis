WITH customer_bands AS (
    SELECT
        contract,
        tenure,
        churn,
        CASE
            WHEN tenure <= 12 THEN '0-12 months'
            WHEN tenure <= 24 THEN '13-24 months'
            WHEN tenure <= 48 THEN '25-48 months'
            ELSE '49-72 months'
        END AS tenure_band,
        CASE
            WHEN tenure <= 12 THEN 1
            WHEN tenure <= 24 THEN 2
            WHEN tenure <= 48 THEN 3
            ELSE 4
        END AS tenure_band_order
    FROM public.telco_customer_churn
)
SELECT
    contract,
    tenure_band,
    COUNT(*) AS total_customers,
    COUNT(*) FILTER (WHERE churn = 'Yes') AS churned_customers,
    COUNT(*) FILTER (WHERE churn = 'No') AS retained_customers,
    ROUND(100.0 * COUNT(*) FILTER (WHERE churn = 'Yes') / NULLIF(COUNT(*), 0), 2) AS churn_rate_pct
FROM customer_bands
GROUP BY contract, tenure_band, tenure_band_order
ORDER BY
    CASE contract WHEN 'Month-to-month' THEN 1 WHEN 'One year' THEN 2 WHEN 'Two year' THEN 3 ELSE 4 END,
    tenure_band_order;
