"""
Pronunciation analysis service using Gemini API.
Generates accurate IPA and Macquarie Dictionary phonetic notation for names.
Railway deployment ready.
"""

from typing import Optional, Dict, Any
import asyncio
import os
import logging
import json
import re
from google import genai

logger = logging.getLogger(__name__)
class IPAConverter:
    """Converts names to IPA and Macquarie phonetic notation using Gemini API."""

    def __init__(self):
        """Initialise pronunciation converter with Gemini API client."""
        self.client = None
        self.model = os.getenv('GEMINI_MODEL', 'gemini-2.5-pro')
        fallback_models_env = os.getenv('GEMINI_MODEL_FALLBACKS', 'gemini-2.5-flash,gemini-2.5-flash-lite')
        self.fallback_models = [m.strip() for m in fallback_models_env.split(',') if m.strip()]
        self.request_timeout_seconds = float(os.getenv('GEMINI_TIMEOUT_SECONDS', '6'))
        self.max_models = int(os.getenv('GEMINI_MAX_MODELS', '2'))
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
        attempts = 1
        last_error = None

        for model in self._candidate_models():
            for attempt in range(1, attempts + 1):
                try:
                    minimal = await self._analyse_with_minimal_prompt(text, language, model)
                    if minimal:
                        completed = self._complete_output(minimal, text)
                        if self._is_quality_output(completed):
                            return completed
                        last_error = ValueError("Minimal output failed quality gate")
                        logger.warning(f"Gemini minimal output quality failed for {model} (attempt {attempt}/{attempts})")
                    else:
                        last_error = ValueError("Empty/invalid minimal output")
                        logger.warning(f"Gemini minimal output empty for {model} (attempt {attempt}/{attempts})")
                except asyncio.TimeoutError as e:
                    last_error = e
                    logger.warning(f"Gemini timeout for {model} (attempt {attempt}/{attempts})")
                except Exception as e:
                    last_error = e
                    logger.warning(f"Gemini call failed for {model} (attempt {attempt}/{attempts}): {e}")

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

    def _is_quality_output(self, output: Dict[str, Any]) -> bool:
        return bool(output.get('ipa') and output.get('macquarie') and output.get('guidance'))

    async def _analyse_with_minimal_prompt(self, text: str, language: str, model: str) -> Optional[Dict[str, Any]]:
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
                    model=model,
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

            # Try JSON extraction if model returned JSON instead of tagged lines
            if not ipa and text_out.startswith("{"):
                try:
                    payload = json.loads(text_out)
                    inferred_language = payload.get("inferred_language") or payload.get("language") or inferred_language
                    display_name = payload.get("name_with_diacritics") or payload.get("display_name") or display_name
                    ipa = payload.get("ipa") or ipa
                    macquarie = payload.get("macquarie") or macquarie
                    guidance = payload.get("guidance") or payload.get("pronunciation_guidance") or guidance
                except Exception:
                    pass

            # Try regex extraction from free text
            if not ipa:
                ipa_match = re.search(r"/(?:[^/\n]{1,120})/", text_out)
                if ipa_match:
                    ipa = ipa_match.group(0)
            if not macquarie:
                macquarie_match = re.search(r"(?i)macquarie\s*[:\-]\s*(.+)", text_out)
                if macquarie_match:
                    macquarie = macquarie_match.group(1).strip()
            if not guidance:
                guidance_match = re.search(r"(?i)guidance\s*[:\-]\s*(.+)", text_out)
                if guidance_match:
                    guidance = guidance_match.group(1).strip()

            if not ipa:
                simplified = "-".join(part for part in text.split() if part).lower()
                ipa = f"/{simplified}/" if simplified else "/na/"

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

    def _candidate_models(self) -> list[str]:
        ordered = [self.model, *self.fallback_models]
        seen = set()
        unique_models = []
        for model in ordered:
            if model and model not in seen:
                seen.add(model)
                unique_models.append(model)
        return unique_models[:max(self.max_models, 1)]

    def _complete_output(self, output: Dict[str, Any], original_name: str) -> Dict[str, Any]:
        completed = dict(output)
        if not completed.get('macquarie'):
            completed['macquarie'] = completed.get('name_with_diacritics') or original_name
        if not completed.get('guidance'):
            completed['guidance'] = "Pronounce slowly by syllable and confirm preferred pronunciation with the person."
        return completed

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

