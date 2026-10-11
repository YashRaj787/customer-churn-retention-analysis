
from pathlib import Path

import pandas as pd


# Locate the project and data files.
PROJECT_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = (
    PROJECT_DIR
    / "data"
    / "raw"
    / "telco_customer_churn_raw.csv"
)

OUTPUT_DIR = PROJECT_DIR / "data" / "processed"
OUTPUT_FILE = OUTPUT_DIR / "telco_customer_churn_clean.csv"

EXPECTED_ROWS = 7043

EXPECTED_COLUMNS = [
    "customerID",
    "gender",
    "SeniorCitizen",
    "Partner",
    "Dependents",
    "tenure",
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod",
    "MonthlyCharges",
    "TotalCharges",
    "Churn",
]

EXPECTED_CATEGORIES = {
    "gender": {"Female", "Male"},
    "Partner": {"Yes", "No"},
    "Dependents": {"Yes", "No"},
    "PhoneService": {"Yes", "No"},
    "MultipleLines": {"Yes", "No", "No phone service"},
    "InternetService": {"DSL", "Fiber optic", "No"},
    "OnlineSecurity": {"Yes", "No", "No internet service"},
    "OnlineBackup": {"Yes", "No", "No internet service"},
    "DeviceProtection": {"Yes", "No", "No internet service"},
    "TechSupport": {"Yes", "No", "No internet service"},
    "StreamingTV": {"Yes", "No", "No internet service"},
    "StreamingMovies": {"Yes", "No", "No internet service"},
    "Contract": {"Month-to-month", "One year", "Two year"},
    "PaperlessBilling": {"Yes", "No"},
    "PaymentMethod": {
        "Electronic check",
        "Mailed check",
        "Bank transfer (automatic)",
        "Credit card (automatic)",
    },
    "Churn": {"Yes", "No"},
}

EXPECTED_RANGES = {
    "SeniorCitizen": (0, 1),
    "tenure": (0, 72),
    "MonthlyCharges": (18.25, 118.75),
    "TotalCharges": (18.8, 8684.8),
}


def main():
    # 1. Confirm that the raw file exists.
    if not RAW_FILE.is_file():
        raise FileNotFoundError(
            f"Raw dataset not found: {RAW_FILE}"
        )

    # 2. Load the raw dataset.
    # Keep IDs and TotalCharges as text initially.
    df = pd.read_csv(
        RAW_FILE,
        dtype={
            "customerID": "string",
            "TotalCharges": "string",
        },
    )

    # 3. Verify the dataset structure.
    if list(df.columns) != EXPECTED_COLUMNS:
        raise ValueError(
            "Unexpected columns or column order. "
            "Stop and investigate."
        )

    if len(df) != EXPECTED_ROWS:
        raise ValueError(
            f"Expected {EXPECTED_ROWS} rows; found {len(df)}."
        )

    # 4. Remove surrounding whitespace from text fields.
    # Turn empty strings into proper missing values.
    text_columns = df.select_dtypes(
        include=["object", "string"]
    ).columns

    for column in text_columns:
        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
            .replace("", pd.NA)
        )

    # 5. Check categorical values against the audit.
    for column, expected_values in EXPECTED_CATEGORIES.items():
        actual_values = set(df[column].dropna().unique())
        unexpected = actual_values - expected_values

        if unexpected:
            raise ValueError(
                f"Unexpected values in {column}: {unexpected}"
            )

    # 6. Convert audited numeric columns to numeric types.
    numeric_columns = [
        "SeniorCitizen",
        "tenure",
        "MonthlyCharges",
        "TotalCharges",
    ]

    for column in numeric_columns:
        original = df[column]
        converted = pd.to_numeric(original, errors="coerce")

        invalid = original.notna() & converted.isna()

        if invalid.any():
            examples = original[invalid].drop_duplicates().head(5).tolist()
            raise ValueError(
                f"Unexpected non-numeric values in {column}: {examples}"
            )

        df[column] = converted

    # 7. Validate customer IDs.
    if df["customerID"].isna().any():
        raise ValueError("Missing customer IDs found.")

    if df["customerID"].nunique() != EXPECTED_ROWS:
        raise ValueError("Customer IDs are not all unique.")

    # 8. Verify the audited numeric ranges.
    for column, (expected_min, expected_max) in EXPECTED_RANGES.items():
        actual_min = df[column].min()
        actual_max = df[column].max()

        if actual_min != expected_min or actual_max != expected_max:
            raise ValueError(
                f"Unexpected range for {column}: "
                f"minimum={actual_min}, maximum={actual_max}"
            )

    # 9. Verify missing values.
    missing_counts = df.isna().sum()

    if missing_counts["TotalCharges"] != 11:
        raise ValueError(
            "Expected 11 missing TotalCharges values; found "
            f"{missing_counts['TotalCharges']}."
        )

    other_missing = missing_counts.drop("TotalCharges")
    other_missing = other_missing[other_missing > 0]

    if not other_missing.empty:
        raise ValueError(
            f"Unexpected missing values in other columns:\n{other_missing}"
        )

    # 10. Create the output folder and save a separate clean file.
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)

    # 11. Verify the saved output.
    saved_df = pd.read_csv(
        OUTPUT_FILE,
        dtype={"customerID": "string"},
    )

    if saved_df.shape != (7043, 21):
        raise ValueError(
            f"Unexpected saved dimensions: {saved_df.shape}"
        )

    if saved_df["customerID"].nunique() != 7043:
        raise ValueError("Saved output failed the unique-ID check.")

    if saved_df["TotalCharges"].isna().sum() != 11:
        raise ValueError("Saved output failed the missing-charge check.")

    print("Cleaning and validation completed successfully.")
    print(f"Output file: {OUTPUT_FILE}")
    print(f"Rows: {saved_df.shape[0]}")
    print(f"Columns: {saved_df.shape[1]}")
    print(f"Unique customer IDs: {saved_df['customerID'].nunique()}")
    print("Missing values:")
    print(missing_counts[missing_counts > 0])


if __name__ == "__main__":
    main()
