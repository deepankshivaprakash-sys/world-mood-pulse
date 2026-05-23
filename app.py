import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# --- STYLING & CONFIG ---
st.set_page_config(page_title="World Mood Pulse Pro", layout="wide", page_icon="🌍")

# Clean, safe background card layout injection
st.markdown("""
    <style>
    .news-card-box {
        background-color: #ffffff; 
        padding: 20px; 
        border-radius: 12px; 
        box-shadow: 0 4px 10px rgba(0,0,0,0.06); 
        margin-bottom: 20px;
        border-top: 4px solid #29b5e8;
    }
    .tag-bubble {
        background-color: #eef2f5;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: bold;
        color: #4a5568;
    }
    </style>
""", unsafe_allow_html=True)

# --- SAFE DATA ECOSYSTEM ---
# 1. Historical Trends Matrix (Static values to prevent any rounding or array issues)
history_data = {
    'Date': ['2026-05-17', '2026-05-18', '2026-05-19', '2026-05-20', '2026-05-21', '2026-05-22', '2026-05-23'],
    'Fear': [21.2, 28.3, 11.4, 24.8, 28.9, 20.5, 20.8],
    'Anger': [15.9, 16.2, 21.9, 17.6, 10.8, 18.0, 14.9],
    'Happiness': [15.2, 25.8, 35.0, 20.5, 10.2, 16.4, 12.9],
    'Sadness': [15.2, 22.6, 17.1, 23.4, 22.1, 15.2, 23.5],
    'Neutral': [32.6, 7.1, 14.6, 13.8, 28.0, 29.9, 27.9]
}
df_history = pd.DataFrame(history_data)

# 2. Rich Deep Articles (Expanded Scope & Layout Data)
headlines_pool = [
    {
        "headline": "Global Stock Indices Plunge 4.2% Triggering Circuit Breakers Worldwide", 
        "emotion": "Fear", "country": "USA", "region": "North America", "icon": "📉",
        "detailed_analysis": "Widespread panic hit global trading floors today as unexpected inflation metrics sparked fears of prolonged high interest rates. Financial analysts suggest a major corrections cycle is underway, forcing immediate defensive asset management.",
        "url": "https://reuters.com"
    },
    {
        "headline": "Cybersecurity Breaches Compromise Infrastructure Hubs Across Three Capitals", 
        "emotion": "Fear", "country": "CAN", "region": "Global Security", "icon": "🔒",
        "detailed_analysis": "A coordinated digital assault has targeted power management nodes and metropolitan transit signals. Defense taskforces are actively managing structural patches while citizens express growing security vulnerabilities.",
        "url": "https://wired.com"
    },
    {
        "headline": "Border Access Disagreements Lead to Stiff Commercial Embargos", 
        "emotion": "Anger", "country": "UKR", "region": "Eastern Europe", "icon": "🚫",
        "detailed_analysis": "Diplomatic talks fractured completely following enforcement updates, resulting in massive shipping supply freezes. Local consumer organizations are mobilizing protests over resulting import price hikes.",
        "url": "https://bbc.com"
    },
    {
        "headline": "Public Transit Union Stages City-Wide Walkouts Over Structural Contracts", 
        "emotion": "Anger", "country": "FRA", "region": "Western Europe", "icon": "📢",
        "detailed_analysis": "Commuters face massive scheduling standstills as negotiation deadlines expired with no settlement. High frustration values are registered across urban community forums regarding municipal management frameworks.",
        "url": "https://apnews.com"
    },
    {
        "headline": "Medical Breakthrough: Universal Vaccine Demonstrates 95% Efficacy Rate", 
        "emotion": "Happiness", "country": "GBR", "region": "Global Health", "icon": "🧬",
        "detailed_analysis": "An unprecedented milestone in immunotherapy has cleared advanced peer-review phases. Healthcare indicators across all regions are signaling long-term macroeconomic optimism as global deployment logs prepare for initial rollout pipelines.",
        "url": "https://nature.com"
    },
    {
        "headline": "Renewable Fusion Inverters Achieve Sustained Net Energy Influx Thresholds", 
        "emotion": "Happiness", "country": "CHN", "region": "East Asia", "icon": "☀️",
        "detailed_analysis": "Engineering teams confirmed a clean energy generation run that significantly surpassed previous thermal performance metrics. Clean-tech investment channels are observing immense upward sentiment spikes.",
        "url": "https://techcrunch.com"
    },
    {
        "headline": "Severe Tsunami Surge Inundates Coastal Agricultural Zones, Thousands Scattered", 
        "emotion": "Sadness", "country": "IDN", "region": "Southeast Asia", "icon": "🌊",
        "detailed_analysis": "A massive structural disaster system has destroyed vital community property arrays. Humanitarian groups have declared regional priority support statuses to handle medical infrastructure supply issues.",
        "url": "https://apnews.com"
    },
    {
        "headline": "Historic Library and Archive Matrix Destroyed in Massive Metropolitan Blaze", 
        "emotion": "Sadness", "country": "BRA", "region": "South America", "icon": "🏛️",
        "detailed_analysis": "Invaluable literature documents and cultural monuments spanning centuries were lost to an absolute containment breach. Global academic networks describe the structural loss as a profound blow to preservation research.",
        "url": "https://bbc.com"
    },
    {
        "headline": "Central Monetary Authority Maintains Current Lending Benchmarks Unchanged", 
        "emotion": "Neutral", "country": "DEU", "region": "Eurozone", "icon": "⚖️",
        "detailed_analysis": "The regional board concluded its standard audit with full consensus, adjusting no asset variables. Markets have factored this neutrality calculation directly into current structural baseline projections.",
        "url": "https://bloomberg.com"
    }
]
df_headlines = pd.DataFrame(headlines_pool)

# 3. Country Geographics
map_data = {
    'CountryISO': ['USA', 'CHN', 'GBR', 'DEU', 'IND', 'BRA', 'ZAF', 'IDN', 'CAN', 'UKR'],
    'Fear': [30.5, 12.4, 20.1, 15.3, 22.1, 18.4, 25.0, 14.2, 35.1, 45.0],
    'Anger': [20.1, 25.3, 15.4, 22.1, 18.2, 30.5, 20.1, 12.4, 15.3, 35.2],
    'Happiness': [15.2, 35.1, 30.5, 25.4, 32.1, 20.2, 15.4, 18.1, 20.5, 5.1],
    'Sadness': [20.1, 15.2, 19.3, 17.2, 15.4, 20.5, 24.1, 45.2, 14.1, 10.3],
    'Neutral': [14.1, 12.0, 14.7, 20.0, 12.2, 10.4, 15.4, 10.1, 15.0, 4.4]
}
df_map = pd.DataFrame(map_data)

# --- HEADER APP SECTION ---
st.title("🌍 World Mood Pulse Pro")
st.caption("Advanced Global Sentiment Engine • Project Dashboard Matrix")
st.write("")

# --- LIVE METRIC PULSE DISPLAY ---
st.markdown("### ⚡ Live Global Sentiment Distribution")
col1, col2, col3, col4, col5 = st.columns(5)

total_h = len(df_headlines)
pulse_vals = {em: round((len(df_headlines[df_headlines['emotion'] == em]) / total_h) * 100, 1) for em in ['Fear', 'Anger', 'Happiness', 'Sadness', 'Neutral']}

with col1: st.metric("😨 Fear Index", f"{pulse_vals['Fear']}%", delta="+4.2%")
with col2: st.metric("😡 Anger Index", f"{pulse_vals['Anger']}%", delta="+1.8%")
with col3: st.metric("😊 Happiness Index", f"{pulse_vals['Happiness']}%", delta="-0.5%")
with col4: st.metric("😢 Sadness Index", f"{pulse_vals['Sadness']}%", delta="+2.1%")
with col5: st.metric("😐 Neutral Index", f"{pulse_vals['Neutral']}%", delta="-7.6%")

st.markdown("---")

# --- CLICKABLE INTERACTIVE EXPLORER ---
st.markdown("### 🔍 Emotion Deep-Dive Explorer & Premium Media Cards")
selected_emotion = st.radio(
    "Select Target Emotion Engine to Filter Data Ecosystem:",
    ["Fear", "Anger", "Happiness", "Sadness", "Neutral"],
    horizontal=True
)

left_panel, right_panel = st.columns(2)

with left_panel:
    st.subheader(f"📰 Premium Analytical Coverage: {selected_emotion}")
    filtered_news = df_headlines[df_headlines['emotion'] == selected_emotion]
    
    if not filtered_news.empty:
        for idx, row in filtered_news.iterrows():
            with st.container():
                st.markdown('<div class="news-card-box">', unsafe_allow_html=True)
                st.subheader(f"{row['icon']} {row['headline']}")
                st.markdown(f"<span class='tag-bubble'>{row['region']}</span> &nbsp;&nbsp; <span class='tag-bubble'>📍 Source: {row['country']}</span>", unsafe_allow_html=True)
                st.write("")
                st.write(row['detailed_analysis'])
                st.markdown(f"🔗 [Access Deep Coverage Source Website]({row['url']})")
                st.markdown('</div>', unsafe_allow_html=True)
                st.write("")
    else:
        st.write("No major headline spikes currently registered for this channel.")

with right_panel:
    st.subheader("Regional Vulnerability Contribution")
    fig_pie = px.pie(df_map, values=selected_emotion, names='CountryISO', 
                     title=f"Top Country Impact Variables for {selected_emotion}",
                     color_discrete_sequence=px.colors.sequential.Plotly3)
    fig_pie.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")

# --- TIME SERIES HISTORICAL TREND GRAPHS ---
st.markdown("### 📈 Historical Sentimental Trajectories")
fig_trend = go.Figure()
for emotion in ['Fear', 'Anger', 'Happiness', 'Sadness', 'Neutral']:
    fig_trend.add_trace(go.Scatter(x=df_history['Date'], y=df_history[emotion], mode='lines+markers', name=emotion))
fig_trend.update_layout(xaxis_title="Timeline Records", yaxis_title="Percentage Allocation (%)", hovermode="x unified")
st.plotly_chart(fig_trend, use_container_width=True)

# --- GLOBAL HEATMAP SECTION ---
st.markdown("### 🗺️ World Emotion Spatial Layout")
fig_map = px.choropleth(df_map, locations="CountryISO", color=selected_emotion,
                        hover_name="CountryISO", color_continuous_scale=px.colors.sequential.Plasma)
fig_map.update_layout(geo=dict(showframe=False, projection_type='equirectangular'))
st.plotly_chart(fig_map, use_container_width=True)
