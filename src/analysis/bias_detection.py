def detect_bias_types(
    dataset_report,
    fairness_report
):
    """
    Detect major bias categories
    using rule-based thresholds
    """

    detected_biases = []

    # -----------------------------------
    # Representation Bias
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
            detected_biases.append(
                "Representation Bias"
            )

    # -----------------------------------
    # Demographic Bias
    # -----------------------------------

    dp_diff = abs(
        fairness_report.get(
            "demographic_parity_difference",
            0
        )
    )

    if dp_diff > 0.10:
        detected_biases.append(
            "Demographic Bias"
        )

    # -----------------------------------
    # Model Bias
    # -----------------------------------

    eo_diff = abs(
        fairness_report.get(
            "equalized_odds_difference",
            0
        )
    )

    if eo_diff > 0.05:
        detected_biases.append(
            "Model Bias"
        )

    if not detected_biases:
        detected_biases.append(
            "No Significant Bias Detected"
        )

    return detected_biases