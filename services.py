from typing import Optional
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from models import PostRequest, PostResponse
from generators import GeneratorFactory
from config import Config
from logger import setup_logger

class TopicAnalyzer:
    def __init__(self, llm: ChatOpenAI = None):
        self.llm = llm or ChatOpenAI(model=Config.MODEL_NAME, temperature=0.3)
        self.logger = setup_logger("TopicAnalyzer")
    
    def extract_topic(self, user_input: str) -> str:
        system_msg = SystemMessage(content="""Extract the main holistic health topic focusing on natural healing, homeopathy, immunity, hormones, mind-body balance, and emotional wellness. 
        Return only the topic name (e.g., 'natural stress relief', 'immune harmony', 'hormonal balance').""")
        
        response = self.llm.invoke([system_msg, HumanMessage(content=user_input)])
        return response.content.strip()

class PostService:
    def __init__(self, topic_analyzer: TopicAnalyzer = None):
        self.topic_analyzer = topic_analyzer or TopicAnalyzer()
        self.logger = setup_logger("PostService")
    
    def generate_post(self, request: PostRequest) -> PostResponse:
        try:
            # Check API key
            if not Config.OPENAI_API_KEY or Config.OPENAI_API_KEY == "your_openai_api_key_here":
                raise ValueError("OpenAI API key not configured")
            
            # Extract topic if needed
            topic = self.topic_analyzer.extract_topic(request.topic)
            
            # Generate post for platform
            generator = GeneratorFactory.create_generator(request.platform)
            content = generator.generate(topic)
            
            self.logger.info(f"Generated {request.platform} post for topic: {topic}")
            
            return PostResponse(
                content=content,
                platform=request.platform,
                topic=topic,
                success=True
            )
            
        except Exception as e:
            error_msg = str(e)
            if "Connection error" in error_msg or "API key" in error_msg:
                error_msg = "OpenAI API connection failed. Check your API key and internet connection."
            
            self.logger.error(f"Error generating post: {error_msg}")
            return PostResponse(
                content="",
                platform=request.platform,
                topic=request.topic,
                success=False,
                error=error_msg
            )