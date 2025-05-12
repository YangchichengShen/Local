# pip install streamlit

import streamlit as st
import json
import os
from reddit_scrape import get_auth_url, auth_and_fetch_user, get_content

from pathlib import Path

st.set_page_config(page_title="Contextify", page_icon="📰")

st.header("Profile")

st.write(
    "Welcome to your Profile! This is the information about you and your interests that your personalized news is built on - take a look and add any that you'd like."
)


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
            <h4 style="margin-top: 0;">Your related interests:</h4>
            <p style="margin: 0.5rem 0;">{interests}</p>
            <h4 style="margin-top: 1rem;">News:</h4>
            <p style="margin: 0.5rem 0;">{news_blurb}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def display_interests():
    st.write(st.session_state.interests)
    label = "Additional Interests (*Optional*)"
    st.write("MAX one interest per submission")

    with st.form(key='interest_form'):
        additional_interest = st.text_input("Additional Interests (*Optional*)")
        submit = st.form_submit_button("Add Interest")
        
        if submit and additional_interest and (additional_interest not in st.session_state.interests):
            st.session_state.interests.append(additional_interest)
            st.success(f"Added: {additional_interest}")
            st.rerun()



 # get root directory
root_dir = Path(__file__).resolve().parent.parent.parent

interests_directory = "outputs"
interest_files = sorted([f for f in os.listdir(interests_directory) if f.startswith("interests")])
path_to_json = os.path.join(interests_directory, interest_files[0])

# Load it
with open(path_to_json, "r", encoding="utf-8") as f:
    interest_json = json.load(f)

# Now you can access interests
interests = interest_json["interests"]

if "interests" not in st.session_state:
    st.session_state.interests = interests

display_interests()

auth_url = get_auth_url()

st.markdown(f"[**Log in with Reddit**]({auth_url})")
params = st.experimental_get_query_params()

if "code" in params:
    code = params["code"][0]
    try:
        user, reddit = auth_and_fetch_user(code)
        st.success(f"Logged in as: {user.name}")

        # Step 3: Fetch submissions
        st.subheader("Your Latest Reddit Submissions:")
        for submission in user.submissions.new(limit=10):
            st.write(f"**{submission.title}** — r/{submission.subreddit}")
            st.write(submission.url)
            st.write("---")
        st.subheader("Subreddits You Belong To:")
        for subreddit in reddit.user.subreddits(limit=20):  # adjust limit as needed
            st.write(f"r/{subreddit.display_name} — {subreddit.title}")

        subs_and_scores = get_content(user, reddit)
        print(subs_and_scores)

    except Exception as e:
        st.error(f"Login failed: {e}")