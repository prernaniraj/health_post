import streamlit as st
from dotenv import load_dotenv
from graph import create_graph
from models import AppState, PostRequest
from services import PostService

load_dotenv()

st.set_page_config(page_title="Homeopathic Social Media Post Generator", page_icon="🌿")

st.title("🌿 Homeopathic Social Media Post Generator")
st.write("Generate engaging homeopathic health posts for multiple social media platforms")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "graph" not in st.session_state:
    st.session_state.graph = create_graph()
if "service" not in st.session_state:
    st.session_state.service = PostService()

# Platform selection
platform = st.selectbox(
    "Select Platform:",
    ["instagram", "facebook", "linkedin"],
    format_func=lambda x: x.title()
)

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input(f"What homeopathic topic for {platform.title()}?"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": f"[{platform.upper()}] {prompt}"})
    with st.chat_message("user"):
        st.markdown(f"[{platform.upper()}] {prompt}")
    
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner(f"Generating {platform} post..."):
            try:
                # Use service layer
                request = PostRequest(topic=prompt, platform=platform)
                result = st.session_state.service.generate_post(request)
                
                if result.success:
                    st.markdown(f"### 📱 Your {platform.title()} Post:")
                    st.markdown(f"**Topic:** {result.topic}")
                    st.code(result.content, language="text")
                    
                    response = f"**Platform:** {platform.title()}\n**Topic:** {result.topic}\n\n{result.content}"
                    st.session_state.messages.append({"role": "assistant", "content": response})
                else:
                    st.error(f"Error: {result.error}")
                    st.session_state.messages.append({"role": "assistant", "content": f"Error: {result.error}"})
                
            except Exception as e:
                error_msg = f"Error generating post: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Sidebar
with st.sidebar:
    st.header("📱 Platforms")
    st.write("""
    **Instagram:** Visual storytelling, hashtags
    **Facebook:** Conversational, detailed
    **LinkedIn:** Professional, evidence-based
    """)
    
    st.header("💡 Example Topics")
    st.write("""
    - Natural stress relief
    - Immune system support
    - Digestive health remedies
    - Sleep improvement
    - Anxiety management
    """)
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()