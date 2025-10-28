from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from config import Config
import random
from interfaces import TrendingTopicsInterface
from logger import setup_logger

class TrendingTopicsService(TrendingTopicsInterface):
    def __init__(self, llm: ChatOpenAI = None):
        self.llm = llm or ChatOpenAI(model=Config.MODEL_NAME, temperature=0.7)
        self.logger = setup_logger("TrendingTopicsService")
        
    def get_trending_topics(self) -> list:
        """Get current trending health topics in India"""
        system_msg = SystemMessage(content="""You are a holistic homeopathic doctor analyzing latest health issues and talks in news in India. 
        Choose 5 homeopathic topics for latest health issues/talks in news in India focusing on:
        - Current health challenges trending in Indian news
        - Seasonal health concerns being discussed
        - Popular wellness topics in Indian media
        - Traditional remedies for current health issues
        - Natural healing approaches for trending health problems
        
        Return only topic names, one per line.""")
        
        response = self.llm.invoke([system_msg, HumanMessage(content="What are the latest health issues/talks in news in India that need homeopathic solutions?")])
        topics = [topic.strip() for topic in response.content.split('\n') if topic.strip()]
        return topics[:5]
    
    def get_random_trending_topic(self) -> str:
        """Get a random trending topic"""
        topics = self.get_trending_topics()
        return random.choice(topics) if topics else "Natural immunity for current health challenges"