"""
Pronunciation analysis service using Gemini API.
Generates accurate IPA and Macquarie Dictionary phonetic notation for names.
Railway deployment ready.
"""

from typing import Optional, Dict, Any
import asyncio
import os
import json
import logging
import re
from google import genai

logger = logging.getLogger(__name__)


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
1. Preserve exact spelling in `name_with_diacritics` except adding tone marks for tonal languages.
2. Infer likely linguistic/cultural origin from name patterns.
3. Provide accurate IPA.
4. Provide Australian-English-friendly Macquarie style respelling with stress in CAPS.
5. Keep guidance practical and brief.
6. Flag ambiguity only when genuinely plausible.

Respond in JSON format:
{{
  "inferred_language": "Chinese (Mandarin)|Vietnamese|Italian|Mixed (Spanish/English)|etc",
  "name_with_diacritics": "Name with ONLY tonal marks added (preserve exact spelling otherwise)",
  "romanization_system": "pinyin|Wade-Giles|null",
  "ipa": "IPA with tone marks and stress",
  "macquarie": "Macquarie phonetic respelling",
  "guidance": "Practical pronunciation tip emphasizing tones/stress",
  "tone_marks_added": true|false,
  "ambiguity": null|{{"note": "Could be X or Y. Pronunciation shown assumes X based on [reason]."}},
  "cultural_notes": "Brief 1 sentence etymology or origin note"
}}

Return ONLY the JSON, no other text."""

        try:
            response = await asyncio.wait_for(
                self.client.aio.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config=genai.types.GenerateContentConfig(
                        response_mime_type="application/json",
                        max_output_tokens=900,
                        temperature=0.2,
                    ),
                ),
                timeout=self.request_timeout_seconds,
            )

            response_text = getattr(response, "text", None)
            if not response_text:
                raise Exception("Empty response from Gemini API")
            response_text = response_text.strip()

            if response_text.startswith('```'):
                lines = response_text.split('\n')
                if lines[0].startswith('```'):
                    lines = lines[1:]
                if lines and lines[-1].strip() == '```':
                    lines = lines[:-1]
                response_text = '\n'.join(lines).strip()

            try:
                result = json.loads(response_text)
                return {
                    'inferred_language': result.get('inferred_language', ''),
                    'name_with_diacritics': result.get('name_with_diacritics', ''),
                    'romanization_system': result.get('romanization_system'),
                    'ipa': result.get('ipa', ''),
                    'macquarie': result.get('macquarie', ''),
                    'guidance': result.get('guidance', ''),
                    'tone_marks_added': result.get('tone_marks_added', False),
                    'ambiguity': result.get('ambiguity'),
                    'cultural_notes': result.get('cultural_notes', '')
                }
            except json.JSONDecodeError:
                logger.error(f"Could not parse Gemini response as JSON: {response_text[:400]}")

                extracted = self._extract_fields_from_text(response_text)
                if extracted:
                    return extracted

                return self._simplified_analysis(text, language)

        except asyncio.TimeoutError:
            raise Exception(f"Gemini API timeout after {self.request_timeout_seconds:.1f}s")
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")

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

    def _extract_fields_from_text(self, text: str) -> Optional[Dict[str, Any]]:
        """Best-effort extraction when model output is malformed JSON."""

        def extract_string(key: str) -> Optional[str]:
            pattern = rf'"{re.escape(key)}"\s*:\s*"([^"\\]*(?:\\.[^"\\]*)*)"'
            match = re.search(pattern, text, re.DOTALL)
            if not match:
                return None
            value = match.group(1)
            return bytes(value, "utf-8").decode("unicode_escape")

        def extract_bool(key: str) -> bool:
            pattern = rf'"{re.escape(key)}"\s*:\s*(true|false)'
            match = re.search(pattern, text, re.IGNORECASE)
            if not match:
                return False
            return match.group(1).lower() == 'true'

        extracted = {
            'inferred_language': extract_string('inferred_language') or '',
            'name_with_diacritics': extract_string('name_with_diacritics') or '',
            'romanization_system': extract_string('romanization_system'),
            'ipa': extract_string('ipa') or '',
            'macquarie': extract_string('macquarie') or '',
            'guidance': extract_string('guidance') or '',
            'tone_marks_added': extract_bool('tone_marks_added'),
            'ambiguity': None,
            'cultural_notes': extract_string('cultural_notes') or ''
        }

        if extracted['ipa'] or extracted['macquarie'] or extracted['guidance']:
            return extracted

        return None
