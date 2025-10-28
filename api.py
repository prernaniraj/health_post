from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Literal
from services import PostService
from models import PostRequest, PostResponse

app = FastAPI(title="Homeopathic Post Generator API", version="1.0.0")

class PostRequestAPI(BaseModel):
    topic: str
    platform: Literal["instagram", "facebook", "linkedin"]
    user_id: str = "anonymous"

service = PostService()

@app.post("/generate", response_model=PostResponse)
async def generate_post(request: PostRequestAPI):
    """Generate homeopathic social media post"""
    try:
        post_request = PostRequest(
            topic=request.topic,
            platform=request.platform,
            user_id=request.user_id
        )
        
        result = service.generate_post(post_request)
        
        if not result.success:
            raise HTTPException(status_code=400, detail=result.error)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    from health_check import health_check
    return health_check()

@app.get("/platforms")
async def get_platforms():
    return {"platforms": ["instagram", "facebook", "linkedin"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)