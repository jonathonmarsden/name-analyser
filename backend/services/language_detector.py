"""
Language detection service using Unicode script ranges.
Detects language origin of names based on character scripts.
"""

import re
from typing import Dict, Tuple


class LanguageDetector:
    """Detects language origin of names using Unicode character ranges."""

    # Unicode script ranges for major language families
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
            (0x0600, 0x06FF),   # Arabic
            (0x0750, 0x077F),   # Arabic Supplement
        ],
        'Devanagari': [  # Hindi, Sanskrit, Marathi, Nepali
            (0x0900, 0x097F),
        ],
        'Thai': [
            (0x0E00, 0x0E7F),
        ],
        'Vietnamese': [
            # Vietnamese uses Latin script with diacritics
            # Will use character analysis
        ],
        'Cyrillic': [
            (0x0400, 0x04FF),   # Cyrillic
        ],
        'Greek': [
            (0x0370, 0x03FF),
        ],
    }

    # Vietnamese diacritics
    VIETNAMESE_CHARS = set('ăâđêôơưàảãáạằẳẵắặầẩẫấậèẻẽéẹềểễếệìỉĩíịòỏõóọồổỗốộờởỡớợùủũúụừửữứựỳỷỹýỵ')

    def detect(self, name: str) -> Tuple[str, float]:
        """
        Detect the language of origin for a name.

        Args:
            name: The name to analyse

        Returns:
            Tuple of (language_name, confidence_score)
        """
        if not name:
            return ('Unknown', 0.0)

        # Count characters by script
        script_counts: Dict[str, int] = {}
        total_chars = 0

        for char in name:
            char_code = ord(char)

            # Check against script ranges
            for script, ranges in self.SCRIPT_RANGES.items():
                for start, end in ranges:
                    if start <= char_code <= end:
                        script_counts[script] = script_counts.get(script, 0) + 1
                        total_chars += 1
                        break

            # Check for Vietnamese diacritics
            if char.lower() in self.VIETNAMESE_CHARS:
                script_counts['Vietnamese'] = script_counts.get('Vietnamese', 0) + 1
                total_chars += 1

        # If no script detected, check for Latin alphabet
        if not script_counts:
            # Check if it's Vietnamese (Latin with diacritics)
            if any(c.lower() in self.VIETNAMESE_CHARS for c in name):
                return ('Vietnamese', 0.85)

            # Otherwise, assume English/Western
            if re.match(r'^[a-zA-Z\s\-\'\.]+$', name):
                return ('English', 0.80)

            return ('Unknown', 0.0)

        # Find dominant script
        dominant_script = max(script_counts.items(), key=lambda x: x[1])
        script_name, count = dominant_script

        # Calculate confidence based on proportion of characters
        confidence = count / len(name) if len(name) > 0 else 0.0

        # Map Devanagari to Hindi (most common)
        if script_name == 'Devanagari':
            script_name = 'Hindi'

        return (script_name, min(confidence, 1.0))

    def get_language_info(self, language: str) -> Dict[str, str]:
        """
        Get additional information about a detected language.

        Args:
            language: The detected language name

        Returns:
            Dictionary with language information
        """
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
