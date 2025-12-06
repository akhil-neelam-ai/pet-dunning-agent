"""
Extractor Agent: Intent Understanding and NLU
Uses Claude to extract user intent from free-form text responses
"""
import json
from anthropic import Anthropic
from state import AgentState, ExtractorOutput
from utils.config import get_api_key

client = Anthropic(api_key=get_api_key())


def extract_intent(user_message: str, conversation_context: str = "") -> ExtractorOutput:
    """
    Extract intent from user's message using Claude

    Supported intents:
    - accept_bridge: User agrees to Bridge Plan
    - decline_bridge: User declines Bridge Plan
    - financial_hardship: User mentions money problems
    - ask_for_more_info: User wants details
    - dispute_charge: User questions the charge
    - cancel_request: User wants to cancel
    - update_payment: User offers to update payment method
    - ask_for_time: User needs more time to pay
    """

    prompt = f"""You are an intent classification system for a veterinary payment system.

User's message: "{user_message}"

Conversation context: {conversation_context if conversation_context else "Initial payment failure notification sent"}

Classify the user's intent into ONE of these categories:
1. accept_bridge - User agrees to the $5 Bridge Plan (e.g., "yes", "ok", "do the $5 plan", "sure", "that works")
2. decline_bridge - User rejects Bridge Plan (e.g., "no thanks", "not interested", "just cancel")
3. financial_hardship - User mentions money problems (e.g., "can't afford", "don't have money", "tight on cash", "what are my options")
4. ask_for_more_info - User wants details (e.g., "what's included?", "tell me more", "how does it work?")
5. dispute_charge - User questions charge (e.g., "I already paid", "this is wrong", "why am I charged?")
6. cancel_request - User wants to cancel (e.g., "cancel my plan", "I'm done", "unsubscribe")
7. update_payment - User offers new payment method (e.g., "I'll update my card", "use my other card")
8. ask_for_time - User needs extension (e.g., "give me a week", "need more time", "ready to pay friday", "can pay next week")

IMPORTANT: Return ONLY valid JSON, no other text or markdown formatting.

{{
  "intent": "the_intent_name",
  "confidence": 0.95,
  "reasoning": "brief explanation",
  "entities": {{}}
}}"""

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )

    # Parse JSON response
    response_text = response.content[0].text.strip()

    # Remove markdown code blocks if present
    if response_text.startswith('```'):
        # Extract JSON from markdown code block
        lines = response_text.split('\n')
        response_text = '\n'.join(lines[1:-1]) if len(lines) > 2 else response_text
        response_text = response_text.replace('```json', '').replace('```', '').strip()

    try:
        result = json.loads(response_text)
        return ExtractorOutput(
            intent=result['intent'],
            confidence=result.get('confidence', 0.8),
            extracted_entities=result.get('entities', {}),
            reasoning=result.get('reasoning', 'Intent extracted successfully')
        )
    except (json.JSONDecodeError, KeyError):
        # Keyword-based fallback
        msg_lower = user_message.lower()

        # Check for common patterns
        if any(word in msg_lower for word in ['yes', 'sure', 'ok', 'do it', 'sounds good', 'that works']):
            return ExtractorOutput(intent='accept_bridge', confidence=0.7,
                                 extracted_entities={}, reasoning='Keyword match: acceptance')
        elif any(word in msg_lower for word in ['no money', "don't have", "can't afford", "tight", 'broke', 'options']):
            return ExtractorOutput(intent='financial_hardship', confidence=0.7,
                                 extracted_entities={}, reasoning='Keyword match: financial hardship')
        elif any(word in msg_lower for word in ['friday', 'next week', 'few days', 'pay later']):
            return ExtractorOutput(intent='ask_for_time', confidence=0.7,
                                 extracted_entities={}, reasoning='Keyword match: needs time')
        elif any(word in msg_lower for word in ['cancel', 'stop', 'unsubscribe']):
            return ExtractorOutput(intent='cancel_request', confidence=0.7,
                                 extracted_entities={}, reasoning='Keyword match: cancellation')
        elif any(word in msg_lower for word in ['what', 'how', 'details', 'tell me more', 'included']):
            return ExtractorOutput(intent='ask_for_more_info', confidence=0.7,
                                 extracted_entities={}, reasoning='Keyword match: asking for info')
        else:
            return ExtractorOutput(intent='financial_hardship', confidence=0.6,
                                 extracted_entities={}, reasoning='Default: assuming financial concern')


def extractor_node(state: AgentState) -> dict:
    """
    Extract intent from the latest user message
    """
    messages = state['messages']

    # Get the last user message
    user_messages = [m for m in messages if m['role'] == 'user']
    if not user_messages:
        return state  # No user message yet

    last_user_message = user_messages[-1]['content']

    # Build conversation context
    context = f"User: {state['user_name']}, Pet: {state['pet_name']} ({state['pet_condition']})"
    if state.get('router_decision'):
        context += f", Recommendation: {state['router_decision']}"

    # Extract intent
    extraction = extract_intent(last_user_message, context)

    # Map intent to conversation stage
    stage_map = {
        'accept_bridge': 'closing',
        'decline_bridge': 'objection_handling',
        'financial_hardship': 'negotiating',
        'ask_for_more_info': 'negotiating',
        'cancel_request': 'objection_handling',
        'update_payment': 'closing'
    }

    new_stage = stage_map.get(extraction['intent'], 'negotiating')

    # Update state
    return {
        'current_intent': extraction['intent'],
        'conversation_stage': new_stage,
        'tool_calls': state.get('tool_calls', []) + [{
            'agent': 'extractor',
            'intent': extraction['intent'],
            'confidence': extraction['confidence'],
            'reasoning': extraction['reasoning']
        }]
    }
