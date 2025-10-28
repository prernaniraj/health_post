import os
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class SocialMediaConfig:
    max_length: int
    hashtag_limit: int
    format_style: str

SOCIAL_MEDIA_CONFIGS = {
    "instagram": SocialMediaConfig(
        max_length=2200,
        hashtag_limit=30,
        format_style="visual_storytelling"
    ),
    "facebook": SocialMediaConfig(
        max_length=63206,
        hashtag_limit=10,
        format_style="conversational"
    ),
    "linkedin": SocialMediaConfig(
        max_length=3000,
        hashtag_limit=5,
        format_style="professional"
    )
}

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    MODEL_NAME = "gpt-3.5-turbo"
    TEMPERATURE = 0.7
    
    @classmethod
    def validate_api_key(cls) -> bool:
        return bool(cls.OPENAI_API_KEY and cls.OPENAI_API_KEY != "your_openai_api_key_here")