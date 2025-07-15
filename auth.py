from backend.database import users_collection
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from bson import ObjectId
import os

# Hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT setup
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"

# ------------------------------
# Utility Functions
# ------------------------------

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# ------------------------------
# Token Management
# ------------------------------

def create_access_token(user_id: str) -> str:
    to_encode = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(hours=12)
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")  # user_id
    except JWTError:
        return None

# ------------------------------
# Auth Workflows
# ------------------------------

def register_user(email: str, password: str):
    if users_collection.find_one({"email": email}):
        return False, "User already exists"

    hashed = hash_password(password)
    users_collection.insert_one({
        "email": email,
        "password": hashed
    })
    return True, "User registered successfully"

def login_user(email: str, password: str):
    user = users_collection.find_one({"email": email})
    if not user or not verify_password(password, user["password"]):
        return False, "Invalid credentials"

    token = create_access_token(user_id=str(user["_id"]))
    return True, token
