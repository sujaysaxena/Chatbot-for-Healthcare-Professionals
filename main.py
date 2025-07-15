from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi import Query
from backend.database import logs_collection
from backend.auth import register_user, login_user, decode_access_token
from backend.models.user_model import LoginRequest
from backend.models.log_model import log_query
from backend.pdf_handler import process_pdf
from backend.image_handler import analyze_medical_image
from backend.text_handler import process_text_rag
from backend.utils import save_upload_file
from pydantic import EmailStr
import os

app = FastAPI()

# CORS to allow frontend (Streamlit)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------
# AUTH ROUTES
# --------------------------

@app.post("/register")
def register(email: EmailStr = Form(...), password: str = Form(...)):
    success, message = register_user(email, password)
    if not success:
        raise HTTPException(status_code=400, detail=message)
    return {"message": message}

@app.post("/login")
def login(email: EmailStr = Form(...), password: str = Form(...)):
    success, token_or_msg = login_user(email, password)
    if not success:
        raise HTTPException(status_code=401, detail=token_or_msg)
    return {"access_token": token_or_msg}

# --------------------------
# AUTH VALIDATION
# --------------------------

def get_current_user(token: str = Form(...)):
    user_id = decode_access_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return user_id

# --------------------------
# PDF Upload Handler
# --------------------------

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...), token: str = Form(...)):
    user_id = get_current_user(token)

    path = await save_upload_file(file)
    response = process_pdf(path)
    os.remove(path)

    log_query(user_id, "pdf", f"PDF: {file.filename}", response)
    return {"response": response}

# --------------------------
# Image Upload Handler (OCR + BLIP)
# --------------------------

@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...), token: str = Form(...)):
    user_id = get_current_user(token)

    result = await analyze_medical_image(file)

    log_query(user_id, "image", result["summary_input"], result["response"])
    return {"response": result["response"]}

# --------------------------
# Text RAG Query Handler
# --------------------------

@app.post("/query-text-rag")
def query_text_rag(query: str = Form(...), token: str = Form(...)):
    user_id = get_current_user(token)

    response = process_text_rag(query)

    log_query(user_id, "text", query, response)
    return {"response": response}

# --------------------------
# User History 
# --------------------------

@app.post("/history")
def get_user_history(token: str = Form(...), limit: int = Form(10)):
    user_id = decode_access_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Fetch logs for the user from MongoDB
    history = logs_collection.find({"user_id": user_id}).sort("timestamp", -1).limit(limit)

    results = []
    for entry in history:
        question = entry.get("input", "")
        response = entry.get("output", "")
        results.append((question, response))

    return {"history": results}

# --------------------------
# Health Check Route
# --------------------------

@app.get("/")
def root():
    return {"message": "✅ Multimodal Medical Assistant backend is running"}
