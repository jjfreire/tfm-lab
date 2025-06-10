import os
from dotenv import load_dotenv

# Automatically load backend/.env
dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path)
