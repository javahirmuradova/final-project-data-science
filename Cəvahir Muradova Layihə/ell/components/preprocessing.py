import pandas as pd
import streamlit as st


def render_preprocessing_section(df: pd.DataFrame) -> None:
    st.markdown("### Feature Engineering Suggestions")
    suggestions = []
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    if len(numeric_cols) >= 2:
        suggestions.append("Create interaction features by multiplying or combining strong numeric predictors.")
    if any(c.lower().endswith(("date", "time")) for c in df.columns):
        suggestions.append("Generate date-based features such as day, month, hour, weekday, and weekend flags.")
    if df.shape[0] > 100:
        suggestions.append("Consider polynomial features for non-linear relationships in regression tasks.")
    if df.select_dtypes(include=['object']).shape[1] > 0:
        suggestions.append("Apply one-hot or target encoding for categorical variables before model training.")
    suggestions.append("Use standard scaling or normalization for distance-based algorithms.")
    for item in suggestions:
        st.write(f"• {item}")
    st.markdown("### ML Recommendation")
    if len(numeric_cols) >= 2:
        st.write("Regression is recommended if the target is numeric and you need to predict a continuous value.")
        st.write("Classification is recommended if the target is categorical and you need a label prediction.")
        st.write("Clustering is recommended if there is no labeled target and you want to discover structure in the data.")
        st.write("Time series modeling is recommended if there is a clear temporal ordering and seasonality.")
