import os
import time
import demo_util
import streamlit as st
from demo_util import DemoFileIOHelper, DemoTextProcessingHelper, DemoUIHelper, truncate_filename

# Set page style and layout adjustments
st.set_page_config(page_title="إنشاء مقال جديد", layout="centered")
st.markdown(
    """
    <style>
        .stButton button {
            font-size: 18px;
            color: white;
            background-color: #4CAF50;
            border-radius: 8px;
            padding: 10px 40px;
            width: 100%; /* Full width for centered alignment */
        }
        .search-input input {
            font-size: 18px;
            padding: 10px;
            width: 100%; /* Full width */
            border: 1px solid #ccc;
            border-radius: 8px;
            margin-bottom: 10px;
        }
        .centered-text {
            text-align: center;
            font-size: 22px;
        }
        .header-text {
            font-size: 26px;
            font-weight: bold;
            text-align: center;
        }
        .description-text {
            font-size: 18px;
            text-align: right;
            color: gray;
        }
    </style>
    """,
    unsafe_allow_html=True
)

def create_new_article_page():
    demo_util.clear_other_page_session_state(page_index=3)

    if "page3_write_article_state" not in st.session_state:
        st.session_state["page3_write_article_state"] = "not started"

    # Page Header
    st.markdown("<div class='header-text'>إنشاء مقال جديد</div>", unsafe_allow_html=True)
    
    if st.session_state["page3_write_article_state"] == "not started":
        # Display instructions above the search box
        st.markdown(
            "<div class='description-text'>يرجى إدخال الموضوع الذي ترغب في التعمق في تعلمه</div>", 
            unsafe_allow_html=True
        )

        # Simplified search form
        with st.form(key='search_form'):
            # Search input with custom styling
            topic_input = st.text_input(
                label='page3_topic',
                placeholder="اكتب موضوع المقال هنا...",
                label_visibility="collapsed",
                key="page3_topic_input"
            )
            # Display the input field styled
            st.markdown(
                f"""
                <div class="search-input">
                    {st.session_state["page3_topic_input"]}
                </div>
                """,
                unsafe_allow_html=True
            )

            submit_button = st.form_submit_button(label="بحث")
            st.session_state["page3_topic"] = topic_input + " (يجب أن تكون المصادر عربية)"
            
            # Handle form submission
            if submit_button:
                if not topic_input.strip():
                    st.warning("لا يمكن ترك الموضوع فارغًا", icon="⚠️")
                else:
                    st.session_state["page3_write_article_state"] = "initiated"
                    st.session_state["page3_topic_name_cleaned"] = topic_input.replace(' ', '_').replace('/', '_')
                    st.session_state["page3_topic_name_truncated"] = truncate_filename(st.session_state["page3_topic_name_cleaned"])

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
