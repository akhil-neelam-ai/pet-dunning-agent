"""
Mock API Tools: Stripe, Email, Database Operations
These simulate real API calls for the demo
"""
import json
import time
from datetime import datetime
from typing import Dict, Any


def mock_stripe_update_subscription(user_id: str, new_plan: str) -> Dict[str, Any]:
    """
    Mock Stripe API call to change subscription plan
    """
    # Simulate API latency
    time.sleep(0.5)

    # Mock response
    return {
        'status': 'success',
        'subscription_id': f'sub_{user_id}_{int(time.time())}',
        'customer_id': f'cus_{user_id}',
        'plan': new_plan,
        'amount': 5.00 if new_plan == 'bridge' else 50.00,
        'interval': 'month',
        'current_period_start': datetime.now().isoformat(),
        'current_period_end': datetime.now().isoformat(),
        'status': 'active'
    }


def mock_stripe_retry_payment(user_id: str) -> Dict[str, Any]:
    """
    Mock Stripe payment retry
    """
    time.sleep(0.5)

    # 50% success rate for demo purposes
    import random
    success = random.choice([True, False])

    if success:
        return {
            'status': 'success',
            'payment_intent_id': f'pi_{user_id}_{int(time.time())}',
            'amount': 50.00,
            'charged': True,
            'message': 'Payment successful'
        }
    else:
        return {
            'status': 'failed',
            'payment_intent_id': f'pi_{user_id}_{int(time.time())}',
            'amount': 50.00,
            'charged': False,
            'message': 'Card declined - insufficient funds'
        }


def mock_stripe_cancel_subscription(user_id: str) -> Dict[str, Any]:
    """
    Mock subscription cancellation
    """
    time.sleep(0.3)

    return {
        'status': 'canceled',
        'subscription_id': f'sub_{user_id}',
        'canceled_at': datetime.now().isoformat(),
        'message': 'Subscription canceled successfully'
    }


def update_user_database(user_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Mock database update
    """
    # Load current data
    with open('data/mock_db.json', 'r') as f:
        db = json.load(f)

    # Update user
    if user_id in db['users']:
        db['users'][user_id].update(updates)

        # Save back
        with open('data/mock_db.json', 'w') as f:
            json.dump(db, f, indent=2)

        return {
            'status': 'success',
            'user_id': user_id,
            'updated_fields': list(updates.keys())
        }
    else:
        return {
            'status': 'error',
            'message': f'User {user_id} not found'
        }


def send_email(to_email: str, subject: str, body: str) -> Dict[str, Any]:
    """
    Mock email sending (in real system, would use SendGrid/Mailgun)
    """
    time.sleep(0.2)

    return {
        'status': 'sent',
        'to': to_email,
        'subject': subject,
        'sent_at': datetime.now().isoformat(),
        'message_id': f'msg_{int(time.time())}'
    }


def tool_executor_node(state: dict) -> dict:
    """
    Execute tools based on current intent
    """
    user_id = state['user_id']
    intent = state.get('current_intent')
    tool_results = []

    # Execute appropriate tool based on intent
    if intent == 'accept_bridge':
        # Switch to bridge plan
        result = mock_stripe_update_subscription(user_id, 'bridge')
        tool_results.append({
            'tool': 'stripe.update_subscription',
            'result': result
        })

        # Update database
        db_result = update_user_database(user_id, {
            'current_plan': 'bridge',
            'last_payment_status': 'active',
            'balance': 0.00
        })
        tool_results.append({
            'tool': 'database.update_user',
            'result': db_result
        })

        # Update state
        return {
            'current_plan': 'bridge',
            'target_plan': 'bridge',
            'churn_prevented': True,
            'revenue_impact': 450.00,  # Calculated saved LTV
            'conversation_stage': 'completed',
            'tool_calls': state.get('tool_calls', []) + tool_results
        }

    elif intent == 'update_payment':
        # Retry payment
        result = mock_stripe_retry_payment(user_id)
        tool_results.append({
            'tool': 'stripe.retry_payment',
            'result': result
        })

        if result['status'] == 'success':
            return {
                'current_plan': 'premium',
                'churn_prevented': True,
                'revenue_impact': 50.00,
                'conversation_stage': 'completed',
                'tool_calls': state.get('tool_calls', []) + tool_results
            }
        else:
            return {
                'conversation_stage': 'negotiating',
                'tool_calls': state.get('tool_calls', []) + tool_results
            }

    elif intent == 'cancel_request':
        # Cancel subscription
        result = mock_stripe_cancel_subscription(user_id)
        tool_results.append({
            'tool': 'stripe.cancel_subscription',
            'result': result
        })

        return {
            'current_plan': 'cancelled',
            'churn_prevented': False,
            'revenue_impact': -12000.00,  # Lost LTV
            'conversation_stage': 'completed',
            'tool_calls': state.get('tool_calls', []) + tool_results
        }

    else:
        # No tool execution needed
        return state
