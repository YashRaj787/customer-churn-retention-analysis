CREATE TABLE telco_customer_churn (
    customer_id TEXT PRIMARY KEY,
    gender TEXT NOT NULL,
    senior_citizen SMALLINT NOT NULL
        CHECK (senior_citizen IN (0, 1)),
    partner TEXT NOT NULL,
    dependents TEXT NOT NULL,
    tenure INTEGER NOT NULL
        CHECK (tenure BETWEEN 0 AND 72),
    phone_service TEXT NOT NULL,
    multiple_lines TEXT NOT NULL,
    internet_service TEXT NOT NULL,
    online_security TEXT NOT NULL,
    online_backup TEXT NOT NULL,
    device_protection TEXT NOT NULL,
    tech_support TEXT NOT NULL,
    streaming_tv TEXT NOT NULL,
    streaming_movies TEXT NOT NULL,
    contract TEXT NOT NULL,
    paperless_billing TEXT NOT NULL,
    payment_method TEXT NOT NULL,
    monthly_charges NUMERIC(10, 2) NOT NULL,
    total_charges NUMERIC(12, 2),
    churn TEXT NOT NULL CHECK (churn IN ('Yes', 'No'))
);