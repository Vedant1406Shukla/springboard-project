import streamlit as st
import fitz
from PIL import Image
import pytesseract
import io
import google.generativeai as genai
import os

# ----------------------------
# CONFIGURE GEMINI API
# ----------------------------
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

# ----------------------------
# TESSERACT PATH (Windows)
# ----------------------------
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Vedan\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"


# ----------------------------
# OCR FUNCTION
# ----------------------------
def extract_text_from_pdf(pdf_bytes):
    text = ""
    pdf = fitz.open(stream=pdf_bytes, filetype="pdf")

    for page_num, page in enumerate(pdf):
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        page_text = pytesseract.image_to_string(img)
        text += f"\n\n--- PAGE {page_num + 1} ---\n"
        text += page_text

    return text


# ----------------------------
# SUMMARY USING GEMINI
# ----------------------------
def summarize_text(text):
    prompt = f"""
    Summarize the following PDF content accurately and concisely:

    {text}
    """
    response = model.generate_content(prompt)
    return response.text


# ----------------------------
# STREAMLIT UI
# ----------------------------
st.title("AI Research Assistant 📄🤖")

# ======================================================
# 1️⃣ SEARCH BAR FUNCTIONALITY (Independent Prompt Input)
# ======================================================
st.subheader("🔍 Ask Anything (Search Bar / Upload pdf)")

user_query = st.text_input("Enter your question or prompt")

if user_query:
    st.info("Generating response...")
    reply = model.generate_content(user_query)
    st.subheader("💡 Response")
    st.write(reply.text)

st.markdown("---")

# ======================================================
# 2️⃣ PDF UPLOAD + OCR + SUMMARY (Existing Feature)
# ======================================================
st.subheader("📄 Upload PDF for OCR + Summary")

uploaded_pdf = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_pdf is not None:
    st.info("Extracting text using OCR...")

    pdf_bytes = uploaded_pdf.read()
    extracted_text = extract_text_from_pdf(pdf_bytes)

    st.subheader("📌 Extracted Text")
    st.text_area("", extracted_text, height=250)

    if st.button("Generate Summary"):
        st.info("Generating summary using Gemini...")
        summary = summarize_text(extracted_text)

        st.subheader("📘 Summary")
        st.write(summary)
