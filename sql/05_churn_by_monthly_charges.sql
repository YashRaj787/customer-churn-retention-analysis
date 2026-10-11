-- Business Question:
-- How does churn vary across monthly charge bands?

WITH charge_groups AS (
    SELECT
        customer_id,
        monthly_charges,
        churn,
        CASE
            WHEN monthly_charges <= 35 THEN 'Up to 35'
            WHEN monthly_charges <= 70 THEN 'Above 35 to 70'
            WHEN monthly_charges <= 100 THEN 'Above 70 to 100'
            ELSE 'Above 100'
        END AS charge_band,
        CASE
            WHEN monthly_charges <= 35 THEN 1
            WHEN monthly_charges <= 70 THEN 2
            WHEN monthly_charges <= 100 THEN 3
            ELSE 4
        END AS band_order
    FROM public.telco_customer_churn
)
SELECT
    charge_band,
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
    ) AS churn_rate_pct,
    ROUND(AVG(monthly_charges), 2) AS avg_monthly_charges
FROM charge_groups
GROUP BY charge_band, band_order
ORDER BY band_order;