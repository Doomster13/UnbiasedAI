import pandas as pd
import shap


def root_cause_analysis(model, X_test):
    """
    Identify top contributing features
    using SHAP values
    """

    try:
        # Create SHAP explainer
        explainer = shap.Explainer(
            model,
            X_test
        )

        shap_values = explainer(X_test)

        # Mean absolute SHAP importance
        importance = pd.DataFrame({
            "feature": X_test.columns,
            "importance": abs(
                shap_values.values
            ).mean(axis=0)
        })

        importance = importance.sort_values(
            by="importance",
            ascending=False
        )

        top_features = (
            importance.head(10)
            .to_dict(orient="records")
        )

        return {
            "top_contributing_features":
                top_features
        }

    except Exception as e:
        return {
            "error": str(e)
        }