import os
import pandas as pd
import streamlit as st

try:
    from openai import OpenAI
except Exception:  # pragma: no cover
    OpenAI = None


def _get_llm_insights(df: pd.DataFrame) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or OpenAI is None:
        return None
    client = OpenAI(api_key=api_key)
    prompt = (
        "You are an expert data analyst. Summarize the dataset in 8 concise bullet points focusing on "
        f"rows={df.shape[0]}, columns={df.shape[1]}, missing_values={df.isna().sum().sum()}, duplicates={df.duplicated().sum()}, "
        f"numeric_columns={len(df.select_dtypes(include=['number']).columns)}, categorical_columns={len(df.select_dtypes(exclude=['number']).columns)}."
    )
    try:
        completion = client.responses.create(
            model="gpt-4o-mini",
            input=prompt,
            max_output_tokens=250,
        )
        return completion.output_text
    except Exception:
        return None


def render_insights_section(df: pd.DataFrame) -> None:
    st.markdown("### AI-Style Insights")
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    summary = []
    summary.append(f"The dataset has {df.shape[0]} rows and {df.shape[1]} columns, with {df.isna().sum().sum()} missing values.")
    if numeric_cols:
        top_col = numeric_cols[0]
        summary.append(f"The column {top_col} appears to be the strongest numeric signal for further analysis.")
    if df.duplicated().sum() > 0:
        summary.append("Duplicated rows were found and should be reviewed before modeling.")
    if df.select_dtypes(include=['object']).shape[1] > 0:
        summary.append("Categorical features are available and may require encoding before machine learning.")
    for item in summary:
        st.write(f"• {item}")
    llm_insights = _get_llm_insights(df)
    if llm_insights:
        st.markdown("### LLM Insight")
        st.write(llm_insights)
    st.markdown("### Business Recommendations")
    st.write("• Drop or impute low-information columns with high missingness.")
    st.write("• Use robust scaling if outliers are present.")
    st.write("• Validate assumptions before fitting models and compare multiple algorithms.")
