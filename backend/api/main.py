"""
FastAPI application for Name Pronunciation Analyser.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path to import services
sys.path.insert(0, str(Path(__file__).parent.parent))

from services import LanguageDetector, IPAConverter

# Load environment variables
load_dotenv()

# Initialise FastAPI app
app = FastAPI(
    title="Name Pronunciation Analyser API",
    description="API for analysing name pronunciations for graduation ceremonies",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://names.jonathonmarsden.com",
        "https://*.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialise services
language_detector = LanguageDetector()
ipa_converter = IPAConverter()


# Request/Response models
class NameAnalysisRequest(BaseModel):
    name: str

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
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/api/analyse", response_model=NameAnalysisResponse)
async def analyse_name(request: NameAnalysisRequest):
    """
    Analyse a name and return pronunciation information.

    Args:
        request: NameAnalysisRequest containing the name to analyse

    Returns:
        NameAnalysisResponse with language, IPA, and additional information
    """
    try:
        name = request.name.strip()

        if not name:
            raise HTTPException(status_code=400, detail="Name cannot be empty")

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

        return NameAnalysisResponse(
            name=display_name,  # Show name with diacritics
            language=inferred_language,  # Use Claude's inference
            ipa=pronunciation.get('ipa', ''),
            macquarie=pronunciation.get('macquarie', ''),
            pronunciation_guidance=pronunciation.get('guidance', ''),
            confidence=1.0 if pronunciation.get('inferred_language') else script_confidence,
            language_info=language_info
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analysing name: {str(e)}"
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
