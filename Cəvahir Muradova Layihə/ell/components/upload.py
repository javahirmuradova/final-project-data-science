import streamlit as st


def render_upload_section():
    with st.container():
        uploaded_file = st.file_uploader("Upload CSV dataset", type=["csv"], accept_multiple_files=False)
    return uploaded_file
