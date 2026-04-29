import streamlit as st
import pandas as pd
import nltk
from news_engine import fetch_upsc_news, clean_data, map_to_syllabus, get_sentiment

# 1. UI SETUP
st.set_page_config(page_title="UPSC Intelligence", layout="wide", page_icon="🏛️")

# 2. ADVANCED CSS (Restoring your clean look)
st.markdown("""
    <style>
    .stApp { background-color: #F8FAFC; font-family: 'Inter', sans-serif; }
    section[data-testid="stSidebar"] { background-color: #FFFFFF !important; border-right: 1px solid #E2E8F0; }
    .stButton>button { background-color: #1E293B; color: white; border-radius: 8px; border: none; padding: 0.6rem 1rem; width: 100%; }
    div[data-testid="stMetric"] { background-color: #FFFFFF; border: 1px solid #E2E8F0; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }
    h1 { color: #0F172A; font-weight: 800; }
    </style>
    """, unsafe_allow_html=True)

# 3. NLTK INITIALIZATION
@st.cache_resource
def init_nlp():
    try:
        nltk.download('punkt')
        nltk.download('punkt_tab')
    except:
        pass

init_nlp()

# 4. SIDEBAR
with st.sidebar:
    st.title("🏛️ Intelligence")
    st.caption("UPSC Current Affairs Tool v2.0")
    st.markdown("---")
    user_query = st.text_input("Syllabus Focus", "Indian Economy")
    fetch_button = st.button("Generate Feed")
    st.markdown("---")
    st.markdown("### 🎯 Active Filter")
    
    paper_options = [
        "High Value: Editorial/Opinion", "GS I: Social Issues", "GS I: Culture",
        "GS II: Polity", "GS II: International Relations", "GS III: Economy",
        "GS III: Environment", "GS IV: Ethics & Security", "General News"
    ]
    selected_papers = st.multiselect("Filter GS Papers:", options=paper_options, default=paper_options)

# 5. MAIN PAGE HEADER
st.title("Current Affairs Intelligence Dashboard")
st.markdown("Filtered and categorized daily news signals for Civil Services preparation.")

# 6. EXECUTION LOGIC
if fetch_button:
    with st.spinner("Syncing data streams..."):
        # Get key from secrets and run engine
        api_key = st.secrets["NEWS_API_KEY"]
        raw_data = fetch_upsc_news(user_query, api_key)
        
        if raw_data is not None:
            # Processing Pipeline
            df = clean_data(raw_data)
            df = map_to_syllabus(df)
            df['Sentiment'] = df['Summary'].apply(get_sentiment)
            
            # Filtering
            filtered_df = df[df['Category'].isin(selected_papers)]
            
            # --- KPI METRICS ---
            m_col1, m_col2, m_col3 = st.columns(3)
            m_col1.metric("Total Articles", len(filtered_df))
            m_col2.metric("Critical Tone", len(filtered_df[filtered_df['Sentiment'] == 'Critical/Negative']))
            m_col3.metric("Supportive Tone", len(filtered_df[filtered_df['Sentiment'] == 'Positive/Supportive']))
            
            st.markdown("### 📊 Syllabus Trend Analysis")
            
            # --- VISUALIZATION CHARTS ---
            c_col1, c_col2 = st.columns([2, 1])
            with c_col1:
                # Bar Chart for Syllabus categories
                st.bar_chart(filtered_df['Category'].value_counts(), color="#1E293B")
            with c_col2:
                # Area Chart for Editorial Tone
                st.write("**Editorial Tone Analysis**")
                st.area_chart(filtered_df['Sentiment'].value_counts(), color="#64748B")

            st.markdown("---")
            
            # --- DATA TABLE ---
            st.subheader("📰 Daily Intelligence Briefing")
            st.dataframe(
                filtered_df[['Category', 'Sentiment', 'Title', 'URL']],
                column_config={
                    "URL": st.column_config.LinkColumn("🔗 View Article"),
                    "Category": "GS Paper",
                    "Sentiment": "Tone"
                },
                use_container_width=True,
                hide_index=True
            )
        else:
            st.error("Engine Connection Timeout. Please check your API key in Secrets.")

else:
    st.info("👋 Welcome! The Intelligence Engine is ready. Enter a topic and click 'Generate Feed'.")
    st.image("https://images.unsplash.com/photo-1505664194779-8beaceb93744?auto=format&fit=crop&q=80&w=1000")
