"""
Pronunciation analysis service using Claude API.
Generates accurate IPA and Macquarie Dictionary phonetic notation for names.
Railway deployment ready.
"""

from typing import Optional, Dict, Any
import os
import json
import logging
from anthropic import Anthropic

logger = logging.getLogger(__name__)


class IPAConverter:
    """Converts names to IPA and Macquarie phonetic notation using Claude API."""

    def __init__(self):
        """Initialise pronunciation converter with Claude API client."""
        self.client = None
        api_key = os.getenv('ANTHROPIC_API_KEY')

        if api_key and api_key != 'your_api_key_here':
            try:
                self.client = Anthropic(api_key=api_key)
                logger.info("Claude API initialized for pronunciation analysis")
            except Exception as e:
                logger.warning(f"Could not initialize Claude API: {e}")
                logger.info("Falling back to simplified notation")
        else:
            logger.info("ANTHROPIC_API_KEY not set")
            logger.info("Add your API key to backend/.env for accurate IPA and Macquarie notation")
            logger.info("Run: ./add-api-key.sh")

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
                logger.error(f"Error using Claude API: {e}")
                logger.info("Falling back to simplified notation")

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
        prompt = f"""You are an expert linguist and onomastician (name etymology specialist) helping professional ceremony readers pronounce names respectfully.

CRITICAL TASK: Analyze NAME ETYMOLOGY to infer cultural/linguistic origin, even from plain Latin alphabet spelling.

Name to analyze: {text}
Script detected: {language}

Your task:
1. **PRESERVE EXACT SPELLING** - Never change the name spelling (e.g., "Sylvia" must stay "Sylvia", not become "Silvia")

2. **INFER LANGUAGE/CULTURAL ORIGIN** by analyzing:
   - Name etymology and structure (e.g., "Zhang Wei" = Chinese, "Collinetti" = Italian)
   - Romanization patterns (e.g., "Nguyen" = Vietnamese romanization, "Szcz-" = Polish)
   - Surname + given name combinations and cultural naming conventions
   - For mixed-heritage names (e.g., "Maria Rodriguez-Smith"), analyze each component separately

3. **ADD TONE MARKS ONLY** where they aid pronunciation (ONLY for tonal languages):
   - Chinese pinyin: Add tone marks (Zhang Wei → Zhāng Wěi)
   - Vietnamese: Add tone marks (Nguyen Van An → Nguyễn Văn An)
   - Thai: Add tone marks where applicable
   - **DO NOT add** European accent marks (José, Müller, François) - these will be captured in IPA/phonetics

4. **GENERATE IPA** with full phonetic detail:
   - Use PROPER IPA SYMBOLS, not romanization (e.g., /joꜜsano akʲiko/ NOT "josano akiko")
   - Tone marks for tonal languages (˥˧˩ etc.)
   - Primary and secondary stress marks (ˈ ˌ)
   - Accurate vowel quality and consonant articulation
   - Japanese: Use IPA symbols with pitch accent marks (ꜜ for downstep)

5. **GENERATE MACQUARIE DICTIONARY** phonetic respelling:
   - Australian English approximation
   - Use hyphen-separated syllables
   - Mark stress with CAPITALS: "jahng-WAY", "sihl-VEE-ah"
   - Make it speakable by an Australian English speaker

6. **PRONUNCIATION GUIDANCE**:
   - For tonal languages: Emphasize tone patterns
   - For stress-accent languages: Note primary stress
   - Brief, practical tips for ceremony readers

7. **DETECT ROMANIZATION SYSTEM** (if applicable):
   - Chinese: pinyin vs Wade-Giles vs Yale
   - Note: "Wong" (Cantonese) vs "Huang" (Mandarin pinyin)

8. **FLAG GENUINE AMBIGUITY** only when multiple pronunciations are equally likely:
   - "Sarah" - could be English /ˈsɛərə/ or Arabic /ˈsaːra/
   - "Andrea" - could be Italian /anˈdreːa/ (male) or English /ˈændriə/ (female)
   - Use context clues (surname, full name pattern) to resolve if possible

CRITICAL EXAMPLES:
- Input: "Zhang Wei" → Output: "Zhāng Wěi" (PRESERVE "Zhang Wei" spelling, ADD pinyin tones)
- Input: "Nguyen Van An" → Output: "Nguyễn Văn An" (ADD Vietnamese tones)
- Input: "Sylvia Collinetti" → Output: "Sylvia Collinetti" (DO NOT change to "Silvia")
- Input: "Jose Garcia" → Output: "Jose Garcia" (DO NOT add José accent - not a tone mark)
- Input: "李明" → Output: "Lǐ Míng" (Chinese script detected, add pinyin tones)
- Input: "Maria Rodriguez-Smith" → Mixed origin: Spanish + English (pronounce each component in its origin language)

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
  "cultural_notes": "Brief (1-2 sentences) etymology, meaning, regional origin, or cultural significance. E.g., 'Common surname in northern China, literally means north island' or 'Italian diminutive surname from the Tuscany region, means little bird' or 'Vietnamese given name meaning spring, commonly used for girls born in spring'. Be specific and interesting, avoid generic statements."
}}

Return ONLY the JSON, no other text."""

        try:
            message = self.client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=500,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # Extract the response
            response_text = message.content[0].text.strip()

            # Strip markdown code blocks if present
            if response_text.startswith('```'):
                # Remove ```json or ``` at the start and ``` at the end
                lines = response_text.split('\n')
                if lines[0].startswith('```'):
                    lines = lines[1:]  # Remove first line with ```json
                if lines and lines[-1].strip() == '```':
                    lines = lines[:-1]  # Remove last line with ```
                response_text = '\n'.join(lines).strip()

            # Parse JSON response
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
                # If JSON parsing fails, try to extract information
                logger.error(f"Could not parse Claude response as JSON: {response_text[:200]}")
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
