# Name Pronunciation Analyser

A comprehensive tool for accurate, respectful pronunciation of names from diverse linguistic and cultural backgrounds.

## Primary Use Case
Professional name readers for University Graduation ceremonies who need to pronounce student names accurately and respectfully.

## Core Features

### Multi-Format Pronunciation Output
- **IPA (International Phonetic Alphabet)**: Standard linguistic representation
- **Macquarie Dictionary Phonetic System**: Australian-specific phonetic notation
- **Original Script with Diacritics**: Proper representation in source language (especially for tonal languages)
- **Audio Pronunciation**: Text-to-speech in appropriate accent/language

### Language & Cultural Analysis
- Language of origin detection
- Cultural background insights
- Name structure analysis (given name/family name order)
- Regional pronunciation variants
- Tonal language support (Chinese, Vietnamese, Thai, etc.)

### Target Languages (Australian University Context)
- Chinese (Mandarin, Cantonese) - with Pinyin and tone marks
- Vietnamese - with full diacritical marks
- Thai - with tone markers and romanisation
- Indian languages (Hindi, Punjabi, Tamil, etc.)
- Indonesian/Malay
- Korean
- Japanese
- Arabic
- And support for any name from any language globally

## Technology Stack

### Frontend
- React with TypeScript
- Vercel/Next.js design system
- Mobile-responsive, WCAG AA compliant
- Audio playback capabilities

### Backend
- Python FastAPI
- Anthropic Claude API for cultural analysis
- Specialised NLP libraries for phonetic conversion
- PostgreSQL for linguistic data

## Project Structure

```
name-analyser/
├── frontend/              # React + TypeScript UI
│   └── src/
│       ├── components/    # UI components
│       ├── services/      # API integration
│       └── utils/         # Helper functions
├── backend/               # Python FastAPI
│   ├── api/              # API endpoints
│   ├── services/         # Core pronunciation logic
│   │   ├── language_detection.py
│   │   ├── ipa_converter.py
│   │   ├── macquarie_phonetic.py
│   │   └── cultural_analyser.py
│   └── data/             # Linguistic databases
└── docs/                 # Documentation
```

## Development Phases

### Phase 1: MVP
- Web interface for name input
- Basic language detection (top 20 languages)
- IPA output
- Simple cultural context

### Phase 2: Enhanced Pronunciation
- Macquarie phonetic system
- Audio generation
- Tonal language support with diacritics

### Phase 3: Advanced Features
- Detailed cultural background insights
- Regional pronunciation variants
- Confidence scoring
- Usage notes for ceremony readers

## Getting Started

See `docs/CLAUDE_CODE_BRIEF.md` for development instructions.

## Design Principles

- **Respectful Representation**: Accurate cultural and linguistic representation
- **Accessibility First**: WCAG AA compliant, clear visual hierarchy
- **Professional Use**: Optimised for ceremony readers who need quick, reliable information
- **Australian Context**: SI units, Australian English spelling, Macquarie phonetic system
