import os
import json
import numpy as np
import tensorflow as tf
from PIL import Image
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load env variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Correct paths based on your structure
working_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(working_dir)  # Go up one level from /app
model_path = os.path.join(project_root, "trained_model", "plant_disease_prediction_model.h5")
class_indices_path = os.path.join(working_dir, "class_indices.json")

# Load class indices
try:
    with open(class_indices_path) as f:
        class_indices = json.load(f)
except FileNotFoundError:
    st.error("class_indices.json not found! Please check the file path.")
    st.stop()

# Load ML model
@st.cache_resource
def load_model():
    try:
        if not os.path.exists(model_path):
            st.error(f"Model file not found at: {model_path}")
            st.stop()
        model = tf.keras.models.load_model(model_path, compile=False)
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        st.stop()

model = load_model()
model_name = "models/gemini-2.0-flash-lite"

def preprocess_image(image, target_size=(224, 224)):
    img = image.resize(target_size)
    arr = np.array(img).astype('float32') / 255.
    return np.expand_dims(arr, axis=0)

def predict_class(image):
    preds = model.predict(preprocess_image(image))
    idx = np.argmax(preds, axis=1)[0]
    return class_indices[str(idx)]

def get_disease_info(disease):
    prompt = f"""
    Please provide information about the plant disease in precise easy english (dont make the ans too short): **{disease}**

    ### 🌱 Disease Name & Affected Plants
    - Which plants are commonly affected by this disease

    ### 🔍 Disease Cause
    - Pathogen type and scientific name if available

    ### ⚠️ Symptoms
    - Main symptoms observed on plants

    ### 📉 Impact on Crops
    - How this disease affects crop yield and quality

    ### 💊 Prevention & Treatment
    - Recommended treatment and preventive measures
    """
    try:
        gemini = genai.GenerativeModel(model_name)
        return gemini.generate_content(prompt).text
    except Exception as e:
        return f"Error: {e}"

def get_disease_answer(disease, question):
    prompt = f"""
    You are an expert plant pathologist. Answer the following question about the plant disease "{disease}":
    
    Question: {question}
    
    Provide answer focusing specifically on this disease.
    """
    try:
        gemini = genai.GenerativeModel(model_name)
        return gemini.generate_content(prompt).text
    except Exception as e:
        return f"Error generating answer: {e}"

# UI
st.title("🌿 Plant Disease Identifier")
st.write("Upload a diseased plant leaf to detect the disease and get info.")

uploaded = st.file_uploader("Upload image...", type=["jpg","jpeg","png"])

if uploaded:
    image = Image.open(uploaded)

    st.subheader("Uploaded Image")
    st.image(image.resize((250, 250)))

    if st.button("🔎 Identify Disease"):
        with st.spinner("Analyzing..."):
            disease = predict_class(image)
            st.session_state.detected_disease = disease
            st.success(f"Detected: {disease}")

        with st.spinner("Fetching information..."):
            info = get_disease_info(disease)
            st.markdown(info)

    if hasattr(st.session_state, 'detected_disease'):
        st.subheader("Ask a Question")
        q = st.text_input(f"Ask about {st.session_state.detected_disease}:")
        
        if st.button("Get Answer") and q:
            with st.spinner("Generating answer..."):
                answer = get_disease_answer(st.session_state.detected_disease, q)
                st.markdown("**Answer:**")
                st.markdown(answer)

st.markdown("---")
st.caption("🔬 Powered by Computer Vision & Generative AI for smarter farming.")
