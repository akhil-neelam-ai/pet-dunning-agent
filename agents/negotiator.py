"""
Negotiator Agent: Claude-powered empathetic message generation
Uses Claude Sonnet 4.5 to craft contextual, emotionally intelligent messages
"""
import os
from anthropic import Anthropic
from state import AgentState, NegotiatorOutput
from dotenv import load_dotenv

load_dotenv()

# Initialize Claude client
client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))


def generate_initial_outreach(state: AgentState) -> str:
    """
    Generate the first message to the user after payment failure
    """
    user_name = state['user_name']
    pet_name = state['pet_name']
    pet_condition = state['pet_condition']
    plan_cost = 50.00  # From state

    prompt = f"""You are a compassionate customer care agent for VCA Animal Hospitals, a leading veterinary care network.

Context:
- Customer: {user_name}
- Pet: {pet_name} (diagnosed with {pet_condition})
- Issue: Payment of ${plan_cost} failed on their Premium Care Plan
- Medical Risk: HIGH - {pet_name}'s condition requires ongoing care

Your goal:
Write a brief, empathetic email (3-4 sentences) that:
1. Acknowledges the payment issue gently (no shame/blame)
2. Emphasizes we understand {pet_name}'s medical needs are critical
3. Introduces a solution: our $5/month "Bridge Plan" that keeps medical records active and telehealth access during financial hardship
4. Asks if they'd like to learn more

Tone: Warm, human, supportive (not corporate). Mention the pet's name and condition to show you care.

Write ONLY the email body (no subject line, no signature)."""

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text


def generate_bridge_plan_explanation(state: AgentState) -> str:
    """
    Explain the Bridge Plan details when user shows interest
    """
    pet_name = state['pet_name']

    prompt = f"""You are explaining the "Bridge Plan" to a customer who's interested but needs details.

Bridge Plan Details:
- Cost: $5/month (vs $50/month Premium)
- Includes: Medical records access, 24/7 telehealth, priority appointment booking
- Paused: In-person unlimited visits, prescription delivery, dental cleanings
- Duration: Flexible - upgrade back to Premium anytime

Write a clear, reassuring explanation (3-4 sentences) that:
1. Lists what {pet_name} KEEPS (telehealth, records)
2. Briefly mentions what's paused
3. Emphasizes this is temporary and they can upgrade anytime
4. Ends with "Would you like me to switch you to the Bridge Plan?"

Tone: Clear, helpful, no pressure."""

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text


def generate_decline_response(state: AgentState) -> str:
    """
    Handle when user declines Bridge Plan
    Offer to update payment method or cancel
    """
    user_name = state['user_name']
    pet_name = state['pet_name']

    prompt = f"""The customer {user_name} has declined the Bridge Plan offer for {pet_name}.

Now offer two options:
1. Update their payment method to keep Premium Plan active
2. Cancel the subscription (acknowledge this means losing access)

Write a brief, respectful message (2-3 sentences) that:
- Acknowledges their decision
- Presents both options clearly
- Asks which they'd prefer

Tone: Professional, no guilt-tripping."""

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=250,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text


def generate_success_confirmation(state: AgentState) -> str:
    """
    Confirm Bridge Plan activation
    """
    pet_name = state['pet_name']

    prompt = f"""The customer just accepted the Bridge Plan for {pet_name}.

Write a warm confirmation message (2-3 sentences) that:
1. Confirms Bridge Plan is now active at $5/month
2. Reassures that {pet_name}'s medical records and telehealth are available 24/7
3. Reminds them they can upgrade back to Premium anytime

Tone: Celebratory but calm, supportive."""

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text


def generate_payment_extension_response(state: AgentState) -> str:
    """
    Handle payment extension/deferment requests
    """
    user_name = state['user_name']
    pet_name = state['pet_name']

    prompt = f"""The customer {user_name} asked if they can stay on their Premium Plan and pay the full amount in 15 days.

Write a response (2-3 sentences) that:
1. Acknowledges their request to defer payment
2. Explains we can offer a 14-day payment extension
3. OR gently suggests the Bridge Plan as a safer alternative during the extension period
4. Asks them which option they'd prefer

Tone: Accommodating, helpful, gives them choices."""

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=250,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text


def generate_clarification_request(state: AgentState) -> str:
    """
    Ask for clarification when user says yes/ok but multiple options were offered
    """
    user_name = state['user_name']

    prompt = f"""The customer {user_name} just said "yes" but you had offered them TWO options:
Option A: 14-day payment extension (stay on Premium Plan, pay full amount later)
Option B: Bridge Plan ($5/month temporary plan with core features)

Write a brief, friendly clarification request (1-2 sentences) that:
1. Thanks them for responding
2. Asks which specific option they'd like to choose
3. Restates the two options clearly

Tone: Friendly, not robotic, quick clarification."""

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text


def generate_extension_confirmation(state: AgentState) -> str:
    """
    Confirm payment extension (staying on Premium Plan)
    """
    user_name = state['user_name']
    pet_name = state['pet_name']

    prompt = f"""The customer {user_name} chose the 14-day payment extension option to stay on their Premium Plan.

Write a confirmation message (2-3 sentences) that:
1. Confirms the 14-day extension is approved
2. Specifies the new payment due date
3. Reassures that {pet_name} keeps all Premium benefits active during this time
4. Mentions they can reach out if anything changes

Tone: Supportive, professional, reassuring."""

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text


def negotiator_node(state: AgentState) -> dict:
    """
    Main negotiator node - generates appropriate message based on conversation stage
    """
    conversation_stage = state['conversation_stage']
    current_intent = state.get('current_intent')

    # Determine which message to generate
    if conversation_stage == 'initial':
        message = generate_initial_outreach(state)
        strategy = 'initial_outreach_with_bridge_offer'

    elif current_intent == 'ambiguous_acceptance':
        # User said yes but didn't specify which option - need clarification
        message = generate_clarification_request(state)
        strategy = 'request_clarification'

    elif current_intent == 'accept_extension':
        # User explicitly chose payment extension
        message = generate_extension_confirmation(state)
        strategy = 'confirm_payment_extension'

    elif current_intent == 'financial_hardship' or current_intent == 'ask_for_more_info':
        message = generate_bridge_plan_explanation(state)
        strategy = 'explain_bridge_plan_details'

    elif current_intent == 'ask_for_time':
        message = generate_payment_extension_response(state)
        strategy = 'offer_payment_extension'

    elif current_intent == 'decline_bridge':
        message = generate_decline_response(state)
        strategy = 'offer_payment_update_or_cancel'

    elif current_intent == 'accept_bridge':
        message = generate_success_confirmation(state)
        strategy = 'confirm_bridge_activation'

    else:
        # Default fallback
        message = "Thank you for your response. Our team will follow up with you shortly."
        strategy = 'default_acknowledgment'

    # Update state with new message
    new_message = {
        'role': 'assistant',
        'content': message,
        'timestamp': ''  # Will be filled by UI
    }

    return {
        'messages': state['messages'] + [new_message],
        'negotiation_strategy': strategy,
        'tool_calls': state.get('tool_calls', []) + [{
            'agent': 'negotiator',
            'strategy': strategy,
            'message_preview': message[:100] + '...'
        }]
    }
