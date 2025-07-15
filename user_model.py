# backend/models/user_model.py

from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# ----- User Registration -----
class User(BaseModel):
    name: str
    email: EmailStr
    password: str  # In production: hashed password

# ----- Login Request -----
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# ----- Query Logging -----
class QueryLog(BaseModel):
    user_email: EmailStr
    query_type: str  # e.g., "text", "image", "pdf", "llava"
    input_summary: Optional[str] = None
    model_used: Optional[str] = "gpt-4"
    response: str
    timestamp: datetime = datetime.utcnow()