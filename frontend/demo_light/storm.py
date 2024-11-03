import os
import sys
import streamlit as st
from streamlit_option_menu import option_menu

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import demo_util
from pages_util import MyArticles, CreateNewArticle, Landing_page
import pages_util.Landing_page as Landing_page  

# Main application function
def main_app():
    global database
    st.set_page_config(layout='wide')

    # First-time setup
    if "first_run" not in st.session_state:
        st.session_state['first_run'] = True

    # Set API keys from secrets
    if st.session_state['first_run']:
        for key, value in st.secrets.items():
            if type(value) == str:
                os.environ[key] = value

    # Initialize session state variables
    if "selected_article_index" not in st.session_state:
        st.session_state["selected_article_index"] = 0
    if "selected_page" not in st.session_state:
        st.session_state["selected_page"] = 0
    if st.session_state.get("rerun_requested", False):
        st.session_state["rerun_requested"] = False
        st.rerun()

    st.write('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)
    
    # Navigation menu
    menu_container = st.container()
    with menu_container:
        pages = ["مقالات سابقة", "إنشاء مقال جديد"]
        menu_selection = option_menu(
            None, pages,
            icons=['house', 'search'],
            menu_icon="cast", default_index=0, orientation="horizontal",
            manual_select=st.session_state.selected_page,
            styles={
                "container": {"padding": "0.2rem 0", "background-color": "#101FED00"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "center",
                    "margin": "0px",
                    "padding": "10px",
                },
                "nav-link-selected": {
                    "background-color": "#15636FFF",
                    "color": "white"
                },
            },
            key='menu_selection'
        )
        if st.session_state.get("manual_selection_override", False):
            menu_selection = pages[st.session_state["selected_page"]]
            st.session_state["manual_selection_override"] = False
            st.session_state["selected_page"] = None

        # Page routing based on selection
        if menu_selection == "مقالات سابقة":
            demo_util.clear_other_page_session_state(page_index=2)
            MyArticles.my_articles_page()
        elif menu_selection == "إنشاء مقال جديد":
            demo_util.clear_other_page_session_state(page_index=3)
            CreateNewArticle.create_new_article_page()

# Main entry point
def main():
     # If the user is not logged in, redirect to landing page with Google login
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        if "code" in st.experimental_get_query_params():
            Landing_page.handle_google_callback()
        else:
            Landing_page.landing_page()
    else:
        main_app()

if __name__ == "__main__":
    main()