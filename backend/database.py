import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")

client = MongoClient(mongo_uri)
db = client["chatbot"]
collection = db["users"]

# 🔹 Create index for faster queries (runs safely if already exists)
collection.create_index("user_id")

def get_history(user_id, limit=10):
    chats = collection.find(
        {"user_id": user_id}
    ).sort("timestamp", -1).limit(limit)

    history = []

    for chat in reversed(list(chats)):
        history.append((chat["role"], chat["message"]))

    return history
