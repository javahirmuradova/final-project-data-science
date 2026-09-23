import io
import pandas as pd
import streamlit as st

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
except Exception:  # pragma: no cover
    letter = None
    canvas = None


def render_report_section(df: pd.DataFrame) -> None:
    st.markdown("### Export Report")
    if st.button("Generate PDF Summary"):
        if canvas is None or letter is None:
            st.warning("ReportLab is not available in the current environment.")
        else:
            buffer = io.BytesIO()
            c = canvas.Canvas(buffer, pagesize=letter)
            c.setFont("Helvetica-Bold", 16)
            c.drawString(40, 760, "AI Data Analyst Agent Report")
            c.setFont("Helvetica", 11)
            c.drawString(40, 740, f"Rows: {df.shape[0]} | Columns: {df.shape[1]}")
            c.drawString(40, 722, f"Missing values: {df.isna().sum().sum()}")
            c.drawString(40, 704, f"Duplicate rows: {df.duplicated().sum()}")
            c.save()
            buffer.seek(0)
            st.download_button("Download PDF", data=buffer.getvalue(), file_name="ai_data_analyst_report.pdf", mime="application/pdf")
    st.download_button("Download CSV Summary", data=df.head(50).to_csv(index=False).encode(), file_name="ai_data_analyst_summary.csv", mime="text/csv")
    st.download_button("Download HTML Summary", data=df.head(50).to_html(index=False).encode(), file_name="ai_data_analyst_summary.html", mime="text/html")
