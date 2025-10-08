"""Services package for name analysis."""

from .language_detector import LanguageDetector
from .ipa_converter import IPAConverter

__all__ = ['LanguageDetector', 'IPAConverter']
