import pandas as pd
import streamlit as st
from utils.helper import format_bytes


def render_kpi_cards(df: pd.DataFrame, profile: dict) -> None:
    metrics = [
        ("Rows", profile["rows"]),
        ("Columns", profile["columns"]),
        ("Missing", f"{df.isna().sum().sum()} ({round(df.isna().mean().mean() * 100, 2)}%)"),
        ("Duplicates", int(df.duplicated().sum())),
        ("Memory", format_bytes(int(df.memory_usage(deep=True).sum()))),
        ("Numerical", int(df.select_dtypes(include=['number']).shape[1])),
        ("Categorical", int(df.select_dtypes(include=['object']).shape[1])),
    ]
    cols = st.columns(len(metrics))
    for col, (label, value) in zip(cols, metrics):
        with col:
            st.metric(label=label, value=value)
