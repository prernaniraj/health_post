from openai import OpenAI
from config import Config
import requests
from io import BytesIO
import os
from datetime import datetime
from interfaces import ImageGeneratorInterface
from logger import setup_logger

class ImageGenerator(ImageGeneratorInterface):
    def __init__(self, client: OpenAI = None):
        self.client = client or OpenAI(api_key=Config.OPENAI_API_KEY)
        self.logger = setup_logger("ImageGenerator")
    
    def generate_image_prompt(self, topic: str, platform: str, subject_line: str = "") -> str:
        """Generate DALL-E prompt for holistic health image"""
        text_overlay = f"Include elegant text overlay with EXACTLY these words '{subject_line}' - spell each letter correctly: {' '.join(list(subject_line))} - in beautiful, readable calming typography. Double-check spelling before rendering." if subject_line else "No text overlay."
        return f"""Create a serene, holistic health image for {topic}. 
        Style: Soft, calming colors (greens, golds, whites), natural elements, 
        peaceful atmosphere, spiritual wellness vibe. 
        Include: nature elements like sunlight, water, plants, peaceful setting.
        {text_overlay}
        CRITICAL: Verify spelling accuracy. Avoid any spelling errors or typos.
        Aesthetic: Minimalist, zen-like, Instagram-worthy for {platform}."""
    
    def generate_image(self, topic: str, platform: str, subject_line: str = "") -> str:
        """Generate image using DALL-E and save locally"""
        try:
            prompt = self.generate_image_prompt(topic, platform, subject_line)
            
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            
            image_url = response.data[0].url
            
            # Download and save image locally
            local_path = self.save_image_locally(image_url, topic, platform)
            return local_path
            
        except Exception as e:
            self.logger.error(f"Image generation error: {str(e)}")
            return None
    
    def save_image_locally(self, image_url: str, topic: str, platform: str) -> str:
        """Download and save image locally with retry logic"""
        try:
            # Retry logic for network issues
            for attempt in range(3):
                try:
                    response = requests.get(image_url, timeout=30)
                    response.raise_for_status()
                    break
                except requests.exceptions.RequestException as e:
                    if attempt == 2:  # Last attempt
                        raise e
                    self.logger.warning(f"Download attempt {attempt + 1} failed, retrying...")
            
            # Create filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).rstrip()[:20]
            filename = f"{platform}_{safe_topic}_{timestamp}.png"
            
            # Ensure images directory exists
            os.makedirs("images", exist_ok=True)
            
            # Save image
            filepath = os.path.join("images", filename)
            with open(filepath, "wb") as f:
                f.write(response.content)
            
            self.logger.info(f"Image saved to: {filepath}")
            return filepath
            
        except Exception as e:
            self.logger.error(f"Image save error: Network connectivity issue - {str(e)}")
            # Return placeholder path for UI
            return "images/placeholder.png"