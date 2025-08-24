import os
import json
import numpy as np
import tensorflow as tf
from PIL import Image
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY")) #type:ignore

# Model configuration
MODEL_NAME = "models/gemini-2.0-flash-lite"

def get_paths():
    working_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(working_dir)
    model_path = os.path.join(project_root, "trained_model", "plant_disease_prediction_model.h5")
    class_indices_path = os.path.join(working_dir, "class_indices.json")
    return model_path, class_indices_path

@st.cache_data
def load_class_indices():
    _, class_indices_path = get_paths()
    try:
        with open(class_indices_path) as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("class_indices.json not found! Please check the file path.")
        st.stop()

@st.cache_resource
def load_tf_model():
    model_path, _ = get_paths()
    try:
        if not os.path.exists(model_path):
            st.error(f"Model file not found at: {model_path}")
            st.stop()
        return tf.keras.models.load_model(model_path, compile=False) #type:ignore
    except Exception as e:
        st.error(f"Error loading model: {e}")
        st.stop()

def preprocess_image(image, target_size=(224, 224)):
    img = image.resize(target_size)
    arr = np.array(img).astype('float32') / 255.
    return np.expand_dims(arr, axis=0)

def predict_disease(model, image, class_indices):
    preprocessed = preprocess_image(image)
    preds = model.predict(preprocessed, verbose=0)
    idx = np.argmax(preds, axis=1)[0]
    confidence = float(np.max(preds))
    disease = class_indices[str(idx)]
    return disease, confidence

def get_disease_info(disease):
    prompt = f"""
    Please provide information about the plant disease in precise easy english: **{disease}**

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
        gemini = genai.GenerativeModel(MODEL_NAME) #type:ignore
        return gemini.generate_content(prompt).text
    except Exception as e:
        return f"Error: {e}"

def get_disease_answer(disease, question):
    prompt = f"""
    You are an expert plant pathologist. Answer the following question about the plant disease "{disease}":
    
    Question: {question}
    
    Provide a accurate answer focusing specifically on this disease. Don't use markdown.
    """
    try:
        gemini = genai.GenerativeModel(MODEL_NAME) #type:ignore
        return gemini.generate_content(prompt).text
    except Exception as e:
        return f"Error generating answer: {e}"
