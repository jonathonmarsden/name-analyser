# 🚀 Quick Start - Name Pronunciation Analyser

## Current Status

✅ **Backend**: Running on http://localhost:8000
✅ **Claude API Integration**: Ready (add API key for accurate IPA)
⏳ **Frontend**: Ready to start

## Quick Start (2 options)

### Option 1: Start Without API Key (Works Immediately)

Open a **new terminal** and run:

```bash
cd /Users/jonathonmarsden/Projects/name-analyser
./start-frontend.sh
```

Then open your browser to: **http://localhost:3000**

The app will work with simplified phonetic notation.

### Option 2: Enable Claude-Powered IPA (Recommended)

For accurate IPA notation, add your Anthropic API key:

```bash
./add-api-key.sh
```

Then restart the backend and start the frontend.

## Test the Application

Try these sample names:

1. **张伟** (Chinese)
2. **Nguyễn Văn An** (Vietnamese)
3. **Smith** (English)
4. **राज कुमार** (Hindi)

## What to Expect

The application will:
- Detect the language of origin
- Show confidence score
- Display phonetic notation (simplified for MVP)
- Provide cultural context (family name order, notes)

## Documentation

- `START_HERE.md` - This file (quick start)
- `ENABLE_CLAUDE_IPA.md` - How to enable Claude-powered IPA conversion
- `PHASE_1_COMPLETE.md` - What's been built and what's next
- `SETUP_GUIDE.md` - Full setup instructions
- `docs/CLAUDE_CODE_BRIEF.md` - Detailed development brief
- `docs/TECHNICAL_SPECS.md` - Technical specifications

## Need Help?

If the backend stopped running:
```bash
./start-backend.sh
```

If you need to reinstall dependencies:
```bash
./setup.sh
```

---

## 🎯 Current Features

✅ Language detection (Chinese, Vietnamese, Hindi, English, Arabic, Thai, Korean, Japanese, etc.)
✅ Cultural context (family name order, pronunciation notes)
✅ IPA conversion with Claude API integration
✅ Automatic fallback (works without API key)
✅ Clean, professional UI (Vercel design system)
✅ REST API with FastAPI
✅ Real-time pronunciation analysis

## 📊 Status

**Phase 1 MVP: COMPLETE** ✅
**Claude IPA Integration: COMPLETE** ✅
**Ready for**: Testing → Phase 2 enhancements

---

**Ready for your review!** 🎉

Try the app, then we can proceed to Phase 2 (Macquarie phonetics, audio, enhanced cultural analysis).
