import ssl
# Fix macOS SSL certificate verification issues for feedparser
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

import streamlit as st
import pandas as pd
import requests
import feedparser
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# --- STYLING & CONFIG ---
st.set_page_config(page_title="World Mood Pulse Live", layout="wide", page_icon="🌍")

# Premium look & card design using Custom CSS
st.markdown("""
    <style>
    /* Main body background styling */
    .stApp {
        background-color: #f8fafc;
    }
    /* Dynamic custom CSS styles for clean, sleek card borders */
    .news-card-box {
        background-color: #ffffff; 
        padding: 20px; 
        border-radius: 12px; 
        box-shadow: 0 4px 10px rgba(0,0,0,0.04); 
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
    .highlight-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.03);
        border-left: 5px solid #29b5e8;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# --- LIVE NEWS ENGINE ---
@st.cache_data(ttl=600)
def fetch_real_live_news():
    columns = ["headline", "emotion", "country", "region", "icon", "detailed_analysis", "url", "score"]
    rss_url = "http://feeds.bbci.co.uk/news/world/rss.xml"
    emotions = ['Fear', 'Anger', 'Happiness', 'Sadness', 'Neutral']
    icons = {'Fear': '😨', 'Anger': '😡', 'Happiness': '😊', 'Sadness': '😢', 'Neutral': '😐'}
    
    analyzer = SentimentIntensityAnalyzer()
    articles = []
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(rss_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        feed = feedparser.parse(response.content)
        for entry in feed.entries[:40]: # parse top 40 live headlines
            title = entry.title
            link = entry.link
            summary = entry.get('summary', 'No live summary provided.')
            source = entry.source.title if hasattr(entry, 'source') else "BBC World News"
            
            if title and link:
                sentiment_scores = analyzer.polarity_scores(title)
                compound = sentiment_scores['compound']
                
                # Determine primary emotion classification based on VADER polarity
                if compound >= 0.2:
                    assigned_emotion = 'Happiness'
                elif compound <= -0.2:
                    if compound < -0.6:
                        assigned_emotion = 'Fear'
                    elif compound < -0.4:
                        assigned_emotion = 'Anger'
                    else:
                        assigned_emotion = 'Sadness'
                else:
                    assigned_emotion = 'Neutral'
                    
                articles.append({
                    "headline": str(title), "emotion": str(assigned_emotion),
                    "country": "International", "region": str(source),
                    "icon": icons[assigned_emotion], "detailed_analysis": str(summary), "url": str(link),
                    "score": float(compound)
                })
        if len(articles) > 0:
            return pd.DataFrame(articles)
    except Exception as e:
        st.warning(f"Error fetching live feed: {e}. Loading fallback dataset instead.")
        
    # --- STATIC FALLBACK DATA ---
    fallback_pool = [
        {"headline": "Global Stock Indices Plunge 4.2% Triggering Circuit Breakers Worldwide", "emotion": "Fear", "country": "USA", "region": "Reuters Markets", "icon": "📉", "detailed_analysis": "Widespread panic hit global trading floors today as unexpected inflation metrics sparked fears of prolonged high interest rates.", "url": "https://reuters.com", "score": -0.65},
        {"headline": "Metropolitan Cybersecurity Breach Compromises Electrical Infrastructure Nodes", "emotion": "Fear", "country": "CAN", "region": "Wired Security", "icon": "🔒", "detailed_analysis": "A coordinated digital assault has targeted power management systems. Civil vulnerability levels are currently elevated.", "url": "https://wired.com", "score": -0.58},
        {"headline": "Tech Security Sectors Sound Alarms Over New Quantum Decryption Tools", "emotion": "Fear", "country": "USA", "region": "TechCrunch", "icon": "💻", "detailed_analysis": "Enterprise security frameworks scramble to deploy protective patches following systemic vulnerability releases.", "url": "https://techcrunch.com", "score": -0.35},
        {"headline": "Public Transit Union Stages City-Wide Walkouts Over Structural Contracts", "emotion": "Anger", "country": "FRA", "region": "AP News", "icon": "📢", "detailed_analysis": "Commuters face massive scheduling standstills as negotiation deadlines expired with no settlement. High frustration values are registered.", "url": "https://apnews.com", "score": -0.42},
        {"headline": "Border Access Disagreements Lead to Stiff Commercial Import Embargos", "emotion": "Anger", "country": "UKR", "region": "BBC World", "icon": "🚫", "detailed_analysis": "Diplomatic talks fractured completely following enforcement updates, resulting in massive shipping supply freezes.", "url": "https://bbc.com", "score": -0.45},
        {"headline": "Medical Breakthrough: Universal Vaccine Demonstrates 95% Efficacy Rate", "emotion": "Happiness", "country": "GBR", "region": "Nature Journal", "icon": "🧬", "detailed_analysis": "An unprecedented milestone in immunotherapy has successfully cleared advanced peer-review phases, sparking optimistic health projections.", "url": "https://nature.com", "score": 0.82},
        {"headline": "Renewable Fusion Inverters Achieve Sustained Net Energy Influx Thresholds", "emotion": "Happiness", "country": "CHN", "region": "TechCrunch", "icon": "☀️", "detailed_analysis": "Engineering teams confirmed a clean energy generation run that significantly surpassed previous thermal performance metrics.", "url": "https://techcrunch.com", "score": 0.75},
        {"headline": "Severe Tsunami Surge Inundates Coastal Agricultural Zones, Thousands Scattered", "emotion": "Sadness", "country": "IDN", "region": "AP News", "icon": "🌊", "detailed_analysis": "A massive structural disaster system has destroyed vital community property arrays. Humanitarian groups have deployed priority resources.", "url": "https://apnews.com", "score": -0.72},
        {"headline": "Central Monetary Authority Maintains Current Lending Benchmarks Unchanged", "emotion": "Neutral", "country": "DEU", "region": "Bloomberg Business", "icon": "⚖️", "detailed_analysis": "The regional board concluded its standard audit with full consensus, adjusting no asset variables. Markets remain in a baseline state.", "url": "https://bloomberg.com", "score": 0.0}
    ]
    return pd.DataFrame(fallback_pool, columns=columns)

# Run Live Fetcher
df_headlines = fetch_real_live_news()

# --- CALCULATING EMOTION METRICS ---
total_articles = len(df_headlines)
emotions_list = ['Fear', 'Anger', 'Happiness', 'Sadness', 'Neutral']

# Fallback pool baseline values (pre-calculated based on 9 items)
baseline_percentages = {'Fear': 33.3, 'Anger': 22.2, 'Happiness': 22.2, 'Sadness': 11.1, 'Neutral': 11.1}

live_percentages = {}
for em in emotions_list:
    subset = df_headlines[df_headlines['emotion'] == em]
    live_percentages[em] = round((len(subset) / total_articles) * 100, 1) if total_articles > 0 else 20.0

# --- HEADER APP SECTION ---
st.title("🌍 World Mood Pulse Live")
st.caption("A beginner-friendly project prototype showing real-time global news sentiment.")

# --- LIVE METRIC COLUMNS ---
st.markdown("### ⚡ Live Global Sentiment Distribution")
col1, col2, col3, col4, col5 = st.columns(5)

icons_map = {'Fear': '😨', 'Anger': '😡', 'Happiness': '😊', 'Sadness': '😢', 'Neutral': '😐'}
for idx, col in enumerate([col1, col2, col3, col4, col5]):
    em = emotions_list[idx]
    pct = live_percentages[em]
    diff = round(pct - baseline_percentages[em], 1)
    
    # Format a simple, easy to understand text delta
    delta_str = f"{diff:+.1f}% vs baseline"
    
    with col:
        st.metric(label=f"{icons_map[em]} {em} Index", value=f"{pct}%", delta=delta_str)

st.markdown("---")

# --- SIDE-BY-SIDE STORY HIGHLIGHTS ---
st.markdown("### 🌟 Headline Spotlights")
h_col1, h_col2 = st.columns(2)

# Uplifting Story (Highest VADER score)
uplifting_story = df_headlines.loc[df_headlines['score'].idxmax()]
# Critical Story (Lowest VADER score)
critical_story = df_headlines.loc[df_headlines['score'].idxmin()]

with h_col1:
    st.markdown("#### ☀️ Today's Most Uplifting Story")
    st.markdown(f"""
    <div class="highlight-card" style="border-left-color: #10b981;">
        <h4 style="margin:0 0 5px 0;">{uplifting_story['icon']} {uplifting_story['headline']}</h4>
        <p style="font-size:13px; color:#4a5568; margin-bottom:8px;">{uplifting_story['detailed_analysis']}</p>
        <span class="tag-bubble">{uplifting_story['region']}</span> &nbsp;
        <span class="tag-bubble" style="background-color:#d1fae5; color:#065f46;">Score: {uplifting_story['score']}</span>
    </div>
    """, unsafe_allow_html=True)

with h_col2:
    st.markdown("#### 🌧️ Today's Most Critical Story")
    st.markdown(f"""
    <div class="highlight-card" style="border-left-color: #ef4444;">
        <h4 style="margin:0 0 5px 0;">{critical_story['icon']} {critical_story['headline']}</h4>
        <p style="font-size:13px; color:#4a5568; margin-bottom:8px;">{critical_story['detailed_analysis']}</p>
        <span class="tag-bubble">{critical_story['region']}</span> &nbsp;
        <span class="tag-bubble" style="background-color:#fee2e2; color:#991b1b;">Score: {critical_story['score']}</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- SEARCH & MOOD BOOSTER ---
st.markdown("### 🔍 Live Explorer & Interaction")
int_col1, int_col2 = st.columns([2, 1])

with int_col1:
    search_query = st.text_input("Search live headlines by keyword:", placeholder="Type a keyword, e.g. 'US', 'China', 'stock'...")

with int_col2:
    st.write("Need some happiness?")
    if st.button("Click for a Mood Boost! 🌟", use_container_width=True):
        st.balloons()
        # Find the happiest fallback / live story to display
        happy_story = df_headlines[df_headlines['emotion'] == 'Happiness'].sample(1).iloc[0]
        st.success(f"**{happy_story['icon']} {happy_story['headline']}**\n\n{happy_story['detailed_analysis']}")

# Apply Search Query filter
if search_query:
    filtered_df = df_headlines[df_headlines['headline'].str.contains(search_query, case=False, na=False)]
    st.info(f"Showing {len(filtered_df)} matches for '{search_query}':")
else:
    filtered_df = df_headlines

# --- DEEP-DIVE EXPLORER FILTERED BY EMOTION ---
selected_emotion = st.radio(
    "Filter news feed by target emotion engine:",
    ["Fear", "Anger", "Happiness", "Sadness", "Neutral"],
    horizontal=True
)

st.subheader(f"📰 Live Feed Slice: {selected_emotion}")
final_display_df = filtered_df[filtered_df['emotion'] == selected_emotion]

if not final_display_df.empty:
    for idx, row in final_display_df.iterrows():
        st.markdown(f"""
        <div class="news-card-box">
            <h3 style="margin-top: 0; color: #1e293b;">{row['icon']} {row['headline']}</h3>
            <p>
                <span class='tag-bubble'>{row['region']}</span> &nbsp;&nbsp; 
                <span class='tag-bubble'>📍 Source: {row['country']}</span>
            </p>
            <p style="color: #4a5568;">{row['detailed_analysis']}</p>
            <a href="{row['url']}" target="_blank" style="text-decoration: none; font-weight: bold; color: #29b5e8;">🔗 Access Full Coverage Source Website</a>
        </div>
        """, unsafe_allow_html=True)
else:
    st.write("No headlines matching the search criteria or selected emotion are currently registered.")
