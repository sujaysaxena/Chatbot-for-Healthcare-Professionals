import streamlit as st
import requests
from PIL import Image
import io

API_URL = "http://localhost:8000"  # Replace with your server URL

# ----------------------
# Session Initialization
# ----------------------
if "history" not in st.session_state:
    st.session_state.history = []
if "theme" not in st.session_state:
    st.session_state.theme = "light"
if "token" not in st.session_state:
    st.session_state.token = None
if "user_email" not in st.session_state:
    st.session_state.user_email = None

# ----------------------
# Theme Toggle
# ----------------------
with st.sidebar:
    theme_choice = st.radio("🌗 Theme Mode", ["light", "dark"], index=(0 if st.session_state.theme == "light" else 1))
    st.session_state.theme = theme_choice

if st.session_state.theme == "dark":
    st.markdown("""
    <style>
        body, .stApp {
            background-color: #0e1117;
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)

# ----------------------
# Page Title
# ----------------------
st.set_page_config(page_title="🧠 Multimodal Medical Assistant", layout="centered")
st.title("🧠 Multimodal Medical Assistant")
st.markdown("Upload **PDFs**, **Images**, or type a **question** to get AI-powered medical insights.")

# ----------------------
# Auth (Login/Register)
# ----------------------
st.sidebar.markdown("---")
st.sidebar.subheader("🔐 Authentication")

auth_mode = st.sidebar.radio("Select Mode", ["Login", "Register"])
email = st.sidebar.text_input("📧 Email")
password = st.sidebar.text_input("🔑 Password", type="password")

if st.sidebar.button("Submit"):
    if not email or not password:
        st.sidebar.warning("Enter both email and password.")
    else:
        try:
            data = {"email": email, "password": password}
            endpoint = "/login" if auth_mode == "Login" else "/register"
            resp = requests.post(f"{API_URL}{endpoint}", data=data)
            if resp.status_code == 200:
                if auth_mode == "Login":
                    token = resp.json().get("access_token")
                    st.session_state.token = token
                    st.session_state.user_email = email
                    st.sidebar.success("Login successful ✅")

                    # ✅ Fetch persistent chat history
                    hist_resp = requests.post(f"{API_URL}/history", data={
                        "token": token,
                        "limit": 10
                    })
                    if hist_resp.status_code == 200:
                        st.session_state.history = hist_resp.json().get("history", [])
                else:
                    st.sidebar.success("Registered successfully. You can now log in.")
            else:
                st.sidebar.error(resp.json().get("detail", "Authentication failed."))
        except Exception as e:
            st.sidebar.error("Error connecting to backend.")

# ----------------------
# Main UI (if logged in)
# ----------------------
if st.session_state.token:
    st.sidebar.markdown("---")
    st.sidebar.success(f"Logged in as: {st.session_state.user_email}")
    if st.sidebar.button("Logout"):
        st.session_state.token = None
        st.session_state.user_email = None
        st.session_state.history = []

    pdf_file = st.sidebar.file_uploader("📎 Upload PDF", type=["pdf"], help="Upload lab report or prescription")
    image_file = st.sidebar.file_uploader("🖼️ Upload Image", type=["jpg", "jpeg", "png"], help="Upload scan or rash photo")

    st.sidebar.markdown("---")
    st.sidebar.subheader("🕓 Chat History")
    if st.session_state.history:
        for i, (q, r) in enumerate(reversed(st.session_state.history)):
            with st.sidebar.expander(f"Q: {q[:30]}..."):
                st.markdown(f"{r}")

    user_query = st.text_input("💬 Ask a medical question (optional)", placeholder="e.g. What does this report say?")

    if image_file:
        st.image(image_file, caption="Uploaded Image", use_column_width=True)
    if pdf_file:
        st.markdown(f"**Uploaded PDF:** `{pdf_file.name}`")

    if st.button("🔍 Analyze & Search"):
        if not any([pdf_file, image_file, user_query]):
            st.warning("Please upload a file or ask a question.")
        else:
            with st.spinner("Processing..."):
                results = []
                token_data = {"token": st.session_state.token}

                # Handle PDF
                if pdf_file:
                    files = {"file": (pdf_file.name, pdf_file, pdf_file.type)}
                    resp = requests.post(f"{API_URL}/upload-pdf", files=files, data=token_data)
                    if resp.status_code == 200:
                        response = resp.json().get("response")
                        results.append(("📄 PDF Summary", response))
                        st.session_state.history.append((f"PDF: {pdf_file.name}", response))

                # Handle Image + Text
                if image_file and user_query:
                    files = {"file": (image_file.name, image_file, image_file.type)}
                    data = {"question": user_query, "token": st.session_state.token}
                    resp = requests.post(f"{API_URL}/upload-image", files=files, data=data)
                    if resp.status_code == 200:
                        response = resp.json().get("response")
                        results.append(("🖼️ Image + Q&A (BLIP/OCR)", response))
                        st.session_state.history.append((user_query, response))

                # Handle Image Only
                elif image_file:
                    files = {"file": (image_file.name, image_file, image_file.type)}
                    resp = requests.post(f"{API_URL}/upload-image", files=files, data=token_data)
                    if resp.status_code == 200:
                        response = resp.json().get("response")
                        results.append(("🧠 Image Summary", response))
                        st.session_state.history.append(("Image Summary", response))

                # Handle Text Only
                elif user_query:
                    data = {"query": user_query, "token": st.session_state.token}
                    resp = requests.post(f"{API_URL}/query-text-rag", data=data)
                    if resp.status_code == 200:
                        response = resp.json().get("response")
                        results.append(("📚 RAG Answer", response))
                        st.session_state.history.append((user_query, response))

                # Show results
                if results:
                    for title, res in results:
                        st.subheader(title)
                        st.success(res)
                else:
                    st.error("Something went wrong.")

# ----------------------
# Button Styling
# ----------------------
st.markdown("""
<style>
    .stButton button {
        border-radius: 10px;
        font-weight: 600;
        background-color: #008cba;
        color: white;
        padding: 0.6em 1.2em;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("---\n👨‍⚕️ *This assistant is not a substitute for professional medical advice.*")
