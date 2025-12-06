#!/bin/bash

echo "🚀 PetDunning GitHub Push Helper"
echo "=================================="
echo ""
echo "This script will help you push to GitHub."
echo ""
echo "📝 Steps:"
echo "1. Go to: https://github.com/settings/tokens/new"
echo "2. Name it: 'PetDunning Deploy'"
echo "3. Select scope: 'repo' (full control)"
echo "4. Click 'Generate token'"
echo "5. COPY the token (starts with ghp_)"
echo ""
echo "Press Enter when you have your token ready..."
read -r

echo ""
echo "Now I'll push to GitHub..."
echo ""

git push -u origin main

echo ""
echo "✅ Done! Check your repository at:"
echo "   https://github.com/Cokeyzha/pet-dunning-agent"
echo ""
