"""
Pronunciation analysis service using Gemini API.
Generates accurate IPA and Macquarie Dictionary phonetic notation for names.
Railway deployment ready.
"""

from typing import Optional, Dict, Any
import asyncio
import os
import logging
from google import genai
from pydantic import BaseModel, Field, ValidationError

logger = logging.getLogger(__name__)


class PronunciationOutput(BaseModel):
    inferred_language: str = Field(default="")
    name_with_diacritics: str = Field(default="")
    romanization_system: Optional[str] = Field(default=None)
    ipa: str = Field(default="")
    macquarie: str = Field(default="")
    guidance: str = Field(default="")
    tone_marks_added: bool = Field(default=False)
    ambiguity: Optional[dict] = Field(default=None)
    cultural_notes: str = Field(default="")


class IPAConverter:
    """Converts names to IPA and Macquarie phonetic notation using Gemini API."""

    def __init__(self):
        """Initialise pronunciation converter with Gemini API client."""
        self.client = None
        self.model = os.getenv('GEMINI_MODEL', 'gemini-3.1-pro-preview')
        self.request_timeout_seconds = float(os.getenv('GEMINI_TIMEOUT_SECONDS', '10'))
        api_key = os.getenv('GEMINI_API_KEY')

        if api_key and api_key != 'your_api_key_here':
            try:
                self.client = genai.Client(api_key=api_key)
                logger.info("Gemini API initialized for pronunciation analysis")
            except Exception as e:
                logger.warning(f"Could not initialize Gemini API: {e}")
                logger.info("Falling back to simplified notation")
        else:
            logger.info("GEMINI_API_KEY not set")
            logger.info("Add your API key to backend/.env for accurate IPA and Macquarie notation")
            logger.info("Run: ./add-api-key.sh")

    async def analyse_pronunciation(self, text: str, language: str) -> Dict[str, Any]:
        """
        Analyse name pronunciation using Gemini API.

        Args:
            text: The name to analyse
            language: The detected language

        Returns:
            Dictionary containing IPA, Macquarie notation, and pronunciation guidance
        """
        if not text:
            return {
                'ipa': '',
                'macquarie': '',
                'guidance': ''
            }

        # Try Gemini API analysis if available
        if self.client:
            try:
                return await self._analyse_with_gemini(text, language)
            except Exception as e:
                logger.error(f"Error using Gemini API: {e}")
                logger.info("Falling back to simplified notation")

        # Fallback to simplified notation
        return self._simplified_analysis(text, language)

    async def convert(self, text: str, language: str) -> str:
        """
        Legacy method for backwards compatibility.
        Returns just the IPA notation.
        """
        result = await self.analyse_pronunciation(text, language)
        return result.get('ipa', '')

    async def _analyse_with_gemini(self, text: str, language: str) -> Dict[str, Any]:
        """
        Use Gemini API for comprehensive pronunciation analysis with language inference.

        Args:
            text: The name to analyse
            language: The script-detected language (may be "English" for Romanized text)

        Returns:
            Dictionary with inferred language, IPA, Macquarie notation, romanized form with diacritics, and guidance
        """
        prompt = f"""You are an expert linguist helping ceremony readers pronounce names respectfully.

Analyze this name:
- Name: {text}
- Script-detected language: {language}

Rules:
1. Preserve exact spelling in name_with_diacritics except tonal marks for tonal languages.
2. Provide full IPA.
3. Provide Macquarie-style respelling (speakable by Australian English speakers).
4. guidance must be practical and short.
5. If uncertain, choose best-likely pronunciation and include note in cultural_notes.
Return only JSON matching the schema.
"""

        attempts = 2
        last_error = None

        for attempt in range(1, attempts + 1):
            try:
                response = await asyncio.wait_for(
                    self.client.aio.models.generate_content(
                        model=self.model,
                        contents=prompt,
                        config=genai.types.GenerateContentConfig(
                            response_mime_type="application/json",
                            response_schema=PronunciationOutput,
                            max_output_tokens=500,
                        ),
                    ),
                    timeout=self.request_timeout_seconds,
                )

                response_text = (getattr(response, "text", "") or "").strip()
                if not response_text:
                    raise ValueError("Empty response from Gemini API")

                parsed = PronunciationOutput.model_validate_json(response_text)
                normalized = self._normalize_output(parsed, text, language)

                if self._is_quality_output(normalized):
                    return normalized

                last_error = ValueError("Schema output passed, but quality gate failed")
                logger.warning(f"Gemini output quality gate failed (attempt {attempt}/{attempts})")

            except (ValidationError, ValueError) as e:
                last_error = e
                logger.warning(f"Gemini structured parse failed (attempt {attempt}/{attempts}): {e}")
            except asyncio.TimeoutError as e:
                last_error = e
                logger.warning(f"Gemini timeout (attempt {attempt}/{attempts})")
            except Exception as e:
                last_error = e
                logger.warning(f"Gemini call failed (attempt {attempt}/{attempts}): {e}")

        minimal = await self._analyse_with_minimal_prompt(text, language)
        if minimal:
            return minimal

        logger.error(f"Gemini analysis failed after retries: {last_error}")
        return self._fallback_from_name(text, language)

    def _simplified_analysis(self, text: str, language: str) -> Dict[str, Any]:
        """
        Provide simplified analysis without Gemini API.

        Args:
            text: The text to analyse
            language: The detected language

        Returns:
            Dictionary with simplified notations
        """
        return {
            'ipa': f"[Add API key for accurate IPA]",
            'macquarie': f"[Add API key for Macquarie notation]",
            'guidance': f"Set GEMINI_API_KEY in backend/.env for accurate pronunciation analysis. Run: ./add-api-key.sh"
        }

    def _normalize_output(self, parsed: PronunciationOutput, text: str, language: str) -> Dict[str, Any]:
        inferred_language = (parsed.inferred_language or '').strip() or language
        name_with_diacritics = (parsed.name_with_diacritics or '').strip() or text
        romanization_system = (parsed.romanization_system or '').strip() or None
        if romanization_system and romanization_system.lower() in ('none', 'null', 'n/a'):
            romanization_system = None

        return {
            'inferred_language': inferred_language,
            'name_with_diacritics': name_with_diacritics,
            'romanization_system': romanization_system,
            'ipa': (parsed.ipa or '').strip(),
            'macquarie': (parsed.macquarie or '').strip(),
            'guidance': (parsed.guidance or '').strip(),
            'tone_marks_added': bool(parsed.tone_marks_added),
            'ambiguity': parsed.ambiguity,
            'cultural_notes': (parsed.cultural_notes or '').strip(),
        }

    def _is_quality_output(self, output: Dict[str, Any]) -> bool:
        return bool(output.get('ipa') and output.get('macquarie') and output.get('guidance'))

    async def _analyse_with_minimal_prompt(self, text: str, language: str) -> Optional[Dict[str, Any]]:
        prompt = f"""Give pronunciation fields for this name.
Name: {text}
Language hint: {language}

Return exactly these lines:
LANGUAGE: <language>
DISPLAY_NAME: <name>
IPA: <ipa>
MACQUARIE: <australian-friendly pronunciation>
GUIDANCE: <short guidance>
"""

        try:
            response = await asyncio.wait_for(
                self.client.aio.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config=genai.types.GenerateContentConfig(
                        max_output_tokens=220,
                    ),
                ),
                timeout=min(self.request_timeout_seconds, 7),
            )
            text_out = (getattr(response, "text", "") or "").strip()
            if not text_out:
                return None

            def line_value(key: str) -> str:
                for line in text_out.splitlines():
                    if line.upper().startswith(f"{key}:"):
                        return line.split(":", 1)[1].strip()
                return ""

            inferred_language = line_value("LANGUAGE") or language
            display_name = line_value("DISPLAY_NAME") or text
            ipa = line_value("IPA")
            macquarie = line_value("MACQUARIE")
            guidance = line_value("GUIDANCE")

            if not ipa:
                return None

            return {
                'inferred_language': inferred_language,
                'name_with_diacritics': display_name,
                'romanization_system': None,
                'ipa': ipa,
                'macquarie': macquarie or text,
                'guidance': guidance or "Pronounce slowly and confirm preferred pronunciation with the person.",
                'tone_marks_added': False,
                'ambiguity': None,
                'cultural_notes': "Generated via minimal fallback prompt due structured JSON truncation."
            }
        except Exception:
            return None

    def _fallback_from_name(self, text: str, language: str) -> Dict[str, Any]:
        simplified = "-".join(part for part in text.split() if part).lower()
        return {
            'inferred_language': language,
            'name_with_diacritics': text,
            'romanization_system': None,
            'ipa': f"/{simplified}/" if simplified else '/na/',
            'macquarie': text,
            'guidance': "Pronounce slowly by syllable and confirm with the person if possible.",
            'tone_marks_added': False,
            'ambiguity': None,
            'cultural_notes': "Automated fallback output used due to temporary model formatting failure."
        }

