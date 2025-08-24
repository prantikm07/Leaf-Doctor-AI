import streamlit as st

def apply_custom_css():
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 1.5rem 0;
        background: linear-gradient(90deg, #e8f5e8, #f0f8f0);
        border-radius: 10px;
        margin-bottom: 1.5rem;
    }
    
    .disease-result {
        background: linear-gradient(90deg, #e8f5e8, #f0f8f0); 
        padding: 1.2rem;
        border-radius: 10px;
        border-left: 5px solid #2E8B57;
        margin: 1rem 0;
    }
    
    .expert-answer {
        background: #e3f2fd;
        padding: 1.2rem;
        border-radius: 8px;
        border-left: 4px solid #2196f3;
        margin: 1rem 0;
        max-height: 400px;
        overflow-y: auto;
    }
    
    .info-box {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    
    .footer {
        text-align: center;
        padding: 2rem;
        color: #666;
        margin-top: 3rem;
    }
    
    /* Fix image sizing */
    .stImage > div {
        max-width: 280px !important;
    }
    
    /* Better column balance */
    .main-content {
        gap: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

def format_disease_name(disease_name):
    formatted = disease_name.replace('___', ' - ').replace('_', ' ')
    
    words = formatted.split()
    formatted_words = []
    for word in words:
        if word == '-':
            formatted_words.append(word)
        else:
            formatted_words.append(word.capitalize())
    
    return ' '.join(formatted_words)

def render_header():
    st.markdown("""
    <div class='main-header'>
        <h1 style='color: #2E8B57; margin-bottom: 0; font-size: 2rem;'>🌿 Plant Disease Identifier</h1>
        <p style='color: #666; font-size: 1rem; margin-top: 0.3rem;'>
            AI-powered disease detection and expert guidance
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar():
    with st.sidebar:
        st.markdown("### 📋 How to Use")
        st.markdown("""
        1. **Upload** a leaf image
        2. **Click** Identify Disease
        3. **Review** diagnosis
        4. **Ask** questions
        """)
        
        st.markdown("### 💡 Tips")
        st.markdown("""
        - Good lighting
        - Clear leaf focus
        - Visible symptoms
        """)
        
        if st.session_state.get('detected_disease'):
            st.markdown("### 🔬 Current Detection")
            formatted_name = format_disease_name(st.session_state.detected_disease)
            st.info(f"**{formatted_name}**")
            if st.session_state.get('confidence'):
                st.progress(st.session_state.confidence)
                st.caption(f"Confidence: {st.session_state.confidence:.1%}")

def render_disease_result(disease, confidence):
    formatted_name = format_disease_name(disease)
    st.markdown(f"""
    <div class='disease-result'>
        <h3 style='color: #2E8B57; margin-top: 0; font-size: 1.3rem;'>🦠 Detected Disease</h3>
        <h2 style='color: #1f4e32; margin: 0.3rem 0; font-size: 1.5rem;'>{formatted_name}</h2>
        <p style='color: #666; margin-bottom: 0; font-size: 0.9rem;'>
            Confidence: <strong>{confidence:.1%}</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_compact_image_upload():
    st.markdown("### 📸 Upload Image")
    uploaded = st.file_uploader(
        "Choose a plant leaf image", 
        type=["jpg", "jpeg", "png"],
        help="Clear image of diseased leaf"
    )
    return uploaded

def render_compact_image_display(image, filename):
    st.markdown("**🖼️ Uploaded**")
    # Smaller, fixed-size image
    st.image(
        image.resize((280, 280)), 
        caption=filename,
        width=280
    )

def render_waiting_state():
    st.markdown("""
    <div style='text-align: center; padding: 2rem; color: #888;'>
        <h4>🔍 Ready to Analyze</h4>
        <p>Upload a plant image to start</p>
    </div>
    """, unsafe_allow_html=True)

def render_expert_answer(answer):
    st.markdown("### 💡 Expert Answer:")
    formatted_answer = answer.replace('\n', '<br>')
    st.markdown(f"""
    <div class='expert-answer'>
        {formatted_answer}
    </div>
    """, unsafe_allow_html=True)

def render_footer():
    st.markdown("---")
    st.markdown("""
    <div class='footer'>
        <h4 style='color: #2E8B57; margin-bottom: 0.5rem;'>🔬 Leaf Doctor AI</h4>
        <p style='margin: 0;'>Powered by AI | Helping farmers worldwide 🌍</p>
    </div>
    """, unsafe_allow_html=True)
