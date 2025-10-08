# Product Roadmap

## Version 1.0 ✅ (Current - Deployed)

**Status**: Live at [names.jonathonmarsden.com](https://names.jonathonmarsden.com)

### Features
- ✅ Etymology-based language inference (Claude AI)
- ✅ Unicode script detection (fallback for non-Latin scripts)
- ✅ IPA pronunciation with tone marks
- ✅ Macquarie Dictionary phonetic respelling
- ✅ Tone marks for tonal languages (Chinese, Vietnamese, Thai)
- ✅ Ambiguity detection and flagging
- ✅ Romanization system identification (pinyin, Wade-Giles, etc.)
- ✅ Mixed heritage name handling
- ✅ Cultural context notes
- ✅ Single name web interface
- ✅ FastAPI backend on Railway
- ✅ React frontend on Vercel

### Recent Improvements (2025-10-08)
- ✅ **Strict spelling preservation** - Never alters the original name spelling
- ✅ **Selective diacritic addition** - Only tonal marks (Chinese/Vietnamese), not European accents
- ✅ **Context-aware ambiguity resolution** - Uses surname context to infer pronunciation
- ✅ **Enhanced API response** - Added `romanization_system`, `tone_marks_added`, `ambiguity` fields

---

## Version 1.5 📋 (Planned - Audio Enhancement)

**Goal**: Add audio pronunciation for Mandarin Chinese as proof-of-concept

### Features
- [ ] **Azure Cognitive Services TTS integration**
  - Voice: `zh-CN-XiaoxiaoNeural` (female, natural Mandarin)
  - Quality: Excellent tone accuracy (⭐⭐⭐⭐⭐)
  - Cost: ~$0.000015 per name (~$15 per 1M characters)

- [ ] **Mandarin-only audio trial**
  - Detect if name is Chinese (Mandarin)
  - Generate audio automatically
  - Stream audio to frontend
  - Play button in UI

- [ ] **Frontend audio player**
  - 🔊 Play button for Mandarin names
  - Show "Audio available (Mandarin)" badge
  - Responsive audio controls

- [ ] **API endpoint**: `GET /api/audio/{name_hash}`
  - Cache generated audio (24h)
  - Return MP3/OGG stream
  - Handle errors gracefully

### Technical Requirements
- Azure Cognitive Services account
- Environment variable: `AZURE_SPEECH_KEY` + `AZURE_SPEECH_REGION`
- Audio caching (filesystem or Redis)
- Frontend audio player component

### Success Criteria
- High-quality Mandarin pronunciation
- <2s latency for audio generation
- Positive user feedback from ceremony readers
- **If successful**: Expand to Vietnamese, then other languages

---

## Version 2.0 📋 (Planned - Bulk Processing)

**Goal**: Handle entire ceremony rosters efficiently

### Features
- [ ] **Bulk CSV upload**
  - Upload roster with Name, Degree columns
  - Process 100-500 names in batch
  - Progress indicator

- [ ] **Batch processing API**
  - Endpoint: `POST /api/analyse/batch`
  - Accept JSON array of names
  - Process in parallel (Claude API supports concurrency)
  - Return results array

- [ ] **Caching system**
  - Redis or in-memory LRU cache
  - Cache common names (24h TTL)
  - Reduce API costs by 50%+

- [ ] **Export formats**
  - Downloadable CSV with all pronunciation data
  - PDF pronunciation guide (formatted for printing)
  - Optional: Ceremony script with phonetic spellings

- [ ] **Separate bulk processing app**
  - Optimized UI for roster upload
  - Batch status tracking
  - Error handling (skip invalid names, continue)

### Technical Considerations
- **Cost management**: Caching crucial for bulk processing
- **Rate limiting**: Claude API has concurrency limits
- **Error handling**: Some names may fail, need partial success
- **UX**: Progress bar, estimated time, cancel operation

---

## Version 2.5 📋 (Planned - Multi-Language Audio)

**Goal**: Expand audio to more languages based on v1.5 success

### Phased Audio Rollout
1. ✅ **Mandarin Chinese** (v1.5)
2. Vietnamese - Good TTS available
3. Spanish - Excellent TTS
4. French - Excellent TTS
5. Arabic - Moderate TTS (dialectal challenges)
6. Hindi/Tamil - Good TTS
7. Japanese - Good TTS (pitch accent tricky)
8. Korean - Good TTS

### Language-Specific TTS Selection
- Use Claude's `inferred_language` to select appropriate TTS voice
- Fallback to English if language TTS not available
- Note in UI: "Audio generated for [language]"

### Cost Optimization
- Cache aggressively (audio files larger than text)
- Offer paid tier for unlimited audio?
- Free tier: 10 audio generations/day

---

## Version 3.0 🔮 (Future - Advanced Features)

### Possible Features (To Be Prioritized)

#### **Practice Mode**
- Interactive pronunciation trainer
- Record yourself → compare to reference
- Useful for ceremony readers preparing

#### **Feedback & Corrections**
- User-submitted corrections
- "Report pronunciation issue" button
- Database of corrections
- Requires: Auth, moderation, database

#### **Integration with Ceremony Systems**
- API for university student management systems
- Bulk import from common formats
- Integration with ceremony runsheets

#### **Analytics Dashboard**
- Track most common languages
- API usage statistics
- Error rates by language
- Performance metrics

#### **Native Speaker Recordings** (Forvo Integration)
- For rare names, fetch crowd-sourced recordings
- Forvo API integration
- Gold standard for ambiguous cases
- Cost considerations

#### **Regional Accent Variations**
- Same name, multiple regional pronunciations
- Example: Arabic name in Egyptian vs. Levantine dialect
- Let user select preferred accent

#### **Mobile App**
- iOS/Android native apps
- Offline mode (with cached pronunciation rules)
- Quick lookup for ceremony readers

---

## Technical Debt & Improvements

### High Priority
- [ ] Add rate limiting (prevent API abuse)
- [ ] Implement proper logging (replace `print()` statements)
- [ ] Add request size/length limits
- [ ] Fix CORS wildcard issue (Railway deployment)

### Medium Priority
- [ ] Create unit test suite (pytest)
- [ ] Integration tests for API endpoints
- [ ] Add health check configuration to Railway
- [ ] Improve error messages in frontend
- [ ] Add loading skeleton UI

### Low Priority
- [ ] API usage monitoring dashboard
- [ ] Architecture diagrams
- [ ] Contributing guidelines
- [ ] Changelog automation

---

## Cost Projections

### Current v1.0 Costs (Per Month)
- **Claude API**: ~$5-10 (depending on usage)
- **Railway hosting**: $0 (free tier with $5 credit)
- **Vercel hosting**: $0 (free tier)
- **Total**: ~$5-10/month

### Projected v1.5 Costs (With Mandarin Audio)
- **Claude API**: ~$10-15
- **Azure Speech**: ~$5-10 (depending on audio generation volume)
- **Railway**: $0-5 (may need paid tier)
- **Total**: ~$15-30/month

### Projected v2.0 Costs (With Bulk Processing & Caching)
- **Claude API**: ~$20-30 (higher volume, but caching helps)
- **Redis caching**: $10 (Railway Redis addon)
- **Azure Speech**: ~$10-20
- **Railway**: $5-10 (likely need paid tier)
- **Total**: ~$45-70/month

### Revenue Model (If Needed)
- **Free tier**: 10 names/day, limited audio
- **Pro tier**: $9.99/month - unlimited names, full audio, batch processing
- **Enterprise**: Custom pricing for institutions, bulk API access

---

## User Feedback & Feature Requests

*To be filled in as users provide feedback*

### Requested Features
- [ ] (Add user requests here)

### Reported Issues
- [ ] (Track bugs and issues here)

### Success Stories
- [ ] (Document positive feedback and use cases)

---

## Development Principles

1. **User-Centric**: Build for ceremony readers, prioritize their needs
2. **Quality Over Speed**: Get pronunciation right, even if it takes time
3. **Cultural Respect**: Handle names with dignity and authenticity
4. **Cost-Conscious**: Optimize API usage, cache aggressively
5. **Iterate Quickly**: Ship small improvements frequently
6. **Document Everything**: Maintain clear docs for future development

---

## Notes

- **Azure TTS Trial (v1.5)**: Start with Mandarin only to validate quality and user demand before expanding
- **Bulk Processing (v2.0)**: May warrant separate app/interface optimized for batch operations
- **Caching Strategy**: Critical for cost management at scale
- **User Feedback Loop**: Need to establish feedback mechanism to prioritize features

---

**Last Updated**: 2025-10-08
**Maintainer**: Jonathon Marsden + Claude Code
