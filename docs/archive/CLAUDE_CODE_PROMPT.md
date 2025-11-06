# Claude Code: Name Pronunciation Analyser - Initial Prompt

Copy and paste this prompt to Claude Code in VS Code to begin development:

---

I need you to build a Name Pronunciation Analyser web application for university graduation ceremony readers. The project structure has been set up at `/Users/jonathonmarsden/Projects/name-analyser`.

## Project Overview
This tool helps ceremony readers pronounce diverse student names accurately and respectfully. It should:
- Accept any name in any language/script
- Detect language of origin and provide cultural context
- Output IPA (International Phonetic Alphabet) notation
- Output Macquarie Dictionary phonetic notation (Australian system)
- Display original script with diacritics for tonal languages (Chinese, Vietnamese, Thai, etc.)
- Generate audio pronunciation

## Key User Stories
**Primary user**: Professional name reader at university graduation ceremonies
- Needs quick, accurate pronunciation guidance
- Must handle names from Chinese, Vietnamese, Thai, Indian, Korean, Japanese, Arabic, and many other languages
- Requires respectful cultural context (e.g., family name order, common pronunciations)

## Technical Stack
- **Frontend**: React + TypeScript with Vite, Vercel design system (Tailwind CSS)
- **Backend**: Python FastAPI
- **Key Libraries**: 
  - epitran (IPA conversion)
  - langdetect or langid (language detection)
  - anthropic (Claude API for cultural analysis - I'll provide API key)
  - gTTS or similar (text-to-speech)

## Development Instructions

### Phase 1: MVP (Start Here)
1. **Set up the development environment**
   - Create frontend: React + TypeScript + Vite in `/frontend`
   - Create backend: FastAPI in `/backend`
   - Set up package.json, requirements.txt, .env templates
   - Install core dependencies

2. **Build basic backend services**
   - Language detection using Unicode script ranges
   - IPA conversion for common languages (focus on Chinese, Vietnamese, English, Hindi first)
   - Simple API endpoint: POST /api/analyse that accepts a name and returns language + IPA

3. **Create minimal frontend**
   - Simple input form for name entry
   - Display area for results (language detected, IPA notation)
   - Clean, professional UI using Vercel/Tailwind design system

4. **Test with sample names**
   - Test Chinese: 张伟 (Zhāng Wěi)
   - Test Vietnamese: Nguyễn Văn An
   - Test English: Smith
   - Verify accuracy

### Phase 2: Enhanced Features (After MVP works)
- Macquarie phonetic conversion (see docs/TECHNICAL_SPECS.md for conversion rules)
- Cultural context using Claude API
- Audio generation
- Tonal language support with proper diacritics

### Phase 3: Polish
- Advanced cultural insights
- Pronunciation variants
- Export functionality
- Accessibility enhancements

## Important Notes
- **Use Australian English spelling** (colour, analyse, centre, etc.)
- **Follow Vercel design system** principles: clean, modern, accessible
- **Reference documentation** in `/docs/` folder:
  - `CLAUDE_CODE_BRIEF.md` - Detailed development brief
  - `TECHNICAL_SPECS.md` - Macquarie phonetic system, tonal language specs
  - `PROJECT_STRUCTURE.md` - File organisation
- **Focus on accuracy first**, then speed
- **Cultural sensitivity** is critical - represent names respectfully

## Getting Started
1. Read the documentation in `/docs/`
2. Set up the development environment (frontend + backend)
3. Build the MVP: name input → language detection → IPA output
4. Ask me for the Anthropic API key when you're ready to integrate Claude for cultural analysis
5. Test thoroughly with diverse names

Let me know when you've completed each phase and I'll review before you proceed to the next.

Begin with Phase 1: Set up the development environment and create the basic scaffolding.
