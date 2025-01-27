# Install necessary libraries
!pip install requests streamlit PyPDF2

# Import libraries
import requests
import textwrap
from PyPDF2 import PdfReader
import streamlit as st

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

# Streamlit user interface
def main():
    st.title("PDF Summarizer")
    st.markdown("Upload a large PDF (up to 200 pages) and get a summarized version.")
    
    # File uploader
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None:
        # Display the file name
        st.write(f"Processing file: {uploaded_file.name}")
        
        # Extract text from PDF
        document_text = extract_text_from_pdf(uploaded_file)

        # Check if the document is too large
        if len(document_text) > 1_000_000:  # Rough estimate for very large PDFs
            st.warning("This document is very large and may take a while to process.")
        
        # Summarize the document
        final_summary = summarize_large_document(document_text)
        
        # Display the summary
        st.text_area("Summarized Text", final_summary, height=400)

# Run the Streamlit app
if __name__ == "__main__":
    main()
