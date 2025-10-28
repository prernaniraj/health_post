import streamlit as st
from dotenv import load_dotenv
from models import PostRequest
from services import PostService
from trending_topics import TrendingTopicsService
from post_editor import PostEditor
from email_service import EmailService
from image_generator import ImageGenerator
import urllib.parse
import os

load_dotenv()

st.set_page_config(page_title="Trending Health Posts Generator", page_icon="🌿")

st.title("🌿 Trending Health Posts Generator for India")
st.write("Generate posts on trending homeopathic health topics in India")

# Initialize services
if "service" not in st.session_state:
    st.session_state.service = PostService()
if "trending_service" not in st.session_state:
    st.session_state.trending_service = TrendingTopicsService()
if "editor" not in st.session_state:
    st.session_state.editor = PostEditor()
if "email_service" not in st.session_state:
    st.session_state.email_service = EmailService()
if "image_generator" not in st.session_state:
    st.session_state.image_generator = ImageGenerator()
if "current_post" not in st.session_state:
    st.session_state.current_post = ""
if "current_topic" not in st.session_state:
    st.session_state.current_topic = ""
if "current_image" not in st.session_state:
    st.session_state.current_image = None
if "current_subject" not in st.session_state:
    st.session_state.current_subject = ""

# Platform selection and image option
col1, col2 = st.columns([2, 1])

with col1:
    platform = st.selectbox(
        "Select Social Media Platform:",
        ["instagram", "facebook", "linkedin"],
        format_func=lambda x: x.title()
    )

with col2:
    st.write("")

# Topic selection method
topic_method = st.radio(
    "Choose topic method:",
    ["Select from trending topics", "Enter custom topic"],
    horizontal=True
)

if topic_method == "Select from trending topics":
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Load trending topics
        if "trending_topics" not in st.session_state:
            with st.spinner("Loading trending topics..."):
                try:
                    st.session_state.trending_topics = st.session_state.trending_service.get_trending_topics()
                except Exception as e:
                    st.error(f"Error loading topics: {str(e)}")
                    st.session_state.trending_topics = ["Mind-body harmony and natural healing"]
        
        selected_topic = st.selectbox(
            "Select a trending topic:",
            st.session_state.trending_topics if "trending_topics" in st.session_state else ["Loading..."]
        )
    
    with col2:
        if st.button("🔄 Refresh Topics"):
            with st.spinner("Generating new trending topics..."):
                try:
                    st.session_state.trending_topics = st.session_state.trending_service.get_trending_topics()
                    st.success("Topics refreshed!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    if st.button(f"🔥 Generate Post for {platform.title()}", type="primary"):
        if selected_topic and selected_topic != "Loading...":
            with st.spinner(f"Generating {platform} post..."):
                try:
                    st.session_state.current_topic = selected_topic
                    request = PostRequest(topic=selected_topic, platform=platform)
                    result = st.session_state.service.generate_post(request)
                    
                    if result.success:
                        # Extract subject line
                        content_lines = result.content.split('\n')
                        subject_line = ""
                        post_content = result.content
                        
                        if content_lines[0].startswith('Subject:'):
                            subject_line = content_lines[0].replace('Subject:', '').strip()
                            post_content = '\n'.join(content_lines[1:]).strip()
                        
                        st.session_state.current_post = post_content
                        st.session_state.current_subject = subject_line
                        

                        
                        st.success(f"Generated post for: **{selected_topic}**")
                    else:
                        st.error(f"Error: {result.error}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

else:
    # Custom topic input
    custom_topic = st.text_input("Enter your custom health topic:")
    
    if st.button(f"✨ Generate Custom Post for {platform.title()}", type="primary"):
        if custom_topic.strip():
            with st.spinner(f"Generating {platform} post..."):
                try:
                    st.session_state.current_topic = custom_topic
                    request = PostRequest(topic=custom_topic, platform=platform)
                    result = st.session_state.service.generate_post(request)
                    
                    if result.success:
                        # Extract subject line
                        content_lines = result.content.split('\n')
                        subject_line = ""
                        post_content = result.content
                        
                        if content_lines[0].startswith('Subject:'):
                            subject_line = content_lines[0].replace('Subject:', '').strip()
                            post_content = '\n'.join(content_lines[1:]).strip()
                        
                        st.session_state.current_post = post_content
                        st.session_state.current_subject = subject_line
                        

                        
                        st.success(f"Generated post for: **{custom_topic}**")
                    else:
                        st.error(f"Error: {result.error}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter a topic first.")

# Display current post
if st.session_state.current_post:
    st.markdown("---")
    st.markdown(f"### 📱 Your {platform.title()} Post")
    st.markdown(f"**Topic:** {st.session_state.current_topic}")
    
    # Display subject line if available
    if st.session_state.current_subject:
        st.markdown(f"### 🏷️ {st.session_state.current_subject}")
    
    # Display image if generated
    if st.session_state.current_image:
        if os.path.exists(st.session_state.current_image) and st.session_state.current_image.endswith('.png'):
            try:
                st.image(st.session_state.current_image, caption="Generated holistic health image", width='stretch')
            except Exception as e:
                st.error(f"Error displaying image: Network connectivity issue")
        else:
            st.warning("Image generation failed due to network connectivity. Please check your internet connection and try again.")
    
    # Editable post area
    edited_post = st.text_area(
        "Edit your post:",
        value=st.session_state.current_post,
        height=200,
        key="post_editor"
    )
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("💾 Save Changes"):
            st.session_state.current_post = edited_post
            st.success("Post updated!")
    
    with col2:
        if st.button("💡 Get Suggestions"):
            with st.spinner("Analyzing post..."):
                suggestions = st.session_state.editor.suggest_improvements(edited_post, platform)
                st.write("**Improvement Suggestions:**")
                for suggestion in suggestions:
                    st.write(f"• {suggestion}")
    
    with col3:
        if st.button("🔄 Regenerate"):
            with st.spinner("Regenerating post..."):
                request = PostRequest(topic=st.session_state.current_topic, platform=platform)
                result = st.session_state.service.generate_post(request)
                if result.success:
                    st.session_state.current_post = result.content
                    st.rerun()
    
    with col4:
        if st.button("🎨 Generate Image"):
            with st.spinner("Generating holistic image..."):
                try:
                    image_url = st.session_state.image_generator.generate_image(
                        st.session_state.current_topic, 
                        platform, 
                        st.session_state.current_subject
                    )
                    st.session_state.current_image = image_url
                    if image_url and image_url != "images/placeholder.png":
                        st.success("Image generated!")
                    else:
                        st.warning("Image generation failed due to network issues. Post content is ready.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error generating image: {str(e)}")
    
    with col5:
        if st.button("📧 Email Post"):
            # Create email content
            email_subject = f"Generated {platform.title()} Post - {st.session_state.current_topic}"
            
            # Build email body
            subject_text = f"Subject Line: {st.session_state.current_subject}\n\n" if st.session_state.current_subject else ""
            image_text = f"Image: {st.session_state.current_image}\n\n" if st.session_state.current_image else ""
            email_body = f"Here's your generated {platform.title()} post:\n\n{subject_text}{image_text}{edited_post}"
            
            # Create proper mailto link
            mailto_link = f"mailto:pn5513580972@gmail.com?subject={urllib.parse.quote(email_subject)}&body={urllib.parse.quote(email_body)}"
            
            # Display clickable link
            st.markdown(f'[📧 Click to send email]({mailto_link})')
            st.success("Email link ready! Click above to open your email client.")
    
    # Interactive editing
    st.markdown("### ✏️ Quick Edits")
    edit_request = st.text_input("What would you like to change? (e.g., 'make it more engaging', 'add more hashtags')")
    
    if st.button("Apply Edit") and edit_request:
        with st.spinner("Editing post..."):
            try:
                edited = st.session_state.editor.edit_post(edited_post, edit_request, platform)
                st.session_state.current_post = edited
                st.success("Post edited successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error editing post: {str(e)}")

# Sidebar
with st.sidebar:
    st.header("🇮🇳 India Health Trends")
    st.write("""
    This app generates posts on trending homeopathic health topics specifically for India, considering:
    - Seasonal health patterns
    - Traditional Indian remedies
    - Current wellness trends
    - Regional health concerns
    """)
    
    st.header("📱 Platform Features")
    st.write("""
    **Instagram:** Visual storytelling, trending hashtags
    **Facebook:** Community engagement, detailed info
    **LinkedIn:** Professional health insights
    """)
    
    st.header("✨ Features")
    st.write("""
    - Auto-trending topic detection
    - Interactive post editing
    - AI-powered suggestions
    - Platform optimization
    - Email posts to pn5513580972@gmail.com
    """)
    
    if st.button("🗑️ Clear All"):
        st.session_state.current_post = ""
        st.session_state.current_topic = ""
        st.session_state.current_subject = ""
        st.session_state.current_image = None
        st.rerun()