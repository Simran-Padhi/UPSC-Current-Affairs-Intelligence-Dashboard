import streamlit as st
import nltk
from news_engine import fetch_upsc_news, clean_data, map_to_syllabus, get_sentiment

# 1. UI SETUP
st.set_page_config(page_title="UPSC Intelligence", layout="wide", page_icon="🏛️")

# 2. DOWNLOAD NLTK (Cloud Friendly)
@st.cache_resource
def init_nlp():
    nltk.download('punkt')
    nltk.download('punkt_tab')

init_nlp()

# 3. SIDEBAR
with st.sidebar:
    st.title("🏛️ Intelligence")
    user_query = st.text_input("Syllabus Focus", "Indian Economy")
    fetch_button = st.button("Generate Feed")
    
    st.markdown("---")
    paper_options = [
        "High Value: Editorial/Opinion", "GS I: Social Issues", "GS I: Culture",
        "GS II: Polity", "GS II: International Relations", "GS III: Economy",
        "GS III: Environment", "GS IV: Ethics & Security", "General News"
    ]
    selected_papers = st.multiselect("Filter GS Papers:", options=paper_options, default=paper_options)

st.title("Current Affairs Intelligence Dashboard")

# 4. EXECUTION
if fetch_button:
    with st.spinner("Syncing data streams..."):
        api_key = st.secrets["NEWS_API_KEY"]
        raw = fetch_upsc_news(user_query, api_key)
        
        if raw is not None:
            df = clean_data(raw)
            df = map_to_syllabus(df)
            df['Sentiment'] = df['Summary'].apply(get_sentiment)
            
            filtered_df = df[df['Category'].isin(selected_papers)]
            
            # Metrics
            m1, m2, m3 = st.columns(3)
            m1.metric("Total Articles", len(filtered_df))
            m2.metric("Critical Tone", len(filtered_df[filtered_df['Sentiment'] == 'Critical/Negative']))
            m3.metric("Supportive Tone", len(filtered_df[filtered_df['Sentiment'] == 'Positive/Supportive']))
            
            st.dataframe(filtered_df[['Category', 'Sentiment', 'Title', 'URL']], 
                         column_config={"URL": st.column_config.LinkColumn("🔗 View")},
                         use_container_width=True, hide_index=True)
        else:
            st.error("Check your API Key in Streamlit Secrets!")
else:
    st.info("👋 Welcome! Click 'Generate Feed' to start.")