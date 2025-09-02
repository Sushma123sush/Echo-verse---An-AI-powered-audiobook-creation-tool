import streamlit as st
from gtts import gTTS
import pdfplumber
import docx
import os

# Function to read PDF
def read_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

# Function to read DOCX
def read_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

# Convert text to speech
def convert_to_audio(text, filename="audiobook.mp3"):
    tts = gTTS(text=text, lang="en")
    tts.save(filename)
    return filename

# Streamlit UI
st.title("📖 Echo Verse - AI Audiobook Creator")

uploaded_file = st.file_uploader("Upload your document (PDF/DOCX/TXT)", type=["pdf", "docx", "txt"])

if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        content = read_pdf(uploaded_file)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        content = read_docx(uploaded_file)
    else:  # TXT
        content = uploaded_file.read().decode("utf-8")

    st.text_area("📜 Extracted Text", content[:1000] + "..." if len(content) > 1000 else content, height=200)

    if st.button("🎧 Convert to Audiobook"):
        audio_file = convert_to_audio(content)
        st.audio(audio_file, format="audio/mp3")
        st.success("✅ Audiobook generated successfully!")
        st.download_button("⬇ Download Audiobook", open(audio_file, "rb"), file_name="audiobook.mp3")
