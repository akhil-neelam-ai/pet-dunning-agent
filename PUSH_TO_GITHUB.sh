#!/bin/bash
# Secure GitHub Push Script with Conflict Resolution

echo "🚀 GitHub Push Script"
echo "====================="
echo ""

# Prompt for GitHub token securely
echo "Enter your GitHub Personal Access Token:"
read -s GITHUB_TOKEN
echo ""

if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ Error: No token provided"
    exit 1
fi

echo "📥 Step 1: Pulling latest changes from remote..."
git pull https://$GITHUB_TOKEN@github.com/Cokeyzha/pet-dunning-agent.git main --allow-unrelated-histories --no-rebase

if [ $? -ne 0 ]; then
    echo "⚠️  Merge conflicts detected. You'll need to resolve them manually."
    echo "Run: git status"
    echo "Then: git add . && git commit -m 'Merge remote changes'"
    unset GITHUB_TOKEN
    exit 1
fi

echo ""
echo "📤 Step 2: Pushing your changes to GitHub..."
git push https://$GITHUB_TOKEN@github.com/Cokeyzha/pet-dunning-agent.git main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Success! Your changes have been pushed to GitHub."
    echo "🔗 View at: https://github.com/Cokeyzha/pet-dunning-agent"
else
    echo ""
    echo "❌ Push failed. Check the error messages above."
    exit 1
fi

# Clear token from memory
unset GITHUB_TOKEN
