# Technical Specifications

## Macquarie Dictionary Phonetic System

The Macquarie Dictionary uses a simplified phonetic notation system designed for Australian English speakers. This is the target output format alongside IPA.

### Key Differences from IPA
- Uses familiar letter combinations rather than special symbols
- Represents sounds as Australian English speakers would naturally read them
- Stress marks using bold or capital letters

### Conversion Guidelines (IPA → Macquarie)

**Vowels:**
- /iː/ → ee (as in "meet")
- /ɪ/ → i (as in "sit")
- /e/ → e (as in "bed")
- /æ/ → a (as in "cat")
- /ɑː/ → ah (as in "father")
- /ɒ/ → o (as in "hot")
- /ɔː/ → aw (as in "saw")
- /ʊ/ → oo (as in "foot")
- /uː/ → oo (as in "boot")
- /ʌ/ → u (as in "cup")
- /ɜː/ → er (as in "bird")
- /ə/ → uh (as in "about")

**Consonants:**
- /ʃ/ → sh
- /ʒ/ → zh
- /tʃ/ → ch
- /dʒ/ → j
- /θ/ → th (thin)
- /ð/ → th (then)
- /ŋ/ → ng

**Stress:**
- Primary stress: CAPITAL letters or bold
- Secondary stress: indicated by accent mark

### Examples
- Nguyễn: IPA /ŋwiən˧˥/ → Macquarie "ngwen" or "NGWEN"
- Zhang: IPA /ʈʂɑŋ/ → Macquarie "jahng" or "JAHNG"
- Patel: IPA /pəˈtel/ → Macquarie "puh-TEL"

## Tonal Language Specifications

### Chinese (Mandarin)
**Tones:**
1. First tone (ā): High, level
2. Second tone (á): Rising
3. Third tone (ǎ): Falling-rising
4. Fourth tone (à): Falling
5. Neutral tone (a): Light, unstressed

**Pinyin System:**
- Use proper tone marks (māo, máo, mǎo, mào)
- Include tone numbers as alternative (mao1, mao2, mao3, mao4)

**Common Names:**
- 张 (Zhāng) - First tone
- 李 (Lǐ) - Third tone
- 王 (Wáng) - Second tone
- 刘 (Liú) - Second tone
- 陈 (Chén) - Second tone

### Vietnamese
**Diacritical Marks:**
- Tone marks: ◌́ (rising), ◌̀ (falling), ◌̉ (questioning), ◌̃ (creaky), ◌̣ (drop)
- Vowel marks: ă, â, ê, ô, ơ, ư

**Name Structure:**
- Family name + Middle name + Given name
- Example: Nguyễn Văn An (Nguyễn is family name)

**Common Names:**
- Nguyễn (most common surname)
- Trần, Lê, Phạm, Hoàng
- Given names: Anh, Hương, Minh, Phương

### Thai
**Tone System:**
- Mid tone (no mark)
- Low tone (◌̀)
- Falling tone (◌̂)
- High tone (◌́)
- Rising tone (◌̌)

**Romanisation:**
- Royal Thai General System (RTGS)
- Include tone markers where possible

### Korean
**Hangul Romanisation:**
- Use Revised Romanisation of Korean (RR)
- Examples: 김 (Kim), 이 (Lee/Yi), 박 (Park)

**Name Order:**
- Family name first: Kim Min-jun
- May be written Western style: Min-jun Kim

### Japanese
**Romanisation Systems:**
- Hepburn (most common): Satō, Tanaka
- Include long vowel marks: ō, ū

**Name Order:**
- Family name first traditionally: Tanaka Yuki
- Given name first in Western contexts: Yuki Tanaka

## Language Detection Algorithm

### Script-based Detection
1. **Unicode Range Analysis:**
   - CJK Unified Ideographs (U+4E00–U+9FFF): Chinese/Japanese/Korean
   - Hangul (U+AC00–U+D7AF): Korean
   - Thai (U+0E00–U+0E7F): Thai
   - Devanagari (U+0900–U+097F): Hindi/Sanskrit
   - Arabic (U+0600–U+06FF): Arabic/Persian/Urdu

2. **Name Pattern Analysis:**
   - Vietnamese: Presence of specific diacritics (ơ, ư, ă, â, ê, ô)
   - Chinese: Character compounds, common surname characters
   - Korean: Hangul patterns

3. **Database Lookup:**
   - Cross-reference against known name databases
   - Check surname lists by language

### Confidence Scoring
- Script match: 60%
- Pattern match: 25%
- Database match: 15%
- Return confidence level with result

## Cultural Context Guidelines

### Information to Provide
1. **Name Order:**
   - Western: Given name + Family name
   - Eastern: Family name + Given name
   - Specify which applies

2. **Cultural Significance:**
   - Common surnames and their prevalence
   - Regional variations
   - Historical context if relevant

3. **Pronunciation Notes:**
   - Syllable stress patterns
   - Common mispronunciations to avoid
   - Regional accent variations

4. **Respectful Usage:**
   - Formal vs. informal address
   - Title usage
   - Name preference notes

## Audio Generation Specifications

### Text-to-Speech Requirements
- Use language-specific TTS engines when available
- Mandarin Chinese: Use zh-CN locale
- Vietnamese: Use vi-VN locale
- Fallback to closest available accent

### Quality Standards
- Sample rate: 44.1 kHz minimum
- Format: MP3 or WAV
- Clear articulation at moderate pace
- Proper tonal inflection for tonal languages

### Storage
- Generate on-demand or cache common names
- Store in `/audio/generated/` directory
- Filename: sanitised name + language code
- Example: `nguyen-van-an-vi.mp3`

## API Response Standards

### Error Handling
```json
{
  "error": {
    "code": "INVALID_INPUT",
    "message": "Name contains invalid characters",
    "details": "Only Unicode letters and common punctuation allowed"
  }
}
```

### Success Response
Include all available data with null values for unavailable fields:
```json
{
  "name": "Original Input",
  "language": {...},
  "cultural_context": {...},
  "pronunciations": {...},
  "audio_url": "..." or null,
  "confidence": 0.95,
  "alternatives": [] // if multiple interpretations exist
}
```

## Testing Data

### Test Names (Diverse Coverage)
- **Chinese:** 张伟 (Zhāng Wěi), 李娜 (Lǐ Nà)
- **Vietnamese:** Nguyễn Văn An, Trần Thị Hương
- **Thai:** สมชาย (Somchai), นภา (Napha)
- **Indian:** पटेल (Patel), सिंह (Singh), முருகன் (Murugan)
- **Arabic:** محمد (Muhammad), فاطمة (Fatima)
- **Korean:** 김민준 (Kim Min-jun), 이서연 (Lee Seo-yeon)
- **Japanese:** 田中陽子 (Tanaka Yōko), 佐藤太郎 (Satō Tarō)
- **European:** Müller, Søren, García, O'Brien

### Expected Accuracy
- Language detection: >90%
- IPA conversion: >85%
- Cultural context: >80%
- Audio quality: Intelligible and accurate for native speakers
