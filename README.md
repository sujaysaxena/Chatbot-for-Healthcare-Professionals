# Chatbot for Health Professionals
# 🩺 AI-Powered Multimodal Medical Assistant Chatbot

An intelligent assistant designed for healthcare professionals and patients, this chatbot leverages OCR, image captioning, PDF summarization, and RAG-based conversational retrieval to answer queries from multimodal medical documents (images, PDFs, text). Securely deployed with FastAPI backend, MongoDB authentication, and a sleek Streamlit frontend.

---

## 🚀 Project Objective

To build a scalable and secure AI-powered assistant that can understand and answer medical queries across:
- 📄 PDF medical reports
- 🖼️ Medical image scans
- ✍️ Free-text user prompts

It streamlines decision support and enhances patient engagement using LLMs and Retrieval-Augmented Generation (RAG) techniques.

---

## 🧩 Problem Statement

Healthcare professionals often need to extract relevant insights from unstructured data such as medical PDFs, scanned reports, or handwritten notes. Manually going through each document can be time-consuming and error-prone.

This project solves:
- Difficulty in extracting context from multimodal medical documents.
- Lack of integrated, AI-assisted tools for querying across PDFs, text, and images.
- Limited accessibility and non-scalable deployment methods in healthcare AI solutions.

---

## 🛠️ Tech Stack

| Layer         | Technology                                  |
|---------------|---------------------------------------------|
| Backend       | FastAPI, Python, Pydantic                   |
| LLM & RAG     | OpenAI GPT-4, LangChain, FAISS              |
| Image Handling| Tesseract OCR, BLIP                         |
| PDF Parsing   | PyMuPDF, LangChain PDF loader               |
| Frontend      | Streamlit (with upload & chat interface)    |
| Auth & Logs   | MongoDB Atlas, JWT                          |
| Deployment    | Docker, Uvicorn, HTTPS-ready                |

---

## 🔍 Features

✅ **User Authentication**: JWT-secured login/register endpoints via FastAPI  
✅ **Text Querying**: Chat-based interface with RAG-powered answers  
✅ **PDF Upload**: Summarize and query medical PDFs using FAISS  
✅ **Image Upload**: Extract insights from medical scans via OCR and BLIP  
✅ **History Tracking**: Retrieve previous queries and responses  
✅ **Secure APIs**: All endpoints protected via token-based auth  
✅ **Streamlit Frontend**: Unified multimodal upload & interaction panel  

---

## 🔒 MongoDB Atlas Setup (for Auth & Logging)
Ensure .env or system environment variable contains:
MONGO_URI = mongodb+srv://<username>:<password>@cluster0.mongodb.net/

---

## 💻 Local Setup

### Clone the repository
git clone https://github.com/your_username/medical-assistant-chatbot.git
cd medical-assistant-chatbot

### Install dependencies
conda create -n medichat python=3.10
conda activate medichat
pip install -r requirements.txt

### Start FastAPI backend
uvicorn main:app --reload

### Launch Streamlit frontend
streamlit run frontend/streamlit_app.py

---

## 🧪 Testing
Test each endpoint with curl or Postman

Validate:

  - Registration/login flow

  - Upload PDF and get summary

  - Upload image and get response

  -  Submit text query and retrieve knowledge

  - Verify MongoDB users and query_logs collections

---

## 🏗️ System Architecture

```plaintext
User ↔ Streamlit UI ↔ FastAPI Backend ↔ MongoDB Atlas
                                 ↕
              ┌────────────── Image Handler (OCR + Captioning)
              │
              ├────────────── PDF Handler (RAG Summary)
              │
              └────────────── Text Handler (RAG Query on FAISS)

---
