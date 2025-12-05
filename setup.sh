#!/bin/bash

# PetDunning Enterprise - Setup Script

echo "🐾 PetDunning Enterprise Setup"
echo "================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip -q

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt -q

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env and add your ANTHROPIC_API_KEY"
    echo ""
    read -p "Press Enter to open .env in your default editor..."
    ${EDITOR:-nano} .env
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run the application:"
echo "  1. source venv/bin/activate"
echo "  2. streamlit run app.py"
echo ""
echo "Or simply run: ./run.sh"
