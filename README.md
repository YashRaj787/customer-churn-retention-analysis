# Customer Churn & Retention Analysis

An end-to-end data analytics project investigating customer churn patterns using Excel for initial data auditing, Python for reproducible cleaning and exploratory data analysis, PostgreSQL for SQL analysis, and Power BI for interactive reporting.

## Project Objective

Identify customer groups with different observed churn rates and translate the results into useful questions for retention analysis. The project is descriptive: it identifies patterns and associations, not proof that any particular factor causes churn.

## Dataset

- **Records:** 7,043 customers
- **Columns:** 21
- **Target field:** `Churn` (`Yes` / `No`)
- **Churned customers:** 1,869
- **Retained customers:** 5,174
- **Overall churn rate:** 26.54%

### Data quality and cleaning decisions

- Audited row and column counts, duplicate customer IDs, blank values, categorical values, numeric ranges, and cross-field relationships before cleaning.
- Found 11 blank or whitespace-only `TotalCharges` values. All 11 records had `tenure = 0` and `Churn = No`.
- Preserved these values as missing instead of replacing them with zero or deleting those customers.
- Cleaned surrounding whitespace and converted `TotalCharges` to numeric in a separate processed dataset.
- Kept the raw CSV unchanged.
- Validated that the processed dataset contains 7,043 rows, 21 columns, and 7,043 unique customer IDs.


## Tools Used

- **Excel:** initial audit, missing-value review, categorical-value audit, numeric-range audit, and cross-field checks
- **Python:** pandas for reproducible cleaning and exploratory analysis; Matplotlib for charts
- **PostgreSQL:** grouped churn analysis, combined-segment analysis, customer profiles, add-on counts, charge exposure, and final validation
- **Power BI:** interactive report and DAX measures

## Key Findings

### Overall

- **26.54%** of customers churned in the dataset.
- The dataset contains 1,869 churned and 5,174 retained customers.

### Contract type

| Contract | Customers | Churned | Observed churn rate |
|---|---:|---:|---:|
| Month-to-month | 3,875 | 1,655 | **42.71%** |
| One year | 1,473 | 166 | 11.27% |
| Two year | 1,695 | 48 | 2.83% |

### Tenure

| Tenure band | Customers | Churned | Observed churn rate |
|---|---:|---:|---:|
| 0–12 months | 2,186 | 1,037 | **47.44%** |
| 13–24 months | 1,024 | 294 | 28.71% |
| 25–48 months | 1,594 | 325 | 20.39% |
| 49–72 months | 2,239 | 213 | 9.51% |

### Internet service

| Internet service | Customers | Churned | Observed churn rate |
|---|---:|---:|---:|
| Fiber optic | 3,096 | 1,297 | **41.89%** |
| DSL | 2,421 | 459 | 18.96% |
| No internet service | 1,526 | 113 | 7.40% |

### Other observed patterns

- Customers without technical support had a 41.64% churn rate, versus 15.17% for customers with support.
- Customers without online security had a 41.77% churn rate, versus 14.61% for customers with online security.
- Electronic-check customers had a 45.29% churn rate, higher than the other recorded payment methods.
- Churn was 54.61% for the combined group of month-to-month contract and Fiber optic internet service.
- Churn by monthly charge band was not monotonic: 10.89% up to 35, 23.94% above 35 to 70, 37.82% above 70 to 100, and 28.05% above 100.

These are observed group-level associations. They should not be interpreted as causal effects. Contract type, tenure, service availability, charges, and customer characteristics may overlap and should be investigated together before recommending interventions.

## Power BI Report

The report contains three pages:

1. **Customer Overview** — overall KPIs and churn by contract, tenure, internet service, and payment method.
2. **Service Drivers** — churn by online security, technical support, and add-on service count.
3. **Customer Risk & Economics** — churn by monthly-charge band and demographic characteristics, with slicers for contract, payment method, and internet service.

Core DAX measures include Total Customers, Churned Customers, Retained Customers, Churn Rate, Retention Rate, Average Monthly Charges, and Average Tenure.

## Repository Structure

```text
customer-churn-retention-analysis/
├── data/
│   ├── raw/
│   │   └── telco_customer_churn_raw.csv
│   └── processed/
│       └── telco_customer_churn_clean.csv
├── python/
│   ├── 01_data_cleaning.py
│   └── 02_exploratory_analysis.py
├── sql/
│   └── numbered SQL analysis and validation scripts
├── reports/
│   └── python_eda/
│       ├── summary CSV files
│       └── charts/
└── powerbi/
    └── customer_churn_retention.pbix
```

## How to Reproduce

1. Install Python and the dependencies:

   ```bash
   py -m pip install pandas matplotlib
   ```

2. From the project root, run the cleaning script:

   ```bash
   py python/01_data_cleaning.py
   ```

3. Run exploratory analysis:

   ```bash
   py python/02_exploratory_analysis.py
   ```

4. Create the PostgreSQL database and table using the included SQL setup scripts; import `data/processed/telco_customer_churn_clean.csv` and run the numbered analysis queries.
5. Open the Power BI file. If refresh is needed on another computer, update the CSV source path to the processed file in this repository.

## Limitations

- This is an observational dataset; relationships do not establish causation.
- The 11 missing `TotalCharges` values were retained as missing. Interpret analyses of total charges with this limitation in mind.
- Charge bands are analyst-defined categories for descriptive comparison, not official industry thresholds.
- No predictive churn model has been built as part of this project.

## Dataset Source
The dataset used in this project is available from the [IBM Telco Customer Churn dataset repository](https://github.com/IBM/telco-customer-churn-on-icp4d/blob/master/data/Telco-Customer-Churn.csv).