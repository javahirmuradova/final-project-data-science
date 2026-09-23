import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


def render_chart_section(df: pd.DataFrame) -> None:
    st.markdown("### Recommended Visualizations")
    if df.empty:
        st.info("No data available")
        return
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    obj_cols = [c for c in df.columns if c not in numeric_cols]
    if numeric_cols:
        col = st.selectbox("Choose numeric column", options=numeric_cols)
        fig = px.histogram(df, x=col, marginal="box", title=f"Distribution of {col}")
        st.plotly_chart(fig, use_container_width=True)
    if len(numeric_cols) >= 2:
        corr = df[numeric_cols].corr().round(2)
        fig = px.imshow(corr, text_auto=True, title="Correlation Heatmap")
        st.plotly_chart(fig, use_container_width=True)
    if obj_cols:
        col = st.selectbox("Choose categorical column", options=obj_cols, key="cat_col")
        counts = df[col].value_counts().head(10)
        fig = px.bar(counts, x=counts.index, y=counts.values, title=f"Top categories for {col}")
        st.plotly_chart(fig, use_container_width=True)
    recs = [
        "Boxplot is recommended because the numeric column shows spread and possible outliers.",
        "Histogram is recommended because the distribution is important for feature engineering.",
        "Correlation heatmap is recommended because you need to understand relationships between numeric variables.",
    ]
    for rec in recs:
        st.write(f"• {rec}")
