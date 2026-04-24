import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score
)

from fairlearn.metrics import (
    demographic_parity_difference,
    equalized_odds_difference
)


def fairness_metrics(y_true, y_pred, sensitive_features):
    """
    Compute core fairness metrics
    """

    report = {
        "demographic_parity_difference": round(
            float(
                demographic_parity_difference(
                    y_true,
                    y_pred,
                    sensitive_features=sensitive_features
                )
            ),
            4
        ),

        "equalized_odds_difference": round(
            float(
                equalized_odds_difference(
                    y_true,
                    y_pred,
                    sensitive_features=sensitive_features
                )
            ),
            4
        )
    }

    return report


def subgroup_performance_analysis(
    y_true,
    y_pred,
    protected_test,
    primary_protected
):
    """
    Analyze model performance for each subgroup

    Example:
    Male vs Female
    White vs Black
    """

    results = {}

    group_values = protected_test[primary_protected].unique()

    for group in group_values:
        mask = protected_test[primary_protected] == group

        y_true_group = y_true[mask]
        y_pred_group = y_pred[mask]

        if len(y_true_group) == 0:
            continue

        results[str(group)] = {
            "accuracy": round(
                accuracy_score(
                    y_true_group,
                    y_pred_group
                ),
                4
            ),

            "precision": round(
                precision_score(
                    y_true_group,
                    y_pred_group,
                    average='weighted',
                    zero_division=0
                ),
                4
            ),

            "recall": round(
                recall_score(
                    y_true_group,
                    y_pred_group,
                    average='weighted',
                    zero_division=0
                ),
                4
            )
        }

    return results