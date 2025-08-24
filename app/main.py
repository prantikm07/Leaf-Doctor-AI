import streamlit as st
from PIL import Image
from model_utils import (
    load_class_indices, 
    load_tf_model, 
    predict_disease, 
    get_disease_info, 
    get_disease_answer
)
from ui_components import (
    apply_custom_css,
    render_header,
    render_sidebar,
    render_disease_result,
    render_compact_image_upload,
    render_compact_image_display,
    render_waiting_state,
    render_footer,
    format_disease_name
)

st.set_page_config(
    page_title="Plant Disease Identifier",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_custom_css()

if 'detected_disease' not in st.session_state:
    st.session_state.detected_disease = None
if 'disease_info' not in st.session_state:
    st.session_state.disease_info = None
if 'confidence' not in st.session_state:
    st.session_state.confidence = None

class_indices = load_class_indices()
model = load_tf_model()

render_header()
render_sidebar()

col1, col2, col3 = st.columns([2, 1, 2], gap="large")

with col1:
    uploaded = render_compact_image_upload()
    
    if uploaded:
        image = Image.open(uploaded)
        render_compact_image_display(image, uploaded.name)
        
        if st.button("Identify Disease", type="primary", use_container_width=True):
            with st.spinner("Analyzing..."):
                disease, confidence = predict_disease(model, image, class_indices)
                st.session_state.detected_disease = disease
                st.session_state.confidence = confidence
            
            st.success("Analysis Complete!")
            st.rerun()

with col2:
    st.write("")

with col3:
    st.markdown("### Diagnosis Results")
    
    if st.session_state.detected_disease:
        render_disease_result(st.session_state.detected_disease, st.session_state.confidence)
        
        if not st.session_state.disease_info:
            with st.spinner("Getting info..."):
                st.session_state.disease_info = get_disease_info(st.session_state.detected_disease)
        
        col3a, col3b = st.columns(2)
        with col3a:
            if st.button("Full Info", use_container_width=True):
                st.session_state.show_info = True
                st.rerun()
        
        with col3b:
            if st.button("New Analysis", use_container_width=True):
                for key in ['detected_disease', 'disease_info', 'confidence', 'show_info']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
    else:
        render_waiting_state()

if st.session_state.disease_info and st.session_state.get('show_info', False):
    st.markdown("---")
    st.markdown("### Disease Information")
    with st.expander("Full Report", expanded=True):
        st.markdown(st.session_state.disease_info)

if st.session_state.detected_disease:
    st.markdown("---")
    
    qa_col1, qa_col2 = st.columns([2, 3], gap="large")
    
    with qa_col1:
        st.markdown("### Ask Kris AI")
        formatted_name = format_disease_name(st.session_state.detected_disease)
        
        st.markdown(f"""
        <div style='background: #f8f9fa; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;'>
            <h4 style='margin: 0; color: #495057; font-size: 1rem;'>Ask about: {formatted_name}</h4>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("question_form", clear_on_submit=True):
            question = st.text_area(
                "Your Question:",
                placeholder="How to treat this disease?",
                height=100
            )
            submit_btn = st.form_submit_button("Get Answer", type="secondary", use_container_width=True)
    
    with qa_col2:
        st.markdown("### Kris AI Response")
        
        if submit_btn and question.strip():
            with st.spinner("Consulting expert..."):
                answer = get_disease_answer(st.session_state.detected_disease, question)
            st.session_state.latest_answer = answer
        
        if hasattr(st.session_state, 'latest_answer'):
            html_answer = st.session_state.latest_answer.replace('\n', '<br>')
            st.markdown(f"""
            <div style='background: ##070024; padding: 1.2rem; border-radius: 8px; 
                        border-left: 4px solid #2196f3; max-height: 300px; overflow-y: auto;'>
                {html_answer}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='text-align: center; padding: 2rem; color: #888;'>
                <p>Ask a question to get expert advice</p>
            </div>
            """, unsafe_allow_html=True)

render_footer()
