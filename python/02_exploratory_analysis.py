"""Exploratory analysis for the IBM Telco Customer Churn project.

Expected location inside the project:
    python/02_exploratory_analysis.py

Reads the cleaned CSV, validates key assumptions, writes summary tables and
charts to reports/python_eda/, and never modifies the raw or cleaned datasets.
"""

from pathlib import Path
import sys

import pandas as pd
import matplotlib.pyplot as plt



PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_DIR / "data" / "processed" / "telco_customer_churn_clean.csv"
OUTPUT_DIR = PROJECT_DIR / "reports" / "python_eda"
CHART_DIR = OUTPUT_DIR / "charts"

EXPECTED_COLUMNS = [
    "customerID", "gender", "SeniorCitizen", "Partner", "Dependents",
    "tenure", "PhoneService", "MultipleLines", "InternetService",
    "OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport",
    "StreamingTV", "StreamingMovies", "Contract", "PaperlessBilling",
    "PaymentMethod", "MonthlyCharges", "TotalCharges", "Churn",
]

if not DATA_FILE.exists():
    raise FileNotFoundError(
        f"Cleaned dataset not found: {DATA_FILE}\n"
        "Confirm that 01_data_cleaning.py ran successfully and created the file."
    )

df = pd.read_csv(DATA_FILE, dtype={"customerID": "string"})

if list(df.columns) != EXPECTED_COLUMNS:
    raise ValueError("Column names or order differ from the audited 21-column dataset.")
if df.shape != (7043, 21):
    raise ValueError(f"Expected 7,043 rows and 21 columns; found {df.shape}.")
if df["customerID"].isna().any():
    raise ValueError("Customer ID contains missing values.")
if df["customerID"].duplicated().any():
    raise ValueError("Duplicate Customer IDs were found.")

for column in ["SeniorCitizen", "tenure", "MonthlyCharges"]:
    df[column] = pd.to_numeric(df[column], errors="raise")

raw_total_charges = df["TotalCharges"].copy()
numeric_total_charges = pd.to_numeric(raw_total_charges, errors="coerce")
invalid_total_charges = raw_total_charges.notna() & numeric_total_charges.isna()
if invalid_total_charges.any():
    raise ValueError("Non-empty TotalCharges values failed numeric conversion.")
df["TotalCharges"] = numeric_total_charges

if not set(df["Churn"].dropna().unique()).issubset({"Yes", "No"}):
    raise ValueError("Unexpected values found in Churn.")
if not set(df["SeniorCitizen"].dropna().unique()).issubset({0, 1}):
    raise ValueError("SeniorCitizen has values other than 0 and 1.")
if not df["tenure"].between(0, 72).all():
    raise ValueError("Tenure contains values outside 0-72 months.")
if (df["MonthlyCharges"] < 0).any():
    raise ValueError("Negative MonthlyCharges values were found.")
if (df["TotalCharges"].dropna() < 0).any():
    raise ValueError("Negative TotalCharges values were found.")

missing_total = df["TotalCharges"].isna()
if int(missing_total.sum()) != 11:
    raise ValueError(f"Expected 11 missing TotalCharges values; found {int(missing_total.sum())}.")
if df.drop(columns=["TotalCharges"]).isna().any().any():
    raise ValueError("Missing values were found outside TotalCharges; investigate before EDA.")
if not (df.loc[missing_total, "tenure"] == 0).all():
    raise ValueError("At least one missing TotalCharges record has nonzero tenure.")
if not (df.loc[missing_total, "Churn"] == "No").all():
    raise ValueError("At least one missing TotalCharges record has Churn other than No.")

churned_count = int(df["Churn"].eq("Yes").sum())
retained_count = int(df["Churn"].eq("No").sum())
if (churned_count, retained_count) != (1869, 5174):
    raise ValueError(
        f"Churn counts differ from the completed audit: Yes={churned_count}, No={retained_count}."
    )

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CHART_DIR.mkdir(parents=True, exist_ok=True)


def summarize_churn(data: pd.DataFrame, group_columns: list[str]) -> pd.DataFrame:
    """Count customers and calculate observed churn rate for each group."""
    working = data.copy()
    working["_churned_flag"] = working["Churn"].eq("Yes").astype(int)
    working["_retained_flag"] = working["Churn"].eq("No").astype(int)

    result = (
        working.groupby(group_columns, dropna=False, observed=True)
        .agg(
            total_customers=("customerID", "size"),
            churned_customers=("_churned_flag", "sum"),
            retained_customers=("_retained_flag", "sum"),
            avg_monthly_charges=("MonthlyCharges", "mean"),
        )
        .reset_index()
    )
    result["churn_rate_pct"] = (
        100 * result["churned_customers"] / result["total_customers"]
    ).round(2)
    result["avg_monthly_charges"] = result["avg_monthly_charges"].round(2)
    return result


def save_csv(data: pd.DataFrame, filename: str) -> None:
    data.to_csv(OUTPUT_DIR / filename, index=False)


def plot_churn_rate(
    summary: pd.DataFrame,
    category_column: str,
    title: str,
    filename: str,
    sort_by_rate: bool = False,
) -> None:
    """Save one legible bar chart per customer breakdown."""
    plot_data = summary.copy()
    if sort_by_rate:
        plot_data = plot_data.sort_values("churn_rate_pct", ascending=False)

    labels = plot_data[category_column].astype(str)
    values = plot_data["churn_rate_pct"]
    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(labels, values)
    ax.set_title(title)
    ax.set_xlabel(category_column.replace("_", " ").title())
    ax.set_ylabel("Observed churn rate (%)")
    ax.set_ylim(0, max(5, float(values.max()) * 1.18))
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    ax.set_axisbelow(True)
    ax.tick_params(axis="x", labelrotation=20)
    for bar, value in zip(bars, values):
        ax.annotate(
            f"{value:.1f}%",
            (bar.get_x() + bar.get_width() / 2, bar.get_height()),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9,
        )
    fig.tight_layout()
    fig.savefig(CHART_DIR / filename, dpi=160, bbox_inches="tight")
    plt.close(fig)



total_customers = len(df)
overall_summary = pd.DataFrame([{
    "total_customers": total_customers,
    "churned_customers": churned_count,
    "retained_customers": retained_count,
    "churn_rate_pct": round(100 * churned_count / total_customers, 2),
    "retention_rate_pct": round(100 * retained_count / total_customers, 2),
    "missing_total_charges": int(df["TotalCharges"].isna().sum()),
    "unique_customer_ids": int(df["customerID"].nunique()),
}])
save_csv(overall_summary, "overall_summary.csv")

missing_audit = (
    df.isna().sum()
    .rename("missing_count")
    .reset_index()
    .rename(columns={"index": "field_name"})
)
save_csv(missing_audit, "missing_value_audit.csv")

quality_checks = [
    ("Rows", len(df)),
    ("Columns", len(df.columns)),
    ("Unique customer IDs", int(df["customerID"].nunique())),
    ("Duplicate customer IDs", int(df["customerID"].duplicated().sum())),
    ("Churned customers", churned_count),
    ("Retained customers", retained_count),
    ("Missing TotalCharges", int(df["TotalCharges"].isna().sum())),
    ("Missing values outside TotalCharges", int(df.drop(columns=["TotalCharges"]).isna().sum().sum())),
    ("Zero-tenure customers", int(df["tenure"].eq(0).sum())),
    ("Negative MonthlyCharges", int(df["MonthlyCharges"].lt(0).sum())),
    ("Negative non-missing TotalCharges", int(df["TotalCharges"].dropna().lt(0).sum())),
]
save_csv(pd.DataFrame(quality_checks, columns=["check", "result"]), "data_quality_validation.csv")



contract_order = {"Month-to-month": 1, "One year": 2, "Two year": 3}
contract_summary = summarize_churn(df, ["Contract"])
contract_summary["_sort"] = contract_summary["Contract"].map(contract_order).fillna(99)
contract_summary = contract_summary.sort_values("_sort").drop(columns="_sort")
save_csv(contract_summary, "churn_by_contract.csv")

tenure_labels = ["0-12 months", "13-24 months", "25-48 months", "49-72 months"]
df["tenure_band"] = pd.cut(
    df["tenure"],
    bins=[-1, 12, 24, 48, 72],
    labels=tenure_labels,
    ordered=True,
)
tenure_summary = summarize_churn(df, ["tenure_band"])
tenure_summary["_sort"] = tenure_summary["tenure_band"].astype(str).map(
    {label: index for index, label in enumerate(tenure_labels)}
)
tenure_summary = tenure_summary.sort_values("_sort").drop(columns="_sort")
save_csv(tenure_summary, "churn_by_tenure_band.csv")

charge_labels = ["Up to 35", "Above 35 to 70", "Above 70 to 100", "Above 100"]
df["monthly_charge_band"] = pd.cut(
    df["MonthlyCharges"],
    bins=[-float("inf"), 35, 70, 100, float("inf")],
    labels=charge_labels,
    ordered=True,
)
charge_summary = summarize_churn(df, ["monthly_charge_band"])
charge_summary["_sort"] = charge_summary["monthly_charge_band"].astype(str).map(
    {label: index for index, label in enumerate(charge_labels)}
)
charge_summary = charge_summary.sort_values("_sort").drop(columns="_sort")
save_csv(charge_summary, "churn_by_monthly_charge_band.csv")

simple_breakdowns = {
    "internet_service": ("InternetService", "churn_by_internet_service.csv"),
    "tech_support": ("TechSupport", "churn_by_tech_support.csv"),
    "payment_method": ("PaymentMethod", "churn_by_payment_method.csv"),
    "online_security": ("OnlineSecurity", "churn_by_online_security.csv"),
}
summary_by_field: dict[str, pd.DataFrame] = {}
for key, (column, filename) in simple_breakdowns.items():
    result = summarize_churn(df, [column]).sort_values("churn_rate_pct", ascending=False)
    save_csv(result, filename)
    summary_by_field[key] = result

contract_internet_summary = summarize_churn(df, ["Contract", "InternetService"])
contract_internet_summary["_contract_order"] = contract_internet_summary["Contract"].map(contract_order).fillna(99)
contract_internet_summary = contract_internet_summary.sort_values(
    ["_contract_order", "InternetService"]
).drop(columns="_contract_order")
save_csv(contract_internet_summary, "churn_by_contract_and_internet_service.csv")

contract_tenure_summary = summarize_churn(df, ["Contract", "tenure_band"])
contract_tenure_summary["_contract_order"] = contract_tenure_summary["Contract"].map(contract_order).fillna(99)
contract_tenure_summary["_tenure_order"] = contract_tenure_summary["tenure_band"].astype(str).map(
    {label: index for index, label in enumerate(tenure_labels)}
)
contract_tenure_summary = contract_tenure_summary.sort_values(
    ["_contract_order", "_tenure_order"]
).drop(columns=["_contract_order", "_tenure_order"])
save_csv(contract_tenure_summary, "churn_by_contract_and_tenure.csv")

contract_payment_summary = summarize_churn(df, ["Contract", "PaymentMethod"])
contract_payment_summary["_contract_order"] = contract_payment_summary["Contract"].map(contract_order).fillna(99)
contract_payment_summary = contract_payment_summary.sort_values(
    ["_contract_order", "churn_rate_pct"], ascending=[True, False]
).drop(columns="_contract_order")
save_csv(contract_payment_summary, "churn_by_contract_and_payment_method.csv")



demographic_columns = [
    "gender", "SeniorCitizen", "Partner", "Dependents", "PaperlessBilling"
]
demographic_tables = []
for column in demographic_columns:
    result = summarize_churn(df, [column]).rename(columns={column: "category_value"})
    result.insert(0, "field_name", column)
    demographic_tables.append(result)
demographic_summary = pd.concat(demographic_tables, ignore_index=True)
save_csv(demographic_summary, "churn_by_demographic_factors.csv")

service_columns = [
    "PhoneService", "MultipleLines", "OnlineSecurity", "OnlineBackup",
    "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies",
]
service_tables = []
for column in service_columns:
    result = summarize_churn(df, [column]).rename(columns={column: "service_status"})
    result.insert(0, "service", column)
    service_tables.append(result)
service_summary = pd.concat(service_tables, ignore_index=True)
save_csv(service_summary, "churn_by_service_status.csv")


addon_columns = [
    "OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport",
    "StreamingTV", "StreamingMovies",
]
df["addon_count"] = df[addon_columns].eq("Yes").sum(axis=1)
addon_summary = summarize_churn(df, ["addon_count"]).sort_values("addon_count")
save_csv(addon_summary, "churn_by_addon_count.csv")



profile_summary = (
    df.groupby("Churn", observed=True)
    .agg(
        total_customers=("customerID", "size"),
        avg_tenure_months=("tenure", "mean"),
        median_tenure_months=("tenure", "median"),
        avg_monthly_charges=("MonthlyCharges", "mean"),
        median_monthly_charges=("MonthlyCharges", "median"),
        customers_with_total_charges=("TotalCharges", "count"),
        avg_total_charges=("TotalCharges", "mean"),
        median_total_charges=("TotalCharges", "median"),
    )
    .reset_index()
)
for column in [
    "avg_tenure_months", "median_tenure_months", "avg_monthly_charges",
    "median_monthly_charges", "avg_total_charges", "median_total_charges",
]:
    profile_summary[column] = profile_summary[column].round(2)
profile_summary["_sort"] = profile_summary["Churn"].map({"Yes": 1, "No": 2}).fillna(3)
profile_summary = profile_summary.sort_values("_sort").drop(columns="_sort")
save_csv(profile_summary, "churned_vs_retained_profile.csv")

monthly_exposure = (
    df.groupby("Churn", observed=True)
    .agg(
        total_customers=("customerID", "size"),
        sum_monthly_charges=("MonthlyCharges", "sum"),
        avg_monthly_charges=("MonthlyCharges", "mean"),
        avg_total_charges=("TotalCharges", "mean"),
    )
    .reset_index()
)
monthly_exposure["share_of_current_monthly_charges_pct"] = (
    100 * monthly_exposure["sum_monthly_charges"] / df["MonthlyCharges"].sum()
).round(2)
for column in ["sum_monthly_charges", "avg_monthly_charges", "avg_total_charges"]:
    monthly_exposure[column] = monthly_exposure[column].round(2)
monthly_exposure["_sort"] = monthly_exposure["Churn"].map({"Yes": 1, "No": 2}).fillna(3)
monthly_exposure = monthly_exposure.sort_values("_sort").drop(columns="_sort")
save_csv(monthly_exposure, "monthly_charge_exposure_by_churn.csv")

# Rank combinations by observed churn rate, excluding very small groups (<50 customers).
profile_columns = ["Contract", "InternetService", "OnlineSecurity", "TechSupport"]
high_churn_profiles = summarize_churn(df, profile_columns)
high_churn_profiles = high_churn_profiles[high_churn_profiles["total_customers"] >= 50].copy()
high_churn_profiles = high_churn_profiles.sort_values(
    ["churn_rate_pct", "total_customers"], ascending=[False, False]
).reset_index(drop=True)
high_churn_profiles.insert(0, "observed_churn_rate_rank", range(1, len(high_churn_profiles) + 1))
save_csv(high_churn_profiles, "high_churn_customer_profiles_min_50.csv")

plot_churn_rate(
    contract_summary, "Contract", "Observed Churn Rate by Contract Type",
    "churn_rate_by_contract.png"
)
plot_churn_rate(
    tenure_summary, "tenure_band", "Observed Churn Rate by Tenure Band",
    "churn_rate_by_tenure_band.png"
)
plot_churn_rate(
    charge_summary, "monthly_charge_band", "Observed Churn Rate by Monthly Charge Band",
    "churn_rate_by_monthly_charge_band.png"
)
plot_churn_rate(
    summary_by_field["internet_service"], "InternetService",
    "Observed Churn Rate by Internet Service", "churn_rate_by_internet_service.png",
    sort_by_rate=True
)
plot_churn_rate(
    summary_by_field["tech_support"], "TechSupport",
    "Observed Churn Rate by Tech Support", "churn_rate_by_tech_support.png",
    sort_by_rate=True
)
plot_churn_rate(
    summary_by_field["payment_method"], "PaymentMethod",
    "Observed Churn Rate by Payment Method", "churn_rate_by_payment_method.png",
    sort_by_rate=True
)
plot_churn_rate(
    summary_by_field["online_security"], "OnlineSecurity",
    "Observed Churn Rate by Online Security", "churn_rate_by_online_security.png",
    sort_by_rate=True
)



print("Python EDA completed successfully.")
print(f"Input file: {DATA_FILE}")
print(f"Rows: {len(df):,} | Columns: {len(df.columns)}")
print(f"Unique customer IDs: {df['customerID'].nunique():,}")
print(f"Churned: {churned_count:,} | Retained: {retained_count:,}")
print(f"Overall churn rate: {100 * churned_count / len(df):.2f}%")
print(f"Missing TotalCharges retained: {df['TotalCharges'].isna().sum()}")
print(f"Tables and charts saved to: {OUTPUT_DIR}")
print("\nChurn by contract:")
print(contract_summary[["Contract", "total_customers", "churned_customers", "churn_rate_pct"]].to_string(index=False))
print("\nChurn by tenure band:")
print(tenure_summary[["tenure_band", "total_customers", "churned_customers", "churn_rate_pct"]].to_string(index=False))
print("\nReminder: group differences are descriptive associations, not proof of causation.")
