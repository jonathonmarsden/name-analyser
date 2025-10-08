# Technical Architecture

## Overview

The Name Pronunciation Analyser uses a **dual-system architecture** for language detection and pronunciation analysis:

1. **Primary**: Claude AI-powered etymology analysis (for Latin-alphabet names)
2. **Fallback**: Unicode script detection (for non-Latin scripts like Chinese characters, Devanagari, etc.)

This document explains the technical design decisions and implementation details.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend (React)                        │
│                    names.jonathonmarsden.com                    │
└─────────────────┬───────────────────────────────────────────────┘
                  │
                  │ HTTPS POST /api/analyse
                  │ { "name": "Zhang Wei" }
                  │
┌─────────────────▼───────────────────────────────────────────────┐
│                    Backend (FastAPI)                            │
│               web-production-972ff.up.railway.app               │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐   │
│  │ 1. Unicode Script Detection (LanguageDetector)         │   │
│  │    - Analyzes Unicode ranges                           │   │
│  │    - Returns: ("English", 0.5) for Latin alphabet      │   │
│  │    - Returns: ("Chinese", 0.95) for CJK characters     │   │
│  └────────────────────────────────────────────────────────┘   │
│                          │                                      │
│  ┌────────────────────────▼───────────────────────────────┐   │
│  │ 2. Etymology Analysis (IPAConverter + Claude API)      │   │
│  │    - Takes: name + script_detected_language            │   │
│  │    - Claude analyzes name structure/etymology          │   │
│  │    - Returns: inferred_language, name_with_diacritics  │   │
│  └────────────────────────────────────────────────────────┘   │
│                          │                                      │
│  ┌────────────────────────▼───────────────────────────────┐   │
│  │ 3. Response Assembly                                    │   │
│  │    - Uses inferred_language (Claude) over script lang   │   │
│  │    - Displays name_with_diacritics                      │   │
│  │    - Includes IPA, Macquarie, guidance                  │   │
│  └────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Etymology-Based Language Inference

### The Problem with Script Detection

Traditional approaches use **character script detection**:
- "Zhang Wei" (Latin alphabet) → Detected as "English" ❌
- User hears English pronunciation /ʒæŋ weɪ/ (wrong!)

### Our Solution: Onomastic Analysis

We use **Claude AI to analyze name etymology**:
- "Zhang Wei" → Analyzes structure → Chinese origin ✅
- Outputs: "Zhāng Wěi" with pinyin tone marks
- User hears Mandarin pronunciation /ʈʂɑŋ˥ weɪ˨˩/ (correct!)

### How It Works

#### Input Processing
```python
# main.py:114-132
name = request.name.strip()  # "Zhang Wei"

# Step 1: Script detection (fallback for non-Latin)
script_language, script_confidence = language_detector.detect(name)
# Returns: ("English", 0.5) - incorrect but useful for rare scripts

# Step 2: Claude etymology analysis
pronunciation = ipa_converter.analyse_pronunciation(name, script_language)
# Claude receives: "Zhang Wei" + hint "English" (from script)
# Claude ignores script hint and analyzes etymology
# Returns: {
#   'inferred_language': 'Chinese',
#   'name_with_diacritics': 'Zhāng Wěi',
#   'ipa': '/ʈʂɑŋ˥ weɪ˨˩/',
#   'macquarie': 'jahng way',
#   'guidance': 'First tone (high level) on Zhang...'
# }

# Step 3: Use Claude's inference (override script detection)
inferred_language = pronunciation.get('inferred_language', script_language)
display_name = pronunciation.get('name_with_diacritics', name)
```

#### Claude Prompt Design

The prompt in `ipa_converter.py:81-121` instructs Claude to:

1. **Analyze etymology**, not just script
   - Example: "Zhang Wei" has Chinese surname structure
   - Example: "Collinetti" has Italian diminutive suffix "-etti"

2. **Infer language of origin**
   - Based on name patterns from different cultures
   - Surname/given name conventions
   - Common name elements (Zhang, Nguyen, -ov, -ski, etc.)

3. **Output with proper diacritics**
   - Chinese: Pinyin tone marks (ā, á, ǎ, à)
   - Vietnamese: Full tone system (ă, â, ê, ơ, ư + various marks)
   - Thai: Tone marks where applicable
   - European: Accent marks (é, ü, ñ, etc.)

4. **Generate pronunciation guidance**
   - Emphasis on tones for tonal languages
   - Stress patterns for non-tonal languages
   - Cultural context where relevant

#### Example Claude Response

```json
{
  "inferred_language": "Chinese",
  "name_with_diacritics": "Zhāng Wěi",
  "ipa": "/ʈʂɑŋ˥ weɪ˨˩/",
  "macquarie": "jahng way",
  "guidance": "First tone (high level) on 'Zhang', third tone (falling-rising) on 'Wei'"
}
```

---

## When Each System Is Used

### Claude Etymology Analysis (Primary)

**Used for**: All names, especially Latin-alphabet romanizations
- "Zhang Wei" → Chinese
- "Nguyen Van An" → Vietnamese
- "Sylvia Collinetti" → Italian
- "Muhammad" → Arabic
- "Smith" → English

**Advantages**:
- ✅ Correctly identifies cultural origin even in Latin script
- ✅ Adds missing diacritics/tone marks
- ✅ Provides culturally appropriate pronunciation
- ✅ Handles mixed-script names

**Limitations**:
- ⚠️ Requires API call (~2-4 seconds)
- ⚠️ Costs per request (minimal with Claude)
- ⚠️ May struggle with very rare names

### Unicode Script Detection (Fallback)

**Used for**: Non-Latin scripts or when Claude fails
- "张伟" (CJK characters) → Chinese
- "राज कुमार" (Devanagari) → Hindi
- "محمد" (Arabic script) → Arabic

**Advantages**:
- ✅ Instant response (no API call)
- ✅ 100% reliable for script detection
- ✅ Free (no API costs)

**Limitations**:
- ❌ Cannot detect language from Latin-alphabet romanizations
- ❌ Treats all Latin text as "English"

### Decision Flow

```python
# Pseudocode
if has_non_latin_script(name):
    # Unicode detection is sufficient
    language = script_detector.detect(name)
    confidence = 0.95
else:
    # Latin alphabet - need etymology analysis
    try:
        result = claude.analyse_etymology(name)
        language = result.inferred_language
        confidence = 1.0  # Claude's inference trusted
    except APIError:
        # Fallback to script detection
        language = "English"  # Assumption
        confidence = 0.5
```

---

## Diacritic Generation

### Why Diacritics Matter

Australian graduation programs print names **without diacritics** due to system limitations:
- Program shows: "Zhang Wei"
- Reader needs to know: "Zhāng Wěi" (tones crucial for pronunciation)

### How We Add Them

Claude AI adds appropriate diacritics based on language:

| Language | Input | Output with Diacritics |
|----------|-------|------------------------|
| Chinese (Mandarin) | Zhang Wei | Zhāng Wěi |
| Vietnamese | Nguyen Van An | Nguyễn Văn An |
| Spanish | Jose Garcia | José García |
| French | Francois | François |
| German | Muller | Müller |

### Tone Marks for Tonal Languages

**Chinese Pinyin** (4 tones + neutral):
- 1st tone (high level): ā, ē, ī, ō, ū
- 2nd tone (rising): á, é, í, ó, ú
- 3rd tone (falling-rising): ǎ, ě, ǐ, ǒ, ǔ
- 4th tone (falling): à, è, ì, ò, ù
- Neutral: a, e, i, o, u

**Vietnamese** (6 tones):
- Level: a, e, i, o, u
- Rising: á, é, í, ó, ú
- Falling: à, è, ì, ò, ù
- Question: ả, ẻ, ỉ, ỏ, ủ
- Tumbling: ã, ẽ, ĩ, õ, ũ
- Heavy: ạ, ệ, ị, ọ, ụ

Plus vowel modifications: ă, â, ê, ô, ơ, ư

---

## API Endpoints

### POST /api/analyse

Analyzes a name and returns comprehensive pronunciation information.

**Request**:
```json
{
  "name": "Zhang Wei"
}
```

**Response**:
```json
{
  "name": "Zhāng Wěi",
  "language": "Chinese",
  "ipa": "/ʈʂɑŋ˥ weɪ˨˩/",
  "macquarie": "jahng way",
  "pronunciation_guidance": "First tone (high level) on 'Zhang', third tone (falling-rising) on 'Wei'",
  "confidence": 1.0,
  "language_info": {
    "family_name_first": true,
    "note": "Chinese names typically have family name first, followed by given name."
  }
}
```

**Error Handling**:
- 400: Empty name
- 500: Internal error (Claude API failure, etc.)

**Performance**:
- With Claude API: ~2-4 seconds
- Without API key: <100ms (returns setup instructions)

### GET /health

Health check endpoint for monitoring.

**Response**:
```json
{
  "status": "healthy"
}
```

---

## Deployment Architecture

### Frontend (Vercel)

- **URL**: https://names.jonathonmarsden.com
- **Platform**: Vercel (free tier)
- **Build**: Vite static site generation
- **Environment Variables**:
  - `VITE_API_URL`: Backend API URL (Railway)
- **Deployment**: Automatic on push to `main` branch

### Backend (Railway)

- **URL**: https://web-production-972ff.up.railway.app
- **Platform**: Railway (free tier with $5 credit)
- **Runtime**: Python 3.9 with uvicorn
- **Build System**: Nixpacks
- **Environment Variables**:
  - `ANTHROPIC_API_KEY`: Claude API key
  - `PORT`: Auto-assigned by Railway
- **Deployment**: Automatic on GitHub push

### Build Configuration

**nixpacks.toml**:
```toml
[phases.setup]
nixPkgs = ["python39", "python39Packages.pip"]

[phases.install]
cmds = ["pip install --break-system-packages -r backend/requirements.txt"]

[start]
cmd = "cd backend/api && python -m uvicorn main:app --host 0.0.0.0 --port $PORT"
```

**Why `--break-system-packages`?**
Railway uses Nix package manager, which has an immutable `/nix/store` filesystem. The flag allows pip to install packages in a user-writable location.

**Why `python -m uvicorn`?**
Packages installed with `--break-system-packages` aren't in the system PATH, so we use Python's module execution to find uvicorn.

### CORS Configuration

```python
# main.py:29-40
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://names.jonathonmarsden.com",
        "https://*.vercel.app"  # ⚠️ Note: May not work (see code review)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Security Considerations

### Current Implementation

✅ **Good practices**:
- API key in environment variable (not hardcoded)
- Input sanitization with `.strip()`
- Error messages don't leak sensitive information
- HTTPS everywhere (Vercel + Railway)
- No database = no SQL injection risk
- React escapes output = no XSS risk

⚠️ **Areas for improvement** (see CODE_REVIEW.md):
- No rate limiting (could lead to API abuse)
- No request size limits
- CORS allows all methods
- Using `print()` instead of proper logging

### Recommended Improvements

1. **Rate Limiting**:
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/analyse")
@limiter.limit("10/minute")
async def analyse_name(request: NameAnalysisRequest):
    # ...
```

2. **Input Length Limits**:
```python
class NameAnalysisRequest(BaseModel):
    name: str = Field(..., max_length=200)
```

3. **API Key Validation**:
```python
if api_key and api_key.startswith('sk-ant-'):
    # Valid Anthropic key format
    self.client = Anthropic(api_key=api_key)
```

---

## Performance Optimization

### Current Metrics

| Operation | Time | Status |
|-----------|------|--------|
| Script detection | <1ms | ✅ Excellent |
| Claude API call | 2-4s | ⚠️ Acceptable |
| Total API response | 2-4s | ⚠️ Acceptable |
| Frontend load | ~300ms | ✅ Good |

### Future Optimizations

1. **Caching Common Names**:
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def analyse_cached(name: str) -> dict:
    return ipa_converter.analyse_pronunciation(name)
```

2. **Redis Cache** (for production scale):
- Cache results for 24 hours
- Reduce API costs for repeated names
- Sub-second responses for cached names

3. **Batch Processing**:
- Process entire ceremony roster at once
- Export results as PDF/CSV
- Pre-generate audio files

---

## Testing

### Manual Testing Completed

✅ Empty input validation
✅ Whitespace handling
✅ Multi-language support (Chinese, Vietnamese, Hindi, Italian, English)
✅ Unicode character handling
✅ API key fallback behavior
✅ CORS functionality

### Missing Automated Tests

The project currently has **no test suite**. Recommended additions:

```python
# tests/test_api.py
def test_analyse_chinese_name():
    response = client.post("/api/analyse", json={"name": "Zhang Wei"})
    assert response.status_code == 200
    data = response.json()
    assert data["language"] == "Chinese"
    assert "tone" in data["pronunciation_guidance"].lower()

def test_analyse_vietnamese_name():
    response = client.post("/api/analyse", json={"name": "Nguyen Van An"})
    assert response.status_code == 200
    assert "Nguyễn" in data["name"]  # Should have diacritics

def test_empty_name():
    response = client.post("/api/analyse", json={"name": ""})
    assert response.status_code == 400
```

---

## Monitoring and Observability

### Current State

- ✅ Health check endpoint (`/health`)
- ❌ No logging framework
- ❌ No error tracking (Sentry, etc.)
- ❌ No usage analytics
- ❌ No API cost monitoring

### Recommended Additions

1. **Structured Logging**:
```python
import logging

logger = logging.getLogger(__name__)

@app.post("/api/analyse")
async def analyse_name(request: NameAnalysisRequest):
    logger.info(f"Analyzing name: {request.name[:20]}...")
    try:
        result = ...
        logger.info(f"Success: {result['language']}")
        return result
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise
```

2. **Usage Tracking**:
- Track most common languages
- Monitor API response times
- Alert on error rate spikes

3. **Cost Monitoring**:
- Log Claude API token usage
- Track monthly API costs
- Set up budget alerts

---

## Future Enhancements

### Short-term (1-2 weeks)

1. Add rate limiting
2. Implement proper logging
3. Create basic test suite
4. Fix CORS wildcard issue

### Medium-term (1-2 months)

1. Add caching layer (Redis or in-memory)
2. Implement batch processing for ceremony rosters
3. Add admin dashboard for usage stats
4. Create downloadable pronunciation guides (PDF)

### Long-term (3+ months)

1. Audio pronunciation generation
2. Regional accent variations
3. Integration with ceremony management systems
4. Machine learning model for rare names
5. Crowd-sourced pronunciation corrections

---

## References

- [Anthropic Claude API Documentation](https://docs.anthropic.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [IPA Chart](https://www.internationalphoneticassociation.org/content/ipa-chart)
- [Macquarie Dictionary](https://www.macquariedictionary.com.au/)
- [Unicode Script Detection](https://unicode.org/reports/tr24/)
