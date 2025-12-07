#!/bin/bash
# Resolve merge conflicts by keeping our local changes

echo "🔧 Resolving merge conflicts..."
echo "Using strategy: Keep LOCAL changes (HEAD)"
echo ""

# For each conflicted file, accept our version
git checkout --ours .env.example
git checkout --ours .gitignore
git checkout --ours agents/extractor.py
git checkout --ours agents/negotiator.py
git checkout --ours agents/router.py
git checkout --ours app.py
git checkout --ours requirements.txt
git checkout --ours state.py
git checkout --ours utils/ui_components.py

# Stage the resolved files
git add .env.example
git add .gitignore
git add agents/extractor.py
git add agents/negotiator.py
git add agents/router.py
git add app.py
git add requirements.txt
git add state.py
git add utils/ui_components.py

echo "✅ Conflicts resolved using local changes"
echo ""
echo "📝 Creating merge commit..."

# Commit the merge
git commit -m "Merge remote changes, keeping local implementation

Resolved conflicts by keeping local changes:
- Complete multi-agent system implementation
- Retention scoring algorithm
- Context-aware intent detection
- ezyVet and payment history integration
- Glass Box transparency UI"

if [ $? -eq 0 ]; then
    echo "✅ Merge commit created successfully"
    echo ""
    echo "Now run: ./push_to_github.sh to push to GitHub"
else
    echo "❌ Failed to create merge commit"
    exit 1
fi
