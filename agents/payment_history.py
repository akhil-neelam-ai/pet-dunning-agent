"""
Payment History Analysis (Compliance-Friendly Alternative to Credit Checks)
Uses internal payment data only - no third-party credit bureaus
"""
from datetime import datetime, timedelta
from typing import Dict, List


def get_payment_history(user_id: str) -> Dict:
    """
    Analyze customer's payment history with VCA.

    This is 100% compliant because it's based on:
    - Actual business relationship data
    - Internal payment records
    - No protected class information
    - No third-party credit bureaus
    """

    mock_payment_data = {
        'user_123': {  # Maria Rodriguez - Reliable payer despite current failure
            'total_payments': 36,
            'successful_payments': 35,
            'failed_payments': 1,  # This is the current one
            'late_payments': 2,
            'avg_days_to_payment': 1.2,  # Pays almost immediately
            'payment_method': 'credit_card',
            'payment_method_changes': 0,
            'declined_transactions_last_6mo': 0,
            'current_balance_owed': 50.00,
            'historical_payment_reliability': 'excellent',
            'longest_late_payment_days': 3,
            'total_lifetime_paid': 1800.00,
            'notes': 'Highly reliable payer. Current failure is first in 36 months.'
        },
        'user_456': {  # James Mitchell - Good payer with occasional issues
            'total_payments': 12,
            'successful_payments': 10,
            'failed_payments': 2,
            'late_payments': 3,
            'avg_days_to_payment': 5.8,
            'payment_method': 'credit_card',
            'payment_method_changes': 1,
            'declined_transactions_last_6mo': 1,
            'current_balance_owed': 50.00,
            'historical_payment_reliability': 'good',
            'longest_late_payment_days': 12,
            'total_lifetime_paid': 500.00,
            'notes': 'Generally reliable. Occasional payment delays but always resolves.'
        },
        'user_789': {  # Sarah Chen - Struggling with payments
            'total_payments': 18,
            'successful_payments': 13,
            'failed_payments': 5,
            'late_payments': 8,
            'avg_days_to_payment': 14.5,
            'payment_method': 'debit_card',
            'payment_method_changes': 3,
            'declined_transactions_last_6mo': 4,
            'current_balance_owed': 150.00,  # Accumulated from past late payments
            'historical_payment_reliability': 'fair',
            'longest_late_payment_days': 28,
            'total_lifetime_paid': 650.00,
            'notes': 'Pattern of financial stress. Frequent late payments and declines.'
        }
    }

    return mock_payment_data.get(user_id, {
        'total_payments': 0,
        'successful_payments': 0,
        'failed_payments': 0,
        'late_payments': 0,
        'avg_days_to_payment': 0,
        'payment_method': 'unknown',
        'payment_method_changes': 0,
        'declined_transactions_last_6mo': 0,
        'current_balance_owed': 0,
        'historical_payment_reliability': 'insufficient_data',
        'notes': 'Insufficient payment history'
    })


def calculate_payment_risk_score(payment_history: Dict) -> Dict:
    """
    Calculate payment risk based on internal history only.

    Returns 0-100 score where:
    - 0-25 = LOW RISK (very reliable)
    - 26-50 = MODERATE RISK (some issues)
    - 51-75 = HIGH RISK (frequent problems)
    - 76-100 = CRITICAL RISK (severe payment issues)
    """

    total_payments = payment_history.get('total_payments', 1)
    failed_payments = payment_history.get('failed_payments', 0)
    late_payments = payment_history.get('late_payments', 0)
    avg_days_to_payment = payment_history.get('avg_days_to_payment', 0)
    declined_last_6mo = payment_history.get('declined_transactions_last_6mo', 0)
    current_balance = payment_history.get('current_balance_owed', 0)

    # Calculate failure rate (0-40 points)
    failure_rate = (failed_payments / total_payments) * 100 if total_payments > 0 else 0
    failure_score = min(40, failure_rate * 4)  # Scale to 0-40

    # Calculate late payment rate (0-30 points)
    late_rate = (late_payments / total_payments) * 100 if total_payments > 0 else 0
    late_score = min(30, late_rate * 3)  # Scale to 0-30

    # Calculate payment delay penalty (0-15 points)
    delay_score = min(15, avg_days_to_payment * 1.5)

    # Recent declined transactions penalty (0-10 points)
    declined_score = min(10, declined_last_6mo * 2.5)

    # Outstanding balance penalty (0-5 points)
    balance_score = 0
    if current_balance > 100:
        balance_score = 5
    elif current_balance > 50:
        balance_score = 3

    # Total risk score
    total_risk = failure_score + late_score + delay_score + declined_score + balance_score

    # Determine risk tier
    if total_risk <= 25:
        risk_tier = 'LOW'
        risk_description = 'Excellent payment history. Very reliable customer.'
        can_afford_premium = True
        recommended_action = 'Standard retry likely to succeed'
    elif total_risk <= 50:
        risk_tier = 'MODERATE'
        risk_description = 'Some payment issues but generally resolves them.'
        can_afford_premium = True
        recommended_action = 'Offer Bridge Plan as safety net'
    elif total_risk <= 75:
        risk_tier = 'HIGH'
        risk_description = 'Frequent payment problems. Financial stress evident.'
        can_afford_premium = False
        recommended_action = 'Bridge Plan critical for retention'
    else:
        risk_tier = 'CRITICAL'
        risk_description = 'Severe payment issues. Immediate intervention needed.'
        can_afford_premium = False
        recommended_action = 'Bridge Plan + payment assistance program'

    return {
        'payment_risk_score': round(total_risk, 1),
        'payment_risk_tier': risk_tier,
        'risk_description': risk_description,
        'can_afford_premium': can_afford_premium,
        'recommended_action': recommended_action,
        'failure_rate_pct': round(failure_rate, 1),
        'late_payment_rate_pct': round(late_rate, 1),
        'avg_days_to_payment': avg_days_to_payment,
        'recent_declines': declined_last_6mo
    }


def assess_financial_capacity(payment_history: Dict, payment_risk: Dict) -> Dict:
    """
    Determine if customer can likely afford Premium vs Bridge Plan.
    Based purely on payment behavior patterns.
    """

    reliability = payment_history.get('historical_payment_reliability', 'insufficient_data')
    risk_tier = payment_risk.get('payment_risk_tier', 'MODERATE')
    current_balance = payment_history.get('current_balance_owed', 0)

    # Decision matrix
    if reliability == 'excellent' and risk_tier == 'LOW':
        recommendation = {
            'likely_can_afford': 'premium',
            'confidence': 'high',
            'reasoning': 'Proven track record of reliable payments. Current failure likely temporary.'
        }
    elif reliability == 'good' and risk_tier in ['LOW', 'MODERATE']:
        recommendation = {
            'likely_can_afford': 'premium_with_support',
            'confidence': 'medium',
            'reasoning': 'Generally reliable but may benefit from payment flexibility.'
        }
    elif current_balance > 100 or risk_tier in ['HIGH', 'CRITICAL']:
        recommendation = {
            'likely_can_afford': 'bridge_only',
            'confidence': 'high',
            'reasoning': 'Payment history indicates financial stress. Bridge Plan is safest option.'
        }
    else:
        recommendation = {
            'likely_can_afford': 'bridge_preferred',
            'confidence': 'medium',
            'reasoning': 'Mixed payment history. Bridge Plan recommended as safety net.'
        }

    return recommendation
