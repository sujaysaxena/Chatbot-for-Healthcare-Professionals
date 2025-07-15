from dotenv import load_dotenv
load_dotenv()

import os
from pymongo import MongoClient

# Fail fast if MONGO_URI is not set
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("❌ MONGO_URI environment variable not set. Please set it in your .env file.")

client = MongoClient(MONGO_URI)
db = client["medical_bot"]

users_collection = db["users"]
logs_collection = db["query_logs"]
