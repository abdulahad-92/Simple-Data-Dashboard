# -*- coding: utf-8 -*-
"""
Created on Thu May  7 04:55:01 2026

@author: DENZEN COMPUTER
"""

import streamlit as st   
import pandas as pd
import plotly.express as px

#temp


st.set_page_config(page_title="Interactive Data Dashboard", layout="wide")
st.title("📈 Advanced Data Analytics Dashboard")

# 1 & 2. File Upload (CSV and XLSX)
uploaded_file = st.file_uploader("Upload your data", type=["csv", "xlsx"])

if uploaded_file:
    # Read data
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    # --- DATA HEALTH SCORE SECTION ---
    st.subheader("🏥 Data Health Overview")

    # Calculate Metrics
    total_cells = df.size
    missing_cells = df.isnull().sum().sum()
    duplicate_rows = df.duplicated().sum()
    
    # Health Score Calculation (Simple logic: 100% minus penalties for issues)
    # Penalty: Missing data % + Duplicate data %
    missing_pct = (missing_cells / total_cells) * 100 if total_cells > 0 else 0
    dup_pct = (duplicate_rows / len(df)) * 100 if len(df) > 0 else 0
    health_score = max(0, int(100 - (missing_pct + dup_pct)))
    
    # Display Metrics in Columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Use color-coded score
        score_color = "green" if health_score > 80 else "orange" if health_score > 50 else "red"
        st.markdown(f"### Score: :{score_color}[{health_score}/100]")
    
    with col2:
        st.metric("Missing Values", f"{missing_cells}", f"-{missing_pct:.1f}%", delta_color="inverse")
    
    with col3:
        st.metric("Duplicates", f"{duplicate_rows}", f"-{dup_pct:.1f}%", delta_color="inverse")
    
    with col4:
        st.metric("Total Rows", len(df))
    
    # Progress Bar for Visual impact
    st.progress(health_score / 100)
    
    # Detailed Health Warnings
    if health_score < 100:
        with st.expander("View Improvement Suggestions"):
            if missing_cells > 0:
                st.write("📍 **Missing Data:** Consider using the 'Remove rows' option in the sidebar.")
            if duplicate_rows > 0:
                st.write("📍 **Duplicates Found:** You may want to add a 'Remove Duplicates' button.")
        
    # --- DATA CLEANING SECTION ---
    st.sidebar.header("1. Data Cleaning")
    
    # Handle Missing Values
    clean_action = st.sidebar.radio(
        "Handle Missing Values:",
        ("Do nothing", "Remove rows containing missing values")
    )
    
    if clean_action == "Remove rows containing missing values":
        df = df.dropna()

    # --- COLUMN SELECTION ---
    st.sidebar.header("2. Filter Columns")
    all_columns = df.columns.tolist()
    selected_columns = st.sidebar.multiselect("Select columns to keep:", all_columns, default=all_columns)
    
    # Filter the dataframe
    if selected_columns:
        df = df[selected_columns]

    # --- DATA SEPARATION ---
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

    # --- VISUALIZATION SECTION ---
    st.subheader("📊 Data Visualization")
    
    plot_type = st.selectbox("Choose plot type:", ["Histogram", "Scatter Plot", "Boxplot"])

    if plot_type == "Histogram":
        if numeric_cols:
            col = st.selectbox("Select Numeric Column:", numeric_cols)
            fig = px.histogram(df, x=col, title=f"Histogram of {col}")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Need at least one numeric column for a Histogram.")

    elif plot_type == "Scatter Plot":
        if len(numeric_cols) >= 2:
            col_x = st.selectbox("Select X-axis (Numeric):", numeric_cols)
            col_y = st.selectbox("Select Y-axis (Numeric):", numeric_cols)
            fig = px.scatter(df, x=col_x, y=col_y, title=f"{col_x} vs {col_y}")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Need at least two numeric columns for a Scatter Plot.")

    elif plot_type == "Boxplot":
        if categorical_cols and numeric_cols:
            cat_col = st.selectbox("Select Category (X-axis):", categorical_cols)
            num_col = st.selectbox("Select Value (Y-axis):", numeric_cols)
            fig = px.box(df, x=cat_col, y=num_col, title=f"Distribution of {num_col} by {cat_col}")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Boxplots require one categorical and one numeric column.")

    # --- DISPLAY PROCESSED DATA ---
    st.divider()
    st.subheader("📋 Processed Dataset")
    st.write(f"Current Shape: {df.shape[0]} rows, {df.shape[1]} columns")
    st.dataframe(df)

else:
    st.info("Waiting for file upload...")
