"""
EcoPulse India Economic Intelligence
Power BI Style Dashboard - Font Sizes Fixed
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="EcoPulse | India Economic Intelligence",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# COLOR PALETTE
# ============================================
SECTOR_COLORS = [
    '#FF6B35', '#2563EB', '#10B981', '#8B5CF6', '#EC4899',
    '#F59E0B', '#06B6D4', '#EF4444', '#84CC16', '#F97316',
    '#0EA5E9', '#A855F7', '#14B8A6', '#F43F5E', '#FB923C'
]

YEAR_COLORS = [
    '#FFB74D', '#FF9933', '#FF6B35', '#F97316',
    '#3B82F6', '#2563EB', '#1E40AF', '#1E3A8A',
    '#10B981', '#059669', '#047857', '#065F46'
]

# ============================================
# CSS
# ============================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #FFF7ED 0%, #FEF3F2 30%, #F0F9FF 70%, #FFF7ED 100%);
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .main .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 2rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    
    /* ========================================
       MAIN TITLE - Big Impact
       ======================================== */
    .main-title {
        font-size: 5rem;
        font-weight: 900;
        color: #1A1A1A;
        text-align: center;
        margin: 0 0 0.2rem 0;
        letter-spacing: -3px;
        line-height: 1;
        padding: 0;
    }
    
    .title-flag { color: #FF6B35; }
    
    /* Subtitle - 18px Imp */
    .subtitle {
        text-align: center;
        color: #6B7280;
        font-size: 18px;
        margin: 0 0 3rem 0;
        font-weight: 600;
    }
    
    /* ========================================
       KPI CARDS
       ======================================== */
    .kpi-card {
        background: #FFFFFF;
        border-radius: 14px;
        padding: 2rem 1.2rem;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transition: all 0.2s ease;
        height: 100%;
        min-height: 150px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .kpi-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.15);
    }
    
    .kpi-card.orange { border: 3px solid #FF6B35; }
    .kpi-card.blue { border: 3px solid #2563EB; }
    .kpi-card.green { border: 3px solid #10B981; }
    .kpi-card.purple { border: 3px solid #8B5CF6; }
    .kpi-card.pink { border: 3px solid #EC4899; }
    
    /* KPI Label - 15px Normal */
    .kpi-label {
        color: #6B7280;
        font-size: 15px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.8rem;
    }
    
    /* KPI Value - 18px Imp */
    .kpi-value {
        font-size: 40px;
        font-weight: 900;
        color: #1A1A1A;
        letter-spacing: -1.5px;
    }
    
    /* ========================================
       SECTION HEADERS - 18px Imp
       ======================================== */
    .section-header {
        font-size: 18px;
        font-weight: 800;
        color: #1A1A1A;
        margin: 3rem 0 1rem 0;
        padding-left: 0.8rem;
        border-left: 5px solid #FF6B35;
    }
    
    /* ========================================
       INSIGHT CARDS - 15px Normal
       ======================================== */
    .insight-card {
        background: #FFFFFF;
        border: 2px solid #E5E7EB;
        border-radius: 10px;
        padding: 1.2rem 1.4rem;
        margin: 0.5rem 0;
        font-size: 15px;
        transition: all 0.2s;
    }
    
    .insight-card:hover {
        border-color: #FF6B35;
        transform: translateX(4px);
        box-shadow: 0 4px 12px rgba(255,107,53,0.15);
    }
    
    /* ========================================
       SIDEBAR
       ======================================== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FFF7ED 0%, #FEF3F2 50%, #F0F9FF 100%) !important;
        border-right: 4px solid #FF6B35 !important;
        min-width: 460px !important;
        max-width: 460px !important;
        width: 460px !important;
    }
    
    section[data-testid="stSidebar"] > div:first-child {
        padding: 1.5rem 1.8rem 8rem 1.8rem !important;
        width: 100% !important;
        min-height: 100vh !important;
        background: linear-gradient(180deg, #FFF7ED 0%, #FEF3F2 50%, #F0F9FF 100%) !important;
    }
    
    section[data-testid="stSidebar"] > div {
        width: 100% !important;
        min-height: 100vh !important;
    }
    
    section[data-testid="stSidebar"] .stSelectbox {
        position: relative !important;
        z-index: 999 !important;
    }
    
    /* Selectbox - 18px Imp */
    section[data-testid="stSidebar"] .stSelectbox > div > div {
        font-size: 18px !important;
        font-weight: 800 !important;
        padding: 1.3rem 1.5rem !important;
        min-height: 80px !important;
        background: #FFFFFF !important;
        border: 3px solid rgba(255,107,53,0.5) !important;
        border-radius: 14px !important;
        box-shadow: 0 3px 10px rgba(255,107,53,0.12) !important;
    }
    
    section[data-testid="stSidebar"] .stSelectbox > div > div:hover {
        border-color: #FF6B35 !important;
        box-shadow: 0 5px 15px rgba(255,107,53,0.25) !important;
    }
    
    /* Selectbox Label - 18px Imp */
    section[data-testid="stSidebar"] .stSelectbox label {
        font-size: 18px !important;
        font-weight: 900 !important;
        color: #1A1A1A !important;
        margin-bottom: 0.8rem !important;
        letter-spacing: -0.5px !important;
    }
    
    /* Dropdown Menu */
    section[data-testid="stSidebar"] [data-baseweb="menu"] {
        background: #FFFFFF !important;
        border: 2px solid #FF6B35 !important;
        border-radius: 10px !important;
        box-shadow: 0 10px 30px rgba(255,107,53,0.3) !important;
    }
    
    /* Dropdown Options - 15px Normal */
    section[data-testid="stSidebar"] [role="option"] {
        font-size: 15px !important;
        padding: 1rem 1.5rem !important;
        color: #1A1A1A !important;
    }
    
    section[data-testid="stSidebar"] [role="option"]:hover {
        background: #FFF7ED !important;
        color: #FF6B35 !important;
    }
    
    section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        gap: 1.2rem !important;
    }
    
    /* Sidebar Header */
    .sidebar-header {
        text-align: center;
        padding: 1.5rem 1.2rem;
        margin-bottom: 1.5rem;
        background: linear-gradient(135deg, rgba(255,107,53,0.15), rgba(37,99,235,0.15));
        border-radius: 14px;
        border: 3px solid rgba(255,107,53,0.35);
        box-shadow: 0 4px 15px rgba(255,107,53,0.15);
    }
    
    /* Sidebar Title - 18px Imp */
    .sidebar-title {
        color: #FF6B35;
        font-weight: 900;
        font-size: 18px;
        margin: 0;
    }
    
    /* Sidebar Subtitle - 15px Normal */
    .sidebar-subtitle {
        color: #6B7280;
        font-size: 15px;
        margin: 0.5rem 0 0 0;
        font-weight: 700;
    }
    
    /* Sidebar General Labels - 15px Normal */
    section[data-testid="stSidebar"] label {
        font-size: 15px !important;
        font-weight: 800 !important;
        color: #1A1A1A !important;
    }
    
    section[data-testid="stSidebar"] .stCheckbox {
        margin: 0.8rem 0 !important;
    }
    
    /* Checkbox Labels - 15px Normal */
    section[data-testid="stSidebar"] .stCheckbox label {
        font-size: 15px !important;
        font-weight: 700 !important;
        padding: 0.4rem 0 !important;
    }
    
    .dataset-card {
        background: linear-gradient(135deg, #FFF7ED, #F0F9FF);
        padding: 1.8rem 1.5rem;
        border-radius: 14px;
        border-left: 5px solid #FF6B35;
        box-shadow: 0 4px 15px rgba(255,107,53,0.12);
        margin-top: 2rem;
        margin-bottom: 2rem;
    }
    
    /* Dataset Title - 18px Imp */
    .dataset-title {
        color: #FF6B35;
        font-size: 18px;
        font-weight: 900;
        margin-bottom: 1rem;
    }
    
    .dataset-row {
        display: flex;
        justify-content: space-between;
        padding: 0.7rem 0;
        border-bottom: 1px dashed rgba(255,107,53,0.2);
    }
    
    .dataset-row:last-child { border-bottom: none; }
    
    /* Dataset Label - 15px Normal */
    .dataset-label {
        color: #6B7280;
        font-size: 15px;
        font-weight: 700;
    }
    
    /* Dataset Value - 15px Normal */
    .dataset-value {
        color: #1A1A1A;
        font-size: 15px;
        font-weight: 900;
    }
    
    /* Footer */
    .footer-text {
        color: #6B7280;
        font-size: 15px;
        margin: 0;
        font-weight: 600;
    }
    
    .footer-sub {
        font-size: 15px;
        color: #9CA3AF;
    }
</style>
""", unsafe_allow_html=True)


# ============================================
# DATA
# ============================================
@st.cache_data
def load_data():
    path = 'data/processed/ecopulse_processed.csv'
    if os.path.exists(path):
        return pd.read_csv(path)
    return None


# ============================================
# HELPERS
# ============================================
def kpi_card(col, color, label, value):
    with col:
        st.markdown(f"""
            <div class="kpi-card {color}">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
            </div>
        """, unsafe_allow_html=True)


def style_fig(fig, height=400, showlegend=False):
    """Charts fonts - 15px normal"""
    fig.update_layout(
        height=height,
        paper_bgcolor='white',
        plot_bgcolor='white',
        font=dict(color='#1A1A1A', family='Inter', size=13),
        title_font=dict(size=18, color='#1A1A1A', family='Inter'),
        xaxis=dict(
            gridcolor='#F3F4F6',
            linecolor='#E5E7EB',
            tickfont=dict(color='#6B7280', size=15),
            title_font=dict(size=15, color='#6B7280')
        ),
        yaxis=dict(
            gridcolor='#F3F4F6',
            linecolor='#E5E7EB',
            tickfont=dict(color='#6B7280', size=15),
            title_font=dict(size=15, color='#6B7280')
        ),
        margin=dict(l=60, r=40, t=60, b=60),
        showlegend=showlegend,
        legend=dict(
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='#E5E7EB',
            borderwidth=1,
            font=dict(size=15)
        )
    )
    return fig


# ============================================
# MAIN
# ============================================
def main():
    # TITLE
    st.markdown('<div class="main-title"><span class="title-flag">🇮🇳</span> EcoPulse</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">India Economic Intelligence & AI Insights Dashboard</div>', unsafe_allow_html=True)

    df = load_data()
    if df is None:
        st.error("⚠️ Data not found! Run `py -3.10 run.py`")
        st.stop()

    # ============================================
    # SIDEBAR
    # ============================================
    st.sidebar.markdown("""
        <div class="sidebar-header">
            <h2 class="sidebar-title">🎛️ Control Panel</h2>
            <p class="sidebar-subtitle">Filter your data</p>
        </div>
    """, unsafe_allow_html=True)

    available_years = sorted(df['Year'].unique().tolist())
    if 2026 not in available_years:
        available_years.append(2026)

    selected_year = st.sidebar.selectbox("📅 Select Year", available_years,
                                          index=len(available_years) - 1)

    sectors = ['All'] + sorted(df['Sector'].unique().tolist())
    selected_sector = st.sidebar.selectbox("🏭 Select Sector", sectors)

    show_table = st.sidebar.checkbox("Show Data Table", value=False)
    show_correlation = st.sidebar.checkbox("Show Correlation", value=False)

    st.sidebar.markdown("""
        <div class="dataset-card">
            <div class="dataset-title">📈 Dataset</div>
            <div class="dataset-row">
                <span class="dataset-label">Records</span>
                <span class="dataset-value">1000+</span>
            </div>
            <div class="dataset-row">
                <span class="dataset-label">Years</span>
                <span class="dataset-value">2015 - 2026</span>
            </div>
            <div class="dataset-row">
                <span class="dataset-label">Sectors</span>
                <span class="dataset-value">15+</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Filter
    filtered = df[df['Year'] == selected_year]
    if selected_sector != 'All':
        filtered = filtered[filtered['Sector'] == selected_sector]

    if len(filtered) == 0:
        filtered = df[df['Year'] == df['Year'].max()]
        selected_year = int(df['Year'].max())
        if selected_sector != 'All':
            filtered = filtered[filtered['Sector'] == selected_sector]

    # ============================================
    # KPI CARDS - 5 CARDS
    # ============================================
    col1, col2, col3, col4, col5 = st.columns(5)

    gdp = filtered['GDP'].sum()
    fdi = filtered['FDI'].sum()
    exports = filtered['Exports'].sum()
    growth = filtered['Growth_Rate'].mean()
    employment = filtered['Employment'].sum()

    kpi_card(col1, 'orange', 'Total GDP (₹ Lakh Cr)', f'{gdp:,.2f}')
    kpi_card(col2, 'blue', 'Total FDI (₹ Cr)', f'{fdi:,.0f}')
    kpi_card(col3, 'green', 'Total Exports (₹ Cr)', f'{exports:,.0f}')
    kpi_card(col4, 'purple', 'Avg Growth (%)', f'{growth:.2f}%')
    kpi_card(col5, 'pink', 'Employment (M)', f'{employment:,.1f}')

    # ============================================
    # TRADE ANALYSIS
    # ============================================
    st.markdown('<div class="section-header">📈 Trade Analysis</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        yearly = df.groupby('Year').agg({
            'Exports': 'sum', 'Imports': 'sum'
        }).reset_index()

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=yearly['Year'], y=yearly['Exports'],
            mode='lines+markers', name='Exports',
            line=dict(color='#2563EB', width=3),
            marker=dict(size=10, color='#2563EB', line=dict(color='white', width=2))
        ))
        fig.add_trace(go.Scatter(
            x=yearly['Year'], y=yearly['Imports'],
            mode='lines+markers', name='Imports',
            line=dict(color='#FF6B35', width=3),
            marker=dict(size=10, color='#FF6B35', line=dict(color='white', width=2))
        ))
        fig.update_layout(title='Exports vs Imports Trend',
                          xaxis_title='Year', yaxis_title='Value (₹ Cr)')
        fig = style_fig(fig, height=380, showlegend=True)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        tax_col = 'Tax_Revenue' if 'Tax_Revenue' in df.columns else 'Tax_Revenue_Crore'
        if tax_col in df.columns:
            tax_yearly = df.groupby('Year')[tax_col].sum().reset_index()

            tax_colors = [
                '#FF6B35', '#F97316', '#F59E0B', '#84CC16',
                '#10B981', '#14B8A6', '#06B6D4', '#0EA5E9',
                '#3B82F6', '#6366F1', '#8B5CF6', '#A855F7'
            ]
            colors = tax_colors[:len(tax_yearly)]

            fig = go.Figure(go.Bar(
                x=tax_yearly['Year'], y=tax_yearly[tax_col],
                marker=dict(color=colors, line=dict(color='white', width=2)),
                text=[f'₹{v/1000:.0f}K' for v in tax_yearly[tax_col]],
                textposition='outside',
                textfont=dict(size=15, color='#1A1A1A')
            ))
            fig.update_layout(title='Tax Revenue By Year',
                              xaxis_title='Year', yaxis_title='Tax Revenue (₹ Cr)')
            fig = style_fig(fig, height=380)
            st.plotly_chart(fig, use_container_width=True)

    # ============================================
    # FDI + TRADE BALANCE
    # ============================================
    col3, col4 = st.columns(2)

    with col3:
        if 'FDI_Category' in df.columns:
            fdi_dist = df.groupby('FDI_Category')['FDI'].sum().reset_index()
        else:
            fdi_dist = df.groupby('Sector')['FDI'].sum().nlargest(5).reset_index()
            fdi_dist.columns = ['FDI_Category', 'FDI']

        fig = go.Figure(go.Pie(
            labels=fdi_dist['FDI_Category'],
            values=fdi_dist['FDI'],
            hole=0.55,
            marker=dict(
                colors=['#FF6B35', '#2563EB', '#10B981', '#8B5CF6', '#EC4899', '#F59E0B'],
                line=dict(color='white', width=3)
            ),
            textinfo='label+percent',
            textfont=dict(size=15, color='white', family='Inter')
        ))
        fig.update_layout(
            title='FDI Distribution',
            annotations=[dict(text=f'₹{fdi_dist["FDI"].sum():,.0f}<br>Total',
                            x=0.5, y=0.5, font_size=18, showarrow=False)]
        )
        fig = style_fig(fig, height=380)
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        yearly_balance = df.groupby('Year').apply(
            lambda x: x['Exports'].sum() - x['Imports'].sum()
        ).reset_index()
        yearly_balance.columns = ['Year', 'Trade_Balance']

        colors = ['#10B981' if v >= 0 else '#EF4444' for v in yearly_balance['Trade_Balance']]

        fig = go.Figure(go.Bar(
            x=yearly_balance['Year'],
            y=yearly_balance['Trade_Balance'],
            marker=dict(color=colors, line=dict(color='white', width=2)),
            text=[f'{"+" if v >= 0 else ""}{v/1000:.0f}K' for v in yearly_balance['Trade_Balance']],
            textposition='outside',
            textfont=dict(size=15, color='#1A1A1A')
        ))
        fig.add_hline(y=0, line_dash="dash", line_color="#6B7280", line_width=1)
        fig.update_layout(title='Trade Balance Trend',
                          xaxis_title='Year', yaxis_title='Trade Balance (₹ Cr)')
        fig = style_fig(fig, height=380)
        st.plotly_chart(fig, use_container_width=True)

    # ============================================
    # SECTOR ANALYSIS
    # ============================================
    st.markdown('<div class="section-header">📊 Sector Analysis</div>', unsafe_allow_html=True)

    col5, col6 = st.columns(2)

    with col5:
        sector_gdp = filtered.groupby('Sector')['GDP'].sum().sort_values(ascending=True).reset_index()
        colors = SECTOR_COLORS[:len(sector_gdp)]

        fig = go.Figure(go.Bar(
            x=sector_gdp['GDP'],
            y=sector_gdp['Sector'],
            orientation='h',
            marker=dict(color=colors, line=dict(color='white', width=2)),
            text=[f'₹{v:.0f}' for v in sector_gdp['GDP']],
            textposition='outside',
            textfont=dict(size=15, color='#1A1A1A')
        ))
        fig.update_layout(title=f'GDP by Sector ({selected_year})',
                          xaxis_title='GDP (₹ Lakh Cr)', yaxis_title='')
        fig = style_fig(fig, height=420)
        st.plotly_chart(fig, use_container_width=True)

    with col6:
        gdp_yearly = df.groupby('Year')['GDP'].sum().reset_index()
        colors = YEAR_COLORS[:len(gdp_yearly)]

        fig = go.Figure(go.Bar(
            x=gdp_yearly['GDP'],
            y=gdp_yearly['Year'].astype(str),
            orientation='h',
            marker=dict(color=colors, line=dict(color='white', width=2)),
            text=[f'₹{v:,.0f}' for v in gdp_yearly['GDP']],
            textposition='outside',
            textfont=dict(size=15, color='#1A1A1A')
        ))
        fig.update_layout(title='GDP Growth Trend (2015-2026)',
                          xaxis_title='GDP (₹ Lakh Cr)', yaxis_title='')
        fig = style_fig(fig, height=420)
        st.plotly_chart(fig, use_container_width=True)

    # ============================================
    # SECTOR GROWTH + DONUT
    # ============================================
    col7, col8 = st.columns(2)

    with col7:
        sector_growth = filtered.groupby('Sector')['Growth_Rate'].mean().sort_values(ascending=True).reset_index()
        colors = SECTOR_COLORS[:len(sector_growth)]

        fig = go.Figure(go.Bar(
            x=sector_growth['Sector'],
            y=sector_growth['Growth_Rate'],
            marker=dict(color=colors, line=dict(color='white', width=2)),
            text=[f'{v:.1f}%' for v in sector_growth['Growth_Rate']],
            textposition='outside',
            textfont=dict(size=15, color='#1A1A1A')
        ))
        fig.update_layout(title=f'Sector-wise Growth ({selected_year})',
                          xaxis_title='Sector', yaxis_title='Growth Rate (%)',
                          xaxis_tickangle=-45)
        fig = style_fig(fig, height=420)
        st.plotly_chart(fig, use_container_width=True)

    with col8:
        if 'Sector_Category' in df.columns:
            activity = df.groupby('Sector_Category')['GDP'].sum().reset_index()
        else:
            activity = df.groupby('Sector')['GDP'].sum().nlargest(5).reset_index()
            activity.columns = ['Sector_Category', 'GDP']

        fig = go.Figure(go.Pie(
            labels=activity['Sector_Category'],
            values=activity['GDP'],
            hole=0.55,
            marker=dict(
                colors=['#FF6B35', '#2563EB', '#10B981', '#8B5CF6', '#EC4899', '#F59E0B'],
                line=dict(color='white', width=3)
            ),
            textinfo='label+percent',
            textfont=dict(size=15, color='white', family='Inter')
        ))
        fig.update_layout(
            title='Economic Activity Distribution',
            annotations=[dict(text=f'₹{activity["GDP"].sum():,.0f}<br>Total',
                            x=0.5, y=0.5, font_size=18, showarrow=False)]
        )
        fig = style_fig(fig, height=420)
        st.plotly_chart(fig, use_container_width=True)

    # ============================================
    # MACROECONOMIC + SCATTER (Separated)
    # ============================================
    st.markdown('<div class="section-header">📉 Macroeconomic Analysis</div>', unsafe_allow_html=True)

    col9, col10 = st.columns(2)

    with col9:
        # 🎯 MACROECONOMIC - VERTICAL BAR
        macro_cols = []
        if 'Inflation' in df.columns:
            macro_cols.append('Inflation')
        if 'CPI' in df.columns:
            macro_cols.append('CPI')
        if 'IIP' in df.columns:
            macro_cols.append('IIP')

        if macro_cols:
            macro_data = df[macro_cols].mean().reset_index()
            macro_data.columns = ['Indicator', 'Value']

            fig = go.Figure(go.Bar(
                x=macro_data['Indicator'],
                y=macro_data['Value'],
                marker=dict(
                    color=['#FF6B35', '#2563EB', '#10B981'],
                    line=dict(color='white', width=2)
                ),
                text=[f'{v:.2f}' for v in macro_data['Value']],
                textposition='outside',
                textfont=dict(size=15, color='#1A1A1A', family='Inter')
            ))
            fig.update_layout(
                title='Macroeconomic Performance Indicators',
                xaxis_title='Indicator',
                yaxis_title='Average Value',
                showlegend=False,
                bargap=0.4
            )
            fig = style_fig(fig, height=420)
            st.plotly_chart(fig, use_container_width=True)

    with col10:
        # 🎯 SCATTER PLOT
        if 'Employment' in filtered.columns:
            fig = go.Figure()

            for i, (_, row) in enumerate(filtered.iterrows()):
                color = SECTOR_COLORS[i % len(SECTOR_COLORS)]
                fig.add_trace(go.Scatter(
                    x=[row['Employment']],
                    y=[row['GDP']],
                    mode='markers+text',
                    marker=dict(
                        size=20,
                        color=color,
                        line=dict(color='white', width=2),
                        opacity=0.85
                    ),
                    text=[row['Sector']],
                    textposition='top center',
                    textfont=dict(size=15, color='#1A1A1A', family='Inter'),
                    name=row['Sector'],
                    showlegend=False,
                    hovertemplate=f"<b>{row['Sector']}</b><br>" +
                                  f"Employment: {row['Employment']:.1f}M<br>" +
                                  f"GDP: ₹{row['GDP']:.2f} Lakh Cr<br>" +
                                  "<extra></extra>"
                ))

            fig.update_layout(
                title=f'GDP vs Employment — {selected_year}',
                xaxis_title='Employment (Million)',
                yaxis_title='GDP (₹ Lakh Cr)',
                hovermode='closest'
            )
            fig = style_fig(fig, height=420)
            st.plotly_chart(fig, use_container_width=True)

    # ============================================
    # GDP OVERVIEW TABLE (Full Width)
    # ============================================
    if 'Sector_Category' in df.columns and 'GDP_Category' in df.columns:
        st.markdown('<div class="section-header">📋 GDP Overview By Category</div>', unsafe_allow_html=True)

        pivot = df.pivot_table(
            values='GDP',
            index='Sector_Category',
            columns='GDP_Category',
            aggfunc='sum',
            fill_value=0
        ).round(2)

        pivot['Total'] = pivot.sum(axis=1)
        pivot.loc['Total'] = pivot.sum()

        st.dataframe(
            pivot.style.background_gradient(cmap='Blues', axis=None).format('{:,.2f}'),
            use_container_width=True,
            height=400
        )

    # ============================================
    # AI INSIGHTS
    # ============================================
    st.markdown('<div class="section-header">🧠 AI-Generated Insights</div>', unsafe_allow_html=True)

    top_gdp = df.groupby('Sector')['GDP'].sum().idxmax()
    top_gdp_val = df.groupby('Sector')['GDP'].sum().max()
    top_growth = df.groupby('Sector')['Growth_Rate'].mean().idxmax()
    top_growth_val = df.groupby('Sector')['Growth_Rate'].mean().max()
    top_fdi = df.groupby('Sector')['FDI'].sum().idxmax()
    top_fdi_val = df.groupby('Sector')['FDI'].sum().max()
    top_emp = df.groupby('Sector')['Employment'].sum().idxmax()
    top_emp_val = df.groupby('Sector')['Employment'].sum().max()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
            <div class="insight-card">
                <span style="font-size: 18px;">💰</span>
                <b style="color: #1A1A1A;"> Top GDP:</b>
                <b style="color: #FF6B35;"> {top_gdp}</b>
                <span style="color: #6B7280;"> — ₹{top_gdp_val:,.2f} Lakh Cr</span>
            </div>
            <div class="insight-card">
                <span style="font-size: 18px;">📈</span>
                <b style="color: #1A1A1A;"> Highest Growth:</b>
                <b style="color: #2563EB;"> {top_growth}</b>
                <span style="color: #6B7280;"> — {top_growth_val:.2f}%</span>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="insight-card">
                <span style="font-size: 18px;">🏦</span>
                <b style="color: #1A1A1A;"> Leading FDI:</b>
                <b style="color: #10B981;"> {top_fdi}</b>
                <span style="color: #6B7280;"> — ₹{top_fdi_val:,.0f} Cr</span>
            </div>
            <div class="insight-card">
                <span style="font-size: 18px;">👥</span>
                <b style="color: #1A1A1A;"> Largest Employer:</b>
                <b style="color: #8B5CF6;"> {top_emp}</b>
                <span style="color: #6B7280;"> — {top_emp_val:,.2f}M</span>
            </div>
        """, unsafe_allow_html=True)

    # ============================================
    # CORRELATION
    # ============================================
    if show_correlation:
        st.markdown('<div class="section-header">🔥 Correlation Analysis</div>', unsafe_allow_html=True)

        numeric_cols = ['GDP', 'Growth_Rate', 'Employment', 'FDI', 'Inflation', 'Exports', 'Imports']
        available_cols = [c for c in numeric_cols if c in df.columns]
        corr_matrix = df[available_cols].corr()

        fig = px.imshow(
            corr_matrix, text_auto='.2f', aspect='auto',
            color_continuous_scale='RdBu_r',
            title='Feature Correlation Matrix'
        )
        fig = style_fig(fig, height=600)
        st.plotly_chart(fig, use_container_width=True)

    # ============================================
    # DATA TABLE
    # ============================================
    if show_table:
        st.markdown('<div class="section-header">📋 Data Table</div>', unsafe_allow_html=True)
        st.dataframe(filtered, use_container_width=True, height=400)

    # ============================================
    # FOOTER
    # ============================================
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div style="text-align: center; padding: 2rem 0; border-top: 2px solid #E5E7EB;">
            <p class="footer-text">
                🇮🇳 <b style="color: #FF6B35;">EcoPulse</b> 
                — India Economic Intelligence & AI Insights<br>
                <span class="footer-sub">
                    1000+ Records • Python • Streamlit • Scikit-learn • XGBoost • PyTorch • TensorFlow
                </span>
            </p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()