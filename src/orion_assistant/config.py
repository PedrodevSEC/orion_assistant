import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configurações globais do Orion Assistant."""
    
    # Modelos e APIs
    MODEL = os.getenv("MODEL")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    