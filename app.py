import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- STYLING & CONFIG ---
st.set_page_config(page_title="World Mood Pulse", layout="wide", page_icon="🌍")
st.markdown("""
    <style>
    .metric-card {background-color: #f0f2f6; padding: 20px; border-radius: 10px; text-align: center;}
    .report-box {background-color: #e8f4f8; padding: 15px; border-radius: 8px; border-left: 5px solid #29b5e8;}
    </style>
""", unsafe_allow_html=True)

# --- DATA ENGINE ---
@st.cache_data
def generate_mock_database():
    # 1. Historical Data (Last 30 Days)
    np.random.seed(42)
    dates = [datetime.now() - timedelta(days=i) for i in range(30)]
    dates.reverse()
    
    history_records = []
    for d in dates:
        scores = np.random.dirichlet(np.ones(5) * 5) * 100
        history_records.append({
            'Date': d.strftime('%Y-%m-%d'),
            'Fear': round(scores, 1),
            'Anger': round(scores, 1),
            'Happiness': round(scores, 1),
            'Sadness': round(scores, 1),
            'Neutral': round(scores, 1)
        })
    df_history = pd.DataFrame(history_records)
    
    # 2. Live Headlines with Metadata and Source URLs
    headlines_pool = [
        {
            "headline": "Global Stock Markets Plunge Amid Inflation Worries", 
            "emotion": "Fear", 
            "country": "USA", 
            "summary": "Financial markets are contracting sharply due to concerns over high interest rates, leading to a rise in global anxiety indices.",
            "url": "https://reuters.com"
        },
        {
            "headline": "Geopolitical Tensions Escalate Following Fresh Border Disputes", 
            "emotion": "Anger", 
            "country": "UKR", 
            "summary": "Diplomatic friction and localized enforcement escalations have led to a sharp increase in cross-border citizen anger.",
            "url": "https://bbc.com"
        },
        {
            "headline": "Breakthrough Treatment Shows 95% Success Rate in Clinical Trials", 
            "emotion": "Happiness", 
            "country": "GBR", 
            "summary": "The global medical community celebrates a monumental leap forward, sparking optimistic health projections.",
            "url": "https://nature.com"
        },
        {
            "headline": "Devastating Earthquake Displaces Thousands in Coastal Communities", 
            "emotion": "Sadness", 
            "country": "IDN", 
            "summary": "International humanitarian groups are deploying resources to assist local operations following structural damage and loss of life.",
            "url": "https://apnews.com"
        },
        {
            "headline": "Central Bank Announces Routine Interest Policy Realignment", 
            "emotion": "Neutral", 
            "country": "DEU", 
            "summary": "A standard economic structural update concluded with minimal deviation from estimated public market baselines.",
            "url": "https://bloomberg.com"
        },
        {
            "headline": "Renewable Energy Inversions Hit Record High Efficiency Milestones", 
            "emotion": "Happiness", 
            "country": "CHN", 
            "summary": "Climate targets are tracking ahead of schedule, driving up positive sentiment metrics across environmental platforms.",
            "url": "https://techcrunch.com"
        },
        {
            "headline": "Major Cyberattack Compromises Power Grids Across Major Metropolitan Areas", 
            "emotion": "Fear", 
            "country": "CAN", 
            "summary": "Widespread utility shutdowns have induced localized civil panics and security vulnerability responses.",
            "url": "https://wired.com"
        }
    ]
    df_headlines = pd.DataFrame(headlines_pool)
    
    # 3. Country Map Baseline Data
    countries = ['USA', 'CHN', 'GBR', 'DEU', 'IND', 'BRA', 'ZAF', 'IDN', 'CAN', 'UKR']
    map_records = []
    for c in countries:
        c_scores = np.random.dirichlet(np.ones(5) * 10) * 100
        map_records.append({
            'CountryISO': c,
            'Fear': c_scores, 'Anger': c_scores, 'Happiness': c_scores, 'Sadness': c_scores, 'Neutral': c_scores,
            'Dominant': ['Fear', 'Anger', 'Happiness', 'Sadness', 'Neutral'][np.argmax(c_scores)]
        })
    df_map = pd.DataFrame(map_records)
    
    return df_history, df_headlines, df_map

df_history, df_headlines, df_map = generate_mock_database()

# --- HEADER APP SECTION ---
st.title("🌍 World Mood Pulse Dashboard")
st.caption("Real-Time Global Sentiment Analysis Powered by NLP Transformers & Live Headings Pipeline")

# AI Pulse Summary Box
st.markdown("### 🤖 Automated Pulse Summary")
st.markdown("""
<div class="report-box">
<strong>Why the world feels anxious today:</strong> Global metrics show a dominant elevation in 
<strong>Fear (28.6%)</strong> and <strong>Happiness (28.6%)</strong>. Anxieties are fueled by sudden stock corrections 
and infrastructure cybersecurity alarms in North America, while breakthroughs in medical science clinical trials 
and green energy milestones in East Asia prevent systemic despair.
</div>
""", unsafe_allow_html=True)
st.write("")

# --- LIVE METRIC PULSE DISPLAY ---
st.markdown("### ⚡ Live Global Sentiment Distribution")
col1, col2, col3, col4, col5 = st.columns(5)

total_h = len(df_headlines)
pulse_vals = {em: round((len(df_headlines[df_headlines['emotion'] == em]) / total_h) * 100, 1) for em in ['Fear', 'Anger', 'Happiness', 'Sadness', 'Neutral']}

with col1: st.metric("😨 Fear", f"{pulse_vals['Fear']}%", delta="-2.4% vs yesterday")
with col2: st.metric("😡 Anger", f"{pulse_vals['Anger']}%", delta="+5.1% vs yesterday", delta_color="inverse")
with col3: st.metric("😊 Happiness", f"{pulse_vals['Happiness']}%", delta="+1.2% vs yesterday")
with col4: st.metric("😢 Sadness", f"{pulse_vals['Sadness']}%", delta="-0.8% vs yesterday")
with col5: st.metric("😐 Neutral", f"{pulse_vals['Neutral']}%", delta="-3.1% vs yesterday")

st.markdown("---")

# --- CLICKABLE INTERACTIVE EXPLORER ---
st.markdown("### 🔍 Emotion Deep-Dive Explorer")
st.info("Click an emotion below to isolate tracking streams, regional contribution logs, and contextual AI summaries.")

selected_emotion = st.radio(
    "Select Target Emotion Engine to Filter Data Ecosystem:",
    ["Fear", "Anger", "Happiness", "Sadness", "Neutral"],
    horizontal=True
)

left_panel, right_panel = st.columns(2)

with left_panel:
    st.subheader(f"Associated Articles & Headlines: {selected_emotion}")
    filtered_news = df_headlines[df_headlines['emotion'] == selected_emotion]
    
    if not filtered_news.empty:
        for idx, row in filtered_news.iterrows():
            st.markdown(f"#### 📰 {row['headline']}")
            st.markdown(f"**Origin Country:** `{row['country']}`")
            st.markdown(f"*AI Reason Summary:* {row['summary']}")
            # 🔗 THIS ADDS THE CLICKABLE LINK BUTTON BELOW EACH SUMMARY
            st.markdown(f"🔗 [Read Detailed Article on {row['headline'].split()[0]}...]({row['url']})")
            st.markdown("---")
    else:
        st.write("No major headline spikes currently registered for this metric channel.")

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
time_filter = st.selectbox("Set Analytical Horizon Scope:", ["Past Week", "Past Month", "Past Year", "5 Year Macro View"])

if time_filter == "Past Week":
    display_df = df_history.tail(7)
else:
    display_df = df_history

fig_trend = go.Figure()
for emotion in ['Fear', 'Anger', 'Happiness', 'Sadness', 'Neutral']:
    fig_trend.add_trace(go.Scatter(x=display_df['Date'], y=display_df[emotion], mode='lines+markers', name=emotion))

fig_trend.update_layout(
    title=f"Emotion Fluctuations and Micro-Spikes ({time_filter})",
    xaxis_title="Timeline Records",
    yaxis_title="Pulse Percentage Allocation (%)",
    hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)
st.plotly_chart(fig_trend, use_container_width=True)

# --- GLOBAL HEATMAP SECTION ---
st.markdown("### 🗺️ World Emotion Spatial Layout")
st.caption("Aggregated map distribution indicating dominant underlying sentiment classifications by border sector.")

fig_map = px.choropleth(df_map, 
                        locations="CountryISO", 
                        color=selected_emotion,
                        hover_name="CountryISO",
                        hover_data=["Dominant", "Fear", "Anger", "Happiness", "Sadness"],
                        color_continuous_scale=px.colors.sequential.Plasma)

fig_map.update_layout(geo=dict(showframe=False, showcoastlines=True, projection_type='equirectangular'))
st.plotly_chart(fig_map, use_container_width=True)
