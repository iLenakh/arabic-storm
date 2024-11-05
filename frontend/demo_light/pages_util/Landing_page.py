import os
import streamlit as st
from authlib.integrations.requests_client import OAuth2Session

# Google OAuth 2.0 Configuration
GOOGLE_CLIENT_ID = st.secrets["GOOGLE_CLIENT_ID"]
GOOGLE_CLIENT_SECRET = st.secrets["GOOGLE_CLIENT_SECRET"]
REDIRECT_URI = "https://arabic-storm.streamlit.app"

# Function to handle Google login
def google_login():
    oauth = OAuth2Session(
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
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
    # Check if already logged in to avoid re-executing on refresh
    if "logged_in" in st.session_state and st.session_state["logged_in"]:
        return

    # Retrieve authorization code and state from query parameters
    code = st.query_params.get("code")
    state = st.query_params.get("state")

    if not code or state != st.session_state.get("oauth_state"):
        st.error("Authorization failed. Please log in again.")
        return

    # Initialize OAuth session
    oauth = OAuth2Session(
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
    )

    try:
        # Exchange code for token
        token = oauth.fetch_token(
            "https://oauth2.googleapis.com/token",
            code=code,
            client_id=GOOGLE_CLIENT_ID,
            client_secret=GOOGLE_CLIENT_SECRET,
        )

        # Use the token to fetch user information
        user_info = oauth.get("https://www.googleapis.com/oauth2/v1/userinfo").json()
        st.session_state["logged_in"] = True
        st.session_state["user_info"] = user_info
        st.experimental_rerun()

    except Exception as e:
        st.error("An error occurred during the login process. Please try again.")
        st.write(f"Error details: {e}")

# Landing page function
def landing_page():
    st.title("Welcome to the Application")
    st.write("Please log in to continue.")

    # Display Google login button if not logged in
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        google_login()
    else:
        user_info = st.session_state.get("user_info", {})
        st.write(f"Welcome, {user_info.get('name', 'User')}!")
        st.write("You are successfully logged in.")
