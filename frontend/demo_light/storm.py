import os
import sys
import streamlit as st
from streamlit_option_menu import option_menu

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import demo_util
from pages_util import MyArticles, CreateNewArticle, landing_page, handle_google_callback

# Main application function
def main_app():
    # Application logic remains the same as previously discussed
    pass

# Main entry point
def main():
    # If the user is not logged in, redirect to landing page with Google login
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        if "code" in st.experimental_get_query_params():
            handle_google_callback()
        else:
            landing_page.show_landing_page()
    else:
        main_app()

if __name__ == "__main__":
    main()
