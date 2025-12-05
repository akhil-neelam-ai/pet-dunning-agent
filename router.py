"""
Router Agent: Risk Assessment and Decision Making
This agent decides whether to retain, downgrade, or cancel a user based on medical risk and LTV
"""
import json
from state import AgentState, RouterOutput
from utils.metrics import calculate_ltv, get_retention_priority


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

    # Calculate risk score
    risk_data = risk_tiers['risk_tiers'][medical_risk]
    risk_score = risk_data['risk_score']

    # Determine retention priority
    retention_priority = get_retention_priority({
        'medical_risk_tier': medical_risk,
        'ltv': ltv,
        'tenure_months': tenure,
        'plan_cost': 50.00  # Add plan_cost for calculate_ltv fallback
    }, risk_tiers)

    # Decision Logic
    should_retain = False
    recommended_action = 'standard_retry'
    reasoning = ""

    if retention_priority == 'critical':
        should_retain = True
        recommended_action = 'offer_bridge_plan'
        reasoning = (
            f"CRITICAL RETENTION: {state['pet_name']} has {pet_condition} (high medical risk). "
            f"Customer has {tenure}-month tenure with ${ltv:,.0f} LTV. "
            f"Offer Bridge Plan to preserve relationship and medical continuity."
        )

    elif retention_priority == 'high':
        should_retain = True
        recommended_action = 'offer_bridge_plan'
        reasoning = (
            f"HIGH PRIORITY: Customer has {'high medical risk' if medical_risk == 'high' else 'high LTV'}. "
            f"Bridge Plan recommended to maintain care continuity."
        )

    elif retention_priority == 'medium':
        should_retain = True
        recommended_action = 'offer_payment_plan'
        reasoning = (
            f"MEDIUM PRIORITY: Offer flexible payment options. "
            f"Standard retention efforts warranted given ${ltv:,.0f} LTV."
        )

    else:
        should_retain = False
        recommended_action = 'standard_retry'
        reasoning = (
            f"LOW PRIORITY: Standard retry logic. "
            f"Limited retention investment justified for {tenure}-month tenure."
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
        'tool_calls': state.get('tool_calls', []) + [{
            'agent': 'router',
            'decision': recommended_action,
            'reasoning': reasoning,
            'risk_score': risk_score
        }]
    }


def should_offer_bridge_plan(state: AgentState) -> bool:
    """
    Conditional edge: Check if we should offer bridge plan
    """
    return state.get('router_decision') == 'offer_bridge_plan'
