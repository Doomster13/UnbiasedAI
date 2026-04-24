def generate_mitigation_suggestions(
    detected_biases,
    dataset_report,
    fairness_report,
    subgroup_report,
    severity_report
):
    """
    Generate actionable suggestions to reduce detected biases
    
    For each bias type, provide specific mitigation strategies:
    - Data-level interventions
    - Model-level adjustments
    - Post-processing techniques
    - Monitoring recommendations
    """
    
    suggestions = {
        "immediate_actions": [],
        "data_level_fixes": [],
        "model_level_fixes": [],
        "long_term_monitoring": [],
        "priority_order": []
    }
    
    # Determine priority based on severity
    if severity_report["severity_level"] == "High":
        suggestions["priority_order"] = ["data_level_fixes", "immediate_actions", "model_level_fixes"]
    elif severity_report["severity_level"] == "Moderate":
        suggestions["priority_order"] = ["data_level_fixes", "model_level_fixes", "immediate_actions"]
    else:
        suggestions["priority_order"] = ["model_level_fixes", "data_level_fixes", "immediate_actions"]
    
    for bias in detected_biases:
        if bias == "Representation Bias":
            add_representation_suggestions(suggestions, dataset_report)
        elif bias == "Demographic Bias":
            add_demographic_suggestions(suggestions, fairness_report)
        elif bias == "Model Bias":
            add_model_suggestions(suggestions, subgroup_report)
    
    # Add general monitoring recommendations
    add_monitoring_suggestions(suggestions)
    
    return suggestions


def add_representation_suggestions(suggestions, dataset_report):
    """
    Suggestions for fixing representation bias
    """
    
    suggestions["data_level_fixes"].extend([
        {
            "action": "Oversample underrepresented groups",
            "description": "Use SMOTE or random oversampling to balance the dataset",
            "implementation": "from imblearn.over_sampling import SMOTE; smote = SMOTE(sampling_strategy='auto')",
            "impact": "High - Directly addresses representation imbalance"
        },
        {
            "action": "Collect more diverse data",
            "description": "Actively collect more samples from underrepresented demographic groups",
            "implementation": "Targeted data collection campaigns focusing on minority groups",
            "impact": "Very High - Most effective but requires resources"
        },
        {
            "action": "Use stratified sampling",
            "description": "Ensure train/test splits maintain demographic balance",
            "implementation": "train_test_split(..., stratify=df[protected_column])",
            "impact": "Medium - Prevents sampling bias"
        }
    ])
    
    suggestions["immediate_actions"].extend([
        {
            "action": "Set minimum group thresholds",
            "description": "Define minimum representation requirements for model deployment",
            "implementation": "Reject datasets where any group < 5% of total",
            "impact": "High - Prevents deployment of biased models"
        }
    ])


def add_demographic_suggestions(suggestions, fairness_report):
    """
    Suggestions for fixing demographic bias
    """
    
    dp_diff = fairness_report.get("demographic_parity_difference", 0)
    
    if dp_diff > 0.15:
        suggestions["model_level_fixes"].extend([
            {
                "action": "Apply fairness constraints",
                "description": "Use fairness-aware machine learning algorithms",
                "implementation": "from fairlearn.reductions import ExponentiatedGradient; DemographicParity",
                "impact": "High - Directly optimizes for fairness"
            },
            {
                "action": "Reweighting approach",
                "description": "Assign different weights to samples based on demographic group",
                "implementation": "from fairlearn.preprocessing import Reweighing; reweigher = Reweighing()",
                "impact": "Medium - Simple but effective"
            }
        ])
    
    suggestions["data_level_fixes"].extend([
        {
            "action": "Remove proxy variables",
            "description": "Identify and remove features that correlate with protected attributes",
            "implementation": "Calculate correlation matrix and drop high-correlation features",
            "impact": "Medium - Reduces indirect discrimination"
        }
    ])
    
    suggestions["immediate_actions"].extend([
        {
            "action": "Set fairness thresholds",
            "description": "Define acceptable limits for demographic parity differences",
            "implementation": "Reject models with demographic_parity_difference > 0.1",
            "impact": "High - Ensures baseline fairness"
        }
    ])


def add_model_suggestions(suggestions, subgroup_report):
    """
    Suggestions for fixing model performance bias
    """
    
    # Find worst performing groups
    accuracies = {}
    for group, metrics in subgroup_report.items():
        accuracies[group] = metrics.get("accuracy", 0)
    
    worst_groups = [g for g, acc in accuracies.items() if acc < min(accuracies.values()) + 0.05]
    
    suggestions["model_level_fixes"].extend([
        {
            "action": "Group-specific models",
            "description": "Train separate models for different demographic groups",
            "implementation": "Split data by protected attribute and train group-specific models",
            "impact": "High - Can significantly improve performance for minority groups"
        },
        {
            "action": "Adversarial debiasing",
            "description": "Use adversarial networks to remove demographic information from predictions",
            "implementation": "from fairlearn.reductions import ExponentiatedGradient; EqualizedOdds",
            "impact": "High - Advanced technique for fairness"
        },
        {
            "action": "Ensemble methods",
            "description": "Combine multiple models with different fairness objectives",
            "implementation": "Use voting ensemble of fairness-aware and accuracy-focused models",
            "impact": "Medium - Balances fairness and performance"
        }
    ])
    
    if worst_groups:
        suggestions["immediate_actions"].extend([
            {
                "action": "Focus on worst-performing groups",
                "description": f"Pay special attention to groups: {', '.join(worst_groups)}",
                "implementation": "Create validation sets specifically for these groups",
                "impact": "High - Targeted improvement"
            }
        ])


def add_monitoring_suggestions(suggestions):
    """
    General monitoring and maintenance recommendations
    """
    
    suggestions["long_term_monitoring"].extend([
        {
            "action": "Regular bias audits",
            "description": "Schedule monthly bias assessments on production data",
            "implementation": "Automated pipeline that runs bias detection on new data",
            "impact": "High - Prevents bias drift over time"
        },
        {
            "action": "Real-time fairness monitoring",
            "description": "Monitor fairness metrics in production with alerts",
            "implementation": "Dashboard showing demographic parity, equalized odds, etc.",
            "impact": "Very High - Immediate detection of issues"
        },
        {
            "action": "Feedback loops",
            "description": "Collect user feedback to identify unfair outcomes",
            "implementation": "Mechanism for users to report biased decisions",
            "impact": "Medium - Human-in-the-loop validation"
        },
        {
            "action": "Documentation and transparency",
            "description": "Maintain detailed documentation of bias mitigation efforts",
            "implementation": "Version-controlled bias reports and mitigation logs",
            "impact": "Medium - Accountability and compliance"
        },
        {
            "action": "Diverse validation teams",
            "description": "Include diverse perspectives in model validation",
            "implementation": "Create review teams with varied demographic backgrounds",
            "impact": "High - Reduces blind spots in bias detection"
        }
    ])


def generate_implementation_plan(suggestions, severity_report):
    """
    Create a step-by-step implementation plan based on priority
    """
    
    plan = {
        "timeline": [],
        "resources_needed": [],
        "success_metrics": []
    }
    
    # Timeline based on severity
    if severity_report["severity_level"] == "High":
        plan["timeline"] = [
            "Week 1-2: Implement immediate data-level fixes",
            "Week 3-4: Apply model-level fairness constraints", 
            "Week 5-6: Set up monitoring and validation",
            "Ongoing: Regular bias audits and adjustments"
        ]
    elif severity_report["severity_level"] == "Moderate":
        plan["timeline"] = [
            "Week 1-2: Apply model-level fixes",
            "Week 3-4: Implement data balancing techniques",
            "Month 2: Set up monitoring systems"
        ]
    else:
        plan["timeline"] = [
            "Week 1: Apply minor model adjustments",
            "Week 2: Set up basic monitoring",
            "Month 1: Review and validate improvements"
        ]
    
    plan["resources_needed"] = [
        "Data engineering support for data collection and preprocessing",
        "ML engineering support for fairness-aware model implementation",
        "Domain experts for validation and feedback",
        "Monitoring infrastructure for production deployment"
    ]
    
    plan["success_metrics"] = [
        "Demographic parity difference < 0.1",
        "Equalized odds difference < 0.05", 
        "Minimum group representation > 5%",
        "Performance gap between groups < 10%",
        "User-reported bias incidents < 1% of decisions"
    ]
    
    return plan


def format_suggestions_for_display(suggestions, implementation_plan):
    """
    Format suggestions for user-friendly display in the web interface
    """
    
    formatted = {
        "priority_actions": [],
        "detailed_recommendations": {},
        "implementation_timeline": implementation_plan["timeline"],
        "success_metrics": implementation_plan["success_metrics"]
    }
    
    # Priority actions (top 3 most important)
    for category in suggestions["priority_order"][:3]:
        if suggestions[category]:
            top_action = suggestions[category][0]
            formatted["priority_actions"].append({
                "category": category.replace("_", " ").title(),
                "action": top_action["action"],
                "impact": top_action["impact"],
                "description": top_action["description"]
            })
    
    # Detailed recommendations by category
    for category, items in suggestions.items():
        if category == "priority_order":
            continue
            
        if items:
            formatted["detailed_recommendations"][category.replace("_", " ").title()] = items
    
    return formatted
