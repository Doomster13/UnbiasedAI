import pandas as pd


def load_data(path):
    """
    Load dataset from CSV
    """
    return pd.read_csv(path)


def detect_target_column(df):
    """
    Automatically detect likely target column
    using flexible keyword matching
    """

    target_keywords = [
        "target",
        "label",
        "class",
        "outcome",
        "salary",
        "income",
        "price",
        "score",
        "amount",
        "revenue",
        "sales",
        "profit",
        "approved",
        "hired",
        "default",
        "loan",
        "status",
        "churn",
        "fraud",
        "diabetes",
        "diagnosis",
        "result"
    ]

    for col in df.columns:
        col_lower = col.lower()

        for keyword in target_keywords:
            if keyword in col_lower:
                return col

    return None


def detect_protected_attributes(df):
    """
    Automatically detect protected attributes

    Prioritize engineered columns like age_group
    instead of raw numeric columns like age
    """

    protected_keywords = [
        "sex",
        "gender",
        "race",
        "ethnicity",
        "religion",
        "marital",
        "nationality",
        "disability",
        "age_group"
    ]

    protected = []

    for col in df.columns:
        col_lower = col.lower()

        # Skip raw age if age_group already exists
        if col_lower == "age" and "age_group" in df.columns:
            continue

        for keyword in protected_keywords:
            if keyword in col_lower:
                protected.append(col)
                break

    return protected


def detect_task_type(df, target):
    """
    Detect whether task is classification or regression
    """

    unique_values = df[target].nunique()

    if unique_values <= 10:
        return "classification"

    return "regression"


def handle_missing_values(df):
    """
    Fill missing values:
    - categorical → 'Unknown'
    - numeric → median
    """

    df = df.copy()

    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(df[col].median())
        else:
            df[col] = df[col].fillna("Unknown")

    return df


def create_age_group(df):
    """
    Dynamically create age groups using quantiles
    instead of using raw age values
    """

    df = df.copy()

    if "age" in df.columns:
        try:
            df["age_group"] = pd.qcut(
                df["age"],
                q=4,
                labels=[
                    "Young",
                    "Adult",
                    "Middle_Age",
                    "Senior"
                ],
                duplicates="drop"
            )
        except Exception:
            print("Warning: Could not create age_group column.")

    return df


def create_intersectional_group(df, protected_cols):
    """
    Create intersectional protected group column

    Example:
    Young_Married_White_Male
    Adult_Single_Black_Female
    """

    df = df.copy()

    if len(protected_cols) >= 2:
        df["intersectional"] = (
            df[protected_cols]
            .astype(str)
            .agg("_".join, axis=1)
        )

    return df


def preprocess_data(path):
    """
    Full preprocessing pipeline

    Flow:
    load dataset
    → handle missing values
    → create age groups
    → detect target column
    → detect protected attributes
    → detect task type
    → create intersectional groups
    """

    # Step 1: Load dataset
    df = load_data(path)

    # Step 2: Handle missing values
    df = handle_missing_values(df)

    # Step 3: Create age groups before protected detection
    df = create_age_group(df)

    # Step 4: Detect target column
    target = detect_target_column(df)

    if not target:
        raise ValueError(
            "Target column could not be detected automatically."
        )

    # Step 5: Detect protected attributes
    protected = detect_protected_attributes(df)

    # Step 6: Detect task type
    task_type = detect_task_type(df, target)

    # Step 7: Create intersectional groups
    df = create_intersectional_group(df, protected)

    return df, target, protected, task_type