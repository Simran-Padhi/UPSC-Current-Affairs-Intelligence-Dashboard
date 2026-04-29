import pandas as pd
from textblob import TextBlob
import os
import nltk
from newsapi import NewsApiClient
import streamlit as st

# --- 1. BOOTSTRAPPER (MUST BE AT TOP) ---
@st.cache_resource
def load_nltk():
    try:
        nltk.download('punkt')
        nltk.download('punkt_tab')
    except:
        pass

load_nltk()

# --- 2. DATA ACQUISITION ---
def fetch_upsc_news(query='Indian Economy'):
    # We initialize INSIDE the function to prevent the startup crash
    try:
        # Pull key from Streamlit Secrets
        api_key = st.secrets["NEWS_API_KEY"]
        newsapi = NewsApiClient(api_key=api_key)
        
        data = newsapi.get_everything(q=query, language='en', sort_by='relevancy')
        
        if data['status'] == 'ok':
            articles = data['articles']
            news_data = [[a['title'], a['source']['name'], a['description'], a['url']] for a in articles]
            df = pd.DataFrame(news_data, columns=['Title', 'Source', 'Summary', 'URL'])
            return df
        return None
    except Exception as e:
        # This helps us see the error in the dashboard instead of a white screen
        st.error(f"Engine Connection Error: {e}")
        return None

# --- 3. ANALYTICS ---
def get_sentiment(text):
    if not text: return "Neutral/Factual"
    analysis = TextBlob(str(text))
    score = analysis.sentiment.polarity
    if score > 0.1: return "Positive/Supportive"
    elif score < -0.1: return "Critical/Negative"
    else: return "Neutral/Factual"

def clean_data(df):
    df = df.drop_duplicates(subset=['Title'])
    df = df.dropna(subset=['Summary'])
    # Fix for the bracket cleaning warning
    df['Summary'] = df['Summary'].str.split(r' \[').str[0]
    df = df[df['Summary'].str.len() > 20]
    return df

def map_to_syllabus(df):
    # Your GS Paper Categories
    editorial_keywords = ['EDITORIAL', 'OPINION', 'ANALYSIS', 'COMMENTARY']
    economy_keywords = ['GDP', 'RBI', 'INFLATION', 'BUDGET', 'ECONOMY']
    env_keywords = ['CLIMATE', 'POLLUTION', 'ENVIRONMENT', 'SUSTAINABLE']
    polity_keywords = ['CONSTITUTION', 'SUPREME COURT', 'BILL', 'PARLIAMENT']
    ir_keywords = ['UNSC', 'BILATERAL', 'DIPLOMATIC', 'SUMMIT', 'G20']
    
    def categorize(text):
        t = str(text).upper()
        if any(word in t for word in editorial_keywords): return 'High Value: Editorial/Opinion'
        if any(word in t for word in economy_keywords): return 'GS III: Economy'
        if any(word in t for word in env_keywords): return 'GS III: Environment'
        if any(word in t for word in polity_keywords): return 'GS II: Polity'
        if any(word in t for word in ir_keywords): return 'GS II: International Relations'
        return 'General News'

    df['Category'] = df['Summary'].apply(categorize)
    return df
