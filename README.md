🏛️ UPSC Current Affairs Intelligence Dashboard
A Python-powered NLP tool to filter noise and prioritize signals for Civil Services preparation.

📌 Project Overview
Aspirants for the UPSC (Union Public Service Commission) exams often spend 2–3 hours daily scanning newspapers. A significant portion of this time is lost to irrelevant news. This project automates the curation process by fetching live news and using Natural Language Processing (NLP) to categorize articles directly into the UPSC Syllabus (GS Papers I, II, III, and IV).

Check out the live dashboard here:https://upsc-current-affairs-intelligence-dashboard.streamlit.app/

🚀 Key Features
1.Smart Categorization: Uses keyword-based NLP to map articles to specific GS Papers (Economy, Polity, Environment, International Relations, etc.).
2.Sentiment Analysis: Analyzes the "Editorial Tone" (Critical vs. Supportive) using TextBlob to help students understand different perspectives on policy issues.
3.Dynamic Filtering: Allows users to focus on specific syllabus areas (e.g., "GS III: Economy") via an interactive sidebar.
4.Aesthetic Visualization: Provides real-time data visualizations of news trends and editorial sentiments.

🛠️ Tech Stack
Language: Python 3.x
Framework: Streamlit (Web UI)
APIs: NewsAPI (Live Data Acquisition)
Libraries: Pandas (Data Transformation), TextBlob (Sentiment Analysis), NLTK (Natural Language Processing)

📊 Data Pipeline Architecture
The system follows a clean modular architecture to ensure stability in a cloud environment:
1.Data Acquisition: Connects to the NewsAPI to fetch the latest 100 global articles based on user focus.
2.Cleaning & Integrity: Removes duplicates, handles missing summaries, and strips API-generated noise.
3.Intelligence Layer: Applies sentiment scoring and multi-tier keyword mapping to categorize unstructured text.
4.UI Controller: Renders interactive charts and a linked data briefing for the end-user.

⚙️ Installation & Setup
To run this project locally:

Clone the repository:

Bash
git clone https://github.com/Simran-Padhi/UPSC-Current-Affairs-Intelligence-Dashboard.git
Install dependencies:

Bash
pip install -r requirements.txt
Set up your API Key:
Create a .streamlit/secrets.toml file and add:

Ini, TOML
NEWS_API_KEY = "f01b108d33af4dbeaee122b566d35892"
Run the app:
Bash
streamlit run app.py
📈 Analytical Insights
During development, a key challenge was handling the ScriptRunContext in cloud environments. I resolved this by decoupling the Data Engine from the UI Controller, ensuring that the application remains stable and responsive during high-frequency API calls.

