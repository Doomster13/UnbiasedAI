import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score


def train_basic_model(df, target, protected_cols):
    """
    Train baseline model and evaluate subgroup performance
    """

    df = df.copy()

    # Encode target column
    le = LabelEncoder()
    df[target] = le.fit_transform(df[target])

    # Keep protected columns separately
    protected_data = df[protected_cols].copy()

    # Features and target
    X = df.drop(
        columns=[target, "intersectional"],
        errors="ignore"
    )

    y = df[target]

    # One-hot encode categorical features
    X = pd.get_dummies(X, drop_first=True)

    # Train-test split
    (
        X_train,
        X_test,
        y_train,
        y_test,
        protected_train,
        protected_test
    ) = train_test_split(
        X,
        y,
        protected_data,
        test_size=0.2,
        random_state=42
    )

    # Scale features while preserving column names
    scaler = StandardScaler()

    X_train_scaled = pd.DataFrame(
        scaler.fit_transform(X_train),
        columns=X_train.columns,
        index=X_train.index
    )

    X_test_scaled = pd.DataFrame(
        scaler.transform(X_test),
        columns=X_test.columns,
        index=X_test.index
    )

    # Train model
    model = LogisticRegression(
        max_iter=2000,
        random_state=42
    )

    model.fit(X_train_scaled, y_train)

    # Predictions
    y_pred = model.predict(X_test_scaled)

    # Overall metrics
    overall_report = {
        "accuracy": round(
            accuracy_score(y_test, y_pred),
            4
        ),
        "precision": round(
            precision_score(
                y_test,
                y_pred,
                average='weighted',
                zero_division=0
            ),
            4
        ),
        "recall": round(
            recall_score(
                y_test,
                y_pred,
                average='weighted',
                zero_division=0
            ),
            4
        )
    }

    return (
        model,
        X_test_scaled,
        y_test,
        y_pred,
        protected_test,
        overall_report
    )