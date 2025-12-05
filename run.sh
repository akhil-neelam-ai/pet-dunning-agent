#!/bin/bash

# PetDunning Enterprise - Run Script

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ Error: .env file not found"
    echo "Please run ./setup.sh first"
    exit 1
fi

# Check if ANTHROPIC_API_KEY is set
if ! grep -q "ANTHROPIC_API_KEY=sk-" .env; then
    echo "⚠️  Warning: ANTHROPIC_API_KEY not configured in .env"
    echo "Please add your API key to .env before running"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Run Streamlit
echo "🚀 Launching PetDunning Enterprise..."
echo "================================"
echo ""
streamlit run app.py
