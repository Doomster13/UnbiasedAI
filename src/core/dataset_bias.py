from scipy.stats import chisquare


def dataset_bias_analysis(df, protected_cols):
    """
    Analyze dataset-level bias:
    - representation imbalance
    - chi-square goodness-of-fit test
    - intersectional imbalance
    """

    report = {}

    for col in protected_cols:
        # normalized distribution
        distribution = df[col].value_counts(normalize=True).to_dict()

        # actual observed counts
        counts = df[col].value_counts()

        # expected uniform distribution
        expected = [counts.sum() / len(counts)] * len(counts)

        # proper chi-square test
        chi_stat, p_value = chisquare(
            f_obs=counts,
            f_exp=expected
        )

        report[col] = {
            "distribution": distribution,
            "chi_square_p_value": round(float(p_value), 6)
        }

    # intersectional distribution
    if "intersectional" in df.columns:
        report["intersectional"] = {
            "distribution": (
                df["intersectional"]
                .value_counts(normalize=True)
                .to_dict()
            )
        }

    return report