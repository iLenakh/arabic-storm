import os
import streamlit as st
from authlib.integrations.requests_client import OAuth2Session
from urllib.parse import urlencode

# Google OAuth 2.0 Configuration
GOOGLE_CLIENT_ID = st.secrets["GOOGLE_CLIENT_ID"]
GOOGLE_CLIENT_SECRET = st.secrets["GOOGLE_CLIENT_SECRET"]
REDIRECT_URI = "https://arabic-storm.streamlit.app/?embedded=true" 

# Function to handle Google login
def google_login():
    oauth = OAuth2Session(
        GOOGLE_CLIENT_ID,
        GOOGLE_CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope="openid email profile"
    )
    authorization_url, state = oauth.create_authorization_url(
        "https://accounts.google.com/o/oauth2/auth"
    )
    # Save the state in session_state for security
    st.session_state["oauth_state"] = state
    # Redirect to Google login
    st.write(f"[Click here to log in with Google]({authorization_url})")

# Function to handle Google OAuth response
def handle_google_callback():
    oauth = OAuth2Session(
        GOOGLE_CLIENT_ID,
        GOOGLE_CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
    )
    token = oauth.fetch_token(
        "https://accounts.google.com/o/oauth2/token",
        authorization_response=st.experimental_get_query_params(),
        state=st.session_state["oauth_state"]
    )
    user_info = oauth.get("https://www.googleapis.com/oauth2/v1/userinfo").json()
    st.session_state["logged_in"] = True
    st.session_state["user_info"] = user_info
    st.experimental_rerun()

# Landing page function
def show_landing_page():
    st.title("Welcome to the Application")
    st.write("Please log in to continue.")

    # Display Google login button if not logged in
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        google_login()
    else:
        st.write(f"Welcome, {st.session_state['user_info']['name']}!")