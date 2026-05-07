# -*- coding: utf-8 -*-
"""
Created on Thu May  7 04:43:25 2026

@author: DENZEN COMPUTER
"""

import streamlit as st
import pandas as pd

# 1. Title and configuration
st.set_page_config(page_title="Data Explorer Pro")
st.title("📊 Data Analysis App")

# 2. Support both CSV and XLSX
uploaded_file = st.file_uploader("Upload your data", type=["csv", "xlsx"])

# 3. Handle data loading
if uploaded_file is not None:
    # Determine which function to use based on file extension
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Display dataset
    st.subheader("Dataset Preview")
    st.dataframe(df)

    # 4. Summary statistics
    st.subheader("Summary Statistics")
    st.write(df.describe())

    # 5. Identify numeric columns
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()

    if numeric_cols:
        st.subheader("Data Visualization")
        selected_col = st.selectbox("Select a column to visualize:", numeric_cols)

        # 6. Generate Histogram
        st.write(f"### Distribution of {selected_col}")
        # Using st.bar_chart on value_counts creates a simple histogram effect
        counts = df[selected_col].value_counts().sort_index()
        st.bar_chart(counts)
    else:
        st.warning("No numeric columns available for visualization.")
else:
    st.info("Please upload a CSV or Excel file.")
