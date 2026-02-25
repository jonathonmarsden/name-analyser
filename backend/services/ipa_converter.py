"""
Pronunciation analysis service using Gemini API.
Generates accurate IPA and Macquarie Dictionary phonetic notation for names.
Railway deployment ready.
"""

from typing import Optional, Dict, Any
import asyncio
import os
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

    Return EXACTLY these 8 lines, one per line, no markdown, no extra text:
    LANGUAGE: <inferred language>
    DISPLAY_NAME: <same spelling, only add tonal marks where needed>
    IPA: <IPA pronunciation>
    MACQUARIE: <Australian-friendly hyphenated pronunciation with CAPS stress>
    GUIDANCE: <brief practical guidance>
    ROMANIZATION: <pinyin|Wade-Giles|none>
    TONE_MARKS_ADDED: <true|false>
    CULTURAL_NOTES: <brief one sentence>
    """

        try:
            response = await asyncio.wait_for(
                self.client.aio.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config=genai.types.GenerateContentConfig(
                        max_output_tokens=320,
                        temperature=0.2,
                    ),
                ),
                timeout=self.request_timeout_seconds,
            )

            response_text = getattr(response, "text", None)
            if not response_text:
                raise Exception("Empty response from Gemini API")
            response_text = response_text.strip()

            def extract_value(key: str) -> str:
                pattern = rf'^{re.escape(key)}\s*:\s*(.+)$'
                match = re.search(pattern, response_text, re.MULTILINE)
                return match.group(1).strip() if match else ''

            inferred_language = extract_value('LANGUAGE')
            display_name = extract_value('DISPLAY_NAME')
            ipa = extract_value('IPA')
            macquarie = extract_value('MACQUARIE')
            guidance = extract_value('GUIDANCE')
            romanization = extract_value('ROMANIZATION')
            tone_marks = extract_value('TONE_MARKS_ADDED').lower()
            cultural_notes = extract_value('CULTURAL_NOTES')

            if not ipa and not macquarie and not guidance:
                logger.error(f"Could not parse Gemini tagged response: {response_text[:400]}")

                retry_prompt = f"""Give pronunciation for this name: {text}
Return exactly 3 lines, no extra text:
IPA: <ipa>
MACQUARIE: <australian-friendly pronunciation>
GUIDANCE: <very brief tip>
"""

                retry_response = await asyncio.wait_for(
                    self.client.aio.models.generate_content(
                        model=self.model,
                        contents=retry_prompt,
                        config=genai.types.GenerateContentConfig(
                            max_output_tokens=180,
                            temperature=0.1,
                        ),
                    ),
                    timeout=min(self.request_timeout_seconds, 6),
                )

                retry_text = (getattr(retry_response, "text", "") or "").strip()
                if retry_text:
                    ipa = extract_value('IPA') if ipa else ''
                    macquarie = extract_value('MACQUARIE') if macquarie else ''
                    guidance = extract_value('GUIDANCE') if guidance else ''

                    if not ipa:
                        ipa_match = re.search(r'^IPA\s*:\s*(.+)$', retry_text, re.MULTILINE)
                        ipa = ipa_match.group(1).strip() if ipa_match else ''
                    if not macquarie:
                        mac_match = re.search(r'^MACQUARIE\s*:\s*(.+)$', retry_text, re.MULTILINE)
                        macquarie = mac_match.group(1).strip() if mac_match else ''
                    if not guidance:
                        guide_match = re.search(r'^GUIDANCE\s*:\s*(.+)$', retry_text, re.MULTILINE)
                        guidance = guide_match.group(1).strip() if guide_match else ''

                if not ipa and not macquarie and not guidance:
                    return self._simplified_analysis(text, language)

            return {
                'inferred_language': inferred_language,
                'name_with_diacritics': display_name,
                'romanization_system': None if romanization in ('', 'none', 'null') else romanization,
                'ipa': ipa,
                'macquarie': macquarie,
                'guidance': guidance,
                'tone_marks_added': tone_marks == 'true',
                'ambiguity': None,
                'cultural_notes': cultural_notes
            }

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

