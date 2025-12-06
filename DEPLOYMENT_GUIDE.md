# 🚀 Deployment Guide for PetDunning Enterprise

## Step 1: Create GitHub Personal Access Token

1. Go to: https://github.com/settings/tokens/new
2. **Name:** `PetDunning Deploy`
3. **Expiration:** 90 days (or custom)
4. **Select scopes:** Check `repo` (Full control of private repositories)
5. Click **"Generate token"**
6. **COPY THE TOKEN** - You won't see it again! (looks like `ghp_xxxxxxxxxxxx`)

## Step 2: Push to GitHub

Open your terminal and run:

```bash
cd /Users/yoyozhang/Downloads/pet-dunning-agent
git push -u origin main
```

When prompted:
- **Username:** `Cokeyzha`
- **Password:** Paste the Personal Access Token you just created

## Step 3: Deploy to Streamlit Community Cloud

1. **Go to:** https://share.streamlit.io/

2. **Sign in** with GitHub account: `Cokeyzha`

3. **Click "New app"**

4. **Fill in the form:**
   - **Repository:** `Cokeyzha/pet-dunning-agent`
   - **Branch:** `main`
   - **Main file path:** `app.py`

5. **Click "Advanced settings"**

6. **Add your API key** in the "Secrets" section:
   ```toml
   ANTHROPIC_API_KEY = "your-anthropic-api-key-here"
   ```

7. **Click "Deploy"**

8. **Wait 2-3 minutes** for deployment

9. **Get your URL!** It will be something like:
   `https://pet-dunning.streamlit.app`

## Step 4: Share with Your Teammate

### Option A: Share the deployed URL
Just send them the Streamlit Cloud URL!

### Option B: Give them GitHub access
1. Go to: https://github.com/Cokeyzha/pet-dunning-agent/settings/access
2. Click **"Invite a collaborator"**
3. Enter their GitHub username
4. Click **"Add [username] to this repository"**

---

## 🎉 Done!

Your PetDunning Enterprise app will be live and accessible to anyone with the URL!

**Questions?** The code is ready to deploy - just follow the steps above.
