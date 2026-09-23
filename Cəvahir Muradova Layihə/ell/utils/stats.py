from typing import Dict, Any
import numpy as np
import pandas as pd
import streamlit as st
from scipy import stats


@st.cache_data(show_spinner=False)
def compute_missing_report(df: pd.DataFrame) -> pd.DataFrame:
    missing = df.isna().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    missing_df = pd.DataFrame({"missing_count": missing, "missing_pct": missing_pct})
    missing_df = missing_df[missing_df["missing_count"] > 0]
    return missing_df.sort_values(["missing_count", "missing_pct"], ascending=False)


@st.cache_data(show_spinner=False)
def compute_stats_summary(df: pd.DataFrame) -> Dict[str, Any]:
    numeric_df = df.select_dtypes(include=[np.number])
    summary = {}
    for column in numeric_df.columns:
        series = numeric_df[column].dropna()
        if series.empty:
            continue
        summary[column] = {
            "mean": float(series.mean()),
            "median": float(series.median()),
            "mode": float(series.mode().iloc[0]) if not series.mode().empty else None,
            "variance": float(series.var()),
            "std": float(series.std()),
            "skewness": float(series.skew()),
            "kurtosis": float(series.kurt()),
            "quantiles": {q: float(series.quantile(q)) for q in [0.25, 0.5, 0.75]},
        }
    return summary


@st.cache_data(show_spinner=False)
def detect_outliers(df: pd.DataFrame) -> Dict[str, Any]:
    outlier_report = {}
    numeric_df = df.select_dtypes(include=[np.number])
    for column in numeric_df.columns:
        series = numeric_df[column].dropna()
        if series.empty or series.nunique() <= 1:
            continue
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        mask = (series < lower) | (series > upper)
        outlier_report[column] = int(mask.sum())
    return outlier_report


@st.cache_data(show_spinner=False)
def run_normality_tests(df: pd.DataFrame) -> Dict[str, Any]:
    result = {}
    numeric_df = df.select_dtypes(include=[np.number])
    for column in numeric_df.columns:
        series = numeric_df[column].dropna()
        if series.empty or series.nunique() <= 2:
            continue
        try:
            stat, p_value = stats.shapiro(series)
            result[column] = {"shapiro_stat": float(stat), "p_value": float(p_value)}
        except Exception:
            continue
    return result
