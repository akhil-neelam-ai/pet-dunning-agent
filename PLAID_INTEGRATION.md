# 💳 Plaid Credit Check Integration

## Overview

PetDunning now includes **Plaid Sandbox API integration** to assess customer financial health before making retention decisions. This adds an additional layer of risk assessment beyond medical risk.

## What Was Added

### 1. **Credit Score Module** (`agents/plaid_client.py`)

New functions:
- `calculate_credit_score(user_id)` - Fetches credit score, DTI ratio, available balance
- `assess_payment_capacity(credit_data, payment_amount)` - Determines if customer can afford Premium or Bridge Plan
- `get_account_balances(access_token)` - Production-ready Plaid API integration (currently using mock data)

### 2. **Router Enhancement**

The Router now:
- Calls Plaid credit check at the start of risk assessment
- Incorporates credit score (300-850) and credit tier (excellent/good/fair/poor)
- Factors in debt-to-income ratio when making retention decisions
- Displays credit context in Glass Box reasoning

### 3. **State Updates**

Added credit fields to `AgentState`:
```python
credit_score: Optional[int]          # 300-850
credit_tier: Optional[str]           # 'excellent', 'good', 'fair', 'poor'
available_balance: Optional[float]   # Current account balance
debt_to_income_ratio: Optional[float]# DTI ratio (0.0-1.0)
payment_risk_level: Optional[str]    # 'low', 'medium', 'high'
financial_recommendation: Optional[str]
```

### 4. **Glass Box Display**

The AI Decision Transparency panel now shows:
- Credit Score (e.g., 620)
- Credit Tier (FAIR)
- Payment Risk Level (MEDIUM)
- Financial Recommendation

## Demo Data

We've configured mock credit profiles for the three demo users:

### Maria Rodriguez (Bella - Diabetes)
- **Credit Score:** 620 (FAIR)
- **Available Balance:** $450
- **DTI Ratio:** 45%
- **Recommendation:** Moderate risk, Bridge Plan recommended

### James Mitchell (Max - Heartworm)
- **Credit Score:** 720 (GOOD)
- **Available Balance:** $2,800
- **DTI Ratio:** 28%
- **Recommendation:** Low risk, standard retry likely to succeed

### Sarah Chen (Whiskers - Kidney Disease)
- **Credit Score:** 580 (POOR)
- **Available Balance:** $120
- **DTI Ratio:** 62%
- **Recommendation:** High risk, Bridge Plan critical for retention

## How to Test

1. **Start the app:**
   ```bash
   streamlit run app.py
   ```

2. **Select Maria Rodriguez** from the sidebar

3. **Click "Simulate Payment Failure"**

4. **Watch the Glass Box panel** - You'll now see:
   - Router decision with credit check results
   - Credit Score: 620 (FAIR tier)
   - Payment Risk: MEDIUM
   - Financial recommendation

5. **Current State section** displays:
   - Credit Score metric
   - Payment Risk metric

## Production Integration

To use **real Plaid API** in production:

1. **Sign up at [dashboard.plaid.com](https://dashboard.plaid.com/)**

2. **Get your credentials:**
   - Client ID
   - Sandbox Secret (for testing)
   - Production Secret (for live)

3. **Add to `.env`:**
   ```bash
   PLAID_CLIENT_ID=your_actual_client_id
   PLAID_SECRET=your_actual_secret
   PLAID_ENV=sandbox  # or 'production'
   ```

4. **Uncomment production code** in `plaid_client.py`:
   - `get_account_balances()` function has production example
   - Replace mock data with real Plaid API calls

## Decision Logic

The router now combines **3 risk factors**:

1. **Medical Risk** (from pet condition)
2. **LTV & Tenure** (customer value)
3. **Credit Risk** (from Plaid)

Example decision:
```
CRITICAL RETENTION: Bella has Diabetes (high medical risk).
Customer has 36-month tenure with $12,000 LTV.
Credit Check: FAIR (620), $450.00 available balance.
Offer Bridge Plan to preserve relationship and medical continuity.
```

## Next Steps

Consider adding:
- **Transaction history analysis** (spending patterns)
- **Income verification** (via Plaid)
- **Payment timing optimization** (suggest retry dates based on income cycles)
- **Dynamic pricing** (adjust Bridge Plan price based on affordability)

## Files Modified

- ✅ `agents/plaid_client.py` - New credit check module
- ✅ `agents/router.py` - Integrated credit check
- ✅ `state.py` - Added credit fields
- ✅ `app.py` - Initialize credit state, display in UI
- ✅ `utils/ui_components.py` - Display credit in Glass Box
- ✅ `requirements.txt` - Added plaid-python==37.1.0
- ✅ `.env` and `.env.example` - Added Plaid credentials

---

Built with ❤️ using Claude Sonnet 4.5 + Plaid Sandbox
