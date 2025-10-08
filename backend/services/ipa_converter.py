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
        Use Claude API for comprehensive pronunciation analysis with language inference.

        Args:
            text: The name to analyse
            language: The script-detected language (may be "English" for Romanized text)

        Returns:
            Dictionary with inferred language, IPA, Macquarie notation, romanized form with diacritics, and guidance
        """
        prompt = f"""You are an expert linguist and onomastician (name etymology specialist) for Australian university graduation ceremonies.

CRITICAL TASK: Analyze the NAME ETYMOLOGY to infer the original cultural/linguistic origin, even if written in plain Latin alphabet.

Name to analyze: {text}
Script detected: {language}

Your task:
1. **INFER THE LANGUAGE OF ORIGIN** by analyzing:
   - Name etymology and structure (e.g., "Zhang Wei" is Chinese, "Collinetti" is Italian)
   - Common name patterns from different cultures
   - Surname and given name conventions

2. **Output the name WITH PROPER DIACRITICS/TONES**:
   - Chinese: Add pinyin tone marks (Zhāng Wěi, Lǐ Míng)
   - Vietnamese: Add tone marks (Nguyễn Văn An)
   - Thai: Add tone marks where applicable
   - Italian/European: Add accent marks (é, ü, etc.)

3. Generate accurate IPA with tone marks for tonal languages

4. Generate Macquarie Dictionary phonetic respelling (Australian English approximation)

5. Provide pronunciation guidance emphasizing tones/stress

CRITICAL EXAMPLES:
- Input: "Zhang Wei" → Infer Chinese → Output with tones: "Zhāng Wěi"
- Input: "Nguyen Van An" → Infer Vietnamese → Output: "Nguyễn Văn An"
- Input: "Collinetti" → Infer Italian → Output: proper Italian pronunciation
- Input: "李明" → Detect Chinese script → Output: "Lǐ Míng"

Respond in JSON format:
{{
  "inferred_language": "Chinese|Vietnamese|Italian|Thai|etc",
  "name_with_diacritics": "Name with proper tone marks/accents",
  "ipa": "IPA notation with tone marks",
  "macquarie": "Macquarie phonetic respelling",
  "guidance": "Brief tip on tones/stress/pronunciation"
}}

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
                    'inferred_language': result.get('inferred_language', ''),
                    'name_with_diacritics': result.get('name_with_diacritics', ''),
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
