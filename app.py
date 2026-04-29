import streamlit as st
import pandas as pd
from news_engine import fetch_upsc_news, clean_data, map_to_syllabus, get_sentiment

# 1. High-End UI Configuration
st.set_page_config(page_title="UPSC Intelligence", layout="wide", page_icon="🏛️")

# 2. Advanced CSS for "Clean & Aesthetic" Look
st.markdown("""
    <style>
    .stApp { background-color: #F8FAFC; font-family: 'Inter', sans-serif; }
    section[data-testid="stSidebar"] { background-color: #FFFFFF !important; border-right: 1px solid #E2E8F0; }
    .stButton>button { background-color: #1E293B; color: white; border-radius: 8px; border: none; padding: 0.6rem 1rem; width: 100%; }
    .stButton>button:hover { background-color: #334155; color: #60A5FA; }
    div[data-testid="stMetric"] { background-color: #FFFFFF; border: 1px solid #E2E8F0; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }
    h1 { color: #0F172A; font-weight: 800; }
    </style>
    """, unsafe_allow_html=True)

# 3. Functional Sidebar
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
    
    selected_papers = st.multiselect("Filter by GS Paper:", options=paper_options, default=paper_options)

# 4. Main Dashboard Header
st.title("Current Affairs Intelligence Dashboard")
st.markdown("Filtered and categorized daily news signals for Civil Services preparation.")

if fetch_button:
    with st.spinner('Syncing data streams...'):
        # Acquisition
        raw_data = fetch_upsc_news(user_query)
        
        if raw_data is not None:
            # Step A: Run the Pipeline
            df = clean_data(raw_data)
            df = map_to_syllabus(df)
            df['Sentiment'] = df['Summary'].apply(get_sentiment)
            
            # Step B: Filter the data based on sidebar selection
            filtered_df = df[df['Category'].isin(selected_papers)]
            
            # 5. KPI Metrics
            m_col1, m_col2, m_col3, m_col4 = st.columns(4)
            m_col1.metric("Total Articles", len(filtered_df))
            
            signals = len(filtered_df[filtered_df['Category'] != 'General News'])
            m_col2.metric("Syllabus Signals", signals)
            
            m_col3.metric("Critical Tone", len(filtered_df[filtered_df['Sentiment'] == 'Critical/Negative']))
            m_col4.metric("Supportive Tone", len(filtered_df[filtered_df['Sentiment'] == 'Positive/Supportive']))
            
            st.markdown("### 📊 Syllabus Trend Analysis")
            
            # 6. Aesthetic Charts
            c_col1, c_col2 = st.columns([2, 1])
            with c_col1:
                st.bar_chart(filtered_df['Category'].value_counts(), color="#1E293B")
            with c_col2:
                st.write("**Editorial Tone Analysis**")
                st.area_chart(filtered_df['Sentiment'].value_counts(), color="#64748B")

            st.markdown("---")
            
            # 7. Modern Data Table
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
            st.error("No articles found or API connection failed.")

# Default Welcome State
else:
    st.info("👋 Welcome! Enter a topic in the sidebar and click 'Generate Feed' to start your intelligence briefing.")
    st.image("https://images.unsplash.com/photo-1505664194779-8beaceb93744?auto=format&fit=crop&q=80&w=1000", caption="UPSC Intelligence Hub")
