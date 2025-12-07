# CareLoop - 2 Minute Demo Script
**Tagline: Keeping Pets in Care, Revenue in Loop**

---

## 🎬 OPENING (0:00 - 0:20) - The Problem
**[Show Dashboard - Main Screen]**

> "Here's the challenge facing veterinary networks: When a customer's payment fails, traditional dunning systems send a generic 'Pay or Cancel' email.
>
> The result? **60% churn rate**. You lose the customer, you lose the revenue, and worst of all—pets lose access to critical care."

**💡 What to Show:**
- Point to the "At-Risk Customers" table
- Highlight Maria Rodriguez: "Bella with diabetes - $12,000 lifetime value"

---

## 🚀 THE SOLUTION (0:20 - 0:35) - Introduce CareLoop
**[Keep Dashboard visible]**

> "CareLoop changes this. Instead of treating every payment failure the same, our AI agent analyzes **medical urgency** and **payment history** to make intelligent, empathetic interventions.
>
> Watch what happens when Maria's payment fails..."

**💡 What to Show:**
- Quickly point to the 4 metrics at top: Revenue Saved, Churn Prevented, Users Processed, Retention Rate
- Click "Simulate Payment Failure" for **Maria Rodriguez**

---

## 🤖 LIVE DEMO - Part 1: AI Risk Assessment (0:35 - 0:55)
**[Split screen appears: Email (left) + Glass Box (right)]**

> "In under 2 seconds, our multi-agent system does this:
>
> 1️⃣ **Router Agent** pulls Maria's payment history—she's a reliable customer with just one late payment
>
> 2️⃣ It checks ezyVet medical records—Bella has diabetes, needs daily insulin, **high medical urgency**
>
> 3️⃣ **Autonomous scoring**: Medical urgency 90/100 + High LTV + Low payment risk = **Priority Outreach**"

**💡 What to Show:**
- Point to RIGHT PANEL as metrics populate:
  - Payment Risk: "23.5 (LOW)"
  - Medical Urgency: "90.0/100"
  - Retention Priority: "87.4/100"
  - AI Decision: "PRIORITY OUTREACH"

- Scroll through Glass Box panel showing:
  - Router decision log
  - Payment history analysis
  - Medical urgency breakdown

---

## 💬 LIVE DEMO - Part 2: Empathetic Negotiation (0:55 - 1:30)
**[Focus on LEFT PANEL - Email conversation]**

> "Now watch the **Negotiator Agent**—powered by Claude Sonnet 4.5—craft a personalized message:"

**💡 What to Show:**
- Point to the email that appears:
  - Mentions Bella by name
  - Acknowledges diabetes
  - Offers $4.99/month Digital Keeper Plan (vs $50 Premium)
  - No shame, pure empathy

**[Type customer response as Maria]**

> "Let me respond as Maria: 'I don't have the money right now, but I can pay the full amount next Friday.'"

**[Wait for AI response]**

> "Watch the **Intent Extractor**—it understands Maria wants a payment extension, not a downgrade."

**💡 What to Show:**
- Point to RIGHT PANEL:
  - Current Intent: "ASK_FOR_TIME"
  - Confidence: "95%"

- AI offers **two options**:
  1. 14-day extension (stay on Premium)
  2. Digital Keeper Plan ($4.99/mo)

**[Type: "Can I have the 14 days please?"]**

**[Wait for confirmation]**

> "Perfect. Extension granted. **Churn prevented.**"

**💡 What to Show:**
- Success message appears
- Balloons animation
- RIGHT PANEL shows:
  - Conversation Stage: "CLOSING"
  - Negotiation strategy applied

---

## 📊 THE RESULTS (1:30 - 1:45)
**[Point to top dashboard metrics - they should have updated]**

> "Let's look at what just happened:
>
> - **Revenue Saved:** $12,000 in lifetime value preserved
> - **Churn Prevented:** 1 customer retained
> - **Retention Rate:** With CareLoop, we're hitting **85%+ retention** vs the industry standard of 40%"

**💡 What to Show:**
- Updated metrics glowing at top
- Point to Maria's row - status changed or highlighted

---

## 🔬 THE TECH MOAT (1:45 - 2:00) - Close Strong
**[Stay on dashboard or switch to Glass Box panel]**

> "Here's why this is hard to replicate:
>
> ✅ **Compliance-first**: No credit bureaus—we use only internal data (FCRA-safe)
>
> ✅ **Context-aware NLU**: Our intent extractor handles ambiguity—if you say 'yes' to two options, it asks for clarification
>
> ✅ **Glass Box transparency**: Every AI decision is logged and explainable—CFOs can audit exactly why we offered what
>
> ✅ **Built with Claude Sonnet 4.5 and LangGraph**—production-ready agentic architecture
>
> CareLoop: Keeping pets in care, revenue in loop. Thank you."

**💡 What to Show:**
- Briefly expand one Glass Box log entry to show detail
- Show the flowchart in sidebar if time permits
- End on the tagline/logo

---

## 🎯 KEY MESSAGING THEMES

### Throughout the demo, emphasize:
1. **Empathy > Automation** - "AI that cares about Bella, not just revenue"
2. **Medical + Financial Context** - "We're the only dunning system that understands medication adherence"
3. **Transparency** - "Glass Box lets CFOs see exactly how AI makes decisions"
4. **Results** - "85% retention vs 40% industry standard = $X million saved"

---

## 🎨 DEMO TIPS

### **Pacing:**
- Speak confidently but not rushed
- Pause after key reveals (retention score, churn prevented animation)
- Let the UI "breathe"—don't click too fast

### **Vocal Emphasis:**
- **LOUD**: "60% churn rate" (problem), "85% retention" (solution)
- **Soft/Empathetic**: When reading AI messages about Bella
- **Technical/Sharp**: When explaining Glass Box and tech moat

### **Body Language (if presenting live):**
- Point to screen for numbers
- Use hand gestures for "traditional dunning" (binary/rigid) vs "CareLoop" (flexible/smart)
- Smile when balloons appear (shows confidence in product)

### **Backup Plan:**
If demo fails or lags:
- Have a screen recording ready
- Alternatively, walk through the Glass Box panel post-facto
- "This is what the AI decided in 2 seconds..."

---

## 📋 PRE-DEMO CHECKLIST

- [ ] App running on localhost:8501
- [ ] Browser zoomed to 100% (for readability)
- [ ] Maria Rodriguez selected in sidebar
- [ ] Metrics reset to 0 (restart app if needed)
- [ ] Test run completed once (know the flow)
- [ ] Glass Box panel pre-scrolled to show Router decision
- [ ] Type responses ready in a note (for speed):
  - Response 1: "I don't have the money right now, but I can pay the full amount next Friday."
  - Response 2: "Can I have the 14 days please?"

---

## 🎭 ALTERNATIVE: 90-SECOND SPEED VERSION

If time is tight, skip Intent Extractor explanation and just show:
1. Problem (15s)
2. Live demo - one back-and-forth (45s)
3. Results + Glass Box highlight (20s)
4. Tech moat rapid-fire (10s)

---

## 🔥 BONUS: AUDIENCE-SPECIFIC VARIATIONS

### For CFOs/Finance:
- Lead with revenue metrics
- Heavy emphasis on Glass Box auditability
- "Your dunning team spends 40 hours/week on this—we automate it with better outcomes"

### For Technical Audience:
- Open with LangGraph architecture
- Show the code or agent workflow diagram
- Emphasize Claude Sonnet 4.5 + structured outputs

### For Mars Veterinary Health:
- Lead with "Bella's diabetes"
- Emphasize continuity of care importance
- "Every churned customer is a pet losing access to life-saving medication"

---

**Good luck with your demo! 🚀**
