def calculate_bias_severity(
    dataset_report,
    fairness_report,
    subgroup_report
):
    """
    Calculate overall bias severity score

    Factors:
    - representation imbalance
    - fairness metric gaps
    - subgroup performance gaps
    """

    score = 0

    # ----------------------------------
    # 1. Fairness metric contribution
    # ----------------------------------

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

    score += dp_diff * 0.4
    score += eo_diff * 0.3

    # ----------------------------------
    # 2. Representation imbalance
    # ----------------------------------

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
            score += 0.2

    # ----------------------------------
    # 3. Subgroup performance gap
    # ----------------------------------

    accuracies = []

    for group, metrics in subgroup_report.items():
        accuracies.append(
            metrics.get("accuracy", 0)
        )

    if accuracies:
        performance_gap = max(accuracies) - min(accuracies)

        if performance_gap > 0.10:
            score += 0.2

    # ----------------------------------
    # Final severity normalization
    # ----------------------------------

    score = round(min(score, 1.0), 4)

    if score < 0.30:
        level = "Low"
    elif score < 0.60:
        level = "Moderate"
    else:
        level = "High"

    confidence = round(
        min(0.80 + score * 0.2, 0.99),
        2
    )

    return {
        "severity_score": score,
        "severity_level": level,
        "confidence": confidence
    }