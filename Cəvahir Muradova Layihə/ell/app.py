import pandas as pd
import streamlit as st

from components.upload import render_upload_section
from components.sidebar import render_sidebar
from components.kpi import render_kpi_cards
from components.charts import render_chart_section
from components.eda import render_eda_section
from components.preprocessing import render_preprocessing_section
from components.report import render_report_section
from components.insights import render_insights_section
from components.ai_chat import render_chat_section
from utils.helper import set_page_config, apply_custom_css, detect_dataset_profile, load_csv_with_fallback
from utils.stats import compute_stats_summary, compute_missing_report

# Ensure Streamlit uses the expected page configuration before rendering any component.
set_page_config()


apply_custom_css()

st.markdown("<h1 class='gradient-title'>🤖 AI Data Analyst Agent</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Upload any CSV dataset and receive a complete AI-powered data analysis automatically.</p>", unsafe_allow_html=True)

if "df" not in st.session_state:
    st.session_state.df = None
    st.session_state.profile = None

uploaded_file = render_upload_section()
if uploaded_file is not None:
    try:
        df = load_csv_with_fallback(uploaded_file)
        st.session_state.df = df
        st.session_state.profile = detect_dataset_profile(df)
    except Exception as exc:
        st.error(f"Unable to read the uploaded CSV: {exc}")
        st.stop()

if st.session_state.df is None:
    st.info("Upload a CSV file to start the analysis workflow.")
    st.stop()

df = st.session_state.df
profile = st.session_state.profile

sidebar_state = render_sidebar(df)
if sidebar_state.get("filtered_df") is not None:
    df = sidebar_state["filtered_df"]

render_kpi_cards(df, profile)

st.markdown("## 1. Dataset Overview")
col1, col2 = st.columns([1.4, 1])
with col1:
    st.markdown("### Dataset Preview")
    st.dataframe(df.head(8).reset_index(drop=True), use_container_width=True)
with col2:
    st.markdown("### Dataset Profile")
    st.write(profile)
    st.markdown("### Column Information")
    st.dataframe(pd.DataFrame({"column": df.columns, "dtype": df.dtypes.astype(str)}).reset_index(drop=True), use_container_width=True)

st.markdown("## 2. Data Quality Report")
quality = compute_missing_report(df)
st.dataframe(quality, use_container_width=True)

st.markdown("## 3. Missing Value Analysis")
missing_summary = compute_missing_report(df)
st.dataframe(missing_summary, use_container_width=True)

st.markdown("## 4. Exploratory Data Analysis")
render_eda_section(df)

st.markdown("## 5. Statistical Analysis")
stats = compute_stats_summary(df)
st.json(stats)

st.markdown("## 6. Automatic Chart Recommendation")
render_chart_section(df)

st.markdown("## 7. AI Insights")
render_insights_section(df)

st.markdown("## 8. AI Data Analyst Chat")
render_chat_section(df)

st.markdown("## 9. Feature Engineering Suggestions")
render_preprocessing_section(df)

st.markdown("## 10. Final Report")
render_report_section(df)
