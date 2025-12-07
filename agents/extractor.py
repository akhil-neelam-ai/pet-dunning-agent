"""
Extractor Agent: Intent Understanding and NLU
Uses Claude to extract user intent from free-form text responses
"""
import os
import json
from anthropic import Anthropic
from state import AgentState, ExtractorOutput
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))


def extract_intent(user_message: str, conversation_context: str = "", last_assistant_message: str = "") -> ExtractorOutput:
    """
    Extract intent from user's message using Claude

    Supported intents:
    - accept_bridge: User agrees to Bridge Plan (explicitly or clearly)
    - accept_extension: User chooses payment extension option
    - ambiguous_acceptance: User says yes/ok but multiple options were offered
    - decline_bridge: User declines Bridge Plan
    - financial_hardship: User mentions money problems
    - ask_for_more_info: User wants details
    - dispute_charge: User questions the charge
    - cancel_request: User wants to cancel
    - update_payment: User offers to update payment method
    - ask_for_time: User needs more time to pay
    """

    # Check if last message offered multiple options
    multiple_options_offered = False
    if last_assistant_message:
        # Look for indicators of multiple options: "or", "option", "which", "prefer", "choose"
        option_indicators = ['which option', 'or', 'prefer', 'choose between', 'two options', 'either']
        multiple_options_offered = any(indicator in last_assistant_message.lower() for indicator in option_indicators)

    prompt = f"""You are an intent classification system for a veterinary payment system.

User's message: "{user_message}"

Conversation context: {conversation_context if conversation_context else "Initial payment failure notification sent"}

Last assistant message: "{last_assistant_message if last_assistant_message else "None"}"

IMPORTANT RULE: If the last assistant message offered MULTIPLE OPTIONS (e.g., "Option A or Option B?", "Which would you prefer?")
and the user responds with just "yes", "ok", "sure" WITHOUT specifying which option, classify as "ambiguous_acceptance".

Classify the user's intent into ONE of these categories:
1. accept_bridge - User EXPLICITLY agrees to Digital Keeper Plan (e.g., "yes to keeper plan", "do the $4.99 plan", "switch to keeper")
2. accept_extension - User EXPLICITLY chooses payment extension (e.g., "yes to extension", "give me 14 days", "keep premium for now")
3. ambiguous_acceptance - User says yes/ok/sure but multiple options were offered and they didn't specify which (IMPORTANT!)
4. decline_bridge - User rejects Bridge Plan (e.g., "no thanks", "not interested", "just cancel")
5. financial_hardship - User mentions money problems (e.g., "can't afford", "don't have money", "tight on cash")
6. ask_for_more_info - User wants details (e.g., "what's included?", "tell me more")
7. cancel_request - User wants to cancel (e.g., "cancel my plan", "I'm done")
8. update_payment - User offers new payment method (e.g., "I'll update my card")
9. ask_for_time - User needs extension (e.g., "give me a week", "need more time")

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
            # Check if multiple options were offered - if so, mark as ambiguous
            if multiple_options_offered and not any(specific in msg_lower for specific in ['bridge', 'keeper', 'extension', '$4.99', '$5', '14 day', 'premium', 'plan']):
                return ExtractorOutput(intent='ambiguous_acceptance', confidence=0.8,
                                     extracted_entities={}, reasoning='Ambiguous: yes/ok without specifying which option')
            # Check for specific option mentions
            elif 'keeper' in msg_lower or '$4.99' in msg_lower or '$5' in msg_lower:
                return ExtractorOutput(intent='accept_bridge', confidence=0.7,
                                     extracted_entities={}, reasoning='Keyword match: accepts Bridge Plan')
            elif 'extension' in msg_lower or 'premium' in msg_lower or '14' in msg_lower:
                return ExtractorOutput(intent='accept_extension', confidence=0.7,
                                     extracted_entities={}, reasoning='Keyword match: accepts extension')
            else:
                return ExtractorOutput(intent='accept_bridge', confidence=0.6,
                                     extracted_entities={}, reasoning='Keyword match: generic acceptance')
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

    # Get the last assistant message (to check for multiple options)
    assistant_messages = [m for m in messages if m['role'] == 'assistant']
    last_assistant_message = assistant_messages[-1]['content'] if assistant_messages else ""

    # Build conversation context
    context = f"User: {state['user_name']}, Pet: {state['pet_name']} ({state['pet_condition']})"
    if state.get('router_decision'):
        context += f", Recommendation: {state['router_decision']}"

    # Extract intent with last assistant message for context
    extraction = extract_intent(last_user_message, context, last_assistant_message)

    # Map intent to conversation stage
    stage_map = {
        'accept_bridge': 'closing',
        'accept_extension': 'closing',
        'ambiguous_acceptance': 'negotiating',  # Need clarification
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
