import pandas as pd
import streamlit as st


def render_sidebar(df: pd.DataFrame) -> dict:
    with st.sidebar:
        st.header("Interactive Filters")
        column = st.selectbox("Column selector", options=[""] + list(df.columns), index=0)
        category = None
        if column and column in df.columns and df[column].dtype == "object":
            category = st.selectbox("Category selector", options=["All"] + sorted(df[column].dropna().astype(str).unique().tolist()))
        date_col = st.selectbox("Date filter", options=[""] + [c for c in df.columns if "date" in c.lower() or "time" in c.lower()], index=0)
        numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
        range_value = None
        if numeric_cols:
            min_val = float(df[numeric_cols[0]].min()) if pd.notna(df[numeric_cols[0]].min()) else 0.0
            max_val = float(df[numeric_cols[0]].max()) if pd.notna(df[numeric_cols[0]].max()) else 1.0
            range_value = st.slider("Numeric range", min_value=min_val, max_value=max_val, value=(min_val, max_val))
        search = st.text_input("Search")
    filtered_df = df.copy()
    if column and column in df.columns and category and category != "All":
        filtered_df = filtered_df[filtered_df[column].astype(str) == category]
    if date_col:
        try:
            filtered_df = filtered_df.dropna(subset=[date_col])
        except Exception:
            pass
    if search:
        filtered_df = filtered_df[filtered_df.astype(str).apply(lambda row: search.lower() in " ".join(row).lower(), axis=1)]
    return {"filtered_df": filtered_df, "column": column, "category": category, "date_col": date_col, "search": search, "range_value": range_value}
