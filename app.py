# Install necessary libraries
# !pip install requests streamlit textwrap

# Import libraries
import streamlit as st
import requests
import textwrap

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

# Function to split the text into smaller chunks
def split_text_into_chunks(text, max_length=1024):
    return textwrap.wrap(text, max_length)

# Function to summarize large documents (100 pages)
def summarize_large_document(document_text):
    chunks = split_text_into_chunks(document_text)
    summarized_text = ""

    for i, chunk in enumerate(chunks):
        summary = summarize_text(chunk)
        summarized_text += summary + " "

    return summarized_text

# Streamlit app
st.title("Document Summarizer")
st.write("Upload a large document and get a summarized version.")

uploaded_file = st.file_uploader("Upload your file", type=["txt"])

if uploaded_file is not None:
    # Read the uploaded file
    document_text = uploaded_file.read().decode("utf-8")

    # Summarize the document
    with st.spinner("Summarizing your document. Please wait..."):
        final_summary = summarize_large_document(document_text)

    # Display the summary
    st.subheader("Summarized Text:")
    st.text_area("", final_summary, height=400)

st.caption("Powered by Hugging Face API and Streamlit")
