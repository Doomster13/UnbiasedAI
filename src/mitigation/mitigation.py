def mitigation_advisor(
    fairness_report,
    severity_report,
    dataset_report
):
    """
    Suggest mitigation strategies
    based on detected fairness issues
    """

    suggestions = []

    dp_diff = abs(
        fairness_report.get(
            "demographic_parity_difference",
            0
        )
    )

    eo_diff = abs(
        fairness_report.get(
            "equalized_odds_difference",
            0
        )
    )

    severity_level = severity_report.get(
        "severity_level",
        "Low"
    )

    # -----------------------------------
    # Representation imbalance
    # -----------------------------------

    race_distribution = dataset_report.get(
        "race",
        {}
    ).get(
        "distribution",
        {}
    )

    if race_distribution:
        min_group_ratio = min(
            race_distribution.values()
        )

        if min_group_ratio < 0.05:
            suggestions.append(
                "Apply reweighing or resampling "
                "for underrepresented groups"
            )

    # -----------------------------------
    # Demographic parity issue
    # -----------------------------------

    if dp_diff > 0.10:
        suggestions.append(
            "Use threshold optimization "
            "to reduce demographic disparity"
        )

    # -----------------------------------
    # Equalized odds issue
    # -----------------------------------

    if eo_diff > 0.05:
        suggestions.append(
            "Apply post-processing fairness "
            "constraints (Equalized Odds)"
        )

    # -----------------------------------
    # Severe bias
    # -----------------------------------

    if severity_level == "High":
        suggestions.append(
            "Perform fairness-aware retraining "
            "using Fairlearn or AIF360"
        )

    if not suggestions:
        suggestions.append(
            "Current fairness levels are acceptable. "
            "Monitor regularly."
        )

    return {
        "recommended_actions": suggestions
    }