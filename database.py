from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get MongoDB connection string from .env
MONGO_DB_URL = os.getenv("MONGO_DB_URL")

# Connect to MongoDB Atlas
client = AsyncIOMotorClient(MONGO_DB_URL)
db = client.student_management
