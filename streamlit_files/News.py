import streamlit as st
import datetime

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
interests = "Swimming"
news_blurb = "The 29-year-old cleared the World Aquatics ‘A’ standard of 22.05 needed for Singapore, hitting the 2nd-best time of his career in the process. The veteran’s lifetime best remains at the 21.90 put up at last year’s European Championships as the 4th-place finisher."
news_box(interests, news_blurb)
news_box(interests, news_blurb)
news_box(interests, news_blurb)
news_box(interests, news_blurb)
news_box(interests, news_blurb)
news_box(interests, news_blurb)
news_box(interests, news_blurb)
news_box(interests, news_blurb)