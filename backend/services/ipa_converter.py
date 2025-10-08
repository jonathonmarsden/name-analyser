"""
Pronunciation analysis service using Claude API.
Generates accurate IPA and Macquarie Dictionary phonetic notation for names.
Railway deployment ready.
"""

from typing import Optional, Dict, Any
import os
import json
from anthropic import Anthropic


class IPAConverter:
    """Converts names to IPA and Macquarie phonetic notation using Claude API."""

    def __init__(self):
        """Initialise pronunciation converter with Claude API client."""
        self.client = None
        api_key = os.getenv('ANTHROPIC_API_KEY')

        if api_key and api_key != 'your_api_key_here':
            try:
                self.client = Anthropic(api_key=api_key)
                print("✓ Claude API initialised for pronunciation analysis")
            except Exception as e:
                print(f"Warning: Could not initialise Claude API: {e}")
                print("Falling back to simplified notation")
        else:
            print("Info: ANTHROPIC_API_KEY not set.")
            print("Add your API key to backend/.env for accurate IPA and Macquarie notation.")
            print("Run: ./add-api-key.sh")

    def analyse_pronunciation(self, text: str, language: str) -> Dict[str, Any]:
        """
        Analyse name pronunciation using Claude API.

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

        # Try Claude API analysis if available
        if self.client:
            try:
                return self._analyse_with_claude(text, language)
            except Exception as e:
                print(f"Error using Claude API: {e}")
                print("Falling back to simplified notation")

        # Fallback to simplified notation
        return self._simplified_analysis(text, language)

    def convert(self, text: str, language: str) -> str:
        """
        Legacy method for backwards compatibility.
        Returns just the IPA notation.
        """
        result = self.analyse_pronunciation(text, language)
        return result.get('ipa', '')

    def _analyse_with_claude(self, text: str, language: str) -> Dict[str, Any]:
        """
        Use Claude API for comprehensive pronunciation analysis.

        Args:
            text: The name to analyse
            language: The detected language

        Returns:
            Dictionary with IPA, Macquarie notation, and guidance
        """
        prompt = f"""You are an expert linguist and phonetician specialising in name pronunciation for Australian university graduation ceremonies.

Analyse this name and provide accurate pronunciation guidance:

Name: {text}
Detected Language: {language}

Your task:
1. Determine the authentic native pronunciation (as a native speaker would say it)
2. Generate accurate IPA (International Phonetic Alphabet) notation
3. Generate Macquarie Dictionary phonetic respelling (Australian English system)
4. Provide brief pronunciation guidance for ceremony readers

IMPORTANT:
- For Chinese names: Use Mandarin pronunciation with proper tones
- For Vietnamese names: Include tone marks
- For names from tonal languages: Preserve tone information
- For English names: Use standard pronunciation (not just spelling)
- Be accurate to how a native speaker would pronounce it

Respond in JSON format:
{{
  "ipa": "IPA notation here",
  "macquarie": "Macquarie phonetic respelling here",
  "guidance": "Brief pronunciation tip (e.g., stress, tones, common errors to avoid)"
}}

Examples of Macquarie notation:
- "John" → "jon"
- "Michael" → "mie·kuhl"
- "Zhang Wei" → "jahng way"
- "Nguyễn" → "ngwin"

Return ONLY the JSON, no other text."""

        try:
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=500,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # Extract the response
            response_text = message.content[0].text.strip()

            # Parse JSON response
            try:
                result = json.loads(response_text)
                return {
                    'ipa': result.get('ipa', ''),
                    'macquarie': result.get('macquarie', ''),
                    'guidance': result.get('guidance', '')
                }
            except json.JSONDecodeError:
                # If JSON parsing fails, try to extract information
                print(f"Could not parse Claude response as JSON: {response_text[:200]}")
                return self._simplified_analysis(text, language)

        except Exception as e:
            raise Exception(f"Claude API error: {str(e)}")

    def _simplified_analysis(self, text: str, language: str) -> Dict[str, Any]:
        """
        Provide simplified analysis without Claude API.

        Args:
            text: The text to analyse
            language: The detected language

        Returns:
            Dictionary with simplified notations
        """
        return {
            'ipa': f"[Add API key for accurate IPA]",
            'macquarie': f"[Add API key for Macquarie notation]",
            'guidance': f"Set ANTHROPIC_API_KEY in backend/.env for accurate pronunciation analysis. Run: ./add-api-key.sh"
        }
