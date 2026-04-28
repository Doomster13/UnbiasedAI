import streamlit as st
import pandas as pd
import sys
import os
import traceback

st.set_page_config(
    page_title="Unbiased AI Debugger",
    page_icon="🧠",
    layout="wide"
)

st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #07122a 0%, #081c3b 45%, #0f2a5a 100%) !important;
    color: #f4f7ff !important;
    font-family: 'DM Sans', sans-serif !important;
}

.report-panel {
    background: rgba(11, 29, 65, 0.96);
    border: 1px solid rgba(94, 153, 255, 0.2);
    border-radius: 24px;
    padding: 28px 30px;
    margin-bottom: 24px;
    box-shadow: 0 24px 60px rgba(0, 0, 0, 0.18);
}

.deep-box {
    background: rgba(17, 36, 83, 0.88);
    border: 1px solid rgba(104, 159, 255, 0.16);
    border-radius: 20px;
    padding: 24px;
    margin-bottom: 24px;
}

.section-title {
    color: #d8e4ff;
    font-size: 1.35rem;
    margin-bottom: 0.8rem;
}

.severity-box {
    border-radius: 20px;
    padding: 20px 22px;
    margin-bottom: 22px;
    background: linear-gradient(180deg, rgba(18, 55, 114, 0.95), rgba(8, 18, 49, 0.95));
    border: 1px solid rgba(104, 161, 255, 0.24);
}

.severity-low { border-left: 6px solid #34d36b; }
.severity-moderate { border-left: 6px solid #f5b43a; }
.severity-high { border-left: 6px solid #f86b6b; }

.metric-card {
    background: rgba(255, 255, 255, 0.05) !important;
    border-radius: 18px !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    padding: 18px !important;
}

.metric-card h4 { color: #edf2ff !important; margin: 0 0 0.6rem 0 !important; }
.metric-card p { color: #b5c6ff !important; margin: 0 !important; }

.stButton > button {
    background: linear-gradient(135deg, #1f67f2 0%, #4f94ff 100%) !important;
    color: white !important;
    border-radius: 16px !important;
    padding: 0.8rem 1.6rem !important;
}

.stFileUploader {
    border-radius: 18px !important;
}

.stMarkdown div p { color: #e6ecff !important; }
</style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <div class="report-panel">
        <h1 style="margin-bottom: 0.2rem;">Unbiased AI Debugger</h1>
        <p style="margin-top: 0; color:#b8c9ff;">
        Bias Detection & Mitigation Platform</p>
    </div>
    """,
    unsafe_allow_html=True
)

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

try:
    from src.engine.debugger import BiasDebugger
    st.sidebar.success("BiasDebugger loaded")
except Exception as e:
    st.sidebar.error("Unable to load the debugging engine.")
    st.sidebar.exception(e)
    st.stop()

if "current_report" not in st.session_state:
    st.session_state.current_report = None


def display_industry_report(report):
    if not report or not isinstance(report, dict):
        st.warning("No report data is available to display.")
        return

    severity = report.get("severity_analysis", {})
    metrics = report.get("fairness_metrics", {})
    performance = report.get("overall_model_performance", {})
    subgroup = report.get("subgroup_performance", {})
    dataset_bias = report.get("dataset_bias", {})
    mitigation_plan = report.get("mitigation_plan", {}).get("recommended_actions", [])
    root_cause = report.get("root_cause_analysis", {})
    top_features = root_cause.get("top_contributing_features", [])

    st.markdown('<div class="deep-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Executive Summary</div>', unsafe_allow_html=True)
    st.markdown(f"- **Target:** `{report.get('target', 'N/A')}`")
    protected_attrs = report.get("protected_attributes", [])
    st.markdown(f"- **Protected attributes:** `{', '.join(protected_attrs) if protected_attrs else 'N/A'}`")
    st.markdown(f"- **Task type:** `{report.get('task_type', 'N/A')}`")
    st.markdown('</div>', unsafe_allow_html=True)

    severity_level = severity.get("severity_level", "Unknown")
    severity_score = severity.get("severity_score", 0.0)
    confidence = severity.get("confidence", 0.0)
    severity_class = {
        "Low": "severity-low",
        "Moderate": "severity-moderate",
        "High": "severity-high"
    }.get(severity_level, "")

    st.markdown(f'<div class="severity-box {severity_class}">', unsafe_allow_html=True)
    st.markdown(f"### Bias Severity: {severity_level}")
    st.markdown(f"- **Score:** {severity_score:.3f}")
    st.markdown(f"- **Confidence:** {confidence * 100:.0f}%")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Model & Fairness Metrics</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("<h4>Accuracy</h4>", unsafe_allow_html=True)
        st.markdown(f"<p>{performance.get('accuracy', 'N/A')}</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("<h4>Demographic Parity Gap</h4>", unsafe_allow_html=True)
        st.markdown(f"<p>{metrics.get('demographic_parity_difference', 'N/A')}</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("<h4>Equalized Odds Gap</h4>", unsafe_allow_html=True)
        st.markdown(f"<p>{metrics.get('equalized_odds_difference', 'N/A')}</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if subgroup:
        st.markdown('<div class="section-title">Subgroup Performance</div>', unsafe_allow_html=True)
        subgroup_df = pd.DataFrame(subgroup).T
        subgroup_df.index.name = "Group"
        st.dataframe(subgroup_df.style.format("{:.4f}"), use_container_width=True)

    if dataset_bias:
        st.markdown('<div class="section-title">Protected Group Distribution</div>', unsafe_allow_html=True)
        for attr, details in dataset_bias.items():
            st.markdown(f"**{attr}**")
            distribution = details.get("distribution", {})
            if distribution:
                dist_df = pd.DataFrame(list(distribution.items()), columns=[attr, "Share"])
                st.bar_chart(dist_df.set_index(attr))
            else:
                st.markdown("No distribution data available.")

    if top_features:
        st.markdown('<div class="section-title">Top Root Causes</div>', unsafe_allow_html=True)
        features_df = pd.DataFrame(top_features)
        if not features_df.empty:
            st.dataframe(features_df, use_container_width=True)
        else:
            st.markdown("No root cause feature data available.")

    if mitigation_plan:
        st.markdown('<div class="section-title">Recommended Mitigation Actions</div>', unsafe_allow_html=True)
        for action in mitigation_plan:
            st.markdown(f"- {action}")

    # Replace JSON with structured columnar report
    st.markdown('<div class="section-title">Structured Report Data</div>', unsafe_allow_html=True)
    
    # Create tabs for different report sections
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "Severity Analysis", "Fairness Metrics", "Model Performance", 
        "Subgroup Performance", "Dataset Bias", "Root Cause Analysis", 
        "Mitigation Plan", "Other Details"
    ])
    
    with tab1:
        if severity:
            severity_df = pd.DataFrame(list(severity.items()), columns=["Metric", "Value"])
            st.dataframe(severity_df, use_container_width=True)
        else:
            st.write("No severity analysis data available.")
    
    with tab2:
        if metrics:
            metrics_df = pd.DataFrame(list(metrics.items()), columns=["Metric", "Value"])
            st.dataframe(metrics_df, use_container_width=True)
        else:
            st.write("No fairness metrics data available.")
    
    with tab3:
        if performance:
            performance_df = pd.DataFrame(list(performance.items()), columns=["Metric", "Value"])
            st.dataframe(performance_df, use_container_width=True)
        else:
            st.write("No model performance data available.")
    
    with tab4:
        if subgroup:
            subgroup_df = pd.DataFrame(subgroup).T.reset_index()
            subgroup_df.columns = ["Group"] + list(subgroup_df.columns[1:])
            st.dataframe(subgroup_df, use_container_width=True)
        else:
            st.write("No subgroup performance data available.")
    
    with tab5:
        if dataset_bias:
            for attr, details in dataset_bias.items():
                st.subheader(f"{attr}")
                distribution = details.get("distribution", {})
                if distribution:
                    dist_df = pd.DataFrame(list(distribution.items()), columns=["Category", "Proportion"])
                    st.dataframe(dist_df, use_container_width=True)
                chi_p = details.get("chi_square_p_value")
                if chi_p is not None:
                    st.write(f"Chi-square p-value: {chi_p}")
        else:
            st.write("No dataset bias data available.")
    
    with tab6:
        if top_features:
            features_df = pd.DataFrame(top_features)
            st.dataframe(features_df, use_container_width=True)
        else:
            st.write("No root cause analysis data available.")
    
    with tab7:
        mitigation = report.get("mitigation_plan", {})
        if mitigation:
            # Flatten mitigation plan into tables
            if "recommended_actions" in mitigation:
                actions_df = pd.DataFrame(mitigation["recommended_actions"], columns=["Action"])
                st.dataframe(actions_df, use_container_width=True)
            
            if "detailed_recommendations" in mitigation:
                detailed = mitigation["detailed_recommendations"]
                for category, recs in detailed.items():
                    st.subheader(category)
                    if recs:
                        recs_df = pd.DataFrame(recs)
                        st.dataframe(recs_df, use_container_width=True)
            
            if "priority_actions" in mitigation:
                priority_df = pd.DataFrame(mitigation["priority_actions"], columns=["Priority Action"])
                st.dataframe(priority_df, use_container_width=True)
        else:
            st.write("No mitigation plan data available.")
    
    with tab8:
        other_data = {
            "target": report.get("target"),
            "protected_attributes": ", ".join(report.get("protected_attributes", [])),
            "task_type": report.get("task_type"),
            "detected_biases": ", ".join(report.get("detected_biases", [])),
            "bias_summary": report.get("bias_summary", ""),
            "bias_explanations": "; ".join(report.get("bias_explanations", [])),
        }
        
        # Implementation details if available
        impl_plan = report.get("implementation_plan", {})
        if impl_plan:
            other_data.update({
                "implementation_timeline": "; ".join(impl_plan.get("timeline", [])),
                "resources_needed": "; ".join(impl_plan.get("resources_needed", [])),
                "success_metrics": "; ".join(impl_plan.get("success_metrics", [])),
            })
        
        other_df = pd.DataFrame(list(other_data.items()), columns=["Field", "Value"])
        st.dataframe(other_df, use_container_width=True)

st.markdown("### Upload your dataset for bias detection")
uploaded_file = st.file_uploader(
    "CSV file",
    type=["csv"],
    help="Upload a CSV dataset to run bias analysis."
)

if uploaded_file is not None:
    try:
        temp_path = os.path.join(os.path.dirname(__file__), "temp_uploaded_dataset.csv")
        df_uploaded = pd.read_csv(uploaded_file)

        if df_uploaded.empty:
            st.error("Uploaded dataset is empty.")
        else:
            df_uploaded.to_csv(temp_path, index=False)
            report = BiasDebugger(temp_path).run()
            st.success("Analysis complete")
            st.session_state.current_report = report
            display_industry_report(report)
    except Exception as e:
        st.error("Analysis failed. See details below.")
        st.exception(e)
elif st.session_state.current_report is not None:
    st.info("Showing the last uploaded dataset result.")
    display_industry_report(st.session_state.current_report)
else:
    st.markdown(
        """
        <div class="deep-box">
            <h2 style="margin-bottom:0.6rem;">Welcome to the Unbiased AI Debugger</h2>
            <p>Upload your CSV dataset and get a polished bias analysis summary with deep blue analytics cards and clear remediation guidance.</p>
            <ul style="margin-top:1rem; color:#c8d5ff;">
                <li>Detect dataset and model fairness issues</li>
                <li>Measure bias severity across protected groups</li>
                <li>See root causes and mitigation suggestions</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )
