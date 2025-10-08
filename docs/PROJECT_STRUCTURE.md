# Name Pronunciation Analyser - Project Structure

## Directory Overview

```
name-analyser/
├── frontend/                 # React + TypeScript application
│   └── src/
│       ├── components/       # React components (to be created)
│       ├── services/         # API integration (to be created)
│       └── utils/            # Helper functions (to be created)
│
├── backend/                  # Python FastAPI application
│   ├── api/                  # API routes and endpoints
│   ├── services/             # Core business logic
│   │   ├── language_detection.py
│   │   ├── ipa_converter.py
│   │   ├── macquarie_phonetic.py
│   │   ├── cultural_analyser.py
│   │   └── audio_generator.py
│   └── data/                 # Linguistic databases and datasets
│
└── docs/                     # Project documentation
    ├── CLAUDE_CODE_BRIEF.md  # Development instructions
    ├── TECHNICAL_SPECS.md    # Technical specifications
    └── PROJECT_STRUCTURE.md  # This file
```

## File Purposes

### Frontend
- **components/**: Reusable React components
  - NameInput.tsx - Input form for name entry
  - ResultsDisplay.tsx - Display pronunciation results
  - AudioPlayer.tsx - Audio playback component
  
- **services/**: API communication layer
  - api.ts - Axios/fetch wrapper for backend calls
  
- **utils/**: Helper functions
  - formatters.ts - Text formatting utilities
  - validators.ts - Input validation

### Backend
- **api/**: HTTP endpoints and routing
  - routes.py - Main API routes
  - __init__.py - Package initialisation
  
- **services/**: Core pronunciation logic
  - language_detection.py - Detect language from name
  - ipa_converter.py - Convert to IPA notation
  - macquarie_phonetic.py - Convert to Macquarie system
  - cultural_analyser.py - Provide cultural context
  - audio_generator.py - Generate pronunciation audio
  
- **data/**: Reference data
  - Name databases by language
  - IPA to Macquarie mapping tables
  - Cultural context templates

### Documentation
- **CLAUDE_CODE_BRIEF.md** - Instructions for Claude Code development
- **TECHNICAL_SPECS.md** - Detailed technical specifications
- **PROJECT_STRUCTURE.md** - This file (project organisation)

## Development Workflow

1. **Setup Phase**: Claude Code creates environment files, installs dependencies
2. **Backend First**: Build API endpoints and core services
3. **Frontend Integration**: Create UI and connect to backend
4. **Testing**: Verify with diverse name samples
5. **Refinement**: Improve accuracy and user experience

## Configuration Files (To Be Created)

### Backend
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (API keys)
- `main.py` - FastAPI application entry point

### Frontend
- `package.json` - Node dependencies
- `vite.config.ts` - Build configuration
- `tsconfig.json` - TypeScript configuration
- `.env` - Environment variables (API endpoint)

### Root
- `.gitignore` - Git exclusions
- `README.md` - Project overview (already created)

## Next Steps for Claude Code

1. Initialise project with package managers
2. Set up development environment
3. Create core service modules
4. Build API endpoints
5. Develop frontend components
6. Integrate and test
