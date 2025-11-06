# 🚀 Name Pronunciation Analyser

## ✅ Current Status (October 9, 2025)

**🎉 FULLY DEPLOYED AND WORKING IN PRODUCTION!**

- **Live Application**: https://names.jonathonmarsden.com
- **Frontend**: Vercel ✅
- **Backend**: Railway ✅
- **Status**: Fully functional

## Quick Links

### Production
- **Use the App**: https://names.jonathonmarsden.com
- **GitHub**: https://github.com/jonathonmarsden/name-analyser
- **Code Review**: See `CODE_REVIEW.md` (Grade: A-, 8.5/10)

### Documentation
- **Project Summary**: `PROJECT_SUMMARY.md` - Overview and features
- **README**: `README.md` - Technical documentation
- **Code Review**: `CODE_REVIEW.md` - Security and quality review
- **Setup Guide**: `SETUP_GUIDE.md` - Local development setup

## For Local Development

### Prerequisites
- Python 3.9+
- Node.js 18+
- Anthropic API key

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Add your API key
echo "ANTHROPIC_API_KEY=your_key_here" > .env

# Run the server
cd api
python main.py
# Backend runs on http://localhost:8000
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
# Frontend runs on http://localhost:5173
```

## What This App Does

Professional name pronunciation tool for graduation ceremonies:
- **Etymology-based language inference** - Determines cultural origin from name structure
- **IPA notation** - International Phonetic Alphabet with tone marks
- **Macquarie phonetics** - Australian English phonetic respelling
- **Pronunciation guidance** - Tips on stress, tones, and common errors
- **Cultural context** - Family name order and cultural notes

## Tech Stack

- **Frontend**: React + TypeScript + Vite + Tailwind CSS
- **Backend**: Python FastAPI + Anthropic Claude API
- **Deployment**: Vercel (frontend) + Railway (backend)
- **Features**: Rate limiting, Unicode validation, accessibility

## Recommended Improvements (Optional)

The app is working well, but these would make it even better:
1. Add test coverage (currently 0%)
2. Implement caching to reduce API costs
3. Tighten CORS configuration slightly
4. Clean up code duplication

See `CODE_REVIEW.md` for details.

---

**Need help?** Check the documentation files listed above or visit the live app!
