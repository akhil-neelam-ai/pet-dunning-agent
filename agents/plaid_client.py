"""
Plaid Integration for Credit Check
Uses Plaid Sandbox API to assess customer financial health
"""
import os
from plaid.api import plaid_api
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.accounts_balance_get_request import AccountsBalanceGetRequest
from plaid.model.liabilities_get_request import LiabilitiesGetRequest
from plaid import ApiClient, Configuration
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

# Plaid configuration
configuration = Configuration(
    host=os.getenv('PLAID_ENV', 'sandbox'),
    api_key={
        'clientId': os.getenv('PLAID_CLIENT_ID'),
        'secret': os.getenv('PLAID_SECRET'),
    }
)

api_client = ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)


def calculate_credit_score(user_id: str, access_token: str = None) -> dict:
    """
    Calculate a simplified credit risk score based on Plaid data.

    In production, this would:
    1. Use real Plaid access token
    2. Pull account balances, transaction history, liabilities
    3. Calculate debt-to-income ratio
    4. Assess payment reliability

    For sandbox demo, we'll return mock but realistic scores.

    Returns:
        dict: {
            'credit_score': int (300-850),
            'credit_tier': str ('excellent', 'good', 'fair', 'poor'),
            'available_balance': float,
            'monthly_income': float,
            'debt_to_income_ratio': float,
            'recommendation': str
        }
    """

    # For hackathon demo: Use mock data based on user_id
    # In production: Replace with real Plaid API calls

    mock_credit_data = {
        'user_123': {  # Maria Rodriguez (Bella - Diabetes)
            'credit_score': 620,
            'credit_tier': 'fair',
            'available_balance': 450.00,
            'monthly_income': 3200.00,
            'debt_to_income_ratio': 0.45,  # 45% DTI - moderate risk
            'recommendation': 'Moderate risk: Has some liquidity but tight budget. Bridge Plan recommended.'
        },
        'user_456': {  # James Mitchell (Max - Heartworm)
            'credit_score': 720,
            'credit_tier': 'good',
            'available_balance': 2800.00,
            'monthly_income': 5500.00,
            'debt_to_income_ratio': 0.28,  # 28% DTI - low risk
            'recommendation': 'Low risk: Good credit and healthy finances. Standard retry likely to succeed.'
        },
        'user_789': {  # Sarah Chen (Whiskers - Kidney Disease)
            'credit_score': 580,
            'credit_tier': 'poor',
            'available_balance': 120.00,
            'monthly_income': 2400.00,
            'debt_to_income_ratio': 0.62,  # 62% DTI - high risk
            'recommendation': 'High risk: Low credit score and limited liquidity. Bridge Plan critical for retention.'
        }
    }

    # Return mock data for demo
    if user_id in mock_credit_data:
        return mock_credit_data[user_id]

    # Default fallback
    return {
        'credit_score': 650,
        'credit_tier': 'fair',
        'available_balance': 500.00,
        'monthly_income': 3000.00,
        'debt_to_income_ratio': 0.40,
        'recommendation': 'Moderate risk: Consider Bridge Plan for retention.'
    }


def get_account_balances(access_token: str) -> dict:
    """
    Fetch account balances from Plaid.

    For production with real access token:
    """
    # Example production code (commented out for demo):
    # try:
    #     request = AccountsBalanceGetRequest(access_token=access_token)
    #     response = client.accounts_balance_get(request)
    #
    #     total_balance = sum(
    #         account.balances.available or 0
    #         for account in response['accounts']
    #     )
    #
    #     return {
    #         'total_available': total_balance,
    #         'accounts': response['accounts']
    #     }
    # except Exception as e:
    #     print(f"Error fetching balances: {e}")
    #     return {'total_available': 0, 'accounts': []}

    # For demo: Return mock data
    return {
        'total_available': 450.00,
        'accounts': []
    }


def assess_payment_capacity(credit_data: dict, payment_amount: float = 50.00) -> dict:
    """
    Determine if customer can afford payment based on credit check.

    Args:
        credit_data: Output from calculate_credit_score()
        payment_amount: Monthly payment amount (default $50 Premium Plan)

    Returns:
        dict: {
            'can_afford_premium': bool,
            'can_afford_bridge': bool,
            'payment_risk_level': str,
            'recommended_plan': str
        }
    """
    available_balance = credit_data['available_balance']
    monthly_income = credit_data['monthly_income']
    dti_ratio = credit_data['debt_to_income_ratio']
    credit_tier = credit_data['credit_tier']

    # Calculate payment-to-income ratio
    payment_to_income = payment_amount / monthly_income if monthly_income > 0 else 1.0

    # Decision logic
    can_afford_premium = (
        available_balance >= payment_amount * 2  # At least 2x buffer
        and dti_ratio < 0.50  # DTI under 50%
        and credit_tier in ['excellent', 'good']
    )

    can_afford_bridge = available_balance >= 5.00  # Bridge Plan is $5/mo

    # Risk assessment
    if can_afford_premium:
        risk_level = 'low'
        recommended_plan = 'premium'
    elif can_afford_bridge:
        risk_level = 'medium'
        recommended_plan = 'bridge'
    else:
        risk_level = 'high'
        recommended_plan = 'bridge_with_extension'

    return {
        'can_afford_premium': can_afford_premium,
        'can_afford_bridge': can_afford_bridge,
        'payment_risk_level': risk_level,
        'recommended_plan': recommended_plan,
        'payment_to_income_ratio': payment_to_income
    }


# For future production use with real Plaid Link flow:
def create_link_token(user_id: str) -> str:
    """
    Create Plaid Link token for user authentication.
    This would be used in a real web app to let users connect their bank accounts.
    """
    try:
        request = LinkTokenCreateRequest(
            user=LinkTokenCreateRequestUser(client_user_id=user_id),
            client_name="PetDunning Enterprise",
            products=[Products('auth'), Products('transactions')],
            country_codes=[CountryCode('US')],
            language='en'
        )
        response = client.link_token_create(request)
        return response['link_token']
    except Exception as e:
        print(f"Error creating link token: {e}")
        return None
