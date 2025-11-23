#1.Imports
import os
import uuid          # UNIQUE ID
import json          # Save JSON
import csv           # Save CSV
from datetime import datetime
from dotenv import load_dotenv
from PIL import Image
import streamlit as st
import google.generativeai as genai


#2.Configuration
load_dotenv()  # Load environment variables from .env
genai.configure(api_key=os.getenv("GENAI_API_KEY"))

MODEL_NAME = "models/gemini-2.5-flash"
model = genai.GenerativeModel(MODEL_NAME)


#3.1Functions
def process_image(uploaded_file):
    """Convert a Streamlit uploaded file into a format accepted by Gemini Vision"""
    if uploaded_file is None:
        raise FileNotFoundError("File not uploaded")
    return [{
        "mime_type": uploaded_file.type,
        "data": uploaded_file.getvalue()
    }]


def get_gemini_response(model_instruction, image_data, user_query):
    """Send the image + prompts to Gemini and return response"""
    response = model.generate_content([
        model_instruction,
        image_data[0],
        user_query
    ])
    return response.text


#3.2Saving Functions
def save_to_json(model_instruction, user_query, response_txt):
    """Save extracted data + query into a JSON file"""
    os.makedirs("saved_outputs", exist_ok=True)
    data_id = str(uuid.uuid4())  # unique id for each json

    data = {
        "document_id": data_id,
        "timestamp": datetime.now().isoformat(),
        "model_instruction": model_instruction,
        "input_prompt": user_query,
        "response": response_txt
    }

    file_path = f"saved_outputs/{data_id}.json"

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return file_path


def save_to_csv(model_instruction, user_query, response_txt):
    """Save extracted data + query into a CSV file"""
    os.makedirs("saved_outputs", exist_ok=True)
    file_path = "saved_outputs/responses.csv"

    # Check if file exists to decide whether to write header
    file_exists = os.path.isfile(file_path)

    with open(file_path, "a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["document_id", "timestamp", "model_instruction", "input_prompt", "response"])
        writer.writerow([
            str(uuid.uuid4()),
            datetime.now().isoformat(),
            model_instruction,
            user_query,
            response_txt
        ])

    return file_path


#4.Streamlit UI
def main():
    st.set_page_config(page_title="Gemini Vision")
    st.header("Gemini Vision CV Analyzer")

    st.write("Upload a resume image and ask a question about it.")

    user_query = st.text_input("🔎 Your question:")
    uploaded_file = st.file_uploader("📎 Upload image")

    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img)

    if st.button("Analyse"):
        if not uploaded_file:
            st.error("❗ Please upload a resume image")
            return

        model_instruction = (
            "You are an expert in analyzing CVs. "
            "You will receive an image of a resume and extract details about the person."
        )

        try:
            image_data = process_image(uploaded_file)
            response_txt = get_gemini_response(model_instruction, image_data, user_query)

            st.subheader("Gemini's Response")
            st.write(response_txt)

            # Save files automatically
            json_path = save_to_json(model_instruction, user_query, response_txt)
            csv_path = save_to_csv(model_instruction, user_query, response_txt)

            st.success(f"Saved to JSON ➜ `{json_path}`")
            st.success(f"Saved to CSV ➜ `{csv_path}`")

        except Exception as e:
            st.error(f"Error: {e}")


#5.Run the app
if __name__ == "__main__":
    main()
