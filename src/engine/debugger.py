from src.core.preprocessing import preprocess_data
from src.core.dataset_bias import dataset_bias_analysis
from src.core.model_bias import train_basic_model
from src.analysis.severity import calculate_bias_severity
from src.core.metrics import (
    fairness_metrics,
    subgroup_performance_analysis
)

from src.analysis.bias_detection import detect_bias_types
from src.analysis.explanation import explain_bias, generate_bias_summary
from src.mitigation.suggestions import generate_mitigation_suggestions, generate_implementation_plan, format_suggestions_for_display


class BiasDebugger:
    def __init__(self, path):
        self.path = path

    def run(self):
        # Step 1: preprocessing
        df, target, protected, task_type = preprocess_data(
            self.path
        )

        # Step 2: dataset bias
        dataset_report = dataset_bias_analysis(
            df,
            protected
        )

        # Step 3: model training
        (
            model,
            X_test,
            y_test,
            y_pred,
            protected_test,
            overall_model_report
        ) = train_basic_model(
            df,
            target,
            protected
        )

        # Step 4: fairness metrics
        fairness_report = fairness_metrics(
            y_test,
            y_pred,
            sensitive_features=protected_test[
                protected[0]
            ]
        )

        # Step 5: subgroup analysis
        subgroup_report = subgroup_performance_analysis(
            y_test,
            y_pred,
            protected_test,
            primary_protected=protected[0]
        )

        # Step 6: bias detection
        bias_types = detect_bias_types(
            dataset_report,
            fairness_report
        )

        # Step 7: severity analysis
        severity_report = calculate_bias_severity(
            dataset_report,
            fairness_report,
            subgroup_report
        )

        # Step 8: bias explanations
        bias_explanations = explain_bias(
            dataset_report,
            fairness_report,
            subgroup_report,
            bias_types
        )

        # Step 9: bias summary
        bias_summary = generate_bias_summary(
            bias_types,
            severity_report
        )

        # Step 10: mitigation suggestions
        mitigation_suggestions = generate_mitigation_suggestions(
            bias_types,
            dataset_report,
            fairness_report,
            subgroup_report,
            severity_report
        )

        # Step 11: implementation plan
        implementation_plan = generate_implementation_plan(
            mitigation_suggestions,
            severity_report
        )

        # Step 12: formatted suggestions for display
        formatted_suggestions = format_suggestions_for_display(
            mitigation_suggestions,
            implementation_plan
        )

        # Final report
        return {
            "severity_analysis": severity_report,
            "bias_summary": bias_summary,
            "bias_explanations": bias_explanations,
            "mitigation_suggestions": formatted_suggestions,
            "implementation_plan": implementation_plan,

            "target": target,
            "protected_attributes": protected,
            "task_type": task_type,

            "dataset_bias": dataset_report,

            "overall_model_performance":
                overall_model_report,

            "fairness_metrics":
                fairness_report,

            "subgroup_performance":
                subgroup_report,

            "detected_biases":
                bias_types}