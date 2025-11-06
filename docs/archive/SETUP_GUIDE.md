# Setup Guide - Name Pronunciation Analyser

## Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.9+
- pip

### Installation

1. **Run the setup script:**
   ```bash
   ./setup.sh
   ```

   This will:
   - Create a Python virtual environment
   - Install all Python dependencies
   - Install all Node.js dependencies
   - Create `.env` files from templates

2. **Configure environment variables (optional for MVP):**
   - Edit `backend/.env` if you want to add your Anthropic API key (needed for Phase 2)
   - The MVP works without the API key

### Running the Application

**Option 1: Use the helper scripts**

Terminal 1 - Start backend:
```bash
./start-backend.sh
```

Terminal 2 - Start frontend:
```bash
./start-frontend.sh
```

**Option 2: Manual startup**

Terminal 1 - Backend:
```bash
cd backend
source venv/bin/activate
cd api
python main.py
```

Terminal 2 - Frontend:
```bash
cd frontend
npm run dev
```

### Access the Application

Open your browser and navigate to:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Testing

Test the application with these sample names:

1. **Chinese**: 张伟
2. **Vietnamese**: Nguyễn Văn An
3. **English**: Smith
4. **Hindi**: राज कुमार

## Project Structure

```
name-analyser/
├── frontend/               # React + TypeScript frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   │   ├── NameInput.tsx
│   │   │   └── ResultsDisplay.tsx
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
│
├── backend/               # FastAPI backend
│   ├── api/
│   │   └── main.py       # FastAPI application
│   ├── services/
│   │   ├── language_detector.py
│   │   └── ipa_converter.py
│   └── requirements.txt
│
└── docs/                 # Documentation
```

## Development Notes

### Frontend
- Built with React 18 + TypeScript
- Uses Vite for fast development
- Styled with Tailwind CSS (Vercel design system)
- Automatically proxies `/api/*` requests to backend

### Backend
- FastAPI for REST API
- Language detection using Unicode script ranges
- IPA conversion using epitran library
- CORS enabled for local development

## Troubleshooting

### Backend won't start
- Ensure Python 3.9+ is installed: `python3 --version`
- Activate virtual environment: `source backend/venv/bin/activate`
- Reinstall dependencies: `pip install -r backend/requirements.txt`

### Frontend won't start
- Ensure Node.js 18+ is installed: `node --version`
- Delete `node_modules` and reinstall: `rm -rf frontend/node_modules && cd frontend && npm install`

### API requests failing
- Check backend is running on port 8000
- Check CORS settings in `backend/api/main.py`
- Verify proxy configuration in `frontend/vite.config.ts`

## Next Steps

This is the **Phase 1 MVP**. Once you've verified it works:

1. Test with the sample names
2. Report any issues
3. Ready for **Phase 2**: Macquarie phonetic conversion, cultural context, audio generation

## Support

For issues or questions, refer to:
- `docs/CLAUDE_CODE_BRIEF.md` - Detailed development brief
- `docs/TECHNICAL_SPECS.md` - Technical specifications
- `docs/PROJECT_STRUCTURE.md` - Project organisation
