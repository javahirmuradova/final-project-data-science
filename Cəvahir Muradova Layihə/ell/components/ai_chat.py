import pandas as pd
import streamlit as st


def render_chat_section(df: pd.DataFrame) -> None:
    st.markdown("### Ask the Analyst")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    for entry in st.session_state.chat_history:
        with st.chat_message(entry["role"]):
            st.markdown(entry["content"])
    prompt = st.chat_input("Ask about the dataset")
    if prompt:
        response = generate_response(df, prompt)
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)


def generate_response(df: pd.DataFrame, prompt: str) -> str:
    prompt = prompt.lower()
    if "missing" in prompt:
        return f"The dataset has {df.isna().sum().sum()} missing values. The largest missingness comes from columns with the highest null count."
    if "correlation" in prompt or "correl" in prompt:
        numeric = df.select_dtypes(include=['number']).columns.tolist()
        if len(numeric) >= 2:
            return f"The strongest numeric relationships can be inspected across the columns: {', '.join(numeric[:5])}."
        return "There are not enough numeric columns to compute a meaningful correlation summary."
    if "summar" in prompt:
        return f"This dataset has {df.shape[0]} rows and {df.shape[1]} columns. It contains {len(df.select_dtypes(include=['number']).columns)} numeric fields and {len(df.select_dtypes(exclude=['number']).columns)} non-numeric fields."
    if "anomal" in prompt:
        return "Anomalies should be inspected using z-scores, IQR rules, and category frequency checks for outliers and rare values."
    if "preprocess" in prompt:
        return "Suggested preprocessing includes imputation for missing values, encoding for categorical features, and scaling for numeric features."
    if "model" in prompt:
        return "Suggested models include linear regression for numeric targets, random forest or XGBoost for tabular tasks, and clustering for unlabeled data."
    return "I can help explain missing values, correlations, anomalies, preprocessing, and modeling recommendations for this dataset."
