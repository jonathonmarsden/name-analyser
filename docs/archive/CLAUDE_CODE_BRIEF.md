# Claude Code Development Brief: Name Pronunciation Analyser

## Project Overview

Build a web-based name pronunciation tool for professional ceremony readers (university graduations) to pronounce diverse student names accurately and respectfully.

## Core User Journey

1. User enters a name (any script/language)
2. System analyses and returns:
   - Language of origin
   - Cultural background context
   - IPA pronunciation
   - Macquarie Dictionary phonetic notation
   - Original script with diacritics (for tonal languages)
   - Audio pronunciation
3. User can play audio and see all formats side-by-side

## Technical Requirements

### Frontend (React + TypeScript)
- Clean, professional UI using Vercel design system
- Input field for name entry
- Display panels for:
  - Language/cultural analysis
  - IPA notation
  - Macquarie phonetics
  - Original script with diacritics
  - Audio player
- Mobile-responsive
- WCAG AA accessibility compliance

### Backend (Python FastAPI)
- RESTful API endpoints
- Services for:
  - Language detection (using Unicode script ranges, name databases)
  - IPA conversion (using epitran, eng_to_ipa libraries)
  - Macquarie phonetic conversion
  - Cultural analysis (using Claude API)
  - Text-to-speech audio generation
- Error handling and validation

### Key Linguistic Features

**Tonal Language Support:**
- Chinese: Pinyin with tone marks (Zhāng 张, Lǐ 李)
- Vietnamese: Full diacritics (Nguyễn, Phương)
- Thai: Tone markers and romanisation

**Cultural Context:**
- Name order (family name first/last)
- Regional variants
- Cultural notes for respectful pronunciation

**Macquarie Phonetic System:**
- Australian English-based phonetic notation
- Reference: Macquarie Dictionary pronunciation guide
- Convert IPA to Macquarie format

## Development Priorities

### Phase 1: MVP (Start Here)
1. Set up project scaffolding
   - Frontend: Create React app with TypeScript, Vite
   - Backend: FastAPI with basic structure
   - Environment setup (.env files, requirements.txt, package.json)

2. Basic name input and language detection
   - Simple input form
   - Unicode script detection
   - Return language family

3. IPA conversion for common languages
   - Focus on: Chinese (Mandarin), Vietnamese, English, Hindi
   - Use epitran or similar library

4. Simple UI to display results
   - Name input
   - Detected language
   - IPA output

### Phase 2: Enhanced Features
- Macquarie phonetic conversion
- Tonal language diacritics
- Cultural context using Claude API
- Audio generation (gTTS or similar)

### Phase 3: Polish
- Advanced cultural insights
- Multiple pronunciation variants
- Confidence scoring
- Export/save functionality for ceremony prep

## Data Sources & Libraries

**Python Libraries:**
- `fastapi` - API framework
- `epitran` - IPA conversion
- `langdetect` or `langid` - language detection
- `anthropic` - Claude API for cultural analysis
- `gTTS` or `pyttsx3` - text-to-speech
- `unicodedata` - script detection

**Frontend Libraries:**
- React + TypeScript
- Axios for API calls
- Tailwind CSS (Vercel style)
- Audio player component

**Data Sources:**
- Unihan database (CJK characters)
- Wiktionary API (pronunciation data)
- Behind the Name API (etymology)

## API Structure

### POST /api/analyse
**Request:**
```json
{
  "name": "Nguyễn Văn An"
}
```

**Response:**
```json
{
  "name": "Nguyễn Văn An",
  "language": {
    "primary": "Vietnamese",
    "confidence": 0.95
  },
  "cultural_context": {
    "origin": "Vietnamese",
    "name_order": "Family name first (Nguyễn)",
    "notes": "Nguyễn is the most common Vietnamese surname"
  },
  "pronunciations": {
    "ipa": "ŋwiən˧˥ van˧˧ an˧˧",
    "macquarie": "ngwen vahn ahn",
    "original_script": "Nguyễn Văn An",
    "romanisation": "Nguyen Van An (with tones: Nguyễn¹ Văn² An³)"
  },
  "audio_url": "/audio/generated/nguyen-van-an.mp3"
}
```

## Development Guidelines

### Code Style
- Australian English spelling (colour, analyse, centre)
- SI units
- Clear, commented code
- Type hints in Python
- TypeScript strict mode

### File Structure
```
frontend/
├── src/
│   ├── components/
│   │   ├── NameInput.tsx
│   │   ├── ResultsDisplay.tsx
│   │   └── AudioPlayer.tsx
│   ├── services/
│   │   └── api.ts
│   ├── types/
│   │   └── index.ts
│   └── App.tsx

backend/
├── api/
│   ├── __init__.py
│   └── routes.py
├── services/
│   ├── __init__.py
│   ├── language_detection.py
│   ├── ipa_converter.py
│   ├── macquarie_phonetic.py
│   ├── cultural_analyser.py
│   └── audio_generator.py
├── models/
│   └── schemas.py
├── data/
│   └── (linguistic databases)
└── main.py
```

### Environment Setup
- Python 3.11+
- Node.js 18+
- Create `.env` files for API keys (Anthropic, etc.)
- Requirements.txt for Python dependencies
- package.json for Node dependencies

## Testing Priorities
- Test with diverse names: Chinese, Vietnamese, Thai, Indian, Arabic, European
- Verify tonal accuracy for CJK and Thai
- Test audio quality and accuracy
- Mobile responsiveness
- Accessibility (screen readers, keyboard navigation)

## Success Criteria
1. Accurately detects language for 90%+ of common names in Australian universities
2. Provides correct IPA for major language families
3. Displays original script with proper diacritics
4. Generates intelligible audio pronunciation
5. Provides useful cultural context for ceremony readers
6. Fast response (<2 seconds for full analysis)

## Notes
- Prioritise accuracy over speed initially
- Focus on respectful, culturally-aware representation
- Build for extensibility (easy to add new languages)
- Consider offline mode for ceremony use (pre-load common names)

## Getting Started Command
```bash
cd /Users/jonathonmarsden/Projects/name-analyser
# Claude Code will set up the environment and begin development
```
