
WITH summary AS (
    SELECT
        COUNT(*) AS total_records,
        COUNT(DISTINCT customer_id) AS unique_customer_ids,
        COUNT(*) FILTER (WHERE churn = 'Yes') AS churned_customers,
        COUNT(*) FILTER (WHERE churn = 'No') AS retained_customers,
        COUNT(*) FILTER (WHERE total_charges IS NULL) AS missing_total_charges,
        COUNT(*) FILTER (WHERE tenure = 0) AS zero_tenure_customers,
        COUNT(*) FILTER (WHERE monthly_charges < 0) AS negative_monthly_charges,
        COUNT(*) FILTER (WHERE total_charges < 0) AS negative_total_charges
    FROM public.telco_customer_churn
),
missing_fields AS (
    SELECT
        t.customer_id,
        fields.field_name
    FROM public.telco_customer_churn AS t
    CROSS JOIN LATERAL (
        VALUES
            ('customer_id', t.customer_id IS NULL),
            ('gender', t.gender IS NULL),
            ('senior_citizen', t.senior_citizen IS NULL),
            ('partner', t.partner IS NULL),
            ('dependents', t.dependents IS NULL),
            ('tenure', t.tenure IS NULL),
            ('phone_service', t.phone_service IS NULL),
            ('multiple_lines', t.multiple_lines IS NULL),
            ('internet_service', t.internet_service IS NULL),
            ('online_security', t.online_security IS NULL),
            ('online_backup', t.online_backup IS NULL),
            ('device_protection', t.device_protection IS NULL),
            ('tech_support', t.tech_support IS NULL),
            ('streaming_tv', t.streaming_tv IS NULL),
            ('streaming_movies', t.streaming_movies IS NULL),
            ('contract', t.contract IS NULL),
            ('paperless_billing', t.paperless_billing IS NULL),
            ('payment_method', t.payment_method IS NULL),
            ('monthly_charges', t.monthly_charges IS NULL),
            ('total_charges', t.total_charges IS NULL),
            ('churn', t.churn IS NULL)
    ) AS fields(field_name, is_missing)
    WHERE fields.is_missing
),
audit_output AS (
    SELECT 1 AS sort_order, 'Summary'::text AS section,
           'Total records'::text AS check_or_customer_id,
           total_records::text AS result
    FROM summary

    UNION ALL
    SELECT 2, 'Summary', 'Unique customer IDs',
           unique_customer_ids::text
    FROM summary

    UNION ALL
    SELECT 3, 'Summary', 'Churned customers',
           churned_customers::text
    FROM summary

    UNION ALL
    SELECT 4, 'Summary', 'Retained customers',
           retained_customers::text
    FROM summary

    UNION ALL
    SELECT 5, 'Summary', 'Missing TotalCharges',
           missing_total_charges::text
    FROM summary

    UNION ALL
    SELECT 6, 'Summary', 'Zero-tenure customers',
           zero_tenure_customers::text
    FROM summary

    UNION ALL
    SELECT 7, 'Summary', 'Negative monthly charges',
           negative_monthly_charges::text
    FROM summary

    UNION ALL
    SELECT 8, 'Summary', 'Negative TotalCharges',
           negative_total_charges::text
    FROM summary

    UNION ALL
    SELECT 9, 'Missing-value count', field_name,
           COUNT(*)::text
    FROM missing_fields
    GROUP BY field_name

    UNION ALL
    SELECT 10, 'Affected record', customer_id, field_name
    FROM missing_fields
)
SELECT
    section,
    check_or_customer_id,
    result
FROM audit_output
ORDER BY sort_order, check_or_customer_id;
