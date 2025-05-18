import streamlit as st

st.set_page_config(page_title="paisapan")

st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1470&q=80");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    .css-18e3th9 {
        background-color: transparent;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Testing Background Image")
st.write("If you don't see the background image, your Streamlit version or CSS class might be different.")
