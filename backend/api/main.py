"""
FastAPI application for Name Pronunciation Analyser.
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
from typing import Optional
import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Add parent directory to path to import services
sys.path.insert(0, str(Path(__file__).parent.parent))

from services import LanguageDetector, IPAConverter

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialise rate limiter
limiter = Limiter(key_func=get_remote_address)

# Initialise FastAPI app
app = FastAPI(
    title="Name Pronunciation Analyser API",
    description="API for analysing name pronunciations for graduation ceremonies",
    version="0.1.0"
)

# Add rate limiter to app state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://names.jonathonmarsden.com",
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",  # Regex pattern for Vercel preview deployments
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialise services
language_detector = LanguageDetector()
ipa_converter = IPAConverter()


# Request/Response models
class NameAnalysisRequest(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Name to analyze"
    )

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        import unicodedata
        # Trim whitespace
        v = v.strip()
        if not v:
            raise ValueError('Name cannot be empty or only whitespace')

        # Normalize to NFC (Canonical Composition) for consistent character representation
        # This ensures combining marks are composed with their base characters
        v = unicodedata.normalize('NFC', v)

        # Count only truly problematic characters (control chars, etc.)
        # Allow letters from any script, numbers, spaces, common name punctuation, and combining marks
        problematic_count = 0
        for c in v:
            cat = unicodedata.category(c)
            # Allow: Letters (L*), Numbers (N*), Spaces (Z*), Marks (M*), common punctuation
            if cat[0] not in ('L', 'N', 'Z', 'M') and c not in '-\'.,':
                problematic_count += 1
        if problematic_count > len(v) * 0.3:  # More than 30% problematic chars
            raise ValueError('Name contains too many special characters')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "name": "张伟"
            }
        }


class NameAnalysisResponse(BaseModel):
    name: str
    language: str
    ipa: str
    macquarie: str = ""
    pronunciation_guidance: str = ""
    confidence: float
    language_info: dict = {}
    romanization_system: Optional[str] = None
    tone_marks_added: bool = False
    ambiguity: Optional[dict] = None
    cultural_notes: str = ""

    class Config:
        json_schema_extra = {
            "example": {
                "name": "张伟",
                "language": "Chinese",
                "ipa": "/ʈʂɑŋ weɪ̯/",
                "macquarie": "jahng way",
                "pronunciation_guidance": "First tone (high level) on 'Zhang', third tone (falling-rising) on 'Wei'",
                "confidence": 0.95,
                "language_info": {
                    "family_name_first": True,
                    "note": "Chinese names typically have family name first, followed by given name."
                }
            }
        }


# Routes
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Name Pronunciation Analyser API",
        "version": "0.1.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint that validates API configuration and connectivity.

    Checks:
    - API key is configured
    - Claude API is accessible

    Returns 200 if healthy, 503 if unhealthy.
    """
    import time
    from anthropic import Anthropic, APIError

    start_time = time.time()

    result = {
        "status": "healthy",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime()),
        "checks": {
            "api_configured": False,
        },
        "app": "name-analyser",
        "version": "0.1.0"
    }

    try:
        # Check 1: API key is configured
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            result["status"] = "unhealthy"
            result["checks"]["api_configured"] = False
            result["checks"]["error"] = "ANTHROPIC_API_KEY not configured"

            # Send alert
            await send_alert({
                "app": "Name Analyser",
                "url": "https://names.jonathonmarsden.com",
                "error": "ANTHROPIC_API_KEY not configured",
                "timestamp": result["timestamp"]
            })

            return result

        result["checks"]["api_configured"] = True

        # Check 2: Test API connectivity
        anthropic = Anthropic(api_key=api_key)

        response = anthropic.messages.create(
            model="claude-haiku-4-5-20251001",  # Latest Haiku model
            max_tokens=10,
            messages=[{
                "role": "user",
                "content": "ok"
            }]
        )

        if response.content and len(response.content) > 0:
            result["checks"]["api_accessible"] = True
            result["status"] = "healthy"
        else:
            raise Exception("Empty response from API")

        duration = (time.time() - start_time) * 1000
        result["response_time_ms"] = int(duration)

        return result

    except Exception as e:
        result["status"] = "unhealthy"
        result["checks"]["api_accessible"] = False

        # Determine error type
        error_message = str(e)
        if "API key" in error_message or "authentication" in error_message.lower():
            error_message = "Invalid API key"
        elif "rate limit" in error_message.lower():
            error_message = "API rate limit exceeded"
        elif "overload" in error_message.lower():
            error_message = "API temporarily overloaded"
        elif "quota" in error_message.lower() or "balance" in error_message.lower():
            error_message = "API quota or balance issue"

        result["checks"]["error"] = error_message

        # Send alert for critical errors (not temporary overloads)
        if "overload" not in error_message.lower():
            await send_alert({
                "app": "Name Analyser",
                "url": "https://names.jonathonmarsden.com",
                "error": error_message,
                "timestamp": result["timestamp"],
                "details": str(e)
            })

        duration = (time.time() - start_time) * 1000
        result["response_time_ms"] = int(duration)

        logger.error(f"Health check failed: {error_message}")

        return result


async def send_alert(payload: dict):
    """Send alert email when health check fails."""
    import httpx

    try:
        alert_endpoint = os.getenv("ALERT_EMAIL_ENDPOINT")
        if not alert_endpoint:
            logger.error(f"ALERT_EMAIL_ENDPOINT not configured - alert not sent: {payload}")
            return

        async with httpx.AsyncClient() as client:
            response = await client.post(
                alert_endpoint,
                json=payload,
                timeout=10.0
            )

            if response.status_code != 200:
                logger.error(f"Failed to send alert: {response.status_code} {response.text}")
    except Exception as e:
        logger.error(f"Error sending alert: {str(e)}")


@app.post("/api/analyse", response_model=NameAnalysisResponse)
@limiter.limit("10/minute")  # 10 requests per minute per IP
async def analyse_name(request: Request, name_request: NameAnalysisRequest):
    """
    Analyse a name and return pronunciation information.

    Args:
        request: FastAPI request object (for rate limiting)
        name_request: NameAnalysisRequest containing the name to analyse

    Returns:
        NameAnalysisResponse with language, IPA, and additional information
    """
    try:
        name = name_request.name.strip()

        if not name:
            raise HTTPException(status_code=400, detail="Name cannot be empty")

        logger.info(f"Analyzing name: {name[:50]}")

        # Detect script (for rare cases with Chinese characters, etc.)
        script_language, script_confidence = language_detector.detect(name)

        # Analyse pronunciation - Claude will infer the actual language from etymology
        pronunciation = ipa_converter.analyse_pronunciation(name, script_language)

        # Use Claude's inferred language if available, otherwise fall back to script detection
        inferred_language = pronunciation.get('inferred_language', script_language)

        # Get language information based on inferred language
        language_info = language_detector.get_language_info(inferred_language)

        # Use name_with_diacritics if provided by Claude, otherwise use original
        display_name = pronunciation.get('name_with_diacritics', name)

        logger.info(f"Successfully analyzed: {name[:50]} -> {inferred_language}")

        return NameAnalysisResponse(
            name=display_name,  # Show name with diacritics
            language=inferred_language,  # Use Claude's inference
            ipa=pronunciation.get('ipa', ''),
            macquarie=pronunciation.get('macquarie', ''),
            pronunciation_guidance=pronunciation.get('guidance', ''),
            confidence=1.0 if pronunciation.get('inferred_language') else script_confidence,
            language_info=language_info,
            romanization_system=pronunciation.get('romanization_system'),
            tone_marks_added=pronunciation.get('tone_marks_added', False),
            ambiguity=pronunciation.get('ambiguity'),
            cultural_notes=pronunciation.get('cultural_notes', '')
        )

    except HTTPException:
        raise
    except Exception as e:
        # Log full error internally
        logger.error(f"Error analyzing name '{name[:50]}': {str(e)}", exc_info=True)

        # Return generic message to client
        raise HTTPException(
            status_code=500,
            detail="An error occurred while analyzing the name. Please try again."
        )


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )
