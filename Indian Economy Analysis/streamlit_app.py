"""
India Economy Analytics - Streamlit Dashboard
"""
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.helpers import load_data

# Page config
st.set_page_config(
    page_title="India Economy Analytics",
    page_icon="🇮🇳",
    layout="wide"
)

# Title
st.title("🇮🇳 India Economy Analytics Dashboard")
st.markdown("---")

# Load data
@st.cache_data
def load_data_cached():
    try:
        df = load_data('indian_economy_processed.csv')
        if df is None:
            df = load_data('indian_economy_featured.csv')
        return df
    except Exception as e:
        return None

df = load_data_cached()

if df is None:
    st.error("❌ Data not found! Please run ETL pipeline first.")
    st.info("Run: python run.py")
    st.stop()

# Sidebar filters
st.sidebar.header("📊 Filters")

# Year filter
years = sorted(df['Year'].unique())
selected_year = st.sidebar.selectbox("Select Year", years, index=len(years)-1)

# Sector filter
sectors = ['All'] + sorted(df['Sector'].unique())
selected_sector = st.sidebar.selectbox("Select Sector", sectors)

# Filter data
filtered_df = df[df['Year'] == selected_year]
if selected_sector != 'All':
    filtered_df = filtered_df[filtered_df['Sector'] == selected_sector]

# Main dashboard
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total GDP", f"₹{filtered_df['GDP'].sum():.2f} Lakh Cr")

with col2:
    st.metric("Avg Growth", f"{filtered_df['Growth_Rate'].mean():.2f}%")

with col3:
    st.metric("Total Employment", f"{filtered_df['Employment'].sum():.2f} M")

with col4:
    st.metric("Total FDI", f"₹{filtered_df['FDI'].sum():.2f} Cr")

st.markdown("---")

# Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 GDP by Sector")
    fig = px.bar(filtered_df, x='Sector', y='GDP', 
                 title=f'GDP by Sector - {selected_year}',
                 color='Sector', color_discrete_sequence=px.colors.qualitative.Set3)
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📈 Growth Rate by Sector")
    fig = px.bar(filtered_df, x='Sector', y='Growth_Rate',
                 title=f'Growth Rate by Sector - {selected_year}',
                 color='Sector', color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    st.subheader("💰 FDI by Sector")
    fig = px.bar(filtered_df, x='Sector', y='FDI',
                 title=f'FDI by Sector - {selected_year}',
                 color='Sector', color_discrete_sequence=px.colors.qualitative.Set1)
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

with col4:
    st.subheader("👥 Employment by Sector")
    fig = px.bar(filtered_df, x='Sector', y='Employment',
                 title=f'Employment by Sector - {selected_year}',
                 color='Sector', color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

# Yearly Trends
st.markdown("---")
st.subheader("📅 Yearly Trends")

col5, col6 = st.columns(2)

with col5:
    yearly_gdp = df.groupby('Year')['GDP'].sum().reset_index()
    fig = px.line(yearly_gdp, x='Year', y='GDP',
                  title='GDP Trend Over Years',
                  markers=True)
    fig.update_traces(line=dict(color='blue', width=3))
    st.plotly_chart(fig, use_container_width=True)

with col6:
    yearly_growth = df.groupby('Year')['Growth_Rate'].mean().reset_index()
    fig = px.line(yearly_growth, x='Year', y='Growth_Rate',
                  title='Average Growth Rate Trend',
                  markers=True)
    fig.update_traces(line=dict(color='green', width=3))
    st.plotly_chart(fig, use_container_width=True)

# Data Table
st.markdown("---")
st.subheader("📋 Data Table")

show_data = st.checkbox("Show Data Table")
if show_data:
    st.dataframe(filtered_df)

# Summary Statistics
st.markdown("---")
st.subheader("📊 Summary Statistics")

col7, col8 = st.columns(2)

with col7:
    st.write("**Numeric Columns Summary**")
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    st.dataframe(df[numeric_cols].describe())

with col8:
    st.write("**Sector Categories**")
    if 'Sector_Category' in df.columns:
        st.dataframe(df['Sector_Category'].value_counts().reset_index())
    else:
        st.info("Sector_Category column not found")

st.markdown("---")
st.caption("🇮🇳 India Economy Analytics - Data Science Portfolio Project")