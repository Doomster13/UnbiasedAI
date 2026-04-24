def explain_bias(
    dataset_report,
    fairness_report,
    subgroup_report,
    detected_biases
):
    """
    Generate human-readable explanations for detected biases
    
    For each bias type detected, provide:
    - What the bias means
    - Why it occurs in this dataset
    - Which groups are affected
    - Evidence from the analysis
    """
    
    explanations = []
    
    for bias in detected_biases:
        if bias == "Representation Bias":
            explanations.append(explain_representation_bias(dataset_report))
        elif bias == "Demographic Bias":
            explanations.append(explain_demographic_bias(fairness_report))
        elif bias == "Model Bias":
            explanations.append(explain_model_bias(fairness_report, subgroup_report))
        elif bias == "No Significant Bias Detected":
            explanations.append("The dataset appears to have balanced representation and fair model performance across different demographic groups.")
    
    return explanations


def explain_representation_bias(dataset_report):
    """
    Explain representation bias in the dataset
    """
    
    explanation = "**Representation Bias Detected**\n\n"
    explanation += "This bias occurs when certain demographic groups are significantly underrepresented in the dataset.\n\n"
    
    # Find the most imbalanced protected attribute
    most_imbalanced = None
    max_imbalance = 0
    
    for attr, data in dataset_report.items():
        if attr == "intersectional":
            continue
            
        distribution = data.get("distribution", {})
        if distribution:
            min_ratio = min(distribution.values())
            if min_ratio < max_imbalance or max_imbalance == 0:
                max_imbalance = min_ratio
                most_imbalanced = attr
    
    if most_imbalanced:
        distribution = dataset_report[most_imbalanced]["distribution"]
        explanation += f"**Most affected attribute:** {most_imbalanced}\n\n"
        explanation += "**Group distribution:**\n"
        
        for group, ratio in distribution.items():
            percentage = ratio * 100
            if ratio < 0.05:
                explanation += f"- {group}: {percentage:.1f}% ⚠️ *Critically low*\n"
            elif ratio < 0.10:
                explanation += f"- {group}: {percentage:.1f}% ⚠️ *Low representation*\n"
            else:
                explanation += f"- {group}: {percentage:.1f}%\n"
        
        explanation += f"\n**Statistical evidence:** Chi-square test p-value = {dataset_report[most_imbalanced]['chi_square_p_value']}\n"
        
        if dataset_report[most_imbalanced]['chi_square_p_value'] < 0.05:
            explanation += "The distribution is significantly different from what would be expected in a balanced dataset.\n"
    
    explanation += "\n**Why this matters:** Underrepresented groups may lead to poor model performance and unfair outcomes for these populations."
    
    return explanation


def explain_demographic_bias(fairness_report):
    """
    Explain demographic parity bias
    """
    
    explanation = "**Demographic Bias Detected**\n\n"
    explanation += "This bias occurs when different demographic groups receive different outcomes at different rates, regardless of their actual qualifications.\n\n"
    
    dp_diff = fairness_report.get("demographic_parity_difference", 0)
    
    explanation += f"**Demographic Parity Difference:** {dp_diff:.4f}\n\n"
    
    if dp_diff > 0.15:
        explanation += "⚠️ **High bias level:** There's a substantial difference in outcome rates between demographic groups.\n"
    elif dp_diff > 0.10:
        explanation += "⚠️ **Moderate bias level:** There's a noticeable difference in outcome rates between demographic groups.\n"
    else:
        explanation += "⚠️ **Low bias level:** There's a small but significant difference in outcome rates between demographic groups.\n"
    
    explanation += "\n**What this means:** Some groups are more likely to receive positive outcomes than others, even when they have similar characteristics.\n"
    explanation += "**Example scenario:** If this is a loan approval dataset, one demographic group might be approved at 70% rate while another group is approved at only 50% rate."
    
    return explanation


def explain_model_bias(fairness_report, subgroup_report):
    """
    Explain model performance bias
    """
    
    explanation = "**Model Performance Bias Detected**\n\n"
    explanation += "This bias occurs when the model performs differently (better or worse) for different demographic groups.\n\n"
    
    eo_diff = fairness_report.get("equalized_odds_difference", 0)
    explanation += f"**Equalized Odds Difference:** {eo_diff:.4f}\n\n"
    
    # Find groups with biggest performance gaps
    accuracies = {}
    for group, metrics in subgroup_report.items():
        accuracies[group] = metrics.get("accuracy", 0)
    
    if accuracies:
        max_acc = max(accuracies.values())
        min_acc = min(accuracies.values())
        gap = max_acc - min_acc
        
        explanation += f"**Performance Gap:** {gap:.4f} ({gap*100:.1f}% difference)\n\n"
        
        explanation += "**Group Performance:**\n"
        for group, acc in sorted(accuracies.items(), key=lambda x: x[1], reverse=True):
            explanation += f"- {group}: {acc*100:.1f}% accuracy\n"
        
        if gap > 0.15:
            explanation += "\n⚠️ **High bias level:** The model performs substantially differently across groups.\n"
        elif gap > 0.10:
            explanation += "\n⚠️ **Moderate bias level:** The model shows noticeable performance differences.\n"
        else:
            explanation += "\n⚠️ **Low bias level:** The model shows small but significant performance differences.\n"
    
    explanation += "\n**Why this happens:** The model may have learned patterns that work well for majority groups but poorly for minority groups due to training data imbalance or feature interactions.\n"
    explanation += "**Real-world impact:** Some groups may experience more errors (false positives or false negatives) than others, leading to unfair treatment."
    
    return explanation


def generate_bias_summary(detected_biases, severity_report):
    """
    Generate a concise summary of all detected biases
    """
    
    summary = f"## Bias Analysis Summary\n\n"
    summary += f"**Severity Level:** {severity_report['severity_level']} (Score: {severity_report['severity_score']:.3f})\n\n"
    
    if not detected_biases or detected_biases == ["No Significant Bias Detected"]:
        summary += "✅ **Good news!** No significant biases were detected in your dataset.\n\n"
        summary += "The model appears to treat different demographic groups fairly and has balanced representation."
    else:
        summary += f"⚠️ **{len(detected_biases)} type(s) of bias detected:**\n\n"
        
        for bias in detected_biases:
            if bias == "Representation Bias":
                summary += "- **Representation Bias:** Uneven distribution of demographic groups\n"
            elif bias == "Demographic Bias":
                summary += "- **Demographic Bias:** Unfair outcome rates between groups\n"
            elif bias == "Model Bias":
                summary += "- **Model Bias:** Different performance accuracy across groups\n"
        
        summary += f"\n**Confidence:** {severity_report['confidence']*100:.0f}%\n"
        summary += "\n**Recommendation:** Review the detailed explanations below and consider the mitigation strategies to improve fairness."
    
    return summary
