"""
Metrics and Revenue Calculation Utilities
"""
import json
from typing import Dict


def load_mock_data():
    """Load mock database"""
    with open('data/mock_db.json', 'r') as f:
        return json.load(f)


def load_risk_tiers():
    """Load medical risk tier definitions"""
    with open('data/medical_risk_tiers.json', 'r') as f:
        return json.load(f)


def calculate_ltv(user_data: Dict) -> float:
    """
    Calculate Lifetime Value (LTV) for a user
    LTV = Monthly Plan Cost × Tenure Months × Expected Retention Multiplier
    """
    base_ltv = user_data['plan_cost'] * user_data['tenure_months']

    # Expected future value (assume avg customer stays 3 more years)
    expected_future_months = 36
    future_value = user_data['plan_cost'] * expected_future_months

    return base_ltv + future_value


def calculate_churn_cost(user_data: Dict) -> float:
    """
    Calculate the cost of losing this customer
    """
    # Future LTV lost
    monthly_revenue = user_data['plan_cost']
    expected_future_months = 36
    lost_revenue = monthly_revenue * expected_future_months

    # Acquisition cost (assumed)
    acquisition_cost = 150  # Industry standard for pet wellness plans

    return lost_revenue + acquisition_cost


def calculate_bridge_plan_value(user_data: Dict) -> float:
    """
    Calculate the value preserved by moving to Bridge Plan
    Bridge Plan keeps the customer relationship alive at $5/mo
    """
    bridge_monthly = 5.00
    bridge_duration_months = 6  # Assume avg bridge duration

    # Value of keeping relationship active
    relationship_value = bridge_monthly * bridge_duration_months

    # Probability of returning to Premium (estimated 60% for high-risk pets)
    return_probability = 0.6 if user_data['medical_risk_tier'] == 'high' else 0.3
    future_premium_value = user_data['plan_cost'] * 24 * return_probability  # 2 years

    return relationship_value + future_premium_value


def get_retention_priority(user_data: Dict, risk_tiers: Dict) -> str:
    """
    Determine retention priority based on medical risk and LTV
    Returns: 'critical', 'high', 'medium', 'low'
    """
    medical_risk = user_data['medical_risk_tier']
    ltv = user_data.get('ltv', calculate_ltv(user_data))
    tenure = user_data['tenure_months']

    # Critical: High medical risk + High LTV + Long tenure
    if medical_risk == 'high' and ltv > 8000 and tenure > 12:
        return 'critical'

    # High: High medical risk OR high LTV
    elif medical_risk == 'high' or ltv > 5000:
        return 'high'

    # Medium: Medium risk or medium LTV
    elif medical_risk == 'medium' or ltv > 2000:
        return 'medium'

    # Low: Everyone else
    else:
        return 'low'


def calculate_revenue_saved(original_plan_cost: float, action_taken: str) -> float:
    """
    Calculate revenue saved by AI intervention vs standard dunning
    """
    if action_taken == 'bridge_plan_accepted':
        # Saved the future LTV by preventing cancellation
        # Assume standard dunning would have led to cancellation
        expected_future_months = 36
        future_premium_value = original_plan_cost * expected_future_months

        # Bridge plan revenue for 6 months
        bridge_revenue = 5.00 * 6

        # Return probability (60% return to premium)
        return_value = future_premium_value * 0.6

        return bridge_revenue + return_value

    elif action_taken == 'payment_retry_success':
        # Recovered the payment
        return original_plan_cost

    else:
        return 0.0


def format_currency(amount: float) -> str:
    """Format number as USD currency"""
    return f"${amount:,.2f}"
