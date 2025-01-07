from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from typing import Optional, List
from enum import Enum
import signal
from phi.agent import Agent
from phi.model.groq import Groq
from phi.model.google import Gemini
from phi.tools.googlesearch import GoogleSearch
from fastapi.middleware.cors import CORSMiddleware
import logging

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Provider(str, Enum):
    GEMINI = "gemini"
    GROQ = "groq"

class GeminiModel(str, Enum):
    PRO = "gemini-1.5-pro"
    FLASH = "gemini-1.5-flash"
    FLASH_8B = "gemini-1.5-flash-8b"

class GroqModel(str, Enum):
    LLAMA = "llama-3.3-70b-versatile"

class Platform(str, Enum):
    # Social Media Platforms
    INSTAGRAM = "instagram"
    INSTAGRAM_REELS = "instagram_reels"
    YOUTUBE = "youtube"
    YOUTUBE_SHORTS = "youtube_shorts"
    TWITTER = "twitter"
    LINKEDIN = "linkedin"
    TIKTOK = "tiktok"
    
    # Blogging Platforms
    MEDIUM = "medium"
    WORDPRESS = "wordpress"
    SUBSTACK = "substack"
    
    # Professional Platforms
    WEBSITE = "website"
    LANDING_PAGE = "landing_page"
    EMAIL = "email_marketing"
    
    # Other
    PODCAST_SCRIPT = "podcast_script"
    VIDEO_SCRIPT = "video_script"

class GenerationRequest(BaseModel):
    provider: Provider
    model_name: str
    api_key: str
    platform: Platform
    input_text: str
    serper_api_key: Optional[str] = None

class GenerationResponse(BaseModel):
    content: str
    summary: Optional[str] = None
    status: str

def get_platform_instructions(platform: Platform) -> str:
    instructions = {
        # Social Media Platforms
        Platform.INSTAGRAM: """
        1. Create engaging Instagram post content (2200 characters max)
        2. Include relevant hashtags (max 30)
        3. Write compelling captions that drive engagement
        4. Include call-to-action
        5. Structure: Hook → Value → Call-to-action
        """,
        Platform.INSTAGRAM_REELS: """
        1. Create short-form video script (15-30 seconds)
        2. Include hook, main points, and call-to-action
        3. Add relevant hashtags
        4. Focus on trending formats and patterns
        5. Include music/sound recommendations
        """,
        Platform.YOUTUBE: """
        1. Create detailed video script with timestamps
        2. Write compelling title (60 characters max)
        3. Create description with timestamps and links
        4. Include relevant tags and keywords
        5. Add end screen suggestions
        """,
        Platform.YOUTUBE_SHORTS: """
        1. Create vertical video script (60 seconds max)
        2. Strong hook in first 3 seconds
        3. Fast-paced, engaging content
        4. Clear call-to-action
        5. Trending audio suggestions
        """,
        Platform.TWITTER: """
        1. Create engaging tweet thread
        2. 280 characters per tweet
        3. Include relevant hashtags
        4. Create thread hooks
        5. End with call-to-action
        """,
        Platform.LINKEDIN: """
        1. Create professional content with industry insights
        2. Include statistics and data points
        3. Use appropriate business terminology
        4. Add relevant hashtags
        5. Professional call-to-action
        """,
        Platform.TIKTOK: """
        1. Create trending-style script
        2. Include popular sound suggestions
        3. Write engaging hooks
        4. Add relevant hashtags
        5. Viral-oriented structure
        """,
        
        # Blogging Platforms
        Platform.MEDIUM: """
        1. Create long-form article (1500-2000 words)
        2. SEO-optimized title and subtitles
        3. Include relevant tags
        4. Add internal and external links
        5. Format for readability with proper sections
        """,
        Platform.WORDPRESS: """
        1. Create SEO-optimized blog post
        2. Include meta description and title tags
        3. Add internal linking structure
        4. Format with proper headings (H1, H2, H3)
        5. Include featured image suggestions
        """,
        Platform.SUBSTACK: """
        1. Create newsletter-style content
        2. Engaging subject line
        3. Clear section breaks
        4. Include subscriber-only content
        5. End with discussion prompt
        """,
        
        # Professional Platforms
        Platform.WEBSITE: """
        1. Create conversion-focused web content
        2. Include meta tags and SEO elements
        3. Clear value proposition
        4. Include call-to-action buttons
        5. Optimize for web readability
        """,
        Platform.LANDING_PAGE: """
        1. Create high-converting landing page copy
        2. Clear unique selling proposition
        3. Include benefit-driven headlines
        4. Add social proof sections
        5. Multiple call-to-action points
        """,
        Platform.EMAIL: """
        1. Create email marketing campaign
        2. Compelling subject line
        3. Personalization elements
        4. Clear value proposition
        5. Strong call-to-action
        """,
        
        # Other
        Platform.PODCAST_SCRIPT: """
        1. Create engaging podcast script
        2. Include intro and outro
        3. Add transition points
        4. Include discussion topics
        5. Write show notes
        """,
        Platform.VIDEO_SCRIPT: """
        1. Create detailed video script
        2. Include B-roll suggestions
        3. Add camera angle notes
        4. Include timing markers
        5. Write production notes
        """
    }
    return instructions.get(platform, "Create general content optimized for the platform")

@app.post("/api/generate", response_model=GenerationResponse)
async def generate_content(request: GenerationRequest):
    try:
        # Initialize the model based on provider
        if request.provider == Provider.GEMINI:
            model = Gemini(
                id=request.model_name,
                api_key=request.api_key,
            )
            print("google api mil gaya malik")
        else:  # GROQ
            model = Groq(
                id=request.model_name,
                api_key=request.api_key
            )
            print("groq api mil gaya malik")

        # Initialize agents
        researcher = Agent(
            role='Content Researcher',
            goal='Find relevant articles and generate concise summaries',
            description='Skilled researcher with expertise in identifying and summarizing key information',
            instructions=f'Research and summarize information about: {request.input_text}',
            model=model,
            tools=[GoogleSearch(api_key=request.serper_api_key)] if request.serper_api_key else [],
            verbose=True
        )
        print("research kr raha hu malik")

        writer = Agent(
            role='Content Writer',
            goal='Generate platform-specific content based on research',
            description='Experienced content writer with platform expertise',
            instructions=f"""
            Generate content for {request.platform.value} with the following requirements:
            {get_platform_instructions(request.platform)}
            Topic: {request.input_text}
            """,
            model=model,
            verbose=True
        )
        print("Likh raha hu malik")

        # Create multi-agent team
        multi_agent = Agent(
            model=model,
            team=[researcher, writer],
            show_tool_calls=True,
            markdown=True
        )

        # Generate content
        response = multi_agent.run(request.input_text)
        print("content generate kr raha hu malik")
        
        return GenerationResponse(
            content=response.content,
            summary=response.summary if hasattr(response, 'summary') else None,
            status="success"
        )
        print("content generate krdiya malik")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        print("error aagya malik")

@app.get("/api/providers")
async def get_providers():
    return {
        "providers": [
            {
                "name": Provider.GEMINI,
                "models": [model.value for model in GeminiModel]
            },
            {
                "name": Provider.GROQ,
                "models": [model.value for model in GroqModel]
            }
        ]
    }
    print("providers mil gaya malik")
    
@app.get("/api/platforms")
async def get_platforms():
    return {
        "platforms": [
            {
                "name": platform.value,
                "instructions": get_platform_instructions(platform)
            } for platform in Platform
        ]
    }
    print("platforms mil gaya malik")

@app.on_event("shutdown")
async def shutdown_event():
    print("Server shutting down...")

if __name__ == "__main__":
    try:
        uvicorn.run(app, host="127.0.0.1", port=8000)
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")