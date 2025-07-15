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

## 🔒 MongoDB Atlas Setup (for Auth & Logging)

---
