from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from typing import Optional, List, Dict, Any
from enum import Enum
from phi.agent import Agent
from phi.model.groq import Groq
from phi.model.google import Gemini
from phi.tools.duckduckgo import DuckDuckGo
from fastapi.middleware.cors import CORSMiddleware
import logging
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import newspaper
from newspaper import Article
from newspaper.article import ArticleException
import trafilatura
from urllib.parse import urlparse
import html2text
import re
import json
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    INSTAGRAM = "instagram"
    INSTAGRAM_REELS = "instagram_reels"
    YOUTUBE = "youtube"
    YOUTUBE_SHORTS = "youtube_shorts"
    TWITTER = "twitter"
    LINKEDIN = "linkedin"
    TIKTOK = "tiktok"
    MEDIUM = "medium"
    WORDPRESS = "wordpress"
    SUBSTACK = "substack"
    WEBSITE = "website"
    LANDING_PAGE = "landing_page"
    EMAIL = "email_marketing"
    PODCAST_SCRIPT = "podcast_script"
    VIDEO_SCRIPT = "video_script"

def get_platform_instructions(platform: Platform) -> str:
    current_year = datetime.now().year
    instructions = {
        Platform.INSTAGRAM: f"""
        Generate Instagram content that:
        - Has a powerful first sentence hook
        - Uses 2-3 short paragraphs (max 2200 characters)
        - Includes 3-5 relevant emojis strategically placed
        - Contains bullet points for key takeaways
        - Ends with 15-20 targeted hashtags
        - Includes a clear call-to-action
        - Uses line breaks for readability
        - References current {current_year} trends
        - Maintains professional but engaging tone
        Do not ask questions or seek clarification. Generate definitive content.
        """,

        Platform.INSTAGRAM_REELS: f"""
        Generate Instagram Reels script that:
        - Opens with a 3-second attention-grabbing hook
        - Includes 15-30 second script timing
        - Contains 3-4 key points or revelations
        - Uses trending audio/music suggestions
        - Incorporates popular {current_year} Reels formats
        - Includes text overlay suggestions
        - Adds 10-15 trending Reels hashtags
        - Specifies transition effects
        - Ends with strong call-to-action
        - Maximum 150 words for entire script
        Generate ready-to-film content without questions.
        """,

        Platform.YOUTUBE: f"""
        Create YouTube video content that:
        - Has an attention-grabbing title (max 60 characters)
        - Includes compelling thumbnail text suggestions
        - Contains detailed video script with timestamps
        - Provides B-roll suggestions
        - Includes chapter markers every 3-4 minutes
        - Features detailed video description (2000 characters)
        - Contains 8-10 relevant tags
        - Includes end screen suggestions
        - Features cards and timestamp links
        - References current {current_year} trends
        - Optimizes for YouTube SEO
        - Suggests video length (10-15 minutes)
        Generate complete video package without questions.
        """,

        Platform.YOUTUBE_SHORTS: f"""
        Create YouTube Shorts content that:
        - Has a 1-second hook opening
        - Contains 30-60 second detailed script
        - Includes text overlay placement
        - Suggests trending music/sounds
        - Uses pattern interrupts every 2-3 seconds
        - Contains vertical framing instructions
        - Includes trending hashtags (3-5)
        - Features quick-cut editing suggestions
        - Ends with subscribe call-to-action
        - Optimizes for {current_year} Shorts algorithm
        Generate ready-to-film content without questions.
        """,

        Platform.TWITTER: f"""
        Create Twitter content that:
        - Opens with high-impact first tweet
        - Structures thread in 5-7 tweets
        - Each tweet maximum 280 characters
        - Uses line breaks for readability
        - Incorporates relevant data points
        - Includes 2-3 engaging hooks
        - Uses 3-4 relevant hashtags
        - Adds appropriate emojis
        - Ends with clear call-to-action
        - References {current_year} trends
        Generate complete thread without questions.
        """,

        Platform.LINKEDIN: f"""
        Create LinkedIn content that:
        - Opens with a compelling business insight
        - Uses data-driven statements and statistics
        - Includes 4-6 paragraphs with professional analysis
        - Highlights industry implications
        - Uses bullet points for key takeaways
        - References relevant {current_year} market trends
        - Includes 3-5 strategic hashtags
        - Ends with a professional call-to-action
        - Maintains executive-level tone
        - Uses white space for readability
        Generate authoritative content without seeking clarification.
        """,

        Platform.TIKTOK: f"""
        Create TikTok content that:
        - Starts with immediate pattern interrupt (2 seconds)
        - Includes 15-60 second script timing
        - Features trending sound suggestions
        - Contains text overlay placements
        - Uses popular {current_year} TikTok formats
        - Incorporates transition suggestions
        - Adds 4-5 trending hashtags
        - Features viral hooks
        - Includes editing suggestions
        - Ends with strong call-to-action
        Generate viral-optimized content without questions.
        """,

        Platform.MEDIUM: f"""
        Create a comprehensive Medium article that:
        - Has a compelling headline and subheading
        - Opens with a strong hook paragraph
        - Contains 1500-2000 words of detailed analysis
        - Uses H2 and H3 subheadings throughout
        - Includes relevant statistics and data
        - References expert opinions and sources
        - Contains real-world examples and case studies
        - Incorporates {current_year} industry trends
        - Uses transition sentences between sections
        - Ends with actionable insights
        - Maintains journalistic quality throughout
        Generate complete, self-contained content without questions.
        """,

        Platform.WORDPRESS: f"""
        Create SEO-optimized WordPress content that:
        - Contains SEO title and meta description
        - Features long-tail keyword optimization
        - Includes 1200-1800 words of content
        - Uses proper heading hierarchy (H1-H4)
        - Incorporates internal and external links
        - Features optimized image alt texts
        - Contains table of contents structure
        - Includes featured image suggestions
        - Adds category and tag recommendations
        - Optimizes for {current_year} SEO trends
        Generate complete blog post without questions.
        """,

        Platform.SUBSTACK: f"""
        Create Substack newsletter content that:
        - Has compelling subject line
        - Opens with personal/engaging intro
        - Contains 800-1200 words of insights
        - Includes section breaks with subheadings
        - Features exclusive analysis
        - Incorporates reader engagement elements
        - Adds premium content section
        - Uses newsletter-optimized formatting
        - Ends with discussion prompt
        - References {current_year} developments
        Generate complete newsletter without questions.
        """,

        Platform.WEBSITE: f"""
        Create website content that:
        - Contains SEO-optimized headlines
        - Features compelling value proposition
        - Includes proper meta descriptions
        - Uses conversion-focused copywriting
        - Incorporates relevant keywords
        - Features clear navigation structure
        - Adds call-to-action buttons
        - Optimizes for {current_year} web standards
        - Includes technical SEO elements
        Generate complete web copy without questions.
        """,

        Platform.LANDING_PAGE: f"""
        Create landing page content that:
        - Has attention-grabbing headline
        - Features compelling sub-headline
        - Includes unique value propositions
        - Contains benefit-focused bullet points
        - Features social proof elements
        - Incorporates trust indicators
        - Adds multiple call-to-action variations
        - Uses persuasive copywriting techniques
        - Includes FAQ section
        - Optimizes for {current_year} conversion rates
        Generate high-converting copy without questions.
        """,

        Platform.EMAIL: f"""
        Create email marketing content that:
        - Has high-impact subject line
        - Includes preview text optimization
        - Contains personalization elements
        - Features compelling opening line
        - Uses short, scannable paragraphs
        - Incorporates social proof
        - Adds urgency elements
        - Features multiple call-to-action placements
        - Includes P.S. section
        - Optimizes for {current_year} email trends
        Generate complete email without questions.
        """,

        Platform.PODCAST_SCRIPT: f"""
        Create podcast script that:
        - Includes show intro and outro
        - Features episode hook (30 seconds)
        - Contains topic breakdown
        - Includes interview questions/talking points
        - Adds transition sentences
        - Features ad placement suggestions
        - Incorporates listener engagement points
        - Includes show notes
        - References {current_year} trends
        - Suggests episode length (30-45 minutes)
        Generate complete episode script without questions.
        """,

        Platform.VIDEO_SCRIPT: f"""
        Create video script that:
        - Opens with attention hook
        - Includes shot-by-shot breakdown
        - Contains camera angle suggestions
        - Features B-roll recommendations
        - Adds music/sound effect cues
        - Incorporates graphics placement
        - Includes timing for each section
        - Features dialogue/voiceover text
        - References {current_year} video trends
        - Suggests video length
        Generate complete video script without questions.
        """
    }
    return instructions.get(platform, "Generate platform-optimized content without asking questions.")

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

class WebScrapingResult(BaseModel): 
    url: str
    title: str
    text: str
    summary: str
    keywords: List[str]

class WebContent:
    def __init__(self):
        self.h = html2text.HTML2Text()
        self.h.ignore_links = False
        self.session = aiohttp.ClientSession()
        
    async def close(self):
        await self.session.close()
        
    async def fetch_url(self, url: str) -> str:
        try:
            async with self.session.get(url, timeout=10) as response:
                return await response.text()
        except Exception as e:
            logger.error(f"Error fetching URL {url}: {str(e)}")
            return ""

    def extract_text_from_html(self, html_content: str) -> str:
        try:
            # Try trafilatura first
            text = trafilatura.extract(html_content)
            if text:
                return text
            
            # Fallback to BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            return " ".join(soup.stripped_strings)
        except Exception as e:
            logger.error(f"Error extracting text: {str(e)}")
            return ""

    def clean_text(self, text: str) -> str:
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove URLs
        text = re.sub(r'http\S+|www.\S+', '', text)
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        return text.strip()

    async def process_url(self, url: str) -> Dict[str, Any]:
        try:
            html_content = await self.fetch_url(url)
            if not html_content:
                return None

            # Try to extract with newspaper3k first
            article = Article(url)
            article.download()
            article.parse()
            article.nlp()

            # Combine different extraction methods for best results
            raw_text = self.extract_text_from_html(html_content)
            cleaned_text = self.clean_text(raw_text)

            return {
                "url": url,
                "title": article.title,
                "text": cleaned_text,
                "summary": article.summary,
                "keywords": article.keywords,
                "publish_date": str(article.publish_date) if article.publish_date else None,
                "authors": article.authors,
                "domain": urlparse(url).netloc
            }
        except Exception as e:
            logger.error(f"Error processing URL {url}: {str(e)}")
            return None

class ContentSource:
    def __init__(self):
        self.web_content = WebContent()
        
    async def search_and_scrape(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        try:
            # Use DuckDuckGo for initial search
            search = DuckDuckGo()
            search_results = search.search(query)
            
            if not search_results:
                return []

            # Extract URLs from search results
            urls = []
            for result in search_results[:max_results]:
                if isinstance(result, dict) and 'link' in result:
                    urls.append(result['link'])
                elif hasattr(result, 'url'):
                    urls.append(result.url)

            # Process URLs concurrently
            tasks = [self.web_content.process_url(url) for url in urls]
            results = await asyncio.gather(*tasks)
            
            # Filter out None results and sort by relevance
            valid_results = [r for r in results if r is not None]
            return valid_results

        except Exception as e:
            logger.error(f"Error in search_and_scrape: {str(e)}")
            return []

    async def close(self):
        await self.web_content.close()

class ResearchAgent:
    def __init__(self, model):
        self.model = model
        self.content_source = ContentSource()

    async def research(self, topic: str) -> Dict[str, Any]:
        try:
            # Fetch web content
            sources = await self.content_source.search_and_scrape(topic)
            
            if not sources:
                logger.warning("No sources found, using fallback content generation")
                return {
                    "content": f"Based on available information about {topic}",
                    "sources": []
                }

            # Prepare source information
            source_info = []
            combined_text = ""
            
            for source in sources:
                if source and 'text' in source and 'url' in source:
                    combined_text += f"\nSource: {source['url']}\n{source['text']}\n"
                    source_info.append({
                        "url": source['url'],
                        "title": source.get('title', 'Untitled'),
                        "domain": source.get('domain', ''),
                        "publish_date": source.get('publish_date', '')
                    })

            # Generate content using the model
            synthesis_prompt = f"""
            Analyze and synthesize the following information about {topic}.
            Use only the information provided in the sources.
            Always cite sources when making statements.
            Include URLs and publication dates where available.

            Source Material:
            {combined_text}

            Generate comprehensive content that:
            1. Uses information only from the provided sources
            2. Cites sources for all claims
            3. Includes specific quotes where relevant
            4. Maintains factual accuracy
            5. Organizes information logically
            6. Provides proper attribution
            """

            synthesis = self.model.complete(synthesis_prompt)
            
            return {
                "content": synthesis.content if hasattr(synthesis, 'content') else "No content generated",
                "sources": source_info
            }

        except Exception as e:
            logger.error(f"Research error: {str(e)}")
            return {
                "content": f"Error processing research for {topic}",
                "sources": []
            }

    async def close(self):
        await self.content_source.close()

@app.post("/api/generate", response_model=GenerationResponse)
async def generate_content(request: GenerationRequest):
    try:
        logger.info(f"Starting content generation for platform: {request.platform.value}")
        
        # Initialize model
        model = Gemini(api_key=request.api_key, id=request.model_name) if request.provider == Provider.GEMINI else Groq(api_key=request.api_key, id=request.model_name)
        
        # Initialize research agent
        researcher = ResearchAgent(model)
        research_results = await researcher.research(request.input_text)
        
        # Format sources for inclusion in content
        source_citations = "\n\nSources:\n"
        for idx, source in enumerate(research_results['sources'], 1):
            source_citations += f"{idx}. {source['title']} - {source['url']} ({source['publish_date']})\n"

        # Generate platform-specific content
        content_prompt = f"""
        Create {request.platform.value} content following these guidelines:
        {get_platform_instructions(request.platform)}
        
        Use this researched information:
        {research_results['content']}
        
        Include source citations appropriately for the platform.
        Maintain factual accuracy and proper attribution.
        """

        final_content = model.complete(content_prompt)
        
        # Add sources to the end of content
        complete_content = f"{final_content.content}\n{source_citations}" if hasattr(final_content, 'content') else "Content generation failed"
        
        await researcher.close()
        
        return GenerationResponse(
            content=complete_content,
            summary=research_results['content'][:500] + "..." if len(research_results['content']) > 500 else research_results['content'],
            status="success"
        )

    except Exception as e:
        logger.error(f"Error during content generation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

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

if __name__ == "__main__":
    try:
        uvicorn.run(app, host="127.0.0.1", port=8000)
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")          