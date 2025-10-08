# Project Setup Complete ✓

## What's Been Created

Your Name Pronunciation Analyser project is now set up at:
**`/Users/jonathonmarsden/Projects/name-analyser`**

### Directory Structure
```
name-analyser/
├── frontend/                 # React + TypeScript (ready for development)
│   └── src/
├── backend/                  # Python FastAPI (ready for development)
│   ├── api/
│   ├── services/
│   └── data/
├── docs/                     # Comprehensive documentation
│   ├── CLAUDE_CODE_BRIEF.md      # Main development instructions
│   ├── TECHNICAL_SPECS.md        # Macquarie system, tonal languages, API specs
│   ├── PROJECT_STRUCTURE.md      # File organisation
│   └── SAMPLE_NAMES.md          # Test data with expected outputs
├── README.md                 # Project overview
├── CLAUDE_CODE_PROMPT.md     # Ready-to-use prompt for Claude Code
└── .gitignore               # Git exclusions

```

### Documentation Files

1. **CLAUDE_CODE_PROMPT.md** ← **START HERE FOR CLAUDE CODE**
   - Complete prompt ready to copy/paste into Claude Code
   - Phase-by-phase development instructions
   - All context needed to begin

2. **docs/CLAUDE_CODE_BRIEF.md**
   - Detailed development brief
   - API structure and examples
   - File structure and guidelines
   - Success criteria

3. **docs/TECHNICAL_SPECS.md**
   - Macquarie Dictionary phonetic system conversion rules
   - Tonal language specifications (Chinese, Vietnamese, Thai, etc.)
   - Language detection algorithms
   - Cultural context guidelines
   - Audio generation specs

4. **docs/SAMPLE_NAMES.md**
   - Test names across all major languages
   - Expected outputs for each
   - Edge cases to handle

5. **docs/PROJECT_STRUCTURE.md**
   - Directory purposes
   - File organisation
   - Development workflow

## How to Use with Claude Code

### Step 1: Open VS Code
```bash
cd /Users/jonathonmarsden/Projects/name-analyser
code .
```

### Step 2: Start Claude Code
In VS Code terminal, launch Claude Code

### Step 3: Copy & Paste This Prompt

Open `CLAUDE_CODE_PROMPT.md` and copy the entire content to Claude Code, OR use this simplified version:

---

**PROMPT FOR CLAUDE CODE:**

Build a Name Pronunciation Analyser for university graduation ceremony readers. Project is at `/Users/jonathonmarsden/Projects/name-analyser`.

**Core functionality:**
- Accept any name (any language/script)
- Output: IPA notation, Macquarie Dictionary phonetics, original script with diacritics, audio pronunciation, cultural context
- Primary languages: Chinese, Vietnamese, Thai, Indian, Korean, Japanese, Arabic

**Tech stack:**
- Frontend: React + TypeScript + Vite (Vercel design system)
- Backend: Python FastAPI
- Libraries: epitran (IPA), langdetect, anthropic (Claude API), gTTS (audio)

**Phase 1 (MVP):**
1. Set up dev environment (frontend + backend)
2. Build language detection + IPA conversion
3. Create basic UI (input → results display)
4. Test with sample names from `docs/SAMPLE_NAMES.md`

**Important:**
- Use Australian English spelling
- Read all docs in `/docs/` folder before starting
- Focus on accuracy and cultural sensitivity
- Build step-by-step, ask for review after each phase

Full documentation is in the `/docs/` folder. Begin with Phase 1: environment setup and MVP.

---

### Step 4: Development Phases

Claude Code will work through:
1. **Phase 1**: Environment setup + MVP (name input → language detection → IPA)
2. **Phase 2**: Macquarie phonetics + cultural context + audio
3. **Phase 3**: Polish, variants, accessibility

### Step 5: Testing

Use sample names from `docs/SAMPLE_NAMES.md`:
- Chinese: 张伟 (Zhāng Wěi)
- Vietnamese: Nguyễn Văn An  
- Thai: สมชาย (Somchai)
- Korean: 김민준 (Kim Min-jun)

## Key Features to Build

✓ Language detection from Unicode scripts
✓ IPA conversion for major languages
✓ Macquarie Dictionary phonetic notation
✓ Original script with diacritics (tonal languages)
✓ Audio pronunciation generation
✓ Cultural context (name order, significance)
✓ Clean, accessible UI (Vercel design system)

## What Claude Code Needs From You

1. **Anthropic API Key** - When ready to integrate Claude for cultural analysis
2. **Feedback** - Review after each phase completion
3. **Testing** - Try the tool with real names from your context

## Success Criteria

- Accurately detects language for 90%+ of names
- Provides correct IPA for major language families
- Displays original script with proper diacritics
- Generates intelligible audio
- Provides useful cultural context
- Responds in <2 seconds

## Next Steps

1. Open project in VS Code
2. Launch Claude Code
3. Paste the prompt from `CLAUDE_CODE_PROMPT.md`
4. Let Claude Code build the MVP
5. Test and iterate

---

**Project is ready for Claude Code development!** 🚀

All documentation, structure, and specifications are in place. Claude Code has everything needed to build this tool from scratch.
