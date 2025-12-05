# ⚡ Quick Start Guide

## 1. Install (2 minutes)

```bash
# Clone/navigate to the project
cd pet-dunning-agent

# Run setup script
./setup.sh
```

The setup script will:
- Create a virtual environment
- Install all dependencies
- Create a `.env` file for you to edit

## 2. Configure API Key (1 minute)

Open `.env` and add your Anthropic API key:

```bash
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

Don't have a Claude API key? Get one at: https://console.anthropic.com/

## 3. Run (30 seconds)

```bash
./run.sh
```

The app will automatically open in your browser at `http://localhost:8501`

## 4. Demo (3 minutes)

### Quick Demo Path:

1. **Select** "Maria Rodriguez (Bella)" from the sidebar dropdown
2. **Click** "🚨 Simulate Payment Failure"
3. **Watch** the AI agent analyze the risk and generate an empathetic message
4. **Type** as Maria: `I can't pay until Friday`
5. **Observe** the intent extraction in the right panel
6. **Type** as Maria: `Yes, do the $5 plan`
7. **Celebrate** the balloons and see metrics update! 🎉

---

## 🆘 Troubleshooting

### Error: "No module named 'streamlit'"
**Fix**: Make sure you activated the virtual environment:
```bash
source venv/bin/activate
```

### Error: "ANTHROPIC_API_KEY not found"
**Fix**: Check your `.env` file has the API key (with no spaces)

### Error: "No such file or directory: data/mock_db.json"
**Fix**: Make sure you're running the app from the `pet-dunning-agent` directory

---

## 📁 File Structure (What's Where)

```
pet-dunning-agent/
├── app.py                      # Start here - main application
├── graph.py                    # LangGraph workflow
├── agents/                     # AI agent logic
│   ├── router.py               # Risk assessment
│   ├── negotiator.py           # Message generation
│   ├── extractor.py            # Intent understanding
│   └── tools.py                # Mock Stripe API
├── data/                       # Demo data
│   ├── mock_db.json            # User profiles
│   └── medical_risk_tiers.json # Risk configuration
├── utils/                      # UI components
└── README.md                   # Full documentation
```

---

## 🎯 What to Expect

### First Run
- Metrics will all be zero
- Select a user to start a demo
- Each simulation is independent

### Successful Demo
- ✅ AI generates personalized message mentioning pet name
- ✅ Intent extraction shows in right panel
- ✅ Metrics update in real-time
- ✅ Balloons appear on success

### Glass Box Panel (Right Side)
Shows AI reasoning:
- **Router**: Risk assessment and decision
- **Extractor**: Intent detection with confidence
- **Negotiator**: Message generation strategy
- **Tool Executor**: API calls (Stripe, Database)

---

## 💡 Pro Tips

1. **Try different users**: See how AI treats high-risk vs low-risk pets differently
2. **Check the plan comparison**: Sidebar has Premium vs Bridge feature table
3. **Watch the metrics**: Top dashboard updates with each successful retention
4. **Read the reasoning**: Right panel shows exactly why AI made each decision

---

## 🚀 Next Steps

After the demo works:
- Read `DEMO_GUIDE.md` for presentation tips
- Customize `data/mock_db.json` with your own scenarios
- Explore `data/medical_risk_tiers.json` to adjust risk scoring
- Check `README.md` for full documentation

---

**Need help?** Check the full README or open an issue.

**Ready to present?** Read the DEMO_GUIDE for speaking points.

---

Built with Claude Sonnet 4.5 🤖
