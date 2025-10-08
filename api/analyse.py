"""
Vercel serverless function for name pronunciation analysis.
Native Python handler without FastAPI/Mangum.
"""

import json
import os
import re
from typing import Dict, Tuple, Any
from anthropic import Anthropic


# Language detection code
class LanguageDetector:
    """Detects language origin of names using Unicode character ranges."""

    SCRIPT_RANGES = {
        'Chinese': [
            (0x4E00, 0x9FFF),   # CJK Unified Ideographs
            (0x3400, 0x4DBF),   # CJK Extension A
            (0x20000, 0x2A6DF), # CJK Extension B
        ],
        'Japanese': [
            (0x3040, 0x309F),   # Hiragana
            (0x30A0, 0x30FF),   # Katakana
        ],
        'Korean': [
            (0xAC00, 0xD7AF),   # Hangul Syllables
            (0x1100, 0x11FF),   # Hangul Jamo
        ],
        'Arabic': [
            (0x0600, 0x06FF),
            (0x0750, 0x077F),
        ],
        'Devanagari': [
            (0x0900, 0x097F),
        ],
        'Thai': [
            (0x0E00, 0x0E7F),
        ],
        'Cyrillic': [
            (0x0400, 0x04FF),
        ],
        'Greek': [
            (0x0370, 0x03FF),
        ],
    }

    VIETNAMESE_CHARS = set('ăâđêôơưàảãáạằẳẵắặầẩẫấậèẻẽéẹềểễếệìỉĩíịòỏõóọồổỗốộờởỡớợùủũúụừửữứựỳỷỹýỵ')

    def detect(self, name: str) -> Tuple[str, float]:
        if not name:
            return ('Unknown', 0.0)

        script_counts: Dict[str, int] = {}
        total_chars = 0

        for char in name:
            char_code = ord(char)
            for script, ranges in self.SCRIPT_RANGES.items():
                for start, end in ranges:
                    if start <= char_code <= end:
                        script_counts[script] = script_counts.get(script, 0) + 1
                        total_chars += 1
                        break

            if char.lower() in self.VIETNAMESE_CHARS:
                script_counts['Vietnamese'] = script_counts.get('Vietnamese', 0) + 1
                total_chars += 1

        if not script_counts:
            if any(c.lower() in self.VIETNAMESE_CHARS for c in name):
                return ('Vietnamese', 0.85)
            if re.match(r'^[a-zA-Z\s\-\'\.]+$', name):
                return ('English', 0.80)
            return ('Unknown', 0.0)

        dominant_script = max(script_counts.items(), key=lambda x: x[1])
        script_name, count = dominant_script
        confidence = count / len(name) if len(name) > 0 else 0.0

        if script_name == 'Devanagari':
            script_name = 'Hindi'

        return (script_name, min(confidence, 1.0))

    def get_language_info(self, language: str) -> Dict[str, Any]:
        info = {
            'Chinese': {
                'family_name_first': True,
                'note': 'Chinese names typically have family name first, followed by given name.',
            },
            'Japanese': {
                'family_name_first': True,
                'note': 'Japanese names typically have family name first in traditional format.',
            },
            'Korean': {
                'family_name_first': True,
                'note': 'Korean names have family name first, usually one syllable.',
            },
            'Vietnamese': {
                'family_name_first': True,
                'note': 'Vietnamese names have family name first. Tones are important for pronunciation.',
            },
            'Hindi': {
                'family_name_first': False,
                'note': 'Indian names vary by region. Given name typically comes first.',
            },
            'Thai': {
                'family_name_first': False,
                'note': 'Thai names have given name first. Nicknames are commonly used.',
            },
            'Arabic': {
                'family_name_first': False,
                'note': 'Arabic names often include patronymic (father\'s name) and family name.',
            },
            'English': {
                'family_name_first': False,
                'note': 'Western names typically have given name first, family name last.',
            },
        }
        return info.get(language, {
            'family_name_first': False,
            'note': 'Name structure varies by culture.',
        })


def analyse_with_claude(text: str, language: str, api_key: str) -> Dict[str, Any]:
    """Use Claude API for pronunciation analysis."""
    client = Anthropic(api_key=api_key)

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

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )

    response_text = message.content[0].text.strip()
    result = json.loads(response_text)

    return {
        'ipa': result.get('ipa', ''),
        'macquarie': result.get('macquarie', ''),
        'guidance': result.get('guidance', '')
    }


def handler(event, context):
    """Vercel serverless function handler."""
    from http.server import BaseHTTPRequestHandler
    from urllib.parse import parse_qs
    import io

    # Handle CORS
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json',
    }

    # Handle preflight
    method = event.get('httpMethod') or event.get('method', 'POST')
    if method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }

    try:
        # Parse request body
        body = event.get('body', '{}')
        if isinstance(body, str):
            data = json.loads(body)
        else:
            data = body

        name = data.get('name', '').strip()

        if not name:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'Name is required'})
            }

        # Detect language
        detector = LanguageDetector()
        language, confidence = detector.detect(name)
        language_info = detector.get_language_info(language)

        # Get API key
        api_key = os.getenv('ANTHROPIC_API_KEY')

        if not api_key:
            return {
                'statusCode': 500,
                'headers': headers,
                'body': json.dumps({'error': 'API key not configured'})
            }

        # Analyse pronunciation
        pronunciation = analyse_with_claude(name, language, api_key)

        # Build response
        response_data = {
            'name': name,
            'language': language,
            'ipa': pronunciation['ipa'],
            'macquarie': pronunciation['macquarie'],
            'pronunciation_guidance': pronunciation['guidance'],
            'confidence': confidence,
            'language_info': language_info
        }

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(response_data)
        }

    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e), 'detail': error_detail})
        }
