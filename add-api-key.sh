#!/bin/bash
# Script to add Anthropic API key to the backend .env file

echo "🔑 Add Anthropic API Key"
echo ""
echo "This will enable Claude-powered IPA conversion for accurate pronunciation."
echo ""
read -p "Enter your Anthropic API key: " api_key

if [ -z "$api_key" ]; then
    echo "❌ No API key provided. Exiting."
    exit 1
fi

# Update the .env file
cd backend
if [ -f ".env" ]; then
    # Replace the API key line
    if grep -q "ANTHROPIC_API_KEY=" .env; then
        # Using | as delimiter since API keys may contain /
        sed -i.bak "s|ANTHROPIC_API_KEY=.*|ANTHROPIC_API_KEY=$api_key|" .env
        rm .env.bak 2>/dev/null
    else
        echo "ANTHROPIC_API_KEY=$api_key" >> .env
    fi
    echo "✅ API key added to backend/.env"
    echo ""
    echo "Restart the backend for changes to take effect:"
    echo "  1. Stop the current backend (Ctrl+C in the backend terminal)"
    echo "  2. Run: ./start-backend.sh"
else
    echo "❌ Error: backend/.env file not found"
    echo "Run ./setup.sh first"
    exit 1
fi
