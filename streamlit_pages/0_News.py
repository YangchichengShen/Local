import streamlit as st
import datetime
import json

from news_contextify import get_contextified_news

st.set_page_config(
    page_title="News in Context",
    page_icon="📰",
)

st.header("News in Context")

def news_box(interests, news_blurb):
    st.markdown(
        f"""
        <div style="
            background-color: #e6f2ff;
            padding: 1.5rem;
            border-radius: 15px;
            border: 1px solid #b3d9ff;
            margin-bottom: 1rem;
        ">
            <h5 style="margin-top: 0;">Your related interests:</h5>
            <p style="margin: 0.5rem 0;">{interests}</p>
            <h5 style="margin-top: 1rem;">News:</h5>
            <p style="margin: 0.5rem 0;">{news_blurb}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
# Gathered from database as a list of interests, currently just as a list of strings from a dummy file.
# Get and read file from interests_outputs using relative path
path_to_json = "interests_outputs/interests_20250428_171726.json"
with open(path_to_json, 'r', encoding='utf-8') as file:
    interests_json = json.load(file)
    interests = interests_json["interests"]

interests_dict_str = get_contextified_news()  # This is already a dict
print("Interests JSON:", interests_json)
print("Raw string:", repr(interests_dict_str))

if interests_dict_str.startswith("```json"):
    interests_dict_str = interests_dict_str.strip("`").strip()
    first_newline = interests_dict_str.find('\n')
    interests_dict_str = interests_dict_str[first_newline + 1:]  # strip first line
    interests_dict_str = interests_dict_str.strip()
    if interests_dict_str.endswith("```"):
        interests_dict_str = interests_dict_str[:-3].strip()

interests_dict = json.loads(interests_dict_str)

for interest, news_blurb in interests_dict.items():
    news_box(interest, news_blurb)