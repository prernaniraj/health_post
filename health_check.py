from fastapi import HTTPException
import os

def health_check():
    """Basic health check for production monitoring"""
    checks = {
        "openai_key": bool(os.getenv("OPENAI_API_KEY")),
        "app_status": "healthy"
    }
    
    if not checks["openai_key"]:
        raise HTTPException(status_code=503, detail="OpenAI API key not configured")
    
    return checks