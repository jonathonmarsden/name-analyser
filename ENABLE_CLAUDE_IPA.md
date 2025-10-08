# Enable Claude-Powered IPA Conversion

The IPA converter has been updated to use Claude API for accurate phonetic notation. Follow these steps to enable it:

## Step 1: Get Your Anthropic API Key

1. Go to https://console.anthropic.com/
2. Sign in or create an account
3. Navigate to API Keys
4. Create a new API key and copy it

## Step 2: Add the API Key

Run the helper script:

```bash
./add-api-key.sh
```

Or manually edit `backend/.env`:

```bash
nano backend/.env
```

Replace the line:
```
ANTHROPIC_API_KEY=your_api_key_here
```

With your actual key:
```
ANTHROPIC_API_KEY=sk-ant-xxxxx...
```

Save and exit.

## Step 3: Restart the Backend

1. Stop the current backend (Ctrl+C in the backend terminal)
2. Start it again:

```bash
./start-backend.sh
```

You should see: "Info: Claude API initialised successfully" in the logs.

## What You'll Get

With Claude API enabled:

- **Accurate IPA notation** for all languages
- **Proper pinyin** for Chinese names with tone marks
- **Correct romanization** for Japanese, Korean, Arabic, Thai, Hindi
- **Multiple pronunciation variants** when applicable

### Example Output

**Without API key:**
```
Name: 张伟
IPA: /张伟/ (Pinyin romanization needed - Phase 2)
```

**With API key:**
```
Name: 张伟
IPA: /ʈʂɑŋ weɪ̯/
```

## Testing

Once enabled, test with:

```bash
curl -X POST http://localhost:8000/api/analyse \
  -H "Content-Type: application/json" \
  -d '{"name": "张伟"}'
```

You should see proper IPA notation in the response!

## Cost Information

- Claude API usage is charged per token
- Name conversions use ~100-150 tokens each
- Current pricing: ~$0.003 per name analysis
- Very affordable for graduation ceremony use

## Fallback Behavior

If the API key is not set or invalid:
- The system automatically falls back to simplified notation
- The application continues to work
- You can add the API key later without reinstalling

## Need Help?

- Check the backend logs for error messages
- Verify your API key is correct
- Ensure you have API credits in your Anthropic account
