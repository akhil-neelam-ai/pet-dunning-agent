"""
Router Agent: Risk Assessment and Decision Making
This agent decides whether to retain, downgrade, or cancel a user based on medical risk and LTV
Now enhanced with internal payment history + ezyVet medical history integration
"""
import json
from state import AgentState, RouterOutput
from utils.metrics import calculate_ltv, get_retention_priority
from agents.payment_history import (
    get_payment_history,
    calculate_payment_risk_score,
    assess_financial_capacity
)
from agents.ezyvet_client import (
    get_pet_medical_history,
    get_medication_adherence_score,
    assess_medical_urgency
)
from agents.retention_scorer import (
    calculate_retention_priority_score,
    get_outreach_recommendation
)


def load_risk_tiers():
    """Load medical risk tier definitions"""
    with open('data/medical_risk_tiers.json', 'r') as f:
        return json.load(f)


def router_node(state: AgentState) -> dict:
    """
    Main router logic that decides the retention strategy

    Decision Tree:
    1. High Medical Risk + High LTV → Offer Bridge Plan
    2. Medium Risk + Medium LTV → Offer Payment Plan
    3. Low Risk + Low LTV → Standard Retry
    """
    risk_tiers = load_risk_tiers()

    # Get user context
    medical_risk = state['medical_risk_tier']
    ltv = state['ltv']
    tenure = state['tenure_months']
    pet_condition = state['pet_condition']
    user_id = state['user_id']

    # Calculate risk score
    risk_data = risk_tiers['risk_tiers'][medical_risk]
    risk_score = risk_data['risk_score']

    # 🆕 PAYMENT HISTORY CHECK (Compliance-Friendly)
    payment_hist = get_payment_history(user_id)
    payment_risk = calculate_payment_risk_score(payment_hist)
    financial_capacity = assess_financial_capacity(payment_hist, payment_risk)

    # Add payment data to state for Glass Box display
    payment_risk_score = payment_risk['payment_risk_score']
    payment_risk_tier = payment_risk['payment_risk_tier']
    failure_rate = payment_risk['failure_rate_pct']
    late_payment_rate = payment_risk['late_payment_rate_pct']
    payment_reliability = payment_hist['historical_payment_reliability']

    # 🆕 EZYVET MEDICAL HISTORY CHECK
    medical_history = get_pet_medical_history(pet_id='pet_001', user_id=user_id)
    adherence_data = get_medication_adherence_score(user_id)
    medical_urgency = assess_medical_urgency(medical_history, adherence_data)

    # Add medical data to state
    medication_adherence_score = adherence_data['adherence_score']
    medical_urgency_score = medical_urgency['urgency_score']
    medical_urgency_tier = medical_urgency['urgency_tier']
    continuity_of_care = medical_history.get('continuity_of_care_importance', 'MEDIUM')

    # 🆕 CALCULATE RETENTION PRIORITY SCORE (AI AUTONOMOUS DECISION)
    retention_score_data = calculate_retention_priority_score(
        medical_urgency_score=medical_urgency_score,
        payment_risk_score=payment_risk_score,
        medication_adherence_score=medication_adherence_score,
        ltv=ltv,
        tenure_months=tenure
    )

    retention_priority_score = retention_score_data['retention_priority_score']
    retention_decision = retention_score_data['decision']
    should_engage_ai = retention_score_data['should_engage_ai']
    outreach_recommendation = get_outreach_recommendation(retention_score_data, medical_urgency_tier)

    # Decision Logic - Tailored Offer Based on Profile
    # Philosophy: Reach out to EVERYONE, but offer different solutions

    should_retain = True  # Always reach out
    reasoning = ""

    # Build medical context
    medications = medical_history.get('current_medications', [])
    critical_meds = [m['name'] for m in medications if m.get('critical')]
    med_context = f"Currently on {len(critical_meds)} critical medications. " if critical_meds else ""

    # Determine offer based on medical urgency + payment history
    if medical_urgency_score >= 70 and payment_risk_score <= 40:
        # High medical urgency + Good payment history
        # → Offer Bridge Plan + Payment Flexibility
        recommended_action = 'offer_bridge_plan_plus_flexibility'
        reasoning = (
            f"📊 RETENTION SCORE: {retention_priority_score:.1f}/100\n"
            f"🏥 HIGH MEDICAL URGENCY ({medical_urgency_score:.1f}/100) + 💳 GOOD PAYMENT HISTORY ({payment_reliability})\n"
            f"{state['pet_name']} has {pet_condition} - {med_context}\n"
            f"Customer: {tenure}-month tenure, ${ltv:,.0f} LTV, {medication_adherence_score}% adherence\n"
            f"→ OFFER: Digital Keeper Plan ($4.99/mo) OR 30-day payment extension + payment plan options"
        )

    elif medical_urgency_score < 50 and payment_risk_score <= 30:
        # Low medical urgency + Excellent payment history
        # → Just offer payment extension, keep Premium benefits
        recommended_action = 'offer_payment_extension_only'
        reasoning = (
            f"📊 RETENTION SCORE: {retention_priority_score:.1f}/100\n"
            f"📅 RELIABLE PAYER ({payment_reliability}) + ✅ LOW MEDICAL URGENCY\n"
            f"Payment history: {failure_rate:.0f}% failure rate (excellent track record)\n"
            f"→ OFFER: 14-day payment extension, keep Premium benefits active during grace period"
        )

    elif medical_urgency_score >= 70:
        # High medical urgency regardless of payment history
        # → Bridge Plan is critical for pet's health
        recommended_action = 'offer_bridge_plan'
        reasoning = (
            f"📊 RETENTION SCORE: {retention_priority_score:.1f}/100\n"
            f"🚨 CRITICAL MEDICAL NEED ({medical_urgency_score:.1f}/100)\n"
            f"{state['pet_name']} has {pet_condition} ({continuity_of_care} importance) - {med_context}\n"
            f"Payment history: {payment_reliability} ({failure_rate:.0f}% failure, {late_payment_rate:.0f}% late)\n"
            f"→ OFFER: Digital Keeper Plan ($4.99/mo) to maintain critical medical care access"
        )

    elif payment_risk_score <= 40:
        # Good payment history but moderate medical need
        # → Offer flexible payment options
        recommended_action = 'offer_flexible_payment'
        reasoning = (
            f"📊 RETENTION SCORE: {retention_priority_score:.1f}/100\n"
            f"💳 RELIABLE CUSTOMER ({payment_reliability}) + MODERATE MEDICAL NEED\n"
            f"Payment history: {failure_rate:.0f}% failure rate, {late_payment_rate:.0f}% late rate\n"
            f"→ OFFER: Payment plan (split over 2-3 months) OR Bridge Plan option"
        )

    else:
        # Poor payment history + moderate/low medical need
        # → Standard retry with firm deadline
        recommended_action = 'offer_standard_retry_with_deadline'
        reasoning = (
            f"📊 RETENTION SCORE: {retention_priority_score:.1f}/100\n"
            f"⚠️ PAYMENT CHALLENGES ({payment_reliability}) + MODERATE MEDICAL NEED\n"
            f"Payment history: {failure_rate:.0f}% failure rate, {late_payment_rate:.0f}% late rate\n"
            f"→ OFFER: 7-day grace period to update payment method, standard retry"
        )

    # Build router output
    router_output: RouterOutput = {
        'should_retain': should_retain,
        'recommended_action': recommended_action,
        'reasoning': reasoning,
        'risk_score': risk_score
    }

    # Update state
    return {
        'router_decision': recommended_action,
        'risk_score': risk_score,
        'conversation_stage': 'initial',
        # Add payment history data to state
        'payment_history': payment_hist,
        'payment_risk_score': payment_risk_score,
        'payment_risk_tier': payment_risk_tier,
        'failure_rate': failure_rate,
        'late_payment_rate': late_payment_rate,
        'payment_reliability': payment_reliability,
        # Add medical data to state
        'medical_history': medical_history,
        'medication_adherence_score': medication_adherence_score,
        'medical_urgency_score': medical_urgency_score,
        'medical_urgency_tier': medical_urgency_tier,
        'continuity_of_care_importance': continuity_of_care,
        # Add retention priority score
        'retention_priority_score': retention_priority_score,
        'retention_decision': retention_decision,
        'should_engage_ai': should_engage_ai,
        'tool_calls': state.get('tool_calls', []) + [{
            'agent': 'router',
            'decision': recommended_action,
            'reasoning': reasoning,
            'risk_score': risk_score,
            'payment_check': {
                'risk_score': payment_risk_score,
                'risk_tier': payment_risk_tier,
                'reliability': payment_reliability,
                'failure_rate': failure_rate,
                'late_rate': late_payment_rate,
                'total_payments': payment_hist.get('total_payments', 0)
            },
            'medical_check': {
                'urgency_score': medical_urgency_score,
                'urgency_tier': medical_urgency_tier,
                'adherence_score': medication_adherence_score,
                'continuity_importance': continuity_of_care,
                'critical_medications': len([m for m in medical_history.get('current_medications', []) if m.get('critical')])
            }
        }]
    }


def should_offer_bridge_plan(state: AgentState) -> bool:
    """
    Conditional edge: Check if we should offer bridge plan
    """
    return state.get('router_decision') == 'offer_bridge_plan'
