import streamlit as st
import json
import os
from reddit_scrape import get_auth_url, auth_and_fetch_user, get_content, save_interests_from_reddit

# --- PAGE CONFIG ---
st.set_page_config(page_title="User Profile", page_icon="👤", layout="wide")

# --- TOP NAVBAR ---
st.markdown("<h1 style='margin-bottom: 0;'>👤 User Profile</h1>", unsafe_allow_html=True)
st.markdown("Use the menu on the left side to navigate to your News Feed")

# --- Intro Text ---
st.write(
    "Welcome to your Profile! This is the information about you and your interests that your personalized news is built on — take a look and add any that you'd like."
)

# --- Interest Storage ---
interests_directory = "outputs"
os.makedirs("outputs", exist_ok=True)
interest_files = sorted([f for f in os.listdir(interests_directory) if f.startswith("interests")])
if not interest_files:
    default_path = os.path.join(interests_directory, "interests.json")
    with open(default_path, "w", encoding="utf-8") as f:
        json.dump({"interests": []}, f)
    interest_files = ["interests.json"]
path_to_json = os.path.join(interests_directory, interest_files[0])

# Load interests
with open(path_to_json, "r", encoding="utf-8") as f:
    interest_json = json.load(f)
interests = interest_json["interests"]

# Session state
if "interests" not in st.session_state:
    st.session_state.interests = interests
if "selected_interest" not in st.session_state:
    st.session_state.selected_interest = None

# --- STYLE ---
st.markdown("""
    <style>
    .interest-tag {
        display: inline-block;
        background-color: #e0f7fa;
        color: #00796b;
        padding: 6px 10px;
        border-radius: 12px;
        font-size: 14px;
        margin: 5px 5px 5px 0;
    }
    .reddit-card {
        background-color: white;
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        overflow: hidden;
        margin-bottom: 20px;
        padding: 15px;
    }
    .reddit-card h4 {
        margin-top: 0;
    }
    </style>
""", unsafe_allow_html=True)

# --- Display Interests ---
st.subheader("🎯 Your Current Interests")
if st.session_state.interests:
    st.markdown("".join([f'<span class="interest-tag">{i}</span>' for i in st.session_state.interests]), unsafe_allow_html=True)
else:
    st.info("No interests added yet! Use the form below to add some.")

# --- Add Interests Form ---
st.subheader("➕ Add Additional Interests")
st.write("*(One interest per submission)*")

with st.form(key='add_interest_form'):
    additional_interest = st.text_input("New Interest")
    submit_add = st.form_submit_button("Add Interest")
    
    if submit_add and additional_interest:
        if additional_interest not in st.session_state.interests:
            st.session_state.interests.append(additional_interest)
            # Save to file
            with open(path_to_json, "w", encoding="utf-8") as f:
                json.dump({"interests": st.session_state.interests}, f, ensure_ascii=False, indent=2)
            st.success(f"Added: {additional_interest}")
            st.rerun()
        else:
            st.warning(f"'{additional_interest}' is already in your interests.")

# --- Remove Interests Form ---
st.subheader("➖ Remove Interests")
st.write("*(One interest per submission)*")

with st.form(key='remove_interest_form'):
    remove_interest = st.text_input("Interest to Remove")
    submit_remove = st.form_submit_button("Remove Interest")
    
    if submit_remove and remove_interest:
        if remove_interest in st.session_state.interests:
            st.session_state.interests.remove(remove_interest)
            # Save to file
            with open(path_to_json, "w", encoding="utf-8") as f:
                json.dump({"interests": st.session_state.interests}, f, ensure_ascii=False, indent=2)
            st.success(f"Removed: {remove_interest}")
            st.rerun()
        else:
            st.warning(f"'{remove_interest}' was not found in your interests.")

# --- Reddit Auth ---
st.subheader("🔗 Connect with Reddit")
auth_url = get_auth_url()

# Styled Reddit login button
st.markdown(f"""
    <a href="{auth_url}" style="
        display: inline-block;
        background-color: #FF5700;
        color: white;
        font-size: 16px;
        font-weight: bold;
        padding: 10px 16px;
        border-radius: 8px;
        text-decoration: none;
        margin-top: 10px;
    ">Log in with Reddit</a>
""", unsafe_allow_html=True)

# --- Handle Reddit OAuth ---
params = st.query_params

if "code" in params:
    code = params["code"][0]
    try:
        user, reddit = auth_and_fetch_user(code)
        st.success(f"✅ Reddit login successful!")

        # Save Reddit-based interests
        save_interests_from_reddit(user, reddit)

        # Reload interests
        with open(path_to_json, "r", encoding="utf-8") as f:
            interest_json = json.load(f)
        st.session_state.interests = interest_json["interests"]

        st.rerun()

    except Exception as e:
        st.error(f"Login failed: {e}")

# If user is already logged in and content is available:
if "code" in params:
    # Reload user and reddit
    try:
        user, reddit = auth_and_fetch_user(params["code"][0])

        st.subheader("📄 Your Latest Reddit Submissions")
        for submission in user.submissions.new(limit=10):
            st.markdown(f"""
                <div class="reddit-card">
                    <h4>{submission.title}</h4>
                    <p><strong>Subreddit:</strong> r/{submission.subreddit}</p>
                    <p><a href="{submission.url}" target="_blank">View Post</a></p>
                </div>
            """, unsafe_allow_html=True)

        st.subheader("👥 Subreddits You Belong To")
        for subreddit in reddit.user.subreddits(limit=20):
            st.markdown(f"""
                <div class="reddit-card">
                    <h4>r/{subreddit.display_name}</h4>
                    <p>{subreddit.title}</p>
                </div>
            """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error loading Reddit data: {e}")