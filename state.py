"""
LangGraph State Definitions for PetDunning Agent
"""
from typing import TypedDict, List, Optional, Literal
from datetime import datetime


class Message(TypedDict):
    """Represents a single message in the conversation"""
    role: Literal["user", "assistant", "system"]
    content: str
    timestamp: str


class AgentState(TypedDict):
    """Main state object passed through the LangGraph workflow"""

    # User Context
    user_id: str
    user_name: str
    user_email: str
    pet_name: str
    pet_condition: str

    # Risk Assessment
    medical_risk_tier: str  # 'high', 'medium', 'low'
    risk_score: float  # 0.0 to 1.0
    ltv: float
    tenure_months: int

    # Conversation State
    messages: List[Message]
    current_intent: Optional[str]  # 'accept_bridge', 'financial_hardship', 'decline_cancel', etc.
    conversation_stage: str  # 'initial', 'negotiating', 'closing', 'completed'

    # Plan State
    current_plan: str  # 'premium', 'bridge', 'cancelled'
    target_plan: Optional[str]  # What plan we're trying to move them to

    # Decision Tracking (for Glass Box visualization)
    router_decision: Optional[str]
    negotiation_strategy: Optional[str]
    tool_calls: List[dict]

    # Metrics
    revenue_impact: float
    churn_prevented: bool


class RouterOutput(TypedDict):
    """Output from the Router agent"""
    should_retain: bool
    recommended_action: str  # 'offer_bridge_plan', 'standard_retry', 'cancel'
    reasoning: str
    risk_score: float


class ExtractorOutput(TypedDict):
    """Output from the Intent Extractor"""
    intent: str
    confidence: float
    extracted_entities: dict
    reasoning: str


class NegotiatorOutput(TypedDict):
    """Output from the Negotiator agent"""
    message: str
    tone: str
    strategy: str
