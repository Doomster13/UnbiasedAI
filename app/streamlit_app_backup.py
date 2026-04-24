import streamlit as st
import pandas as pd
import sys
import os
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import json

# Configure page
st.set_page_config(
    page_title="Unbiased AI Debugger - Enterprise Edition",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f2937;
        text-align: center;
        margin-bottom: 2rem;
    }
    .severity-high {
        background-color: #fee2e2;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #dc2626;
    }
    .severity-medium {
        background-color: #fef3c7;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #f59e0b;
    }
    .severity-low {
        background-color: #dcfce7;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #16a34a;
    }
    .metric-card {
        background-color: #f8fafc;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #e2e8f0;
        margin: 0.5rem 0;
    }
    .insight-box {
        background-color: #eff6ff;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #3b82f6;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar for navigation and configuration
st.sidebar.markdown("## 🔧 Configuration")

# Session state for maintaining data across pages
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'current_report' not in st.session_state:
    st.session_state.current_report = None

# Debug path check
project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if project_root not in sys.path:
    sys.path.append(project_root)

# Import check
try:
    from src.engine.debugger import BiasDebugger
    st.sidebar.success("✅ All modules loaded")
except Exception as e:
    st.sidebar.error(f"❌ Import error: {str(e)}")
    st.stop()

# Main header
st.markdown('<h1 class="main-header">🔍 Unbiased AI Debugger</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #6b7280; margin-bottom: 2rem;">Enterprise-grade bias detection and mitigation platform</p>', unsafe_allow_html=True)

# File upload section
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("### 📁 Dataset Upload")
    uploaded_file = st.file_uploader(
        "Upload your dataset for bias analysis",
        type=["csv"],
        help="Supported formats: CSV. The system will automatically detect target columns and protected attributes."
    )

if uploaded_file is not None:
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Step 1: Load and validate data
        status_text.text("📊 Loading and validating dataset...")
        progress_bar.progress(10)
        
        temp_path = "temp_uploaded_dataset.csv"
        df_uploaded = pd.read_csv(uploaded_file)
        
        # Basic data validation
        if df_uploaded.empty:
            st.error("❌ The uploaded dataset is empty. Please check your file.")
            st.stop()
            
        if len(df_uploaded.columns) < 2:
            st.error("❌ Dataset must have at least 2 columns (features + target).")
            st.stop()
        
        df_uploaded.to_csv(temp_path, index=False)
        
        # Step 2: Show data preview
        status_text.text("🔍 Analyzing dataset structure...")
        progress_bar.progress(25)
        
        with st.expander("📋 Dataset Preview", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Shape:** {df_uploaded.shape[0]} rows, {df_uploaded.shape[1]} columns")
                st.write(f"**Memory usage:** {df_uploaded.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
            with col2:
                st.write(f"**Missing values:** {df_uploaded.isnull().sum().sum()}")
                st.write(f"**Duplicate rows:** {df_uploaded.duplicated().sum()}")
            
            st.dataframe(df_uploaded.head(), use_container_width=True)
        
        # Step 3: Run bias analysis
        status_text.text("🧠 Running comprehensive bias analysis...")
        progress_bar.progress(40)
        
        debugger = BiasDebugger(temp_path)
        
        status_text.text("⚡ Generating insights and recommendations...")
        progress_bar.progress(60)
        
        report = debugger.run()
        
        status_text.text("✅ Analysis complete!")
        progress_bar.progress(100)
        
        # Store in session state
        st.session_state.analysis_complete = True
        st.session_state.current_report = report
        
        # Clear status
        status_text.empty()
        progress_bar.empty()
        
        # Display comprehensive report
        def display_industry_report(report):
            st.subheader("Bias Explanations")
            st.write(report["bias_explanations"])
            st.subheader("Suggestions")
            st.write(report["suggestions"])
            st.subheader("Bias Metrics")
            st.write(report["bias_metrics"])
            st.subheader("Fairness Metrics")
            st.write(report["fairness_metrics"])
            st.subheader("Data Quality Metrics")
            st.write(report["data_quality_metrics"])

        display_industry_report(report)
        
    except Exception as e:
        st.error(f"❌ Analysis failed: {str(e)}")
        st.exception(e)
        
elif st.session_state.analysis_complete and st.session_state.current_report:
    # Display previous analysis if available
    st.info("📈 Showing previous analysis results. Upload a new dataset to run a fresh analysis.")
    def display_industry_report(report):
        st.subheader("Bias Explanations")
        st.write(report["bias_explanations"])
        st.subheader("Suggestions")
        st.write(report["suggestions"])
        st.subheader("Bias Metrics")
        st.write(report["bias_metrics"])
        st.subheader("Fairness Metrics")
        st.write(report["fairness_metrics"])
        st.subheader("Data Quality Metrics")
        st.write(report["data_quality_metrics"])

    display_industry_report(st.session_state.current_report)

else:
    # Welcome screen
    st.markdown("""
    ## 🚀 Welcome to Unbiased AI Debugger
    
    This enterprise-grade platform helps you:
    
    🔍 **Detect Bias** - Automatically identify various types of bias in your datasets
    📊 **Measure Impact** - Quantify bias severity with industry-standard metrics
    💡 **Get Explanations** - Understand why bias occurs and which groups are affected
    🛠️ **Mitigate Issues** - Receive actionable recommendations to reduce bias
    📈 **Monitor Progress** - Track improvements over time
    
    ### How it works:
    1. **Upload** your CSV dataset
    2. **Auto-detect** target columns and protected attributes
    3. **Analyze** bias using multiple fairness metrics
    4. **Receive** comprehensive report with explanations and mitigation strategies
    
    ---
    
    ### 📊 Supported Bias Types:
    - **Representation Bias** - Uneven distribution of demographic groups
    - **Demographic Bias** - Unfair outcome rates between groups  
    - **Model Performance Bias** - Different accuracy across demographic groups
    - **Intersectional Bias** - Combined effects of multiple protected attributes
    
    ### 🛡️ Fairness Metrics:
    - Demographic Parity Difference
    - Equalized Odds Difference
    - Subgroup Performance Analysis
    - Statistical Significance Testing
    
    **Ready to get started? Upload your dataset above!**
    """)

def display_industry_report(report):
    """Display comprehensive industry-level bias analysis report"""
    
    # Executive Summary
    st.markdown("---")
    st.markdown("## 📊 Executive Summary")
    
    # Severity indicator with styling
    severity = report["severity_analysis"]
    severity_class = {
        "Low": "severity-low",
        "Moderate": "severity-medium", 
        "High": "severity-high"
    }
    
    st.markdown(f'<div class="{severity_class.get(severity["severity_level"], "")}">', unsafe_allow_html=True)
    st.markdown(f"### 🎯 Bias Severity: {severity['severity_level']}")
    st.markdown(f"**Score:** {severity['severity_score']:.3f} | **Confidence:** {severity['confidence']*100:.0f}%")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Bias Summary
    if "bias_summary" in report:
        st.markdown(report["bias_summary"])
    
    # Key Metrics Dashboard
    st.markdown("---")
    st.markdown("## 📈 Key Metrics Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Overall Accuracy", f"{report['overall_model_performance']['accuracy']:.3f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        dp_diff = report['fairness_metrics'].get('demographic_parity_difference', 0)
        st.metric("Demographic Parity Gap", f"{dp_diff:.3f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        eo_diff = report['fairness_metrics'].get('equalized_odds_difference', 0)
        st.metric("Equalized Odds Gap", f"{eo_diff:.3f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        detected_count = len([b for b in report['detected_biases'] if b != "No Significant Bias Detected"])
        st.metric("Bias Types Detected", detected_count)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Bias Explanations
    st.markdown("---")
    st.markdown("## 🔍 Bias Analysis & Explanations")
    
    if "bias_explanations" in report and report["bias_explanations"]:
        for i, explanation in enumerate(report["bias_explanations"], 1):
            with st.expander(f"📝 Explanation {i}: {report['detected_biases'][i-1] if i-1 < len(report['detected_biases']) else 'Analysis'}", expanded=i==1):
                st.markdown(explanation)
    else:
        st.info("No detailed explanations available.")
    
    # Mitigation Strategies
    st.markdown("---")
    st.markdown("## 🛠️ Mitigation Strategies")
    
    if "mitigation_suggestions" in report:
        suggestions = report["mitigation_suggestions"]
        
        # Priority Actions
        if suggestions.get("priority_actions"):
            st.markdown("### 🚀 Priority Actions")
            for i, action in enumerate(suggestions["priority_actions"], 1):
                st.markdown(f'<div class="insight-box">', unsafe_allow_html=True)
                st.markdown(f"**{i}. {action['action']}** ({action['category']})")
                st.write(action['description'])
                st.write(f"*Impact Level:* {action['impact']}")
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Detailed Recommendations
        if suggestions.get("detailed_recommendations"):
            st.markdown("### 📋 Detailed Recommendations")
            for category, items in suggestions["detailed_recommendations"].items():
                with st.expander(f"📚 {category}", expanded=False):
                    for i, item in enumerate(items, 1):
                        st.markdown(f"**{i}. {item['action']}**")
                        st.write(item['description'])
                        if 'implementation' in item:
                            st.code(item['implementation'], language="python")
                        st.write(f"*Impact:* {item['impact']}")
                        if i < len(items):
                            st.markdown("---")
        
        # Implementation Timeline
        if suggestions.get("implementation_timeline"):
            st.markdown("### 📅 Implementation Timeline")
            for i, step in enumerate(suggestions["implementation_timeline"], 1):
                st.write(f"{i}. {step}")
        
        # Success Metrics
        if suggestions.get("success_metrics"):
            st.markdown("### ✅ Success Metrics")
            for metric in suggestions["success_metrics"]:
                st.write(f"• {metric}")
    
    # Visualizations
    st.markdown("---")
    st.markdown("## 📊 Visual Analytics")
    
    create_bias_visualizations(report)
    
    # Technical Details
    st.markdown("---")
    st.markdown("## 🔧 Technical Analysis Details")
    
    with st.expander("📋 Dataset Bias Analysis", expanded=False):
        st.json(report["dataset_bias"])
    
    with st.expander("⚖️ Fairness Metrics", expanded=False):
        st.json(report["fairness_metrics"])
    
    with st.expander("🎯 Model Performance", expanded=False):
        st.json(report["overall_model_performance"])
    
    with st.expander("👥 Subgroup Performance", expanded=False):
        st.json(report["subgroup_performance"])
    
    with st.expander("🔍 Detected Biases", expanded=False):
        st.write(report["detected_biases"])
    
    # Export Options
    st.markdown("---")
    st.markdown("## 📤 Export & Sharing")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Download Report (JSON)", help="Download complete analysis report"):
            st.download_button(
                label="Click to Download",
                data=json.dumps(report, indent=2),
                file_name=f"bias_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with col2:
        if st.button("📊 Download Summary (CSV)", help="Download summary metrics"):
            summary_data = {
                "Metric": ["Severity Score", "Confidence", "Overall Accuracy", "Demographic Parity Gap", "Equalized Odds Gap", "Bias Types Detected"],
                "Value": [
                    severity["severity_score"],
                    severity["confidence"],
                    report["overall_model_performance"]["accuracy"],
                    report["fairness_metrics"].get("demographic_parity_difference", 0),
                    report["fairness_metrics"].get("equalized_odds_difference", 0),
                    len([b for b in report['detected_biases'] if b != "No Significant Bias Detected"])
                ]
            }
            summary_df = pd.DataFrame(summary_data)
            st.download_button(
                label="Click to Download",
                data=summary_df.to_csv(index=False),
                file_name=f"bias_analysis_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    with col3:
        if st.button("🔄 Clear Analysis", help="Clear current analysis and start fresh"):
            st.session_state.analysis_complete = False
            st.session_state.current_report = None
            st.rerun()

def create_bias_visualizations(report):
    """Create interactive visualizations for bias analysis"""
    
    # Subgroup Performance Chart
    if "subgroup_performance" in report and report["subgroup_performance"]:
        st.markdown("### 📈 Subgroup Performance Analysis")
        
        subgroups = list(report["subgroup_performance"].keys())
        accuracies = [report["subgroup_performance"][sg].get("accuracy", 0) * 100 for sg in subgroups]
        precisions = [report["subgroup_performance"][sg].get("precision", 0) * 100 for sg in subgroups]
        recalls = [report["subgroup_performance"][sg].get("recall", 0) * 100 for sg in subgroups]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Accuracy',
            x=subgroups,
            y=accuracies,
            marker_color='#3b82f6'
        ))
        
        fig.add_trace(go.Bar(
            name='Precision',
            x=subgroups,
            y=precisions,
            marker_color='#10b981'
        ))
        
        fig.add_trace(go.Bar(
            name='Recall',
            x=subgroups,
            y=recalls,
            marker_color='#f59e0b'
        ))
        
        fig.update_layout(
            title="Model Performance by Demographic Group",
            xaxis_title="Demographic Groups",
            yaxis_title="Performance (%)",
            barmode='group',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Dataset Distribution
    if "dataset_bias" in report and report["dataset_bias"]:
        st.markdown("### 📊 Dataset Demographic Distribution")
        
        for attr, data in report["dataset_bias"].items():
            if attr == "intersectional":
                continue
                
            if "distribution" in data and data["distribution"]:
                groups = list(data["distribution"].keys())
                percentages = [data["distribution"][g] * 100 for g in groups]
                
                fig = px.pie(
                    values=percentages,
                    names=groups,
                    title=f"Distribution of {attr.title()}",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                
                fig.update_traces(textposition='inside', textinfo='percent+label')
                fig.update_layout(height=400)
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Add chi-square significance if available
                if "chi_square_p_value" in data:
                    p_value = data["chi_square_p_value"]
                    significance = "Significant" if p_value < 0.05 else "Not Significant"
                    st.write(f"**Chi-square Test:** p-value = {p_value:.6f} ({significance})")
    
    # Fairness Metrics Comparison
    st.markdown("### ⚖️ Fairness Metrics Overview")
    
    fairness_metrics = report["fairness_metrics"]
    metrics_names = ["Demographic Parity", "Equalized Odds"]
    metrics_values = [
        fairness_metrics.get("demographic_parity_difference", 0),
        fairness_metrics.get("equalized_odds_difference", 0)
    ]
    
    # Create threshold indicators
    thresholds = [0.1, 0.05]  # Industry standard thresholds
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Current Value',
        x=metrics_names,
        y=metrics_values,
        marker_color=['#3b82f6', '#10b981']
    ))
    
    fig.add_trace(go.Scatter(
        name='Threshold',
        x=metrics_names,
        y=thresholds,
        mode='lines+markers',
        line=dict(color='red', dash='dash'),
        marker=dict(color='red', size=8)
    ))
    
    fig.update_layout(
        title="Fairness Metrics vs Industry Thresholds",
        xaxis_title="Fairness Metrics",
        yaxis_title="Value",
        height=400,
        annotations=[
            dict(x=xi, yi=thresholds[i] + 0.01, text=f"Threshold: {thresholds[i]}", 
                 showarrow=False, font=dict(color='red', size=10))
            for i, xi in enumerate(metrics_names)
        ]
    )
    
    st.plotly_chart(fig, use_container_width=True)