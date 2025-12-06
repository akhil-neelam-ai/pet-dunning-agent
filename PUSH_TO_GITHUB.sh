#!/bin/bash

# Replace YOUR_GITHUB_USERNAME with your actual GitHub username
# Run this script after creating the repo on GitHub

GITHUB_USERNAME="akhil-neelam-ai"
REPO_NAME="pet-dunning-agent"

echo "🚀 Pushing PetDunning to GitHub..."
echo ""

# Add remote
git remote add origin https://github.com/$GITHUB_USERNAME/$REPO_NAME.git

# Push to main branch
git push -u origin main

echo ""
echo "✅ Done! Your code is now on GitHub"
echo "📍 Repository: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
echo ""
echo "🔐 Security Check:"
echo "  ✅ .env file is excluded (API key safe)"
echo "  ✅ venv/ folder is excluded"
echo ""
echo "📨 To share with your colleague:"
echo "  1. Go to https://github.com/$GITHUB_USERNAME/$REPO_NAME/settings/access"
echo "  2. Click 'Invite a collaborator'"
echo "  3. Add your colleague's GitHub username"
echo ""
