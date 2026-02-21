#!/bin/bash
# Quick deployment script for Name Pronunciation Analyser

echo "🚀 Deploying Name Pronunciation Analyser to Vercel"
echo ""

# Check if vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "📦 Vercel CLI not found. Installing..."
    npm install -g vercel
fi

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📝 Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit: Name Pronunciation Analyser"
fi

echo ""
echo "🔑 Make sure you have:"
echo "  1. Signed up at https://vercel.com"
echo "  2. Your Gemini API key ready"
echo ""
read -p "Press Enter to continue with deployment..."

# Login to Vercel
echo ""
echo "🔐 Logging in to Vercel..."
vercel login

# Deploy
echo ""
echo "🚀 Deploying to Vercel..."
vercel

echo ""
echo "✅ Deployment initiated!"
echo ""
echo "Next steps:"
echo "  1. Set environment variable:"
echo "     vercel env add GEMINI_API_KEY production"
echo "  2. Deploy to production:"
echo "     vercel --prod"
echo "  3. Add custom domain in Vercel dashboard:"
echo "     names.jonathonmarsden.com"
echo "  4. Configure Cloudflare DNS (see DEPLOYMENT.md)"
echo ""
echo "📖 For detailed instructions, see: DEPLOYMENT.md"
