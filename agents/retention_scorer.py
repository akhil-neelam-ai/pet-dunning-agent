"""
Retention Priority Scorer
Autonomous decision-making for which customers deserve AI agent intervention
"""
from typing import Dict


def calculate_retention_priority_score(
    medical_urgency_score: float,
    payment_risk_score: float,
    medication_adherence_score: int,
    ltv: float,
    tenure_months: int
) -> Dict:
    """
    Calculate a comprehensive retention priority score (0-100) that determines
    if a customer is worth AI agent intervention or should go through standard dunning.

    Philosophy:
    - High medical urgency + good payment history = PRIORITY (don't lose engaged customers)
    - High medical urgency + poor payment history = PRIORITY (need intervention to save them)
    - Low medical urgency + poor payment history = IGNORE (let standard dunning handle it)
    - High LTV + good adherence = PRIORITY (valuable customers deserve white-glove treatment)

    Returns retention score where:
    - 70-100 = PRIORITY OUTREACH (AI agent intervention)
    - 40-69 = SECONDARY OUTREACH (reach out if capacity available)
    - 0-39 = IGNORE (standard dunning, no AI agent)
    """

    # Component 1: Medical Urgency (40% weight - most important)
    # If the pet's health is at risk, we need to act regardless of other factors
    medical_component = (medical_urgency_score / 100) * 40

    # Component 2: Customer Value (30% weight)
    # Combine LTV and tenure to assess customer value

    # LTV scoring (0-20 points)
    if ltv >= 10000:
        ltv_score = 20
    elif ltv >= 5000:
        ltv_score = 15
    elif ltv >= 2000:
        ltv_score = 10
    else:
        ltv_score = 5

    # Tenure scoring (0-10 points)
    if tenure_months >= 24:
        tenure_score = 10
    elif tenure_months >= 12:
        tenure_score = 7
    elif tenure_months >= 6:
        tenure_score = 4
    else:
        tenure_score = 2

    customer_value_component = ltv_score + tenure_score

    # Component 3: Engagement Quality (20% weight)
    # High adherence means they're engaged and worth saving
    if medication_adherence_score >= 85:
        engagement_score = 20
    elif medication_adherence_score >= 70:
        engagement_score = 15
    elif medication_adherence_score >= 50:
        engagement_score = 10
    else:
        engagement_score = 5

    # Component 4: Financial Risk Modifier (10% weight)
    # INVERSE scoring - lower payment risk = higher retention priority
    # (We want to save customers who usually pay but hit a bump)
    if payment_risk_score <= 25:  # Excellent payer
        financial_modifier = 10
    elif payment_risk_score <= 50:  # Decent payer
        financial_modifier = 7
    elif payment_risk_score <= 75:  # Struggling payer
        financial_modifier = 4
    else:  # Chronic payment issues
        financial_modifier = 2

    # Calculate total retention priority score
    total_score = (
        medical_component +
        customer_value_component +
        engagement_score +
        financial_modifier
    )

    # Determine decision tier
    if total_score >= 70:
        decision = 'PRIORITY_OUTREACH'
        action = 'Immediate AI agent intervention'
        reasoning = 'High-value retention opportunity. AI negotiation recommended.'
    elif total_score >= 40:
        decision = 'SECONDARY_OUTREACH'
        action = 'Queue for AI agent if capacity available'
        reasoning = 'Moderate retention potential. Consider AI intervention if resources permit.'
    else:
        decision = 'IGNORE'
        action = 'Standard dunning process only'
        reasoning = 'Low retention priority. Not worth AI agent resources.'

    # Build detailed breakdown
    breakdown = {
        'medical_component': round(medical_component, 1),
        'customer_value_component': customer_value_component,
        'engagement_component': engagement_score,
        'financial_modifier': financial_modifier
    }

    return {
        'retention_priority_score': round(total_score, 1),
        'decision': decision,
        'action': action,
        'reasoning': reasoning,
        'breakdown': breakdown,
        'should_engage_ai': total_score >= 70  # Boolean flag for easy filtering
    }


def get_outreach_recommendation(retention_data: Dict, medical_urgency_tier: str) -> str:
    """
    Generate specific outreach recommendation based on retention score.
    """
    decision = retention_data['decision']
    score = retention_data['retention_priority_score']

    if decision == 'PRIORITY_OUTREACH':
        if medical_urgency_tier == 'MAXIMUM_RETENTION':
            return (
                f"🚨 CRITICAL: Retention score {score}/100. "
                "Life-threatening medical condition + high-value customer. "
                "Deploy AI agent with Bridge Plan offer immediately."
            )
        elif score >= 85:
            return (
                f"⚠️ URGENT: Retention score {score}/100. "
                "Highly engaged customer at risk of churn. "
                "Deploy AI agent with personalized intervention."
            )
        else:
            return (
                f"📍 HIGH PRIORITY: Retention score {score}/100. "
                "Strong retention opportunity. AI agent should engage."
            )

    elif decision == 'SECONDARY_OUTREACH':
        return (
            f"📋 MODERATE PRIORITY: Retention score {score}/100. "
            "Retention possible but not critical. Queue for AI if capacity available."
        )

    else:  # IGNORE
        return (
            f"🔕 LOW PRIORITY: Retention score {score}/100. "
            "Not worth AI resources. Route to standard dunning."
        )


def batch_score_customers(customers: list) -> list:
    """
    Score multiple customers and rank by retention priority.
    Useful for daily batch processing of payment failures.

    Returns sorted list of customers with scores.
    """
    scored_customers = []

    for customer in customers:
        score_data = calculate_retention_priority_score(
            medical_urgency_score=customer.get('medical_urgency_score', 50),
            payment_risk_score=customer.get('payment_risk_score', 50),
            medication_adherence_score=customer.get('medication_adherence_score', 70),
            ltv=customer.get('ltv', 0),
            tenure_months=customer.get('tenure_months', 0)
        )

        scored_customers.append({
            **customer,
            'retention_score': score_data['retention_priority_score'],
            'retention_decision': score_data['decision'],
            'should_engage': score_data['should_engage_ai']
        })

    # Sort by retention score (highest first)
    scored_customers.sort(key=lambda x: x['retention_score'], reverse=True)

    return scored_customers


def get_daily_outreach_list(all_payment_failures: list, ai_agent_capacity: int = 10) -> Dict:
    """
    Given a list of payment failures, determine which ones should get AI agent outreach.

    Args:
        all_payment_failures: List of customers with payment failures
        ai_agent_capacity: How many customers can the AI agent handle today (default 10)

    Returns:
        Dict with priority tiers and recommendations
    """
    scored = batch_score_customers(all_payment_failures)

    priority = [c for c in scored if c['retention_decision'] == 'PRIORITY_OUTREACH']
    secondary = [c for c in scored if c['retention_decision'] == 'SECONDARY_OUTREACH']
    ignore = [c for c in scored if c['retention_decision'] == 'IGNORE']

    # Select customers for AI agent
    ai_outreach = priority[:ai_agent_capacity]  # Start with priority customers

    if len(ai_outreach) < ai_agent_capacity:
        # If we have capacity, add secondary customers
        remaining_capacity = ai_agent_capacity - len(ai_outreach)
        ai_outreach.extend(secondary[:remaining_capacity])

    return {
        'total_failures': len(all_payment_failures),
        'priority_count': len(priority),
        'secondary_count': len(secondary),
        'ignore_count': len(ignore),
        'ai_outreach_list': ai_outreach,
        'standard_dunning_list': ignore,
        'recommendation': (
            f"Deploy AI agent to {len(ai_outreach)} customers. "
            f"Route {len(ignore)} to standard dunning. "
            f"{len(secondary) - (len(ai_outreach) - len(priority))} customers queued for follow-up."
        )
    }
