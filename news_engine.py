import pandas as pd
from newsapi import NewsApiClient
from textblob import TextBlob

# 1. Initialize the API
newsapi = NewsApiClient(api_key='f01b108d33af4dbeaee122b566d35892')

def fetch_upsc_news(query='Indian Economy'):
    # Fetch data from the last 24 hours
    data = newsapi.get_everything(q=query, language='en', sort_by='relevancy')
    
    if data['status'] == 'ok':
        articles = data['articles']
        # Selecting only the 'Signals' (Title, Source, Summary, URL)
        news_data = [[a['title'], a['source']['name'], a['description'], a['url']] for a in articles]
        
        # Convert to a structured Pandas DataFrame
        df = pd.DataFrame(news_data, columns=['Title', 'Source', 'Summary', 'URL'])
        return df
    else:
        print("Error fetching data.")
        return None

def get_sentiment(text):
    # TextBlob turns text into a polarity score between -1 (Negative) and 1 (Positive)
    analysis = TextBlob(str(text))
    score = analysis.sentiment.polarity
    if score > 0.1: return "Positive/Supportive"
    elif score < -0.1: return "Critical/Negative"
    else: return "Neutral/Factual"

def clean_data(df):
    # 1. Remove duplicates based on the 'Title' to reduce noise
    initial_count = len(df)
    df = df.drop_duplicates(subset=['Title'])

    # 2. Handle missing values: Remove rows where the 'Summary' is empty
    df = df.dropna(subset=['Summary'])

    # 3. Data Integrity Check: Filter out very short summaries or API noise
    df['Summary'] = df['Summary'].str.split('\[').str[0] # Cleans truncated tags like [+123 chars]
    df = df[df['Summary'].str.len() > 20]

    final_count = len(df)
    print(f"✅ Cleaning Complete: Removed {initial_count - final_count} noisy rows.")
    return df

def map_to_syllabus(df):
    # Define Keyword Buckets
    editorial_keywords = [
        'Editorial', 'Opinion', 'Analysis', 'Perspective', 'Commentary', 'Viewpoint', 
        'column' , 'discourse' , 'critique', 'assessment' , 'Insight', 'Discussion', 
        'Debate', 'Reflection' , 'evaluation', 'implications' , 'framework' , 
        'paradigm', 'contextualizing' , 'reform' , 'manifesto' , 'roadmap' , 
        'narrative', 'underlying', 'systemic','structural','core issue','nuanced',
        'complexities','way forward','counter-view','consensus','rationale','takeaway'
    ]
    
    economy_keywords = [
        'GDP', 'RBI', 'Inflation', 'Budget', 'Fiscal', 'Banking', 'Trade', 'Tax', 'MSME', 
        'Infrastructure', 'FDI', 'Stock Market', 'Repo Rate', 'Current Account Deficit', 
        'Direct Tax', 'Indirect Tax', 'Monetary Policy', 'Capital Market', 'Inclusive Growth', 
        'Investment', 'Disinvestment', 'NITI Aayog', 'Privatization', 'Financial Inclusion', 
        'Digital Rupee', 'Exports', 'Imports', 'Blue Economy', 'Special Economic Zone', 'FII'
    ]

    env_keywords = [
        'Climate', 'Pollution', 'Wildlife', 'Emission', 'Forest', 'Sustainable', 'Ecology', 
        'Biodiversity', 'Renewable', 'Green Hydrogen', 'Global Warming', 'Conservation', 
        'National Park', 'Wetlands', 'Sanctuary', 'Environmental Impact', 'Net Zero', 
        'Carbon Credit', 'Paris Agreement', 'COP28', 'Endangered', 'Pollutant', 'Eco-system', 
        'Deforestation', 'Renewable Energy', 'Solar Power', 'Wind Energy', 'Circular Economy', 
        'Waste Management', 'Plastic Ban'
    ]

    polity_keywords = [
        'Constitution', 'Supreme Court', 'Bill', 'Parliament', 'Election', 'Judiciary', 'Citizen',
        'Fundamental Rights', 'High Court', 'Federalism', 'Panchayat', 'Governor', 'Cabinet',
        'Speaker', 'Ordinance', 'Amendment', 'Reservation', 'Vigilance', 'Tribunal', 'CBI',
        'Electoral Reform', 'Delimitation', 'Legislative', 'Quorum', 'Writ', 'Article', 
        'Secularism', 'Governance', 'Bureaucracy', 'Public Policy'
    ]

    ir_keywords = [
        'UNSC', 'Bilateral', 'Diplomatic', 'Treaty', 'Border', 'Summit', 'G20', 'ASEAN',
        'Indo-Pacific', 'Quad', 'BRICS', 'SCO', 'WTO', 'FTA', 'Geopolitics', 'Look East',
        'Diaspora', 'Soft Power', 'Maritime', 'Sanctions', 'Embassy', 'UNGA', 'NATO',
        'Line of Control', 'LOC', 'Line of Actual Control', 'LAC', 'Territorial', 'Non-Alignment', 'I2U2'
    ]

    society_keywords = [
        'Poverty', 'Education', 'Health', 'Empowerment', 'Population', 'Urbanization', 'Caste',
        'Gender', 'Social Justice', 'Migration', 'Globalization', 'Tribal', 'Secularism', 
        'Heritage', 'Ancient', 'Medieval', 'Archeology', 'Monument', 'Renaissance', 'Monsoon', 
        'Cyclone', 'Earthquake', 'Tsunami', 'Landscape', 'Resource', 'Demography', 
        'Diversity', 'Inclusion', 'Communalism', 'Regionalism'
    ]

    culture_keywords = [
        'Heritage', 'Monument', 'Archaeology', 'Excavation', 'Inscription', 'Architecture', 
        'UNESCO', 'Classical Dance', 'Folk Art', 'Ancient', 'Medieval', 'Temple', 'Sculpture', 
        'Manuscript', 'Artifact', 'Textiles', 'Handicraft', 'Philosophy', 'Literature', 
        'Epics', 'Mythology', 'Paintings', 'Music', 'Festivals', 'Pottery', 'Stupa', 'Cave', 
        'Vedic', 'Buddhist', 'Jainism'
    ]

    ethics_security_keywords = [
        'Corruption', 'Ethical', 'Integrity', 'Governance Crisis', 'Protest', 'Accountability',
        'Probity', 'Empathy', 'Compassion', 'Values', 'Code of Conduct', 'Aptitude', 'Conscience',
        'Transparency', 'Cyberattack', 'Terrorism', 'Insurgency', 'Naxalism', 'Defense', 
        'Cybersecurity', 'Radicalization', 'Sedition', 'Border Management', 'Missile', 
        'AFSPA', 'UAPA', 'Intelligence', 'Militancy', 'Narcotics', 'Extradition'
    ]

    def categorize(text):
        text = str(text).upper()
        # Priority check for Editorials first as they are high yield
        if any(word.upper() in text for word in editorial_keywords): return 'High Value: Editorial/Opinion'
        
        # GS Papers
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

# Main Execution Block
if __name__ == "__main__":
    # 1. Fetch
    raw_data = fetch_upsc_news()
    
    if raw_data is not None:
        # 2. Clean
        cleaned_data = clean_data(raw_data)
        
        # 3. Map to Syllabus
        mapped_data = map_to_syllabus(cleaned_data)
        
        # 4. Enrich with Sentiment Analysis
        mapped_data['Sentiment'] = mapped_data['Summary'].apply(get_sentiment)
        
        print("\n--- Intelligent UPSC Data Preview ---")
        # Showing top 15 results with our newly created Metadata
        print(mapped_data[['Title', 'Category', 'Sentiment']].head(15))