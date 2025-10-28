# Homeopathic Social Media Post Generator

Production-grade modular application that generates homeopathic health posts for Instagram, Facebook, and LinkedIn using LangGraph.

## Architecture

- **Modular Design**: Separate generators for each platform
- **Service Layer**: Business logic and error handling
- **API Layer**: REST API for integration
- **Configuration**: Platform-specific settings
- **Testing**: Unit tests for quality assurance

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables:
```bash
cp .env.example .env
# Edit .env with your OPENAI_API_KEY
```

## Running

### Streamlit App
```bash
streamlit run app.py
```

### REST API
```bash
uvicorn api:app --reload
```

### Docker
```bash
docker-compose up
```

## API Usage

```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{"topic": "stress relief", "platform": "instagram"}'
```

## Testing

```bash
pytest tests.py -v
```

## Platforms

- **Instagram**: Visual storytelling, up to 30 hashtags
- **Facebook**: Conversational tone, detailed content
- **LinkedIn**: Professional insights, evidence-based