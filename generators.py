from abc import ABC, abstractmethod
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from config import Config, SOCIAL_MEDIA_CONFIGS
from interfaces import PostGeneratorInterface
from logger import setup_logger

class PostGenerator(PostGeneratorInterface):
    def __init__(self, llm: ChatOpenAI = None):
        self.llm = llm or ChatOpenAI(model=Config.MODEL_NAME, temperature=Config.TEMPERATURE)
        self.logger = setup_logger(f"{self.__class__.__name__}")
    
    @abstractmethod
    def generate_prompt(self, topic: str) -> str:
        pass
    
    def generate(self, topic: str) -> str:
        self.logger.info(f"Generating post for topic: {topic}")
        prompt = self.generate_prompt(topic)
        response = self.llm.invoke([
            SystemMessage(content=prompt),
            HumanMessage(content=f"Generate post about: {topic}")
        ])
        self.logger.info(f"Post generated successfully for topic: {topic}")
        return response.content

class InstagramGenerator(PostGenerator):
    def generate_prompt(self, topic: str) -> str:
        config = SOCIAL_MEDIA_CONFIGS["instagram"]
        return f"""Create posts in the voice of a holistic homeopathic doctor — compassionate, scientific, and hopeful.
Focus on natural healing, homeopathy, immunity, hormones, mind-body balance, and emotional wellness.
Ensure all content is vegetarian/vegan-friendly, promoting harmony, sunlight, water, sleep, breath, and nature.
Keep the tone poetic yet factual, visually calm (greens, golds, whites), and spiritually uplifting.
Avoid criticism; instead, offer integration, awareness, and empowerment.
Every post should feel warm, wise, and awakening — like medicine for the mind and soul.

Topic: {topic}

Format:
- Subject Line: Create a compelling subject line (5-8 words)
- Poetic opening that connects to nature
- 3-4 gentle healing insights with emojis
- Up to {config.hashtag_limit} relevant hashtags
- Empowering call to action

Start with 'Subject: [your subject line]' then the post content.
Max {config.max_length} characters. Use warm, wise, awakening tone."""

class FacebookGenerator(PostGenerator):
    def generate_prompt(self, topic: str) -> str:
        config = SOCIAL_MEDIA_CONFIGS["facebook"]
        return f"""Create posts in the voice of a holistic homeopathic doctor — compassionate, scientific, and hopeful.
Focus on natural healing, homeopathy, immunity, hormones, mind-body balance, and emotional wellness.
Ensure all content is vegetarian/vegan-friendly, promoting harmony, sunlight, water, sleep, breath, and nature.
Keep the tone poetic yet factual, visually calm (greens, golds, whites), and spiritually uplifting.
Avoid criticism; instead, offer integration, awareness, and empowerment.
Every post should feel warm, wise, and awakening — like medicine for the mind and soul.

Topic: {topic}

Format:
- Subject Line: Create a compelling subject line (5-8 words)
- Gentle, wise opening that connects to nature
- Detailed healing wisdom (2-3 paragraphs)
- Personal healing story or insight
- Up to {config.hashtag_limit} hashtags
- Empowering question for community

Start with 'Subject: [your subject line]' then the post content.
Max {config.max_length} characters. Use compassionate, scientific tone."""

class LinkedInGenerator(PostGenerator):
    def generate_prompt(self, topic: str) -> str:
        config = SOCIAL_MEDIA_CONFIGS["linkedin"]
        return f"""Create posts in the voice of a holistic homeopathic doctor — compassionate, scientific, and hopeful.
Focus on natural healing, homeopathy, immunity, hormones, mind-body balance, and emotional wellness.
Ensure all content is vegetarian/vegan-friendly, promoting harmony, sunlight, water, sleep, breath, and nature.
Keep the tone poetic yet factual, visually calm (greens, golds, whites), and spiritually uplifting.
Avoid criticism; instead, offer integration, awareness, and empowerment.
Every post should feel warm, wise, and awakening — like medicine for the mind and soul.

Topic: {topic}

Format:
- Subject Line: Create a compelling subject line (5-8 words)
- Professional yet poetic opening
- Evidence-based healing wisdom
- Integration with modern wellness
- Up to {config.hashtag_limit} professional hashtags
- Thought-provoking, empowering conclusion

Start with 'Subject: [your subject line]' then the post content.
Max {config.max_length} characters. Use scientific yet spiritual tone."""

class GeneratorFactory:
    @staticmethod
    def create_generator(platform: str) -> PostGenerator:
        generators = {
            "instagram": InstagramGenerator,
            "facebook": FacebookGenerator,
            "linkedin": LinkedInGenerator
        }
        
        if platform not in generators:
            raise ValueError(f"Unsupported platform: {platform}")
        
        return generators[platform]()