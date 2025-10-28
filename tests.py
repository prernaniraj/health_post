import pytest
from unittest.mock import Mock, patch
from services import PostService, TopicAnalyzer
from generators import GeneratorFactory
from models import PostRequest

class TestTopicAnalyzer:
    @patch('services.ChatOpenAI')
    def test_extract_topic(self, mock_llm):
        mock_response = Mock()
        mock_response.content = "stress relief"
        mock_llm.return_value.invoke.return_value = mock_response
        
        analyzer = TopicAnalyzer()
        result = analyzer.extract_topic("I need help with stress")
        
        assert result == "stress relief"

class TestGeneratorFactory:
    def test_create_instagram_generator(self):
        generator = GeneratorFactory.create_generator("instagram")
        assert generator is not None
    
    def test_create_facebook_generator(self):
        generator = GeneratorFactory.create_generator("facebook")
        assert generator is not None
    
    def test_create_linkedin_generator(self):
        generator = GeneratorFactory.create_generator("linkedin")
        assert generator is not None
    
    def test_invalid_platform(self):
        with pytest.raises(ValueError):
            GeneratorFactory.create_generator("invalid")

class TestPostService:
    @patch('services.GeneratorFactory')
    @patch('services.TopicAnalyzer')
    def test_generate_post_success(self, mock_analyzer, mock_factory):
        mock_analyzer.return_value.extract_topic.return_value = "stress relief"
        mock_generator = Mock()
        mock_generator.generate.return_value = "Test post content"
        mock_factory.create_generator.return_value = mock_generator
        
        service = PostService()
        request = PostRequest(topic="stress", platform="instagram")
        result = service.generate_post(request)
        
        assert result.success is True
        assert result.content == "Test post content"
        assert result.topic == "stress relief"