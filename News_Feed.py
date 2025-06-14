import streamlit as st
import datetime
import json
import os
from news_contextify import get_contextified_news

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="News in Context",
    page_icon="📰",
    layout="wide",
)

# --- TOP NAVBAR ---
st.markdown("<h1 style='margin-bottom: 0;'>📰 News in Context</h1>", unsafe_allow_html=True)
st.markdown("Use the menu on the left side to navigate to your User Profile")

st.info("**Disclaimer:** Connections between news and your interests are generated by AI and may not always be accurate.")

# --- LOAD INTERESTS ---
interests_directory = "outputs"
interest_files = sorted([f for f in os.listdir(interests_directory) if f.startswith("interests")])
if interest_files:
    path_to_json = os.path.join(interests_directory, interest_files[0])
    with open(path_to_json, 'r', encoding='utf-8') as file:
        interests_json = json.load(file)
        interests = interests_json["interests"]
else:
    st.error("No interests files found in directory.")
    interests = []

# --- GET CONTEXTIFIED NEWS ---
interests_dict_str = get_contextified_news()

if interests_dict_str.startswith("```json"):
    interests_dict_str = interests_dict_str.strip("`").strip()
    first_newline = interests_dict_str.find('\n')
    interests_dict_str = interests_dict_str[first_newline + 1:]
    interests_dict_str = interests_dict_str.strip()
    if interests_dict_str.endswith("```"):
        interests_dict_str = interests_dict_str[:-3].strip()

interests_dict = json.loads(interests_dict_str)

# --- LOAD NewsAPI ARTICLES ---
news_json_path = os.path.join("outputs", "news.json")
if os.path.exists(news_json_path):
    with open(news_json_path, "r", encoding='utf-8') as f:
        news_api_raw = json.load(f)
        news_api_articles = news_api_raw.get("articles", [])
else:
    st.error("No news.json file found in outputs directory.")
    news_api_articles = []

# --- MAP NewsAPI ARTICLES by title ---
news_api_lookup = {
    article["title"]: article
    for article in news_api_articles
    if article.get("title")
}

# --- STYLE ---
st.markdown("""
    <style>
    .news-card {
        background-color: white;
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        overflow: hidden;
        margin-bottom: 20px;
        transition: transform 0.2s;
    }
    .news-card:hover {
        transform: scale(1.02);
    }
    .news-image {
        width: 100%;
        height: 200px;
        object-fit: cover;
    }
    .news-content {
        padding: 15px;
    }
    .interest-tag {
        display: inline-block;
        background-color: #e0f7fa;
        color: #00796b;
        padding: 4px 8px;
        border-radius: 12px;
        font-size: 12px;
        margin-right: 5px;
        margin-bottom: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# --- NEWS FEED ---
st.markdown("## 🗞️ Your Personalized News Feed")

cols = st.columns(3)

# --- LOOP through Contextified News ---
for idx, (article_title, content) in enumerate(interests_dict.items()):
    article = news_api_lookup.get(article_title)

    if not article:
        st.warning(f"⚠️ No matching NewsAPI article found for: '{article_title}' — skipping.")
        continue  # skip if no matching article

    # Extract from NewsAPI
    url = article.get("url", "#")
    image_url = article.get("urlToImage") or f"https://source.unsplash.com/400x300/?news"
    title = article.get("title", article_title)

    # Extract from Gemini result
    summary = content.get("summary", "")
    matched_interests = content.get("interests", [])

    # Render card
    with cols[idx % 3]:
        st.markdown(f"""
            <div class="news-card">
                <img src="{image_url}" class="news-image" alt="news image">
                <div class="news-content">
                    <h4 style="margin-top:0;">
                        <a href="{url}" target="_blank" style="text-decoration: none; color: #1a73e8;">
                            {title}
                        </a>
                    </h4>
                    <div>
                        {" ".join(f'<span class="interest-tag">{i}</span>' for i in matched_interests)}
                    </div>
                    <p style="margin-top: 10px; font-size: 15px; color: #333;">{summary}</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
