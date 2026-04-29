import pandas as pd
from textblob import TextBlob
import os
import nltk
from newsapi import NewsApiClient
import streamlit as st

# --- 1. CLOUD BOOTSTRAPPER ---
# This ensures NLTK works on the Streamlit Server
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt')
    nltk.download('punkt_tab')

# --- 2. DATA ACQUISITION ENGINE ---
def fetch_upsc_news(query='Indian Economy'):
    # FIXED: Initialize inside the function for security and cloud stability
    # It will pull the key from your Streamlit Secrets
    try:
        api_key = st.secrets["NEWS_API_KEY"]
        newsapi = NewsApiClient(api_key=api_key)
        
        data = newsapi.get_everything(q=query, language='en', sort_by='relevancy')
        
        if data['status'] == 'ok':
            articles = data['articles']
            news_data = [[a['title'], a['source']['name'], a['description'], a['url']] for a in articles]
            df = pd.DataFrame(news_data, columns=['Title', 'Source', 'Summary', 'URL'])
            return df
        else:
            return None
    except Exception as e:
        st.error(f"Engine Error: {e}")
        return None

# --- 3. ANALYTICAL INTELLIGENCE ---
def get_sentiment(text):
    if not text: return "Neutral/Factual"
    analysis = TextBlob(str(text))
    score = analysis.sentiment.polarity
    if score > 0.1: return "Positive/Supportive"
    elif score < -0.1: return "Critical/Negative"
    else: return "Neutral/Factual"

def clean_data(df):
    initial_count = len(df)
    df = df.drop_duplicates(subset=['Title'])
    df = df.dropna(subset=['Summary'])
    
    # Cleaning truncated text tags safely
    df['Summary'] = df['Summary'].str.split(r' \[').str[0]
    df = df[df['Summary'].str.len() > 20]
    
    final_count = len(df)
    print(f"✅ Cleaning Complete: Removed {initial_count - final_count} rows.")
    return df

def map_to_syllabus(df):
    # Your keyword buckets (Editorial, Economy, Env, Polity, IR, Society, Culture, Ethics)
    # [Rest of your extensive keyword lists stay the same...]
    
    editorial_keywords = ['Editorial', 'Opinion', 'Analysis', 'Perspective', 'Commentary', 'Viewpoint']
    economy_keywords = ['GDP', 'RBI', 'Inflation', 'Budget', 'Fiscal', 'Banking', 'Trade']
    env_keywords = ['Climate', 'Pollution', 'Wildlife', 'Emission', 'Sustainable']
    polity_keywords = ['Constitution', 'Supreme Court', 'Bill', 'Parliament', 'Election']
    ir_keywords = ['UNSC', 'Bilateral', 'Diplomatic', 'Treaty', 'Summit', 'G20']
    society_keywords = ['Poverty', 'Education', 'Health', 'Empowerment', 'Migration']
    culture_keywords = ['Heritage', 'Monument', 'Archaeology', 'UNESCO']
    ethics_security_keywords = ['Corruption', 'Ethical', 'Integrity', 'Cyberattack', 'Terrorism']

    def categorize(text):
        text = str(text).upper()
        if any(word.upper() in text for word in editorial_keywords): return 'High Value: Editorial/Opinion'
        if any(word.upper() in text for word in economy_keywords): return 'GS III: Economy'
        if any(word.upper() in text for word in env_keywords): return 'GS III: Environment'
        if any(word.upper() in text for word in polity_keywords): return 'GS II: Polity'
        if any(word.upper() in text for word in ir_keywords): return 'GS II: International Relations'
        if any(word.upper() in text for word in culture_keywords): return 'GS I: Culture'
        if any(word.upper() in text for word in society_keywords): return 'GS I: Social Issues'
        if any(word.upper() in text for word in ethics_security_keywords): return 'GS IV: Ethics & Security'
        return 'General News'

    df['Category'] = df['Summary'].apply(categorize)
    return df
