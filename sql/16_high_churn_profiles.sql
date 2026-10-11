WITH profile_metrics AS (
    SELECT
        contract,
        internet_service,
        online_security,
        tech_support,
        COUNT(*) AS total_customers,
        COUNT(*) FILTER (WHERE churn = 'Yes') AS churned_customers,
        COUNT(*) FILTER (WHERE churn = 'No') AS retained_customers
    FROM public.telco_customer_churn
    GROUP BY contract, internet_service, online_security, tech_support
    HAVING COUNT(*) >= 50
),
ranked_profiles AS (
    SELECT
        *,
        100.0 * churned_customers / NULLIF(total_customers, 0) AS churn_rate_raw,
        RANK() OVER (
            ORDER BY 100.0 * churned_customers / NULLIF(total_customers, 0) DESC
        ) AS churn_risk_rank
    FROM profile_metrics
)
SELECT
    churn_risk_rank,
    contract,
    internet_service,
    online_security,
    tech_support,
    total_customers,
    churned_customers,
    retained_customers,
    ROUND(churn_rate_raw, 2) AS churn_rate_pct
FROM ranked_profiles
ORDER BY churn_risk_rank, total_customers DESC;
