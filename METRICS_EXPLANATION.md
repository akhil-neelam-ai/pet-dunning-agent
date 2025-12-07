# CareLoop Metrics Explanation Guide
**For Demo & Questions**

---

## 🔍 Current State Metrics Breakdown

### **ROW 1: Conversation Context**

#### 1. **Conversation Stage**
- **What it shows:** Where we are in the customer conversation
- **Possible values:**
  - `INITIAL` - First outreach message being sent
  - `NEGOTIATING` - Customer responded, AI is discussing options
  - `OBJECTION_HANDLING` - Customer declined, AI offering alternatives
  - `CLOSING` - Agreement reached or final decision made
  - `COMPLETED` - Conversation ended (success or churn)

**Why it matters:** Shows the conversation flow in real-time. CFOs can see how many touches it takes to retain a customer.

---

#### 2. **Current Plan**
- **What it shows:** The subscription plan the customer is currently on
- **Possible values:**
  - `PREMIUM` - $50/month full-featured plan
  - `BRIDGE` - $5/month temporary hardship plan
  - `BASIC` - Standard plan (if applicable)

**Why it matters:** Context for what the customer is paying and what we're trying to retain them on.

---

#### 3. **Payment Risk**
- **What it shows:** Risk score (0-100) + tier based on internal payment history
- **How it's calculated:**
  - Failure rate (0-40 points): % of failed payments
  - Late payment rate (0-30 points): % of late payments
  - Days overdue (0-20 points): Current outstanding balance
  - Dispute history (0-10 points): Chargebacks/disputes

- **Tiers:**
  - `LOW (0-25)` - Excellent payment history, very reliable
  - `MODERATE (26-50)` - Some issues but manageable
  - `HIGH (51-75)` - Frequent problems, higher risk
  - `CRITICAL (76-100)` - Severe payment issues

**Why it matters:** Helps AI decide WHICH offer to make. Low risk = maybe just needs payment extension. High risk = might need Bridge Plan with gentler terms.

**Key point:** This uses ONLY internal data (no credit bureaus), so it's FCRA-compliant.

---

### **ROW 2: Combined Risk Assessment**

#### 4. **Risk Score**
- **What it shows:** A composite risk score (0.00-1.00) combining payment + medical factors
- **How it's calculated:**
  - Weighted average of payment risk + medical urgency
  - Lower = lower overall risk
  - Higher = higher overall risk

**Example:** 0.90 means high combined risk (needs urgent intervention)

**Why it matters:** Single number summary for executive dashboards.

---

#### 5. **Payment Reliability**
- **What it shows:** Qualitative assessment of payment behavior
- **Possible values:**
  - `EXCELLENT` - <15% failure rate, no late payments
  - `GOOD` - 15-30% failure rate, occasional late
  - `FAIR` - 30-50% failure rate, frequent issues
  - `POOR` - >50% failure rate, chronic problems

**Why it matters:** Quick human-readable label for payment trustworthiness. Used in AI's messaging tone (we're gentler with "EXCELLENT" customers having a one-time issue).

---

#### 6. **Detected Intent** (appears after customer responds)
- **What it shows:** What the AI understood from the customer's message
- **Possible values:**
  - `Accept Bridge` - Customer agrees to Bridge Plan
  - `Accept Extension` - Customer wants payment extension
  - `Ambiguous Acceptance` - Said "yes" but didn't specify which option
  - `Decline Bridge` - Doesn't want Bridge Plan
  - `Financial Hardship` - Mentions money problems
  - `Ask For More Info` - Wants details
  - `Ask For Time` - Needs more time to pay
  - `Cancel Request` - Wants to cancel

**Why it matters:** Shows the AI's NLU (natural language understanding) in action. Demonstrates intelligence and context awareness.

**Demo tip:** This is where you show the "ambiguous acceptance" feature - if customer says "yes" to multiple options, AI asks for clarification.

---

### **ROW 3: Medical Context (The Secret Sauce)**

#### 7. **Medical Urgency**
- **What it shows:** How critical continuous care is for this pet (0-100)
- **How it's calculated:**
  - Base score from condition severity:
    - `CRITICAL` conditions (diabetes, kidney disease): 100 base
    - `HIGH` conditions (heart disease, cancer): 75 base
    - `MEDIUM` conditions (arthritis, allergies): 50 base
    - `LOW` conditions (routine care): 25 base
  - Multiplied by medication adherence modifier:
    - 85%+ adherence: 1.2x boost (engaged customer)
    - 70-84% adherence: 1.1x boost
    - <70% adherence: 1.0x (no boost)

**Example:** Bella has diabetes (CRITICAL = 100 base) × 95% adherence (1.2x boost) = 100/100 (capped)

**Why it matters:** This is CareLoop's **differentiation**. Traditional dunning doesn't know Bella needs insulin daily. We do.

**Demo talking point:** "If Bella loses access to insulin because we churned Maria, that's not just lost revenue—that's a pet's health at risk."

---

#### 8. **Medication Adherence**
- **What it shows:** % of prescribed medications being refilled on time (from ezyVet)
- **How it's calculated:**
  - (Refills on time / Total refills needed) × 100
  - Tracked over last 6 months

**Example:** 95% means highly engaged pet parent, rarely misses medication

**Why it matters:**
- High adherence = engaged customer worth retaining
- Shows the customer USES the service (sticky)
- Predictive of LTV

**Demo talking point:** "Maria's 95% adherence shows she's not just paying—she's actively using the service. That's a customer worth fighting for."

---

#### 9. **Care Importance**
- **What it shows:** How important continuity of care is for this condition
- **Possible values:**
  - `CRITICAL` - Life-threatening if care interrupted (diabetes, kidney disease)
  - `HIGH` - Serious consequences if interrupted (heart disease, cancer)
  - `MEDIUM` - Manageable but important (chronic conditions)
  - `LOW` - Routine/preventive care

**Why it matters:** Informs the urgency and tone of AI's messaging. CRITICAL cases get immediate, empathetic outreach.

---

### **ROW 4: AI's Decision (The Output)**

#### 10. **🎯 Retention Priority**
- **What it shows:** AI's composite score (0-100) determining intervention strategy
- **How it's calculated:**
  - **Medical Urgency: 40% weight** (most important)
  - **Customer Value: 30% weight** (LTV + tenure)
    - LTV scoring: >$10K = 20pts, $5-10K = 15pts, $2-5K = 10pts
    - Tenure scoring: >24mo = 10pts, 12-24mo = 7pts, 6-12mo = 4pts
  - **Engagement: 20% weight** (medication adherence)
    - 85%+ adherence = 20pts, 70-84% = 15pts, 50-69% = 10pts
  - **Financial Risk Modifier: 10% weight** (INVERSE - lower risk = higher priority)
    - Low payment risk (≤25) = 10pts
    - Moderate payment risk (26-50) = 7pts
    - High payment risk (51-75) = 4pts

**Example Calculation:**
- Maria: Medical 40 + Customer Value 30 + Engagement 20 + Financial 7 = **97/100**

**Why it matters:** This is the **autonomous decision-making** in action. AI decides intervention type without human involvement.

**Demo talking point:** "In traditional dunning, every customer gets the same 'Pay or Cancel' email. CareLoop's AI scores each customer and tailors the approach. Maria's 97/100 gets priority treatment—immediate Bridge Plan offer with flexibility."

---

#### 11. **Outreach Strategy**
- **What it shows:** Which intervention approach the AI chose
- **Possible values:**
  - `PRIORITY_OUTREACH` - High urgency + high value → Bridge Plan + flexibility
  - `SECONDARY_OUTREACH` - Moderate urgency → Standard Bridge Plan offer
  - `OFFER_BRIDGE_PLAN_PLUS_FLEXIBILITY` - High medical urgency + low payment risk → Bridge + extensions
  - `OFFER_PAYMENT_EXTENSION_ONLY` - Low urgency + good payment history → Just extend payment
  - `OFFER_FLEXIBLE_PAYMENT` - Moderate urgency → Payment plan options
  - `OFFER_STANDARD_RETRY_WITH_DEADLINE` - Low urgency + low value → Standard retry

**How it's decided:**
```
IF medical_urgency ≥ 70 AND payment_risk ≤ 40:
    → Bridge Plan + Flexibility
ELIF medical_urgency < 50 AND payment_risk ≤ 30:
    → Payment Extension Only
ELIF medical_urgency ≥ 70:
    → Bridge Plan
ELIF payment_risk ≤ 40:
    → Flexible Payment
ELSE:
    → Standard Retry
```

**Why it matters:** Shows the AI is making intelligent, context-aware decisions—not just blasting everyone with the same offer.

**Demo talking point:** "Notice it says 'Priority Outreach' not 'Engage AI: YES/NO.' We reach out to EVERYONE. The difference is WHAT we offer. High urgency cases like Maria get the Bridge Plan immediately. Low urgency cases might just get a 14-day extension."

---

## 🎯 Quick Reference: What to Emphasize in Demo

### **For CFOs/Finance:**
- **Retention Priority** - "Autonomous scoring means no human review needed"
- **Payment Risk** - "Uses only internal data—no compliance issues"
- **Revenue Saved** - "Each retention preserves lifetime value"

### **For Technical Audience:**
- **Detected Intent** - "NLU with disambiguation for ambiguous responses"
- **Medication Adherence** - "ezyVet API integration for real-time data"
- **Outreach Strategy** - "Multi-agent LangGraph workflow with Claude Sonnet 4.5"

### **For Mars Veterinary Health:**
- **Medical Urgency** - "We understand Bella's diabetes—traditional dunning doesn't"
- **Care Importance** - "Every churn is a pet losing access to life-saving care"
- **Medication Adherence** - "Shows the customer is engaged and using the service"

---

## ❓ Common Questions & Answers

**Q: "Why is Payment Risk 'MODERATE' if Payment Reliability is 'EXCELLENT'?"**

A: "Great question! These measure different things:
- **Payment Risk (29.6)** looks at the CURRENT situation—there's a failed payment right now, so there's moderate risk TODAY.
- **Payment Reliability (EXCELLENT)** looks at HISTORICAL behavior—Maria has a great track record over time.

This combination tells us: 'Reliable customer having a one-time issue.' That's exactly who we want to save!"

---

**Q: "How do you get Medical Urgency data?"**

A: "We integrate with ezyVet, the veterinary practice management system used by Mars Veterinary Health clinics. It provides:
- Pet's condition/diagnosis
- Prescription history
- Medication refill patterns
- Visit frequency

All data is already owned by the business—no third-party APIs, no compliance issues."

---

**Q: "What if the customer doesn't respond?"**

A: "Good question! After 48 hours of no response, the system:
1. Sends a second message with more urgency
2. Offers a direct 'Click to keep Bridge Plan' button
3. After 72 hours, escalates to human CSR for phone call

The Glass Box logs all of this, so CFOs can see where customers drop off."

---

**Q: "Why engage with EVERYONE? Isn't that expensive?"**

A: "Actually, it's MORE cost-effective because:
1. AI messaging is instant and cheap (pennies per interaction)
2. The cost of churning even ONE high-LTV customer ($12K) far exceeds the cost of reaching out to 100 customers
3. Traditional dunning has 40% retention. We're hitting 85%+. The ROI is massive.

Plus, offering a $5 Bridge Plan beats losing $50/month entirely."

---

## 🎬 Demo Script Integration

**When showing this screen, say:**

> "Let me walk you through what the AI just analyzed in under 2 seconds.
>
> [Point to Medical Urgency] Bella has diabetes—Medical Urgency is 100/100. She needs daily insulin. Losing access isn't just lost revenue; it's a health crisis.
>
> [Point to Payment Risk] Maria's Payment Risk is only 29 (MODERATE), and her reliability is EXCELLENT. This tells us: 'Great customer having a one-time issue.'
>
> [Point to Retention Priority] The AI combines these factors into a Retention Priority score: **97/100**. That's a slam dunk.
>
> [Point to Outreach Strategy] So the AI chooses 'Priority Outreach'—immediate Bridge Plan offer at $5/month to keep Bella's care active.
>
> This is what I mean by **Glass Box transparency**. Every decision is explainable, auditable, and intelligent."

---

**Good luck with your demo! 🚀**
