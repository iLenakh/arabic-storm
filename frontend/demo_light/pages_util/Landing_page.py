import os
import streamlit as st
from authlib.integrations.requests_client import OAuth2Session

# Google OAuth 2.0 Configuration
GOOGLE_CLIENT_ID = st.secrets["GOOGLE_CLIENT_ID"]
GOOGLE_CLIENT_SECRET = st.secrets["GOOGLE_CLIENT_SECRET"]
REDIRECT_URI = "https://arabic-storm.streamlit.app/?embedded=true" 

# Function to initiate Google login
def show_landing_page():
    st.title("Welcome to the Application")
    st.write("Please log in to continue.")
    google_login()

def google_login():
    oauth = OAuth2Session(
        GOOGLE_CLIENT_ID,
        GOOGLE_CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope="openid email profile"
    )
    
    # Generate authorization URL and state
    authorization_url, state = oauth.create_authorization_url(
        "https://accounts.google.com/o/oauth2/auth"
    )
    
    # Store the state in session_state
    st.session_state["oauth_state"] = state
    st.write(f"[Click here to log in with Google]({authorization_url})")

# Function to handle Google OAuth response
def handle_google_callback():
    # Get query parameters
    query_params = st.experimental_get_query_params()
    
    # Log query parameters for debugging
    st.write("Query Parameters:", query_params)

    code = query_params.get("code", [None])[0]  # Get code or None
    state = query_params.get("state", [None])[0]  # Get state or None

    # Log the state for debugging
    st.write("Received state:", state)
    st.write("Stored oauth_state:", st.session_state.get("oauth_state"))

    if not code or not state:
        st.error("Authorization failed or missing parameters.")
        return
    
    # Check if 'oauth_state' matches
    stored_state = st.session_state.get("oauth_state")
    if stored_state is None or stored_state != state:
        st.error("Invalid state parameter. Please log in again.")
        return

    # Initialize OAuth client
    oauth = OAuth2Session(
        GOOGLE_CLIENT_ID,
        GOOGLE_CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
    )
    
    try:
        # Fetch the token using the authorization code
        token = oauth.fetch_token(
            "https://accounts.google.com/o/oauth2/token",
            code=code,
            client_secret=GOOGLE_CLIENT_SECRET
        )
        
        # Fetch user info
        user_info = oauth.get("https://www.googleapis.com/oauth2/v1/userinfo").json()
        st.session_state["logged_in"] = True
        st.session_state["user_info"] = user_info
        st.session_state.pop("oauth_state", None)  # Clear the oauth_state

        # Redirect to the main application
        st.experimental_rerun()

    except Exception as e:
        st.error(f"Authentication failed: {e}")
        st.session_state.pop("oauth_state", None)  # Clear oauth_state on error
        st.experimental_rerun()
