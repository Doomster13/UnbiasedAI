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

st.set_page_config(
    page_title="Unbiased AI Debugger",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; }

@keyframes bgMove {
    0% { background-position: 0% 0%; }
    100% { background-position: 100% 100%; }
}

html, body, [data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at 15% 50%, rgba(124, 111, 247, 0.08), transparent 25%),
                radial-gradient(circle at 85% 30%, rgba(167, 139, 250, 0.08), transparent 25%),
                #09090f !important;
    background-attachment: fixed !important;
    color: #e8e6f0 !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stSidebar"] {
    background: rgba(15, 15, 26, 0.6) !important;
    backdrop-filter: blur(16px) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
}

[data-testid="stSidebar"] * {
    color: #a0a0c0 !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stSidebar"] .stButton > button {
    background: rgba(26, 26, 46, 0.6) !important;
    backdrop-filter: blur(8px) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    color: #c0b8f0 !important;
    border-radius: 8px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    width: 100% !important;
    padding: 0.6rem 1rem !important;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(42, 42, 74, 0.8) !important;
    border-color: rgba(124, 111, 247, 0.5) !important;
    color: #c8c0ff !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 15px rgba(124, 111, 247, 0.2) !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }
.stDeployButton { display: none !important; }

/* ── Typography ── */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Syne', sans-serif !important;
    color: #f0eeff !important;
    letter-spacing: -0.02em !important;
}

/* ── Main header ── */
@keyframes pulseGlow {
    0% { transform: translateX(-50%) scale(1); opacity: 0.5; }
    50% { transform: translateX(-50%) scale(1.1); opacity: 0.8; }
    100% { transform: translateX(-50%) scale(1); opacity: 0.5; }
}

@keyframes gradientText {
    0% { background-position: 0% center; }
    100% { background-position: 200% center; }
}

.main-header-wrap {
    padding: 4rem 0 3rem 0;
    text-align: center;
    position: relative;
    overflow: visible;
}
.main-header-wrap::before {
    content: '';
    position: absolute;
    top: -50%;
    left: 50%;
    transform: translateX(-50%);
    width: 600px;
    height: 400px;
    background: radial-gradient(ellipse, rgba(124,111,247,0.25) 0%, transparent 70%);
    pointer-events: none;
    animation: pulseGlow 8s infinite alternate ease-in-out;
}
.main-title {
    font-family: 'Syne', sans-serif;
    font-size: 3.5rem;
    font-weight: 800;
    letter-spacing: -0.04em;
    color: #f0eeff;
    margin: 0;
    line-height: 1.1;
    text-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
}
.main-title span {
    background: linear-gradient(to right, #7c6ff7 0%, #c4b5fd 50%, #7c6ff7 100%);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: gradientText 4s linear infinite;
}
.main-subtitle {
    font-family: 'DM Mono', monospace;
    font-size: 0.85rem;
    letter-spacing: 0.2em;
    color: #8a88aa;
    text-transform: uppercase;
    margin-top: 1.2rem;
}

/* ── Upload zone ── */
[data-testid="stFileUploader"] {
    background: rgba(13, 13, 26, 0.5) !important;
    backdrop-filter: blur(10px) !important;
    border: 1.5px dashed rgba(124, 111, 247, 0.3) !important;
    border-radius: 16px !important;
    padding: 2.5rem !important;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2) !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: #7c6ff7 !important;
    background: rgba(20, 20, 40, 0.6) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 40px rgba(124, 111, 247, 0.15) !important;
}
[data-testid="stFileUploader"] label {
    color: #a0a0c0 !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Progress bar ── */
[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, #7c6ff7, #a78bfa) !important;
    box-shadow: 0 0 10px rgba(124, 111, 247, 0.5) !important;
}

/* ── Metric cards ── */
.metric-card {
    background: rgba(20, 20, 35, 0.4);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    padding: 1.5rem 1.75rem;
    position: relative;
    overflow: hidden;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #7c6ff7, #a78bfa, #c4b5fd);
    background-size: 200% auto;
    animation: gradientText 3s linear infinite;
}
.metric-card:hover { 
    transform: translateY(-5px);
    border-color: rgba(124, 111, 247, 0.4);
    box-shadow: 0 12px 32px rgba(124, 111, 247, 0.15);
}
.metric-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #8a88aa;
    margin-bottom: 0.8rem;
}
.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    color: #f0eeff;
    line-height: 1;
    text-shadow: 0 2px 10px rgba(0,0,0,0.3);
}
.metric-sub {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    color: #606080;
    margin-top: 0.6rem;
}

/* ── Severity banners ── */
.sev-high {
    background: linear-gradient(90deg, rgba(239,68,68,0.15), rgba(239,68,68,0.05));
    border: 1px solid rgba(239,68,68,0.3);
    border-left: 4px solid #ef4444;
    padding: 1.5rem;
    border-radius: 12px;
    margin: 1.5rem 0;
    box-shadow: 0 8px 24px rgba(239, 68, 68, 0.1);
}
.sev-medium {
    background: linear-gradient(90deg, rgba(245,158,11,0.15), rgba(245,158,11,0.05));
    border: 1px solid rgba(245,158,11,0.3);
    border-left: 4px solid #f59e0b;
    padding: 1.5rem;
    border-radius: 12px;
    margin: 1.5rem 0;
    box-shadow: 0 8px 24px rgba(245, 158, 11, 0.1);
}
.sev-low {
    background: linear-gradient(90deg, rgba(16,185,129,0.15), rgba(16,185,129,0.05));
    border: 1px solid rgba(16,185,129,0.3);
    border-left: 4px solid #10b981;
    padding: 1.5rem;
    border-radius: 12px;
    margin: 1.5rem 0;
    box-shadow: 0 8px 24px rgba(16, 185, 129, 0.1);
}
.sev-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 0.4rem;
}
.sev-meta {
    font-family: 'DM Mono', monospace;
    font-size: 0.8rem;
    color: #a0a0c0;
}

/* ── Section headers ── */
.section-header {
    font-family: 'Syne', sans-serif;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #a78bfa;
    margin-top: 3rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 1rem;
}
.section-header::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(124,111,247,0.3), transparent);
}

/* ── Insight box ── */
.insight-box {
    background: rgba(20, 20, 35, 0.4);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-left: 3px solid #7c6ff7;
    padding: 1.5rem;
    border-radius: 12px;
    margin: 1rem 0;
    transition: all 0.3s ease;
}
.insight-box:hover {
    background: rgba(25, 25, 45, 0.6);
    border-color: rgba(124, 111, 247, 0.3);
    transform: translateX(4px);
}
.insight-box h4 {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: #d8d0ff;
    margin-bottom: 0.6rem;
}
.insight-box .impact-tag {
    display: inline-block;
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    background: rgba(124,111,247,0.15);
    color: #c4b5fd;
    border: 1px solid rgba(124,111,247,0.3);
    padding: 0.3rem 0.6rem;
    border-radius: 6px;
    margin-top: 0.8rem;
    box-shadow: 0 2px 8px rgba(124, 111, 247, 0.1);
}

/* ── Data preview ── */
.stDataFrame {
    background: rgba(13, 13, 26, 0.6) !important;
    backdrop-filter: blur(8px) !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-radius: 12px !important;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2) !important;
}

/* ── Expanders ── */
.streamlit-expanderHeader {
    background: rgba(20, 20, 35, 0.4) !important;
    backdrop-filter: blur(8px) !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-radius: 12px !important;
    color: #a0a0c0 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.05em !important;
    transition: all 0.3s ease !important;
}
.streamlit-expanderHeader:hover {
    background: rgba(30, 30, 50, 0.6) !important;
    border-color: rgba(124, 111, 247, 0.4) !important;
    color: #d8d0ff !important;
}
.streamlit-expanderContent {
    background: rgba(15, 15, 26, 0.4) !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-top: none !important;
    border-bottom-left-radius: 12px !important;
    border-bottom-right-radius: 12px !important;
}

/* ── Buttons ── */
.stButton > button {
    background: rgba(26, 26, 46, 0.6) !important;
    backdrop-filter: blur(10px) !important;
    border: 1px solid rgba(124, 111, 247, 0.3) !important;
    color: #c0b8f0 !important;
    border-radius: 12px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    padding: 0.75rem 1.5rem !important;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
}
.stButton > button:hover {
    background: rgba(42, 26, 78, 0.8) !important;
    border-color: #7c6ff7 !important;
    color: #ffffff !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(124, 111, 247, 0.25) !important;
}
.stButton > button:focus { 
    box-shadow: 0 0 0 2px rgba(124,111,247,0.5) !important; 
}

/* ── Download button ── */
.stDownloadButton > button {
    background: linear-gradient(135deg, #7c6ff7, #a78bfa) !important;
    border: none !important;
    color: #ffffff !important;
    border-radius: 12px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    padding: 0.75rem 1.5rem !important;
    box-shadow: 0 6px 20px rgba(124, 111, 247, 0.4) !important;
    transition: all 0.3s ease !important;
}
.stDownloadButton > button:hover {
    background: linear-gradient(135deg, #6b5ce6, #967ae9) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(124, 111, 247, 0.5) !important;
}

/* ── Info / warning / error ── */
[data-testid="stAlert"] {
    background: rgba(20, 20, 35, 0.5) !important;
    backdrop-filter: blur(8px) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 12px !important;
    color: #c0c0e0 !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1) !important;
}

/* ── Dividers ── */
hr {
    border: none !important;
    border-top: 1px solid rgba(255, 255, 255, 0.05) !important;
    margin: 2.5rem 0 !important;
}

/* ── Welcome feature grid ── */
.feat-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1.5rem;
    margin: 2rem 0;
}
.feat-card {
    background: rgba(20, 20, 35, 0.4);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    padding: 2rem;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}
.feat-card:hover {
    border-color: rgba(124, 111, 247, 0.4);
    transform: translateY(-6px);
    box-shadow: 0 16px 40px rgba(124, 111, 247, 0.15);
    background: rgba(25, 25, 45, 0.6);
}
.feat-icon {
    font-size: 2rem;
    margin-bottom: 1rem;
    color: #a78bfa;
    text-shadow: 0 0 20px rgba(167, 139, 250, 0.5);
}
.feat-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 800;
    color: #f0eeff;
    margin-bottom: 0.5rem;
}
.feat-desc {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.9rem;
    color: #8a88aa;
    line-height: 1.6;
}

/* ── Step list ── */
.step-list {
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
    margin: 1.5rem 0;
}
.step-item {
    display: flex;
    align-items: flex-start;
    gap: 1.25rem;
    background: rgba(20, 20, 35, 0.3);
    padding: 1.25rem;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.03);
    transition: all 0.3s ease;
}
.step-item:hover {
    background: rgba(25, 25, 45, 0.5);
    border-color: rgba(124, 111, 247, 0.2);
    transform: translateX(4px);
}
.step-num {
    font-family: 'DM Mono', monospace;
    font-size: 0.8rem;
    font-weight: 600;
    color: #c4b5fd;
    background: rgba(124,111,247,0.15);
    border: 1px solid rgba(124,111,247,0.3);
    border-radius: 8px;
    padding: 0.35rem 0.65rem;
    white-space: nowrap;
    flex-shrink: 0;
    box-shadow: 0 2px 10px rgba(124, 111, 247, 0.2);
}
.step-text {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.95rem;
    color: #a0a0c0;
    padding-top: 0.2rem;
    line-height: 1.5;
}

/* ── Info stat row ── */
.info-row {
    display: flex;
    flex-wrap: wrap;
    gap: 2.5rem;
    background: rgba(20, 20, 35, 0.4);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    padding: 1.5rem 2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}
.info-stat { display: flex; flex-direction: column; gap: 0.3rem; }
.info-stat-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #8a88aa;
}
.info-stat-val {
    font-family: 'Syne', sans-serif;
    font-size: 1.3rem;
    font-weight: 800;
    color: #f0eeff;
}

/* ── Sidebar branding ── */
.sidebar-brand {
    font-family: 'Syne', sans-serif;
    font-size: 1.2rem;
    font-weight: 800;
    color: #d8d0ff !important;
    letter-spacing: -0.02em;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    margin-bottom: 1.25rem;
    text-shadow: 0 2px 10px rgba(124, 111, 247, 0.3);
}
.sidebar-version {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    color: #606080 !important;
    text-transform: uppercase;
}
</style>
""", unsafe_allow_html=True)

if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'current_report' not in st.session_state:
    st.session_state.current_report = None

with st.sidebar:
    st.markdown('<div class="sidebar-brand">⬡ Unbiased AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-version">v2.0 · Enterprise</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**Configuration**")

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

try:
    from src.engine.debugger import BiasDebugger
    st.sidebar.success("✓ Engine loaded")
except Exception as e:
    st.sidebar.error(f"Import error: {str(e)}")
    st.stop()

st.markdown("""
<div class="main-header-wrap">
    <h1 class="main-title">Unbiased <span>AI</span> Debugger</h1>
    <p class="main-subtitle">Enterprise · Bias Detection &amp; Mitigation Platform</p>
</div>
""", unsafe_allow_html=True)

_, col_up, _ = st.columns([1, 2, 1])
with col_up:
    st.markdown('<div class="section-header">Dataset</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Drop your CSV file here, or click to browse",
        type=["csv"],
        label_visibility="visible",
        help="CSV format · Auto-detects target columns and protected attributes"
    )

if uploaded_file is not None:
    progress_bar = st.progress(0)
    status_text = st.empty()

    try:
        status_text.markdown(
            '<p style="font-family:\'DM Mono\',monospace;font-size:0.75rem;color:#7c6ff7;'
            'letter-spacing:0.1em;text-transform:uppercase;">↻ Loading dataset…</p>',
            unsafe_allow_html=True
        )
        progress_bar.progress(10)

        temp_path = "temp_uploaded_dataset.csv"
        df_uploaded = pd.read_csv(uploaded_file)

        if df_uploaded.empty:
            st.error("The uploaded dataset is empty.")
            st.stop()
        if len(df_uploaded.columns) < 2:
            st.error("Dataset must have at least 2 columns.")
            st.stop()

        df_uploaded.to_csv(temp_path, index=False)

        status_text.markdown(
            '<p style="font-family:\'DM Mono\',monospace;font-size:0.75rem;color:#7c6ff7;'
            'letter-spacing:0.1em;text-transform:uppercase;">↻ Analysing structure…</p>',
            unsafe_allow_html=True
        )
        progress_bar.progress(25)

        # Dataset preview
        with st.expander("Dataset Preview", expanded=True):
            st.markdown(f"""
            <div class="info-row">
                <div class="info-stat">
                    <span class="info-stat-label">Rows</span>
                    <span class="info-stat-val">{df_uploaded.shape[0]:,}</span>
                </div>
                <div class="info-stat">
                    <span class="info-stat-label">Columns</span>
                    <span class="info-stat-val">{df_uploaded.shape[1]}</span>
                </div>
                <div class="info-stat">
                    <span class="info-stat-label">Missing Values</span>
                    <span class="info-stat-val">{df_uploaded.isnull().sum().sum():,}</span>
                </div>
                <div class="info-stat">
                    <span class="info-stat-label">Duplicate Rows</span>
                    <span class="info-stat-val">{df_uploaded.duplicated().sum():,}</span>
                </div>
                <div class="info-stat">
                    <span class="info-stat-label">Memory</span>
                    <span class="info-stat-val">{df_uploaded.memory_usage(deep=True).sum()/1024**2:.1f} MB</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.dataframe(df_uploaded.head(), use_container_width=True)

        status_text.markdown(
            '<p style="font-family:\'DM Mono\',monospace;font-size:0.75rem;color:#7c6ff7;'
            'letter-spacing:0.1em;text-transform:uppercase;">↻ Running bias analysis…</p>',
            unsafe_allow_html=True
        )
        progress_bar.progress(50)

        debugger = BiasDebugger(temp_path)

        status_text.markdown(
            '<p style="font-family:\'DM Mono\',monospace;font-size:0.75rem;color:#7c6ff7;'
            'letter-spacing:0.1em;text-transform:uppercase;">↻ Generating insights…</p>',
            unsafe_allow_html=True
        )
        progress_bar.progress(80)

        report = debugger.run()
        progress_bar.progress(100)
        status_text.empty()
        progress_bar.empty()

        st.session_state.analysis_complete = True
        st.session_state.current_report = report

        display_industry_report(report)

    except Exception as e:
        st.error(f"Analysis failed: {str(e)}")
        st.exception(e)

elif st.session_state.analysis_complete and st.session_state.current_report:
    st.info("Showing previous results · Upload a new dataset to re-run analysis.")
    display_industry_report(st.session_state.current_report)

else:
    st.markdown('<div class="section-header">Capabilities</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="feat-grid">
        <div class="feat-card">
            <div class="feat-icon">⬡</div>
            <div class="feat-title">Detect Bias</div>
            <div class="feat-desc">Automatically identify representation, demographic, performance, and intersectional bias across your datasets.</div>
        </div>
        <div class="feat-card">
            <div class="feat-icon">◈</div>
            <div class="feat-title">Measure Impact</div>
            <div class="feat-desc">Quantify severity using demographic parity, equalized odds, and statistical significance testing.</div>
        </div>
        <div class="feat-card">
            <div class="feat-icon">◎</div>
            <div class="feat-title">Explain Results</div>
            <div class="feat-desc">Understand why bias occurs, which groups are affected, and the magnitude of disparity.</div>
        </div>
        <div class="feat-card">
            <div class="feat-icon">⟳</div>
            <div class="feat-title">Mitigate Issues</div>
            <div class="feat-desc">Receive prioritised, actionable mitigation strategies with implementation timelines.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">How It Works</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="step-list">
        <div class="step-item">
            <span class="step-num">01</span>
            <span class="step-text">Upload your CSV dataset — the engine auto-detects target columns and protected attributes.</span>
        </div>
        <div class="step-item">
            <span class="step-num">02</span>
            <span class="step-text">Multi-metric bias analysis runs automatically across all demographic subgroups.</span>
        </div>
        <div class="step-item">
            <span class="step-num">03</span>
            <span class="step-text">Review the executive summary, interactive charts, and severity scoring.</span>
        </div>
        <div class="step-item">
            <span class="step-num">04</span>
            <span class="step-text">Act on prioritised recommendations with code-level implementation guidance.</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def display_industry_report(report):
    """Display comprehensive modern bias analysis report."""

    st.markdown('<div class="section-header">Executive Summary</div>', unsafe_allow_html=True)

    severity = report["severity_analysis"]
    sev_level = severity["severity_level"]
    sev_class = {"High": "sev-high", "Moderate": "sev-medium", "Low": "sev-low"}.get(sev_level, "sev-low")
    sev_icon = {"High": "⚠", "Moderate": "◈", "Low": "✓"}.get(sev_level, "✓")

    st.markdown(f"""
    <div class="{sev_class}">
        <div class="sev-title">{sev_icon}  Bias Severity: {sev_level}</div>
        <div class="sev-meta">Score: {severity['severity_score']:.3f} &nbsp;·&nbsp; Confidence: {severity['confidence']*100:.0f}%</div>
    </div>
    """, unsafe_allow_html=True)

    if "bias_summary" in report:
        st.markdown(f'<p style="color:#9090b0;font-size:0.9rem;line-height:1.7;margin:1rem 0;">{report["bias_summary"]}</p>',
                    unsafe_allow_html=True)

    st.markdown('<div class="section-header">Key Metrics</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    acc = report['overall_model_performance']['accuracy']
    dp  = report['fairness_metrics'].get('demographic_parity_difference', 0)
    eo  = report['fairness_metrics'].get('equalized_odds_difference', 0)
    n_bias = len([b for b in report['detected_biases'] if b != "No Significant Bias Detected"])

    for col, label, value, sub in [
        (c1, "Overall Accuracy",       f"{acc:.3f}",  "Model performance"),
        (c2, "Demographic Parity Gap", f"{dp:.3f}",   "Threshold: 0.10"),
        (c3, "Equalized Odds Gap",     f"{eo:.3f}",   "Threshold: 0.05"),
        (c4, "Bias Types Detected",    str(n_bias),   "Unique bias signals"),
    ]:
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-sub">{sub}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">Bias Analysis</div>', unsafe_allow_html=True)

    if "bias_explanations" in report and report["bias_explanations"]:
        for i, explanation in enumerate(report["bias_explanations"], 1):
            label = report['detected_biases'][i-1] if i-1 < len(report['detected_biases']) else f"Finding {i}"
            with st.expander(f"  {i:02d} · {label}", expanded=(i == 1)):
                st.markdown(f'<div style="color:#a0a0c0;font-size:0.87rem;line-height:1.7;">{explanation}</div>',
                            unsafe_allow_html=True)
    else:
        st.info("No detailed explanations available.")

    if "mitigation_suggestions" in report:
        suggestions = report["mitigation_suggestions"]
        st.markdown('<div class="section-header">Mitigation Strategies</div>', unsafe_allow_html=True)

        if suggestions.get("priority_actions"):
            st.markdown('<p style="font-family:\'DM Mono\',monospace;font-size:0.72rem;color:#5a587a;'
                        'letter-spacing:0.12em;text-transform:uppercase;margin-bottom:0.75rem;">Priority Actions</p>',
                        unsafe_allow_html=True)
            for i, action in enumerate(suggestions["priority_actions"], 1):
                st.markdown(f"""
                <div class="insight-box">
                    <h4>{i}. {action['action']}</h4>
                    <p style="color:#8080a0;font-size:0.85rem;margin:0.3rem 0 0.5rem;">{action['description']}</p>
                    <span class="impact-tag">⬡ {action['category']} · {action['impact']}</span>
                </div>
                """, unsafe_allow_html=True)

        if suggestions.get("detailed_recommendations"):
            st.markdown('<p style="font-family:\'DM Mono\',monospace;font-size:0.72rem;color:#5a587a;'
                        'letter-spacing:0.12em;text-transform:uppercase;margin:1.5rem 0 0.75rem;">Detailed Recommendations</p>',
                        unsafe_allow_html=True)
            for category, items in suggestions["detailed_recommendations"].items():
                with st.expander(f"  {category}"):
                    for i, item in enumerate(items, 1):
                        st.markdown(f'**{i}. {item["action"]}**')
                        st.markdown(f'<p style="color:#8080a0;font-size:0.85rem;">{item["description"]}</p>',
                                    unsafe_allow_html=True)
                        if 'implementation' in item:
                            st.code(item['implementation'], language="python")
                        st.markdown(f'<span class="impact-tag">Impact: {item["impact"]}</span>',
                                    unsafe_allow_html=True)
                        if i < len(items):
                            st.divider()

        col_tl, col_sm = st.columns(2)
        with col_tl:
            if suggestions.get("implementation_timeline"):
                st.markdown('<p style="font-family:\'DM Mono\',monospace;font-size:0.72rem;color:#5a587a;'
                            'letter-spacing:0.12em;text-transform:uppercase;margin-bottom:0.5rem;">Timeline</p>',
                            unsafe_allow_html=True)
                for i, step in enumerate(suggestions["implementation_timeline"], 1):
                    st.markdown(f"""
                    <div style="display:flex;gap:0.75rem;margin-bottom:0.5rem;align-items:flex-start;">
                        <span style="font-family:'DM Mono',monospace;font-size:0.65rem;color:#7c6ff7;
                              background:rgba(124,111,247,0.1);border:1px solid rgba(124,111,247,0.2);
                              border-radius:4px;padding:0.15rem 0.4rem;flex-shrink:0;">{i:02d}</span>
                        <span style="font-size:0.85rem;color:#9090b0;">{step}</span>
                    </div>
                    """, unsafe_allow_html=True)
        with col_sm:
            if suggestions.get("success_metrics"):
                st.markdown('<p style="font-family:\'DM Mono\',monospace;font-size:0.72rem;color:#5a587a;'
                            'letter-spacing:0.12em;text-transform:uppercase;margin-bottom:0.5rem;">Success Metrics</p>',
                            unsafe_allow_html=True)
                for metric in suggestions["success_metrics"]:
                    st.markdown(f'<p style="font-size:0.85rem;color:#9090b0;margin:0.4rem 0;">◈ {metric}</p>',
                                unsafe_allow_html=True)

    st.markdown('<div class="section-header">Visual Analytics</div>', unsafe_allow_html=True)
    create_bias_visualizations(report)

    st.markdown('<div class="section-header">Technical Details</div>', unsafe_allow_html=True)

    for label, key in [
        ("Dataset Bias Analysis", "dataset_bias"),
        ("Fairness Metrics",      "fairness_metrics"),
        ("Model Performance",     "overall_model_performance"),
        ("Subgroup Performance",  "subgroup_performance"),
        ("Detected Biases",       "detected_biases"),
    ]:
        with st.expander(f"  {label}"):
            if key == "detected_biases":
                st.write(report[key])
            else:
                st.json(report[key])

    st.markdown('<div class="section-header">Export</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)

    severity = report["severity_analysis"]

    with c1:
        st.download_button(
            label="↓ Full Report (JSON)",
            data=json.dumps(report, indent=2),
            file_name=f"bias_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True,
        )
    with c2:
        summary_df = pd.DataFrame({
            "Metric": ["Severity Score", "Confidence", "Accuracy",
                       "Demographic Parity Gap", "Equalized Odds Gap", "Bias Types Detected"],
            "Value": [
                severity["severity_score"], severity["confidence"],
                report["overall_model_performance"]["accuracy"],
                report["fairness_metrics"].get("demographic_parity_difference", 0),
                report["fairness_metrics"].get("equalized_odds_difference", 0),
                len([b for b in report['detected_biases'] if b != "No Significant Bias Detected"]),
            ]
        })
        st.download_button(
            label="↓ Summary (CSV)",
            data=summary_df.to_csv(index=False),
            file_name=f"bias_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with c3:
        if st.button("✕ Clear Analysis", use_container_width=True):
            st.session_state.analysis_complete = False
            st.session_state.current_report = None
            st.rerun()


def create_bias_visualizations(report):
    """Interactive Plotly charts styled for the dark theme."""

    DARK_BG      = "#09090f"
    CARD_BG      = "#0d0d1a"
    GRID_COLOR   = "#1e1e2e"
    TEXT_COLOR   = "#6060a0"
    FONT_FAMILY  = "DM Mono, monospace"
    ACCENT       = ["#7c6ff7", "#a78bfa", "#10b981", "#f59e0b", "#ec4899", "#38bdf8"]

    base_layout = dict(
        paper_bgcolor=CARD_BG,
        plot_bgcolor=CARD_BG,
        font=dict(family=FONT_FAMILY, color=TEXT_COLOR, size=11),
        margin=dict(l=24, r=24, t=48, b=24),
        height=380,
        xaxis=dict(gridcolor=GRID_COLOR, linecolor=GRID_COLOR, tickfont=dict(size=10)),
        yaxis=dict(gridcolor=GRID_COLOR, linecolor=GRID_COLOR, tickfont=dict(size=10)),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=GRID_COLOR, borderwidth=1,
                    font=dict(size=10)),
    )

    if report.get("subgroup_performance"):
        sg = report["subgroup_performance"]
        groups    = list(sg.keys())
        acc_vals  = [sg[g].get("accuracy",  0) * 100 for g in groups]
        prec_vals = [sg[g].get("precision", 0) * 100 for g in groups]
        rec_vals  = [sg[g].get("recall",    0) * 100 for g in groups]

        fig = go.Figure()
        for name, vals, color in [
            ("Accuracy",  acc_vals,  ACCENT[0]),
            ("Precision", prec_vals, ACCENT[2]),
            ("Recall",    rec_vals,  ACCENT[3]),
        ]:
            fig.add_trace(go.Bar(
                name=name, x=groups, y=vals,
                marker=dict(color=color, opacity=0.85, cornerradius=4),
            ))

        layout = dict(**base_layout)
        layout.update(
            title=dict(text="Performance by Demographic Group", font=dict(size=13, color="#a0a0c0")),
            barmode="group",
            bargap=0.25,
            bargroupgap=0.08,
        )
        fig.update_layout(**layout)
        st.plotly_chart(fig, use_container_width=True)

    if report.get("dataset_bias"):
        attrs = [(k, v) for k, v in report["dataset_bias"].items()
                 if k != "intersectional" and "distribution" in v and v["distribution"]]

        if attrs:
            cols = st.columns(min(len(attrs), 2))
            for idx, (attr, data) in enumerate(attrs):
                groups = list(data["distribution"].keys())
                pcts   = [data["distribution"][g] * 100 for g in groups]

                fig = go.Figure(go.Pie(
                    labels=groups, values=pcts,
                    hole=0.5,
                    marker=dict(colors=ACCENT, line=dict(color=DARK_BG, width=2)),
                    textfont=dict(family=FONT_FAMILY, size=10),
                    textposition="outside",
                ))

                layout = dict(**base_layout)
                layout.update(
                    title=dict(text=f"Distribution · {attr.title()}", font=dict(size=13, color="#a0a0c0")),
                    showlegend=True,
                    height=360,
                )
                del layout["xaxis"], layout["yaxis"]
                fig.update_layout(**layout)

                with cols[idx % 2]:
                    st.plotly_chart(fig, use_container_width=True)
                    if "chi_square_p_value" in data:
                        p = data["chi_square_p_value"]
                        sig = "Significant" if p < 0.05 else "Not Significant"
                        sig_color = "#ef4444" if p < 0.05 else "#10b981"
                        st.markdown(
                            f'<p style="font-family:\'DM Mono\',monospace;font-size:0.7rem;color:{sig_color};">'
                            f'χ² p-value: {p:.6f} · {sig}</p>',
                            unsafe_allow_html=True
                        )

    fm = report["fairness_metrics"]
    metrics_labels = ["Demographic Parity", "Equalized Odds"]
    metrics_vals   = [fm.get("demographic_parity_difference", 0),
                      fm.get("equalized_odds_difference", 0)]
    thresholds     = [0.10, 0.05]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Current Value",
        x=metrics_labels,
        y=metrics_vals,
        marker=dict(color=[ACCENT[0], ACCENT[2]], opacity=0.85, cornerradius=6),
        width=0.4,
    ))
    fig.add_trace(go.Scatter(
        name="Industry Threshold",
        x=metrics_labels,
        y=thresholds,
        mode="lines+markers",
        line=dict(color="#ef4444", dash="dot", width=1.5),
        marker=dict(color="#ef4444", size=7, symbol="diamond"),
    ))

    layout = dict(**base_layout)
    layout.update(
        title=dict(text="Fairness Metrics vs Industry Thresholds", font=dict(size=13, color="#a0a0c0")),
    )
    fig.update_layout(**layout)
    st.plotly_chart(fig, use_container_width=True)