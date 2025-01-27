# Install necessary libraries
!pip install requests PyPDF2 streamlit

# Import libraries
import streamlit as st
import requests
import textwrap
from PyPDF2 import PdfReader

# Set Hugging Face API Key
API_KEY = "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"  # Replace with your API key
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": f"Bearer {API_KEY}"}

# Function to summarize the text
def summarize_text(text):
    payload = {"inputs": text}
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()[0]["summary_text"]
    else:
        return f"Error: {response.status_code}, {response.text}"

# Function to split the text into larger chunks
def split_text_into_chunks(text, max_length=5000):  # Increase chunk size
    return textwrap.wrap(text, max_length)

# Function to summarize large documents
def summarize_large_document(document_text):
    chunks = split_text_into_chunks(document_text)
    summarized_text = ""

    for i, chunk in enumerate(chunks):
        try:
            summary = summarize_text(chunk)
            summarized_text += f"Chunk {i+1} Summary:\n{summary}\n\n"
        except Exception as e:
            summarized_text += f"Error summarizing chunk {i+1}: {str(e)}\n\n"

    return summarized_text

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Streamlit app
st.title("PDF Summarizer")
st.write("Upload a PDF document to get a summarized version.")

# File upload section
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    document_text = extract_text_from_pdf(uploaded_file)
    if len(document_text) > 1_000_000:  # Warn for extremely large documents
        st.warning("This document is too large and may take a long time to summarize.")
    else:
        final_summary = summarize_large_document(document_text)
        st.subheader("Summary")
        st.text(final_summary)
