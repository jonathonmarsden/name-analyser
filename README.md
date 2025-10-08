# Name Pronunciation Analyser

A comprehensive tool for accurate, respectful pronunciation of names from diverse linguistic and cultural backgrounds, using **etymology-based language inference** to determine the cultural origin of names even when written in plain Latin alphabet.

**Live Demo**: [https://names.jonathonmarsden.com](https://names.jonathonmarsden.com)

## Primary Use Case
Professional name readers for University Graduation ceremonies who need to pronounce student names accurately and respectfully.

## How It Works

### Etymology-Based Language Inference

Unlike traditional script-based detection, this system **analyzes name etymology** to infer the cultural and linguistic origin:

- **Input**: "Zhang Wei" (plain Latin alphabet, no diacritics)
- **Analysis**: Claude AI analyzes name structure and etymology
- **Inference**: Identifies as Chinese origin
- **Output**: "Zhāng Wěi" (with pinyin tone marks)

### Examples

| Input (as written in ceremony programs) | Inferred Language | Output with Diacritics |
|----------------------------------------|-------------------|------------------------|
| Zhang Wei | Chinese | Zhāng Wěi |
| Nguyen Van An | Vietnamese | Nguyễn Văn An |
| Sylvia Collinetti | Italian | Silvia Collinetti |
| राज कुमार | Hindi (script detected) | राज कुमार |

**Critical Distinction**: The system does NOT simply detect Latin script as "English". It performs onomastic analysis to determine the name's cultural origin and provides pronunciation as a native speaker would say it.

## Core Features

### Multi-Format Pronunciation Output
- **IPA (International Phonetic Alphabet)**: Standard linguistic representation with tone marks
- **Macquarie Dictionary Phonetic System**: Australian-specific phonetic respelling
- **Romanized Form with Diacritics**: Proper tone marks and accents added (Zhāng Wěi, Nguyễn, etc.)
- **Pronunciation Guidance**: Specific tips on tones, stress, and cultural context

### Language & Cultural Analysis
- **Etymology-based language inference** using Claude AI (primary method)
- **Unicode script detection** for non-Latin scripts (fallback method)
- Cultural background insights
- Name structure analysis (given name/family name order)
- Regional pronunciation variants
- Tonal language support (Chinese, Vietnamese, Thai, Yoruba, etc.)

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
- **React with TypeScript** - Type-safe component architecture
- **Vite** - Fast development and build tooling
- **Tailwind CSS** - Vercel design system styling
- **Accessibility**: ARIA labels, live regions, keyboard navigation
- **Deployed on Vercel** - [names.jonathonmarsden.com](https://names.jonathonmarsden.com)

### Backend
- **Python FastAPI** - High-performance async API framework
- **Anthropic Claude 3.5 Sonnet** - Etymology analysis and pronunciation generation
- **slowapi** - Rate limiting (10 requests/minute per IP)
- **Unicode-based script detection** - Fallback for non-Latin scripts
- **Structured logging** - Production-ready error tracking
- **Deployed on Railway** - Free tier with automatic deployments

### Security Features
- ✅ Rate limiting to prevent API abuse
- ✅ Input validation (length limits, special character filtering)
- ✅ CORS configuration with regex pattern matching
- ✅ Secure error handling (no information disclosure)
- ✅ Request timeouts (30-second frontend timeout)
- ✅ Proper logging for debugging without exposing sensitive data

### Key Architecture Decisions

1. **Dual Language Detection System**:
   - **Primary**: Claude AI etymology analysis (for Latin-alphabet names)
   - **Fallback**: Unicode script detection (for Chinese characters, Devanagari, etc.)

2. **No Database Required**: Stateless API design for simplicity and cost-efficiency

3. **Graceful Degradation**: Works without API key (displays setup instructions)

## Project Structure

```
name-analyser/
├── frontend/              # React + TypeScript UI
│   └── src/
│       ├── components/    # UI components
│       │   ├── NameInput.tsx
│       │   └── ResultsDisplay.tsx
│       └── App.tsx        # Main application
├── backend/               # Python FastAPI
│   ├── api/
│   │   └── main.py       # FastAPI routes and CORS configuration
│   └── services/
│       ├── language_detector.py  # Unicode script detection (fallback)
│       └── ipa_converter.py      # Claude AI etymology analysis (primary)
└── docs/                  # Deployment and setup guides
```

## API Response Format

```json
{
  "name": "Zhāng Wěi",                    // Name with diacritics added
  "language": "Chinese",                  // Inferred from etymology
  "ipa": "tʂɑŋ˥ weɪ˨˩",                   // IPA with tone marks
  "macquarie": "jahng way",               // Australian phonetic respelling
  "pronunciation_guidance": "First syllable 'Zhang' has high level tone...",
  "confidence": 1.0,                      // 1.0 for Claude inference
  "language_info": {
    "family_name_first": true,
    "note": "Chinese names typically have family name first..."
  }
}
```

## Getting Started

### Prerequisites
- Python 3.9+
- Node.js 18+
- Anthropic API key (sign up at [console.anthropic.com](https://console.anthropic.com))

### Local Development

1. **Clone the repository**:
```bash
git clone https://github.com/jonathonmarsden/name-analyser.git
cd name-analyser
```

2. **Backend setup**:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Add your Anthropic API key
echo "ANTHROPIC_API_KEY=your_key_here" > .env

# Run the server
cd api
python main.py
```

3. **Frontend setup** (in a new terminal):
```bash
cd frontend
npm install
npm run dev
```

4. **Access the application**:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Deployment

See deployment guides:
- `docs/RAILWAY_DEPLOYMENT.md` - Backend deployment to Railway
- Frontend deploys automatically to Vercel on push to main branch

## Design Principles

- **Respectful Representation**: Accurate cultural and linguistic representation
- **Accessibility First**: WCAG AA compliant, clear visual hierarchy
- **Professional Use**: Optimised for ceremony readers who need quick, reliable information
- **Australian Context**: SI units, Australian English spelling, Macquarie phonetic system
