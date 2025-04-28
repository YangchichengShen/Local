import streamlit as st
import datetime

st.set_page_config(
    page_title="News in Context",
    page_icon="📰",
)

st.header("News in Context")
c = st.container()
st.write("CCC")
c.write("AAA")
c.write("BBB")

st.sidebar.success("Select a Relevance Ranking:")
datetime.datetime.now()

st.markdown(
    """
    Streamlit is an open-source app framework built specifically for
    Machine Learning and Data Science projects.
    **👈 Select a demo from the sidebar** to see some examples
    of what Streamlit can do!
    ### Want to learn more?
    - Check out [streamlit.io](https://streamlit.io)
    - Jump into our [documentation](https://docs.streamlit.io)
    - Ask a question in our [community
        forums](https://discuss.streamlit.io)
    ### See more complex demos
    - Use a neural net to [analyze the Udacity Self-driving Car Image
        Dataset](https://github.com/streamlit/demo-self-driving)
    - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
"""
)