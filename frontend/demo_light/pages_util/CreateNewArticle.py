import os
import time
import demo_util
import streamlit as st
from demo_util import DemoFileIOHelper, DemoTextProcessingHelper, DemoUIHelper, truncate_filename

# Set page configuration
st.set_page_config(page_title="إنشاء مقال جديد", layout="centered")

def create_new_article_page():
    demo_util.clear_other_page_session_state(page_index=3)

    if "page3_write_article_state" not in st.session_state:
        st.session_state["page3_write_article_state"] = "not started"

    # Page Header
    st.markdown(
        "<h1 style='font-size: 26px; font-weight: bold; text-align: center; margin-bottom: 20px;'>إنشاء مقال جديد</h1>",
        unsafe_allow_html=True
    )
    
    if st.session_state["page3_write_article_state"] == "not started":
        # Display instructions above the search box
        st.markdown(
            "<p style='font-size: 18px; text-align: right; color: gray; margin-bottom: 10px;'>يرجى إدخال الموضوع الذي ترغب في التعمق في تعلمه</p>", 
            unsafe_allow_html=True
        )

        # Custom style for centering the text input and button
        st.markdown("""
            <style>
                /* Center both the input field and button */
                .center-container {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    flex-direction: column;
                    width: 100%;
                }

                /* Style the custom text input */
                .custom-input {
                    width: 70%;  /* Full width */
                    padding: 12px;
                    font-size: 16px;
                    border: 2px solid #ddd;
                    border-radius: 8px;
                    margin-bottom: 20px;
                    box-sizing: border-box;  /* Ensure padding does not affect the width */
                    transition: border-color 0.3s ease;
                    text-align: center;  /* Center text inside input */
                }

                .custom-input:focus {
                    border-color: #4CAF50;
                    outline: none;
                }

                /* Custom button style */
                .custom-button {
                    display: inline-block;
                    padding: 12px 24px;
                    font-size: 16px;
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    cursor: pointer;
                    text-align: center;
                    width: 70%;
                    margin-top: 20px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                    transition: background-color 0.3s ease, box-shadow 0.3s ease;
                }

                .custom-button:hover {
                    background-color: #45a049;
                    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
                }

                /* Hide the default Streamlit text input field */
                .streamlit-expanderHeader {
                    display: none;
                }
            </style>
        """, unsafe_allow_html=True)

        # Container to center input and button
        st.markdown('<div class="center-container">', unsafe_allow_html=True)

        # Custom HTML input field
        topic_input = st.text_input(
            label="",
            key="page3_topic_input",
            placeholder="أدخل الموضوع هنا",
            max_chars=200
        )

        # Apply custom style to the input field
        st.markdown(f"""
            <style>
                #{st.session_state['page3_topic_input']} {{
                    font-size: 16px;
                    padding: 12px;
                    width: 70%;
                    border: 2px solid #ddd;
                    border-radius: 8px;
                    text-align: center;
                    transition: border-color 0.3s ease;
                }}
                #{st.session_state['page3_topic_input']}:focus {{
                    border-color: #4CAF50;
                    outline: none;
                }}
            </style>
        """, unsafe_allow_html=True)

        # Submit button with custom style
        if st.button("بحث"):
            st.session_state["page3_topic"] = topic_input + " (يجب أن تكون المصادر عربية)"
            
            if not topic_input.strip():
                st.warning("لا يمكن ترك الموضوع فارغًا", icon="⚠️")
            else:
                st.session_state["page3_write_article_state"] = "initiated"
                st.session_state["page3_topic_name_cleaned"] = topic_input.replace(' ', '_').replace('/', '_')
                st.session_state["page3_topic_name_truncated"] = truncate_filename(st.session_state["page3_topic_name_cleaned"])

        # Closing container div
        st.markdown('</div>', unsafe_allow_html=True)

    # Handle states for writing articles (same logic as before)

    if st.session_state["page3_write_article_state"] == "initiated":
        current_working_dir = os.path.join(demo_util.get_demo_dir(), "DEMO_WORKING_DIR")
        if not os.path.exists(current_working_dir):
            os.makedirs(current_working_dir)

        if "runner" not in st.session_state:
            demo_util.set_storm_runner()
        st.session_state["page3_current_working_dir"] = current_working_dir
        st.session_state["page3_write_article_state"] = "pre_writing"

    if st.session_state["page3_write_article_state"] == "pre_writing":
        st.write("أنا الآن أبحث في الموضوع. الرجاء الانتظار، هذه العملية قد تستغرق 2-3 دقائق.")
        st_callback_handler = demo_util.StreamlitCallbackHandler()
        with st.spinner("جاري البحث عن المعلومات..."):
            st.session_state["runner"].run(
                topic=st.session_state["page3_topic"],
                do_research=True,
                do_generate_outline=True,
                do_generate_article=False,
                do_polish_article=False,
                callback_handler=st_callback_handler
            )
            st.session_state["page3_write_article_state"] = "final_writing"

    if st.session_state["page3_write_article_state"] == "final_writing":
        with st.spinner("جاري إنشاء المقال النهائي... الرجاء الانتظار."):
            st.session_state["runner"].run(
                topic=st.session_state["page3_topic"], 
                do_research=False,
                do_generate_outline=False,
                do_generate_article=True, 
                do_polish_article=True, 
                remove_duplicate=False
            )
            st.session_state["runner"].post_run()
            st.session_state["page3_write_article_state"] = "prepare_to_show_result"

    if st.session_state["page3_write_article_state"] == "prepare_to_show_result":
        if st.button("عرض المقال النهائي"):
            st.session_state["page3_write_article_state"] = "completed"
            st.experimental_rerun()

    if st.session_state["page3_write_article_state"] == "completed":
        current_working_dir_paths = DemoFileIOHelper.read_structure_to_dict(st.session_state["page3_current_working_dir"])
        current_article_file_path_dict = current_working_dir_paths[st.session_state["page3_topic_name_truncated"]]
        demo_util.display_article_page(
            selected_article_name=st.session_state["page3_topic_name_cleaned"],
            selected_article_file_path_dict=current_article_file_path_dict,
            show_title=True, 
            show_main_article=True
        )
