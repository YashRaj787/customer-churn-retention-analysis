
-- Business Question:
-- How does churn vary by customer tenure?

WITH tenure_groups AS (
    SELECT
        customer_id,
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
        END AS band_order
    FROM public.telco_customer_churn
)
SELECT
    tenure_band,
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
FROM tenure_groups
GROUP BY tenure_band, band_order
ORDER BY band_order;
