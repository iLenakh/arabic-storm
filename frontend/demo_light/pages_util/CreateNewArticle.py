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
            padding: 10px 20px;
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

    st.markdown("<div class='header-text'>إنشاء مقال جديد</div>", unsafe_allow_html=True)
    
    if st.session_state["page3_write_article_state"] == "not started":
        _, search_form_column, _ = st.columns([2, 6, 2])
        
        with search_form_column:
            st.markdown(
                "<div class='description-text'>يرجى إدخال الموضوع الذي ترغب في التعمق في تعلمه</div>", 
                unsafe_allow_html=True
            )
            
            with st.form(key='search_form'):
                # Text input for the search topic
                topic_input = st.text_input(
                    label='page3_topic',
                    placeholder="اكتب موضوع المقال هنا...",
                    label_visibility="collapsed"
                )
                
                st.session_state["page3_topic"] = topic_input + " (يجب أن تكون المصادر عربية)"
                pass_appropriateness_check = True

                # Submit button for the form
                submit_button = st.form_submit_button(label="بحث")
                if submit_button and st.session_state["page3_write_article_state"] in ["not started", "show results"]:
                    if not st.session_state["page3_topic"].strip():
                        pass_appropriateness_check = False
                        st.session_state["page3_warning_message"] = "لا يمكن ترك الموضوع فارغًا"
                    
                    st.session_state["page3_topic_name_cleaned"] = st.session_state["page3_topic"].replace(' ', '_').replace('/', '_')
                    st.session_state["page3_topic_name_truncated"] = truncate_filename(st.session_state["page3_topic_name_cleaned"])
                    
                    if not pass_appropriateness_check:
                        st.session_state["page3_write_article_state"] = "not started"
                        st.warning(st.session_state["page3_warning_message"], icon="⚠️")
                    else:
                        st.session_state["page3_write_article_state"] = "initiated"

    if st.session_state["page3_write_article_state"] == "initiated":
        current_working_dir = os.path.join(demo_util.get_demo_dir(), "DEMO_WORKING_DIR")
        if not os.path.exists(current_working_dir):
            os.makedirs(current_working_dir)

        if "runner" not in st.session_state:
            demo_util.set_storm_runner()
        
        st.session_state["page3_current_working_dir"] = current_working_dir
        st.session_state["page3_write_article_state"] = "pre_writing"

    if st.session_state["page3_write_article_state"] == "pre_writing":
        st.markdown("<div class='centered-text'>يتم الآن جمع المعلومات حول الموضوع... الرجاء الانتظار لبضع دقائق.</div>", unsafe_allow_html=True)
        st_callback_handler = demo_util.StreamlitCallbackHandler()
        
        # Perform research and generate outline
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
        st.markdown("<div class='centered-text'>الرجاء الانتظار، يتم الآن إنشاء المقال...</div>", unsafe_allow_html=True)
        
        # Generate the article content
        st.session_state["runner"].run(
            topic=st.session_state["page3_topic"],
            do_research=False,
            do_generate_outline=False,
            do_generate_article=True,
            do_polish_article=False,
            remove_duplicate=False
        )
        
        st.session_state["page3_write_article_state"] = "prepare_to_show_result"

    if st.session_state["page3_write_article_state"] == "prepare_to_show_result":
        st.markdown("<div class='centered-text'>تم الانتهاء من جمع المعلومات. يمكنك الآن عرض المقال.</div>", unsafe_allow_html=True)
        if st.button("عرض المقال النهائي"):
            st.session_state["page3_write_article_state"] = "completed"
            st.experimental_rerun()

    if st.session_state["page3_write_article_state"] == "completed":
        # Display polished article
        current_working_dir_paths = DemoFileIOHelper.read_structure_to_dict(st.session_state["page3_current_working_dir"])
        current_article_file_path_dict = current_working_dir_paths[st.session_state["page3_topic_name_truncated"]]
        
        demo_util.display_article_page(
            selected_article_name=st.session_state["page3_topic_name_cleaned"],
            selected_article_file_path_dict=current_article_file_path_dict,
            show_title=True,
            show_main_article=True
        )
