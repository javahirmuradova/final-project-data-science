import io
import hashlib
from typing import Any, Dict
import pandas as pd
import streamlit as st


def set_page_config() -> None:
    st.set_page_config(page_title="AI Data Analyst Agent", page_icon="🤖", layout="wide")


def apply_custom_css() -> None:
    st.markdown(
        """
        <style>
        :root {
            --bg: #07111f;
            --panel: rgba(255,255,255,0.06);
            --text: #ecf2ff;
            --muted: #9fb2d8;
            --accent: #6c63ff;
            --accent-2: #2dd4bf;
        }
        .stApp {
            background: radial-gradient(circle at top left, rgba(109, 40, 217, 0.25), transparent 25%),
                        radial-gradient(circle at bottom right, rgba(45, 212, 191, 0.18), transparent 25%),
                        linear-gradient(135deg, #07111f 0%, #111827 100%);
            color: var(--text);
        }
        .gradient-title {
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(90deg, #8b5cf6, #22d3ee, #34d399);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.3rem;
        }
        .subtitle {
            color: #cbd5e1;
            font-size: 1.05rem;
            margin-bottom: 1rem;
        }
        div[data-testid="stMetric"] {
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.12);
            box-shadow: 0 10px 28px rgba(0,0,0,0.22);
            border-radius: 18px;
            padding: 0.75rem 1rem;
        }
        .stDataFrame, .stTable {
            border-radius: 14px;
            overflow: hidden;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def format_bytes(size: int) -> str:
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024 or unit == "GB":
            return f"{size:.2f} {unit}" if unit != "B" else f"{size} {unit}"
        size /= 1024.0
    return f"{size:.2f} GB"


@st.cache_data(show_spinner=False)
def load_csv_with_fallback(uploaded_file: Any) -> pd.DataFrame:
    if uploaded_file is None:
        raise ValueError("No file provided")
    if uploaded_file.name.endswith(".csv"):
        raw_bytes = uploaded_file.getvalue()
        try:
            return pd.read_csv(io.BytesIO(raw_bytes))
        except UnicodeDecodeError:
            return pd.read_csv(io.BytesIO(raw_bytes), encoding="latin1")
    raise ValueError("Only CSV uploads are supported")


@st.cache_data(show_spinner=False)
def detect_dataset_profile(df: pd.DataFrame) -> Dict[str, Any]:
    profile = {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_names": list(df.columns),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "memory_usage": format_bytes(int(df.memory_usage(deep=True).sum())),
        "duplicate_rows": int(df.duplicated().sum()),
        "missing_percentage": round(float(df.isna().mean().mean() * 100), 2),
    }
    return profile


def hash_text(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()
