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

# Paths
working_dir = os.path.dirname(os.path.abspath(__file__))
model_path = f"{working_dir}/trained_model/plant_disease_prediction_model.h5"
with open(f"{working_dir}/class_indices.json") as f:
    class_indices = json.load(f)

# Load ML model
model = tf.keras.models.load_model(model_path)
model_name = "models/gemini-2.0-flash-lite"

# Image preprocessing
def preprocess_image(image, target_size=(224, 224)):
    img = image.resize(target_size)
    arr = np.array(img).astype('float32') / 255.
    return np.expand_dims(arr, axis=0)

# Predict class
def predict_class(image):
    preds = model.predict(preprocess_image(image))
    idx = np.argmax(preds, axis=1)[0]
    return class_indices[str(idx)]

# Get disease info from Gemini
def get_disease_info(disease):
    prompt = f"""
    বাংলায় সহজভাবে ব্যাখ্যা করুন গাছের রোগ: **{disease}**

    ### 🌱 রোগের নাম ও প্রভাবিত গাছপালা
    - কোন গাছে এ রোগ হয়

    ### 🔍 রোগের কারণ
    - প্যাথোজেন ও বৈজ্ঞানিক নাম

    ### ⚠️ লক্ষণ
    - প্রধান উপসর্গ

    ### 📉 ফসলের উপর প্রভাব
    - ফলন হ্রাস

    ### 💊 প্রতিরোধ ও চিকিৎসা
    - করণীয় পদক্ষেপ
    """
    try:
        gemini = genai.GenerativeModel(model_name)
        return gemini.generate_content(prompt).text
    except Exception as e:
        return f"Error: {e}"

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
            st.success(f"Detected: {disease}")

        with st.spinner("Fetching information..."):
            info = get_disease_info(disease)
            st.markdown(info)

        st.subheader("Ask a Question")
        q = st.text_input("Type your question about this disease:")
        if q and st.button("Get Answer"):
            try:
                gemini = genai.GenerativeModel(model_name)
                resp = gemini.generate_content(f"Disease: {disease}\nQuestion: {q}")
                st.markdown("**Answer:**")
                st.markdown(resp.text)
            except Exception as e:
                st.error(f"Error: {e}")

st.markdown("---")
st.caption("🔬 Powered by Computer Vision & Generative AI for smarter farming.")
