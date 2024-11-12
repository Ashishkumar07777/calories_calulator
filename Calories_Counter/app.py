from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Load all environment variables
load_dotenv()

# Configure Google Generative AI with the new model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Updated function to load Google Gemini 1.5 Flash model and get a response
def get_gemini_response(input_text, image, prompt):
    # Use the updated model 'gemini-1.5-flash'
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_text, image[0], prompt])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize Streamlit app
st.set_page_config(page_title=" Calories Calculator")

st.header("calories calculator")
user_input = st.text_input("Input Prompt:", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Display the uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

submit = st.button("Analyze Image and Get Calorie Information")

# Updated prompt for the new model
input_prompt = """
You are an AI assistant that helps analyze food items in the uploaded image. 
Please list out the items you recognize and provide an estimate of their calorie content. 
Do not offer any health or dietary advice, and always suggest consulting a qualified professional for personalized guidance.

1. Item 1 - Estimated calories
2. Item 2 - Estimated calories
---
"""

# If submit button is clicked
if submit and uploaded_file:
    image_data = input_image_setup(uploaded_file)
    try:
        # Get the response using the updated model
        response = get_gemini_response(user_input, image_data, input_prompt)
        st.subheader("Response:")
        st.write(response)

        # Add a disclaimer message
        st.markdown("""
        **Disclaimer**: The calorie information provided is an estimate based on the image recognition model. For personalized dietary advice, please consult a registered dietitian or nutritionist.
        """)
    except Exception as e:
        st.error(f"Error fetching response: {e}")
