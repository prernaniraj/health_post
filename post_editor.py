from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from config import Config

class PostEditor:
    def __init__(self):
        self.llm = ChatOpenAI(model=Config.MODEL_NAME, temperature=0.5)
    
    def edit_post(self, original_post: str, edit_request: str, platform: str) -> str:
        """Edit post based on user feedback"""
        system_msg = SystemMessage(content=f"""You are a holistic homeopathic doctor editing a {platform} post.
        
        Original post: {original_post}
        
        User wants: {edit_request}
        
        Modify the post maintaining the voice of a compassionate, scientific, and hopeful holistic doctor.
        Focus on natural healing, mind-body balance, and emotional wellness.
        Keep tone poetic yet factual, spiritually uplifting, and empowering.
        Ensure content promotes harmony, nature, and vegetarian/vegan healing.
        
        Return only the edited post.""")
        
        response = self.llm.invoke([system_msg, HumanMessage(content=f"Edit the post: {edit_request}")])
        return response.content
    
    def suggest_improvements(self, post: str, platform: str) -> list:
        """Suggest improvements for the post"""
        system_msg = SystemMessage(content=f"""As a holistic homeopathic doctor, analyze this {platform} post and suggest 3 improvements:
        
        Post: {post}
        
        Focus on enhancing:
        - Compassionate, scientific, hopeful voice
        - Natural healing and mind-body balance elements
        - Poetic yet factual tone
        - Spiritual upliftment and empowerment
        
        Return 3 numbered suggestions.""")
        
        response = self.llm.invoke([system_msg, HumanMessage(content="Suggest improvements")])
        suggestions = [s.strip() for s in response.content.split('\n') if s.strip() and any(c.isdigit() for c in s[:3])]
        return suggestions[:3]