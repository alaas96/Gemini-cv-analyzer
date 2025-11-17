#1.Imports
import os

from dotenv import load_dotenv # function that reads file .env and loads the variables inside it  into the system environment
from PIL import Image
import streamlit as st
import google.generativeai as genai


#2.Configuration
load_dotenv() #Load environment variables form .env
genai.configure(api_key=os.getenv("GENAI_API_KEY")) #tells the Library which API to use for requests

MODEL_NAME = "models/gemini-2.5-flash"
model = genai.GenerativeModel(MODEL_NAME) #cretaing object that communicates with the API

#3.Functions
def process_image(uploaded_file):
    """convert a Streamlit uploaded file into a format accepted by Gemini Vision"""
    if uploaded_file is None:
        raise FileNotFoundError("File not uploaded") # Python will immediately stop running
    return [{
        "mime_type": uploaded_file.type,
        "data": uploaded_file.getvalue()
    }]

def get_gemini_response(model_instruction, image_data, user_query):
    """send the image and prompts to Gemini and returns its text response"""
    response = model.generate_content([
        model_instruction,
        image_data[0],
        user_query
    ])
    return response.text

#4.Streamlit UI
def main():
    st.set_page_config(page_title="Gemini Vision")
    st.header("Gemini Vison CV analyser")

    st.write("upload a resume image and ask question.")

    user_query = st.text_input("Your question:")
    uploaded_file = st.file_uploader("Upload image")

    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img)

    if st.button("Analyse"):
        if not uploaded_file:
            st.error("Please upload a resume image")
            return
        model_instruction = (
            "you are an expert in analyzing CVs. "
            "you will receive an image of a resume and extract details about the person"
        )

        try: #test a block of code for errors
            image_data = process_image(uploaded_file)
            response_txt = get_gemini_response(model_instruction, image_data, user_query)
            st.subheader("Gemini´s Response")
            st.write(response_txt)
        except Exception as e: # to do if there is an error
            st.error(f"Error: {e}")

#5.Run the app
if __name__ == "__main__": # the file is safe to import
    main()






