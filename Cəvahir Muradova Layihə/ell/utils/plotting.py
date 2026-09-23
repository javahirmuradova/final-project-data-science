from typing import List
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def make_histogram(df: pd.DataFrame, column: str):
    return px.histogram(df, x=column, title=f"Distribution: {column}", marginal="box")


def make_boxplot(df: pd.DataFrame, column: str):
    return px.box(df, y=column, title=f"Boxplot: {column}")


def make_scatter(df: pd.DataFrame, x_col: str, y_col: str):
    return px.scatter(df, x=x_col, y=y_col, title=f"{x_col} vs {y_col}")


def make_correlation_heatmap(df: pd.DataFrame):
    numeric = df.select_dtypes(include=['number'])
    corr = numeric.corr().round(3)
    return px.imshow(corr, text_auto=True, title="Correlation Heatmap")


def make_bar_chart(df: pd.DataFrame, column: str, top_n: int = 10):
    counts = df[column].value_counts().head(top_n)
    return px.bar(counts, x=counts.index, y=counts.values, title=f"Top values: {column}")
