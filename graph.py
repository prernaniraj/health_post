from langgraph.graph import StateGraph, END
from langchain.schema import HumanMessage
from models import AppState
from services import PostService
from generators import GeneratorFactory

def analyze_request(state: AppState):
    """Extract topic from user request"""
    service = PostService()
    topic = service.topic_analyzer.extract_topic(state["messages"][-1])
    
    return {
        "topic": topic,
        "messages": [HumanMessage(content=f"Topic: {topic}")]
    }

def generate_post(state: AppState):
    """Generate post for specified platform"""
    try:
        generator = GeneratorFactory.create_generator(state["platform"])
        content = generator.generate(state["topic"])
        
        return {
            "post_content": content,
            "messages": [HumanMessage(content="Post generated")]
        }
    except Exception as e:
        return {
            "error": str(e),
            "messages": [HumanMessage(content=f"Error: {str(e)}")]
        }

def create_graph():
    workflow = StateGraph(AppState)
    
    workflow.add_node("analyze", analyze_request)
    workflow.add_node("generate", generate_post)
    
    workflow.set_entry_point("analyze")
    workflow.add_edge("analyze", "generate")
    workflow.add_edge("generate", END)
    
    return workflow.compile()