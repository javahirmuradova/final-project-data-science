import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.stats import detect_outliers


def render_eda_section(df: pd.DataFrame) -> None:
    st.markdown("### Distribution Analysis")
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    if numeric_cols:
        col = st.selectbox("Numeric axis", options=numeric_cols, key="eda_num")
        fig1 = px.histogram(df, x=col, nbins=30, title=f"Histogram - {col}")
        fig2 = px.box(df, y=col, title=f"Boxplot - {col}")
        fig3 = px.violin(df, y=col, title=f"Violin Plot - {col}")
        st.plotly_chart(fig1, use_container_width=True)
        st.plotly_chart(fig2, use_container_width=True)
        st.plotly_chart(fig3, use_container_width=True)
    if len(numeric_cols) >= 2:
        fig = px.scatter_matrix(df[numeric_cols[:5]], title="Scatter Matrix")
        st.plotly_chart(fig, use_container_width=True)
        corr = df[numeric_cols].corr().round(2)
        fig_corr = px.imshow(corr, text_auto=True, title="Correlation Matrix")
        st.plotly_chart(fig_corr, use_container_width=True)
    categorical_cols = [c for c in df.columns if c not in numeric_cols]
    if categorical_cols:
        cat = st.selectbox("Categorical axis", options=categorical_cols, key="eda_cat")
        counts = df[cat].value_counts().head(12)
        fig = px.bar(counts, x=counts.index, y=counts.values, title=f"Top categories - {cat}")
        st.plotly_chart(fig, use_container_width=True)
    outlier_counts = detect_outliers(df)
    if outlier_counts:
        st.markdown("### Outlier Detection")
        st.dataframe(pd.DataFrame({"column": list(outlier_counts.keys()), "outlier_count": list(outlier_counts.values())}), use_container_width=True)
