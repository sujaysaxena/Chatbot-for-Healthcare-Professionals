from backend.database import logs_collection
from datetime import datetime

def log_query(user_id: str, query_type: str, input_content: str, output_content: str, model_used: str = "gpt-4"):
    """
    Logs a user's query into the MongoDB logs collection.
    """
    logs_collection.insert_one({
        "user_id": user_id,                  # Can be user_id (str) or email, depending on your flow
        "query_type": query_type,            # e.g., "text", "image", "pdf"
        "input_summary": input_content,      # what was asked / uploaded
        "response": output_content,          # what LLM responded
        "model_used": model_used,
        "timestamp": datetime.utcnow()
    })
