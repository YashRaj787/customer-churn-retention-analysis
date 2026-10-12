# Customer Churn & Retention Analysis

This project looks at customer churn for a telecom service. It uses Excel, Python, PostgreSQL, and Power BI to check the data, study churn patterns, and present the results in an interactive dashboard.

The analysis shows patterns in the data. It does not prove that any factor causes a customer to leave.

## Dashboard Preview

The Power BI report has three pages. Open the screenshots below to preview each page.

### 1. Customer Overview

Shows the main customer numbers and churn rates by contract type, tenure, internet service, and payment method.

![Customer Overview dashboard](screenshots/customer_overview.png)

### 2. Service Drivers

Compares churn rates by online security, technical support, and number of optional services.

![Service Drivers dashboard](screenshots/service_drivers.png)

### 3. Customer Risk & Economics

Compares churn across monthly-charge bands and customer groups. It includes filters for contract, payment method, and internet service.

![Customer Risk & Economics dashboard](screenshots/customer_risk_economics.png)

## Business Questions

This project explores questions such as:

- Which contract types have the highest churn rate?
- How does churn change with customer tenure?
- How do churn rates differ by internet service, payment method, online security, and technical support?
- Do churn rates differ across monthly-charge bands and customer groups?
- Which combinations of customer characteristics have high observed churn rates?

## Dataset

The project uses the IBM Telco Customer Churn dataset.

- **Customers:** 7,043
- **Columns:** 21
- **Target field:** `Churn` (`Yes` or `No`)
- **Churned customers:** 1,869
- **Retained customers:** 5,174
- **Overall churn rate:** 26.54%

**Source:** [IBM Telco Customer Churn dataset](https://github.com/IBM/telco-customer-churn-on-icp4d/blob/master/data/Telco-Customer-Churn.csv)

Review the source repository's license and data terms before redistributing the CSV files. If permission to share the dataset is unclear, keep the data files out of the public repository and follow the source link to obtain the data.

## Data Checks and Cleaning

I checked the data before analyzing it. The checks covered row and column counts, duplicate customer IDs, blank values, category values, numeric ranges, and relationships between fields.

The audit found 11 blank or space-only values in `TotalCharges`. All 11 records had `tenure = 0` and `Churn = No`.

I kept these values missing instead of changing them to zero or deleting those customers. The cleaning script converts `TotalCharges` to a numeric field in a separate processed dataset. The raw file is kept unchanged.

The processed dataset was checked to confirm that it has 7,043 rows, 21 columns, and 7,043 unique customer IDs.

## Tools Used

- **Excel:** initial data audit and checks for missing values, categories, numeric ranges, and field relationships
- **Python:** pandas for data cleaning and analysis; Matplotlib for charts
- **PostgreSQL:** grouped churn analysis, comparisons across customer groups, customer profiles, and validation checks
- **Power BI:** DAX measures, KPI cards, charts, and interactive filters

## Key Findings

### Overall churn

26.54% of customers had churned: 1,869 out of 7,043. The other 5,174 customers were retained.

### Churn by contract type

| Contract type | Customers | Churned customers | Churn rate |
|---|---:|---:|---:|
| Month-to-month | 3,875 | 1,655 | **42.71%** |
| One year | 1,473 | 166 | 11.27% |
| Two year | 1,695 | 48 | 2.83% |

Month-to-month customers had the highest observed churn rate among the three contract groups.

### Churn by tenure

| Tenure | Customers | Churned customers | Churn rate |
|---|---:|---:|---:|
| 0–12 months | 2,186 | 1,037 | **47.44%** |
| 13–24 months | 1,024 | 294 | 28.71% |
| 25–48 months | 1,594 | 325 | 20.39% |
| 49–72 months | 2,239 | 213 | 9.51% |

The shortest-tenure group had the highest observed churn rate. Churn rates were lower in the longer-tenure groups.

### Churn by internet service

| Internet service | Customers | Churned customers | Churn rate |
|---|---:|---:|---:|
| Fiber optic | 3,096 | 1,297 | **41.89%** |
| DSL | 2,421 | 459 | 18.96% |
| No internet service | 1,526 | 113 | 7.40% |

### Other patterns

- Customers without technical support had a 41.64% churn rate, compared with 15.17% for customers with support.
- Customers without online security had a 41.77% churn rate, compared with 14.61% for customers with online security.
- Customers using electronic check had a 45.29% churn rate, higher than the other payment-method groups.
- The month-to-month and Fiber optic group had a 54.61% churn rate (1,162 churned customers out of 2,128).
- Churn was highest in the monthly-charge band above 70 and up to 100: 37.82%. The rate was 28.05% for customers paying above 100, so the pattern did not keep increasing with every charge band.
- Churn rates by the number of optional services were: 0 services, 21.41%; 1, 45.76%; 2, 35.82%; 3, 27.37%; 4, 22.30%; 5, 12.43%; and 6, 5.28%.

The optional-service count covers six fields marked `Yes`: `OnlineSecurity`, `OnlineBackup`, `DeviceProtection`, `TechSupport`, `StreamingTV`, and `StreamingMovies`. It is a simple count, and it can also reflect which services are available to a customer.

These results describe differences between groups. They do not prove cause and effect. Contract type, tenure, service availability, monthly charges, and other customer characteristics may overlap, so they should be studied together before making business recommendations.

## Power BI Measures

The report includes measures for:

- Total Customers
- Churned Customers
- Retained Customers
- Churn Rate
- Retention Rate
- Average Monthly Charges
- Average Tenure (Months)

The three report pages are described in the Dashboard Preview section above.

## Project Files

```text
customer-churn-retention-analysis/
├── data/
│   ├── raw/                  # original dataset used locally
│   ├── processed/            # cleaned dataset used locally
│   └── telco_customer_churn_audit.xlsx
├── evidence/                 # supporting audit or analysis evidence
├── screenshots/              # dashboard images used in this README
├── python/
│   ├── 01_data_cleaning.py
│   └── 02_exploratory_analysis.py
├── reports/
│   └── python_eda/           # summary CSV files and charts
├── sql/                      # table setup, analysis, and validation queries
└── powerbi/
    └── customer_churn_retention.pbix
```

Only include the raw CSV, processed CSV, and audit workbook in the public repository if their sharing terms permit it. The folder list above describes the project layout; some local data files may be excluded from GitHub.

## How to Reproduce the Analysis

1. Install Python and the required packages:

   ```bash
   py -m pip install pandas matplotlib
   ```

2. Get the dataset from the source link above. Save the original CSV as `data/raw/telco_customer_churn_raw.csv`. Keep the original file unchanged.
3. From the project root, run the cleaning script:

   ```bash
   py python/01_data_cleaning.py
   ```

4. Run the exploratory analysis script:

   ```bash
   py python/02_exploratory_analysis.py
   ```

5. Create a PostgreSQL database and table using the included SQL setup script. Import `data/processed/telco_customer_churn_clean.csv`, then run the SQL analysis and validation scripts.
6. Open `powerbi/customer_churn_retention.pbix` in Power BI Desktop. If Power BI asks for the data source, point it to the processed CSV on your computer.

File paths may need to be updated for your computer. Run the SQL queries separately and check their results before using them in a report.

## Limitations

- This is descriptive analysis of an existing dataset, not a study that proves causes of churn.
- The 11 missing `TotalCharges` values were retained as missing. Analyses that use this field should account for them.
- Charge bands were chosen for this project; they are not official industry thresholds.
- No predictive churn model was built in this project.

