import pandas as pd
from textblob import TextBlob
from newsapi import NewsApiClient

def fetch_upsc_news(query, api_key):
    newsapi = NewsApiClient(api_key=api_key)
    try:
        data = newsapi.get_everything(q=query, language='en', sort_by='relevancy')
        if data['status'] == 'ok':
            articles = data['articles']
            news_data = [[a['title'], a['source']['name'], a['description'], a['url']] for a in articles]
            return pd.DataFrame(news_data, columns=['Title', 'Source', 'Summary', 'URL'])
        return None
    except:
        return None

def get_sentiment(text):
    if not text: return "Neutral/Factual"
    analysis = TextBlob(str(text))
    score = analysis.sentiment.polarity
    if score > 0.1: return "Positive/Supportive"
    elif score < -0.1: return "Critical/Negative"
    else: return "Neutral/Factual"

def clean_data(df):
    df = df.drop_duplicates(subset=['Title']).dropna(subset=['Summary'])
    df['Summary'] = df['Summary'].str.split(r' \[').str[0]
    return df[df['Summary'].str.len() > 20]

def map_to_syllabus(df):
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
    ethics_keywords = [
        'Corruption', 'Ethical', 'Integrity', 'Governance Crisis', 'Protest', 'Accountability',
        'Probity', 'Empathy', 'Compassion', 'Values', 'Code of Conduct', 'Aptitude', 'Conscience',
        'Transparency', 'Cyberattack', 'Terrorism', 'Insurgency', 'Naxalism', 'Defense', 
        'Cybersecurity', 'Radicalization', 'Sedition', 'Border Management', 'Missile', 
        'AFSPA', 'UAPA', 'Intelligence', 'Militancy', 'Narcotics', 'Extradition'
    ]

    def categorize(text):
        t = str(text).upper()
        if any(w.upper() in t for w in editorial_keywords): return 'High Value: Editorial/Opinion'
        if any(w.upper() in t for w in economy_keywords): return 'GS III: Economy'
        if any(w.upper() in t for w in env_keywords): return 'GS III: Environment'
        if any(w.upper() in t for w in polity_keywords): return 'GS II: Polity'
        if any(w.upper() in t for w in ir_keywords): return 'GS II: International Relations'
        if any(w.upper() in t for w in culture_keywords): return 'GS I: Culture'
        if any(w.upper() in t for w in society_keywords): return 'GS I: Social Issues'
        if any(w.upper() in t for w in ethics_keywords): return 'GS IV: Ethics & Security'
        return 'General News'

    df['Category'] = df['Summary'].apply(categorize)
    return df