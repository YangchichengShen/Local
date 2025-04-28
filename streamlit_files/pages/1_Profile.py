import streamlit as st
import json
import os

st.set_page_config(page_title="Contextify", page_icon="📰")

st.markdown("# Profile")
st.sidebar.header("Profile")
st.markdown("*Hi, Shraeya Iyer!*")
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


# Get the directory of the *current* Python file
#base_dir = os.path.dirname(__file__)

# Now correctly join paths relative to this file
#path_to_json = os.path.abspath(os.path.join(base_dir, "..", "..", "..", "interests", "interests_20250428_171726.json"))

# Path to your output JSON (adjust depending on your folder structure)
#path_to_json = "../../interests_outputs/interests_20250428_171726.json"
            
path_to_json = "/Users/shraeyaiyer/Desktop/cs338/Local/interests_outputs/interests_20250428_171726.json"

# Load it
with open(path_to_json, "r", encoding="utf-8") as f:
    interest_json = json.load(f)

# Now you can access interests
interests = interest_json["interests"]

if "interests" not in st.session_state:
    st.session_state.interests = interests

display_interests()
