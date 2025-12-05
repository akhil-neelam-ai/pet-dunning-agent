# 🐾 PetDunning Setup for Collaborators

## Prerequisites
- Python 3.9+
- Anthropic API Key (get at https://console.anthropic.com/)

## Quick Setup (5 minutes)

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/pet-dunning-agent.git
cd pet-dunning-agent
```

### 2. Run Setup Script
```bash
./setup.sh
```

This will:
- Create a virtual environment
- Install all dependencies
- Create a `.env` file for you to edit

### 3. Add Your API Key
```bash
nano .env
```

Replace `your_api_key_here` with your Anthropic API key:
```
ANTHROPIC_API_KEY=sk-ant-api03-your-actual-key-here
```

Save and exit (Ctrl+X, then Y, then Enter)

### 4. Run the App
```bash
./run.sh
```

The app will open at http://localhost:8501

---

## 🎮 Demo the App

1. **Select** "Maria Rodriguez (Bella)" from sidebar
2. **Click** "🚨 Simulate Payment Failure"
3. **Type** as Maria: `I can't pay right now`
4. **Watch** the AI offer the Bridge Plan
5. **Type**: `Yes, switch me to the $5 plan`
6. **Celebrate** the balloons! 🎉

---

## 📚 Documentation

- **README.md** - Full project documentation
- **QUICKSTART.md** - 3-minute setup guide
- **DEMO_GUIDE.md** - Presentation script for hackathon

---

## 🔒 Security Notes

- **NEVER** commit your `.env` file
- The `.gitignore` is already configured to exclude it
- If you accidentally commit secrets, rotate your API key immediately

---

## 🐛 Troubleshooting

### Error: "No module named 'streamlit'"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Error: "API key not found"
Check your `.env` file has the correct format with no spaces:
```
ANTHROPIC_API_KEY=sk-ant-your-key
```

### Error: "Low credit balance"
Add credits at https://console.anthropic.com/settings/billing

---

## 🤝 Contributing

To make changes:
```bash
git checkout -b feature/your-feature-name
# Make your changes
git add .
git commit -m "Description of changes"
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

---

Built with ❤️ using Claude Sonnet 4.5
