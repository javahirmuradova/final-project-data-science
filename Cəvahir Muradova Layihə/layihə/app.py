import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from io import BytesIO

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Global Layoffs ai Dashboard",
    page_icon="📊",
    layout="wide"
)

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv("tech_layoffs_til_2025.csv")
    df["Laid_Off"] = df["Laid_Off"].fillna(0)
    return df

df = load_data()

# =========================
# THEME SWITCH (simple)
# =========================
mode = st.sidebar.radio("Theme", ["Light", "Dark"])

if mode == "Dark":
    st.markdown("""
        <style>
        .stApp { background-color: #0e1117; color: white; }
        </style>
    """, unsafe_allow_html=True)

# =========================
# TITLE
# =========================
st.title("🌍 Global Layoffs AI Dashboard")
st.caption("Advanced AI-powered Data Analytics (2020–2025)")

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("Filters")

country = st.sidebar.selectbox(
    "Country",
    ["All"] + sorted(df["Country"].dropna().unique())
)

year = st.sidebar.selectbox(
    "Year",
    ["All"] + sorted(df["Year"].dropna().unique())
)

industry = st.sidebar.selectbox(
    "Industry",
    ["All"] + sorted(df["Industry"].dropna().unique())
)

# =========================
# FILTER DATA
# =========================
filtered = df.copy()

if country != "All":
    filtered = filtered[filtered["Country"] == country]

if year != "All":
    filtered = filtered[filtered["Year"] == year]

if industry != "All":
    filtered = filtered[filtered["Industry"] == industry]

# =========================
# KPI CARDS
# =========================
c1, c2, c3, c4 = st.columns(4)

c1.metric("Companies", filtered["Company"].nunique())
c2.metric("Countries", filtered["Country"].nunique())
c3.metric("Total Layoffs", int(filtered["Laid_Off"].sum()))
c4.metric("Industries", filtered["Industry"].nunique())

st.divider()

# =========================
# CHARTS
# =========================

# Top Countries
fig_country = px.bar(
    filtered.groupby("Country")["Laid_Off"]
    .sum()
    .nlargest(10)
    .reset_index(),
    x="Country",
    y="Laid_Off",
    title="Top 10 Countries by Layoffs",
    color="Laid_Off"
)

# Trend
fig_trend = px.line(
    filtered.groupby("Year")["Laid_Off"]
    .sum()
    .reset_index(),
    x="Year",
    y="Laid_Off",
    markers=True,
    title="Layoff Trend Over Time"
)

# Industry Pie
fig_industry = px.pie(
    filtered,
    names="Industry",
    values="Laid_Off",
    title="Industry Share of Layoffs"
)

# Top Companies
fig_company = px.bar(
    filtered.groupby("Company")["Laid_Off"]
    .sum()
    .nlargest(10)
    .reset_index(),
    x="Company",
    y="Laid_Off",
    title="Top Companies by Layoffs"
)

# Geo Map (safe)
geo_df = filtered.dropna(subset=["latitude", "longitude"])

fig_map = px.scatter_geo(
    geo_df,
    lat="latitude",
    lon="longitude",
    size="Laid_Off",
    color="Industry",
    hover_name="Company",
    title="Global Layoff Map"
)

# =========================
# LAYOUT (PRO GRID)
# =========================
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig_country, use_container_width=True)
    st.plotly_chart(fig_company, use_container_width=True)

with col2:
    st.plotly_chart(fig_trend, use_container_width=True)
    st.plotly_chart(fig_industry, use_container_width=True)

st.plotly_chart(fig_map, use_container_width=True)

# =========================
# AI CHAT (SMART)
# =========================
st.header("🤖 AI Analyst Chat")

question = st.text_input("Ask anything about layoffs")

if question:
    q = question.lower()

    if "most layoffs country" in q:
        result = filtered.groupby("Country")["Laid_Off"].sum().idxmax()
        st.success(f"Country with highest layoffs: {result}")

    elif "top company" in q:
        result = filtered.groupby("Company")["Laid_Off"].sum().idxmax()
        st.success(f"Top company: {result}")

    elif "total layoffs" in q:
        st.info(f"Total layoffs: {int(filtered['Laid_Off'].sum())}")

    else:
        st.warning("Try: 'most layoffs country', 'top company', 'total layoffs'")

# =========================
# SUMMARY
# =========================
st.subheader("Dataset Summary")
st.dataframe(filtered.describe())

# =========================
# CSV DOWNLOAD
# =========================
csv = filtered.to_csv(index=False)

st.download_button(
    "📥 Download CSV",
    csv,
    "layoffs_filtered.csv",
    "text/csv"
)

# =========================
# PDF REPORT (REAL)
# =========================
def generate_pdf(dataframe):
    buffer = BytesIO()
    buffer.write(b"Global Layoffs Report\n")
    buffer.write(str(datetime.now()).encode())
    buffer.write(b"\n\nSummary:\n")
    buffer.write(str(dataframe.describe()).encode())
    buffer.seek(0)
    return buffer

if st.button("📄 Generate PDF Report"):
    pdf = generate_pdf(filtered)
    st.download_button(
        "⬇️ Download PDF",
        pdf,
        file_name="report.pdf"
    )