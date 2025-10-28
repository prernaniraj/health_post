from abc import ABC, abstractmethod
from typing import Optional

class PostGeneratorInterface(ABC):
    @abstractmethod
    def generate(self, topic: str) -> str:
        pass

class EmailServiceInterface(ABC):
    @abstractmethod
    def send_post_email(self, post_content: str, topic: str, platform: str, 
                       subject_line: str = "", image_url: str = None, 
                       recipient_email: str = "pn5513580972@gmail.com") -> bool:
        pass

class ImageGeneratorInterface(ABC):
    @abstractmethod
    def generate_image(self, topic: str, platform: str, subject_line: str = "") -> Optional[str]:
        pass

class TrendingTopicsInterface(ABC):
    @abstractmethod
    def get_trending_topics(self) -> list:
        pass