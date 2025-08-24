# 🌿 Leaf-Doctor-AI

AI-powered plant disease identification system that combines computer vision and generative AI to help farmers diagnose plant diseases and get expert treatment recommendations.

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-red)
![TensorFlow](https://img.shields.io/badge/ML-TensorFlow-orange)

## Features

- **Disease Detection**: Upload leaf images for instant AI diagnosis
- **Expert Kris AI**: Ask specific questions about detected diseases
- **Detailed Information**: Get comprehensive disease descriptions and treatments
- **Confidence Scoring**: View prediction accuracy levels
- **Responsive UI**: Works on desktop, tablet, and mobile

## Quick Start

1. **Clone and install**
   ```
   git clone https://github.com/prantikm07/Leaf-Doctor-AI.git
   cd leaf-doctor-ai
   pip install -r app/requirements.txt
   ```

2. **Setup API key**
   Create `.env` file:
   ```
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

3. **Run**
   ```
   streamlit run app/main.py
   ```

4. **Open** http://localhost:8501

## Project Structure

```
├── app/
│   ├── main.py              # Main Streamlit app
│   ├── model_utils.py       # ML utilities
│   ├── ui_components.py     # UI components
│   └── requirements.txt     # Dependencies
├── trained_model/
│   └── plant_disease_prediction_model.h5  # CNN model (574MB)
├── test_images/            # Sample images
└── .env                    # Environment variables
```

## Tech Stack

- **Frontend**: Streamlit, HTML, CSS
- **ML**: TensorFlow 2.13.0 (CNN model)
- **AI**: Google Gemini API
- **Image Processing**: Pillow
- **Python**: 3.10+

## Usage

1. Upload a clear leaf image (JPG, PNG)
2. Click "Identify Disease"
3. View diagnosis results and confidence score
4. Get detailed disease information
5. Ask expert questions for treatment advice

## Model Info

- **Type**: Convolutional Neural Network
- **Size**: 574MB
- **Input**: 224x224 RGB images
- **Output**: Disease classification with confidence

## API Requirements

Get your free Gemini API key from [Google AI Studio](https://aistudio.google.com/) and add it to your `.env` file.


## Contact

If you have any questions, feel free to contact me via:
- Email: [prantik25m@gmail.com](mailto:prantik25m@gmail.com)
- LinkedIn: [Prantik Mukhopadhyay](https://www.linkedin.com/in/prantikm07/)
