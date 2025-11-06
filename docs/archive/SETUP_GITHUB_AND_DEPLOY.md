# Complete Production Deployment Guide

## Step 1: Push to GitHub (2 minutes)

### Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `name-analyser`
3. Description: `Name Pronunciation Analyser for graduation ceremonies`
4. Visibility: **Public** (required for Railway free tier) or **Private** (works with Railway paid)
5. **DO NOT** check "Add a README file"
6. Click **"Create repository"**

### Push Your Code

After creating the repo, GitHub shows you commands. Run these in your terminal:

```bash
# Navigate to project
cd /Users/jonathonmarsden/Projects/name-analyser

# Check current status
git status

# Add remote (replace USERNAME with your GitHub username)
git remote add origin https://github.com/USERNAME/name-analyser.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

**Common GitHub usernames to use:**
- Your main GitHub account
- `carbtallys` (if that's your account based on Vercel deployments)
- Create a new account if needed at https://github.com/signup

## Step 2: Deploy Backend to Railway (3 minutes)

### Create Railway Account

1. Go to https://railway.app
2. Click **"Login with GitHub"**
3. Authorize Railway to access your GitHub account
4. **Important**: Allow access to the `name-analyser` repository

### Deploy from GitHub

1. In Railway dashboard, click **"New Project"**
2. Click **"Deploy from GitHub repo"**
3. Select **`name-analyser`** from the list
4. Railway will:
   - Auto-detect it's a Python project
   - Read the `Procfile` for startup command
   - Install dependencies from `backend/requirements.txt`
   - Start deploying (takes 2-3 minutes)

### Add Environment Variable

1. While it's deploying, click on your service
2. Go to **"Variables"** tab
3. Click **"New Variable"**
4. Add:
   - **Variable**: `ANTHROPIC_API_KEY`
   - **Value**: `YOUR_ANTHROPIC_API_KEY_HERE`
5. Click **"Add"**
6. Railway will automatically redeploy with the new variable

### Generate Public Domain

1. Go to **"Settings"** tab
2. Scroll to **"Networking"** section
3. Click **"Generate Domain"**
4. You'll get a URL like: `https://name-analyser-production.up.railway.app`
5. **Copy this URL** - you'll need it for the next step

### Test Railway Deployment

```bash
# Test the API (replace with your actual Railway URL)
curl -X POST https://your-app.up.railway.app/api/analyse \
  -H "Content-Type: application/json" \
  -d '{"name": "张伟"}'
```

You should get back JSON with IPA, Macquarie notation, etc.

## Step 3: Connect Vercel Frontend to Railway Backend (2 minutes)

### Add Environment Variable to Vercel

```bash
# Navigate to project
cd /Users/jonathonmarsden/Projects/name-analyser

# Add Railway URL to Vercel
vercel env add VITE_API_URL production

# When prompted, paste your Railway URL with /api:
# https://your-app.up.railway.app/api
```

### Redeploy Frontend

```bash
# Deploy to production
vercel --prod
```

This will rebuild the frontend with the Railway API URL and deploy to `names.jonathonmarsden.com`.

## Step 4: Test Production App

1. Visit https://names.jonathonmarsden.com
2. Enter a name: `张伟`
3. Click "Analyse"
4. You should see:
   - IPA: `tʂɑŋ˥˥ weɪ̯˥˩`
   - Macquarie: `jahng way`
   - Pronunciation guidance
   - Cultural context

### Test Multiple Names

- **Chinese**: 张伟
- **Vietnamese**: Nguyễn Văn An
- **English**: Jonathon Marsden
- **Hindi**: राज कुमार

## Architecture

```
User Browser
    ↓
https://names.jonathonmarsden.com (Vercel)
    ↓ HTTPS
https://name-analyser-production.up.railway.app/api (Railway)
    ↓ HTTPS
Anthropic Claude API
```

## Costs

- **Vercel**: $0/month (free tier)
- **Railway**: $1-2/month (within $5 free credit)
- **Cloudflare**: $0/month (free tier)
- **Claude API**: ~$0.003 per analysis

**Total**: ~$1-2/month

## Troubleshooting

### Railway Build Fails

Check deployment logs in Railway:
1. Click on your service
2. Click "Deployments" tab
3. Click latest deployment
4. View logs

Common issues:
- Missing `Procfile` (already included ✓)
- Wrong Python version (using 3.9+ ✓)
- Missing dependencies (check `backend/requirements.txt`)

### Frontend Can't Connect to Backend

1. Check Railway logs for errors
2. Verify `ANTHROPIC_API_KEY` is set in Railway
3. Test Railway endpoint directly with curl
4. Check Vercel environment variable is set correctly:
   ```bash
   vercel env ls
   ```

### CORS Errors

Backend already has CORS configured in `backend/api/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Success Checklist

- [ ] Code pushed to GitHub
- [ ] Railway project created and deployed
- [ ] `ANTHROPIC_API_KEY` added to Railway
- [ ] Railway domain generated
- [ ] Railway API tested with curl
- [ ] Vercel environment variable `VITE_API_URL` added
- [ ] Frontend redeployed to Vercel
- [ ] App tested at names.jonathonmarsden.com
- [ ] Multiple name types tested

## Next Steps After Deployment

1. **Monitor Railway**: Keep an eye on usage in Railway dashboard
2. **Add Custom Domain** (optional):
   - Railway: `api.jonathonmarsden.com`
   - Add CNAME in Cloudflare pointing to Railway
3. **Enable Analytics** (optional): Add Vercel Analytics
4. **Phase 2 Features**:
   - Audio pronunciation
   - Batch processing
   - Export functionality

## Support

- Railway Documentation: https://docs.railway.app
- Vercel Documentation: https://vercel.com/docs
- This project's docs: See `RAILWAY_DEPLOYMENT.md`

---

**Your app will be live at**: https://names.jonathonmarsden.com

**Production-ready and permanent!** 🎉
