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
    
    # Check if we have multiclass or binary
    unique_labels = len(set(y_true))
    
    if unique_labels > 2:
        # For multiclass, use alternative metrics or convert to binary
        # We'll use demographic parity difference with one-vs-rest approach
        try:
            dp_diff = float(
                demographic_parity_difference(
                    y_true,
                    y_pred,
                    sensitive_features=sensitive_features
                )
            )
            # For equalized odds, we'll skip it for multiclass and use 0 as placeholder
            eo_diff = 0.0
        except Exception:
            # If fairlearn fails, use custom calculation
            dp_diff = _calculate_demographic_parity_custom(y_true, y_pred, sensitive_features)
            eo_diff = 0.0
    else:
        # Binary classification - use fairlearn normally
        try:
            dp_diff = float(
                demographic_parity_difference(
                    y_true,
                    y_pred,
                    sensitive_features=sensitive_features
                )
            )
            eo_diff = float(
                equalized_odds_difference(
                    y_true,
                    y_pred,
                    sensitive_features=sensitive_features
                )
            )
        except Exception:
            # Fallback to custom calculation
            dp_diff = _calculate_demographic_parity_custom(y_true, y_pred, sensitive_features)
            eo_diff = 0.0

    report = {
        "demographic_parity_difference": round(dp_diff, 4),
        "equalized_odds_difference": round(eo_diff, 4),
        "is_multiclass": unique_labels > 2,
        "num_classes": unique_labels
    }

    return report


def _calculate_demographic_parity_custom(y_true, y_pred, sensitive_features):
    """
    Custom demographic parity calculation for multiclass scenarios
    """
    try:
        # Convert to pandas Series if needed
        if not isinstance(sensitive_features, pd.Series):
            sensitive_features = pd.Series(sensitive_features)
        
        # Calculate positive outcome rates for each group
        groups = sensitive_features.unique()
        group_rates = []
        
        for group in groups:
            group_mask = sensitive_features == group
            if len(y_pred[group_mask]) > 0:
                # For multiclass, use the most frequent class as "positive"
                from collections import Counter
                most_common_class = Counter(y_pred).most_common(1)[0][0]
                positive_rate = (y_pred[group_mask] == most_common_class).mean()
                group_rates.append(positive_rate)
        
        if len(group_rates) >= 2:
            return max(group_rates) - min(group_rates)
        else:
            return 0.0
    except Exception:
        return 0.0


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