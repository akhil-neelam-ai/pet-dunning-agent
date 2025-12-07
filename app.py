"""
CareLoop - Keeping Pets in Care, Revenue in Loop
Main Streamlit Application
"""
import streamlit as st
import json
import time
from datetime import datetime
from graph import create_petdunning_graph, create_response_graph
from state import AgentState
from utils.ui_components import (
    gmail_style_message,
    typing_indicator,
    plan_comparison_table,
    glass_box_panel,
    user_table,
    flowchart_visualization
)
from utils.metrics import calculate_revenue_saved, format_currency

# Page config
st.set_page_config(
    layout="wide",
    page_title="CareLoop | AI-Powered Revenue Retention",
    page_icon="🔄"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 36px;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    .subtitle {
        color: #666;
        font-size: 16px;
        margin-bottom: 30px;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 10px 24px;
        font-weight: 600;
        border-radius: 8px;
    }
    .email-container {
        background-color: #fff;
        border: 1px solid #E0E0E0;
        border-radius: 12px;
        padding: 20px;
        max-height: 600px;
        overflow-y: auto;
    }
    .glass-box-container {
        background-color: #F8F9FA;
        border: 1px solid #E0E0E0;
        border-radius: 12px;
        padding: 20px;
        max-height: 600px;
        overflow-y: auto;
    }
    /* Make metrics text smaller to fit better */
    [data-testid="stMetricValue"] {
        font-size: 20px !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: 12px !important;
    }
    /* Make dataframe text larger for better readability */
    [data-testid="stDataFrame"] {
        font-size: 16px !important;
    }
    [data-testid="stDataFrame"] table {
        font-size: 16px !important;
    }
    [data-testid="stDataFrame"] th {
        font-size: 17px !important;
        font-weight: 700 !important;
    }
    /* Make chat input larger */
    [data-testid="stChatInput"] textarea {
        font-size: 16px !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.current_user = None
    st.session_state.agent_state = None
    st.session_state.conversation_active = False
    st.session_state.total_revenue_saved = 0
    st.session_state.users_processed = 0
    st.session_state.churn_prevented_count = 0
    st.session_state.show_typing = False

# Load data
@st.cache_data
def load_data():
    with open('data/mock_db.json', 'r') as f:
        return json.load(f)

data = load_data()

# Header
st.markdown('<div class="main-header">🔄 CareLoop</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Keeping Pets in Care, Revenue in Loop | AI-Powered Retention for Veterinary Networks</div>', unsafe_allow_html=True)

# CFO Dashboard - Top Metrics
st.markdown("### 📊 Real-Time Impact Dashboard")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="💰 Revenue Saved (LTV)",
        value=format_currency(st.session_state.total_revenue_saved),
        help="Total future LTV preserved by AI interventions"
    )

with col2:
    st.metric(
        label="🛡️ Churn Prevented",
        value=st.session_state.churn_prevented_count,
        help="Customers retained vs. standard dunning"
    )

with col3:
    st.metric(
        label="👥 Users Processed",
        value=st.session_state.users_processed,
        help="Total payment failures handled today"
    )

with col4:
    retention_rate = (
        (st.session_state.churn_prevented_count / st.session_state.users_processed * 100)
        if st.session_state.users_processed > 0 else 0
    )
    st.metric(
        label="📈 Retention Rate",
        value=f"{retention_rate:.0f}%",
        help="AI success rate vs. 40% standard dunning"
    )

st.divider()

# Multi-User Table
st.markdown("### 📋 At-Risk Customers")

# Build users list
users_list = []
for user_id, user_data in data['users'].items():
    users_list.append({
        'User': user_data['name'],
        'Pet': f"{user_data['pet_name']} ({user_data['pet_condition']})",
        'LTV': user_data['ltv'],
        'Tenure': f"{user_data['tenure_months']} mo",
        'Risk': user_data['medical_risk_tier'].upper(),
        'Status': user_data['current_plan'].upper()
    })

# Display table with container for better spacing
with st.container():
    user_table(users_list)

st.divider()

# Sidebar - Demo Controls
with st.sidebar:
    st.markdown("### 🎮 Demo Controls")

    # User selector
    user_names = {
        f"{data['users'][uid]['name']} ({data['users'][uid]['pet_name']})": uid
        for uid in data['users'].keys()
    }

    selected_user_name = st.selectbox(
        "Select Customer",
        options=list(user_names.keys()),
        key="user_selector"
    )

    selected_user_id = user_names[selected_user_name]

    # Trigger button
    if st.button("🚨 Simulate Payment Failure", use_container_width=True):
        # Initialize agent state
        user_data = data['users'][selected_user_id]

        st.session_state.agent_state = AgentState(
            user_id=selected_user_id,
            user_name=user_data['name'],
            user_email=user_data['email'],
            pet_name=user_data['pet_name'],
            pet_condition=user_data['pet_condition'],
            medical_risk_tier=user_data['medical_risk_tier'],
            risk_score=0.0,
            ltv=user_data['ltv'],
            tenure_months=user_data['tenure_months'],
            # Payment history data (will be populated by router)
            payment_history=None,
            payment_risk_score=None,
            payment_risk_tier=None,
            failure_rate=None,
            late_payment_rate=None,
            payment_reliability=None,
            # Medical data (will be populated by router)
            medical_history=None,
            medication_adherence_score=None,
            medical_urgency_score=None,
            medical_urgency_tier=None,
            continuity_of_care_importance=None,
            # Retention priority (will be populated by router)
            retention_priority_score=None,
            retention_decision=None,
            should_engage_ai=None,
            # Conversation data
            messages=[],
            current_intent=None,
            conversation_stage='initial',
            current_plan=user_data['current_plan'],
            target_plan=None,
            router_decision=None,
            negotiation_strategy=None,
            tool_calls=[],
            revenue_impact=0.0,
            churn_prevented=False
        )

        st.session_state.conversation_active = True
        st.session_state.current_user = selected_user_id
        st.session_state.users_processed += 1
        st.session_state.show_typing = True
        st.rerun()

    st.divider()

    # Show plan comparison
    st.markdown("### 💎 Plan Comparison")
    with st.expander("Premium vs Bridge", expanded=False):
        plan_comparison_table()

    st.divider()

    # Workflow visualization
    st.markdown("### 🔄 Agent Workflow")
    with st.expander("View Flowchart", expanded=False):
        flowchart_visualization()

# Main Content - Split Screen
if st.session_state.conversation_active:
    col_left, col_right = st.columns([1, 1])

    # LEFT PANEL: Email Interface
    with col_left:
        st.markdown("### 📧 Email Conversation")
        st.caption(f"To: {st.session_state.agent_state['user_email']}")

        email_container = st.container()

        with email_container:
            st.markdown('<div class="email-container">', unsafe_allow_html=True)

            # Run initial agent workflow if no messages yet
            if len(st.session_state.agent_state['messages']) == 0:
                with st.spinner("AI Agent analyzing risk..."):
                    # Create and run graph
                    graph = create_petdunning_graph()

                    # Stream through the graph
                    for event in graph.stream(st.session_state.agent_state):
                        # Update state with each event
                        for key, value in event.items():
                            if isinstance(value, dict):
                                st.session_state.agent_state.update(value)

                    time.sleep(1)  # Simulate processing time
                    st.session_state.show_typing = False
                    st.rerun()

            # Display conversation history
            for msg in st.session_state.agent_state['messages']:
                gmail_style_message(msg, is_user=(msg['role'] == 'user'))

            # Show typing indicator
            if st.session_state.show_typing:
                typing_indicator()

            st.markdown('</div>', unsafe_allow_html=True)

        # User input
        if not st.session_state.show_typing and st.session_state.agent_state['conversation_stage'] != 'completed':
            user_input = st.chat_input("Type your reply as the customer...")

            if user_input:
                # Add user message to state
                user_message = {
                    'role': 'user',
                    'content': user_input,
                    'timestamp': datetime.now().isoformat()
                }
                st.session_state.agent_state['messages'].append(user_message)

                # Show typing indicator
                st.session_state.show_typing = True
                st.rerun()

        # Process user response
        if st.session_state.show_typing and len([m for m in st.session_state.agent_state['messages'] if m['role'] == 'user']) > 0:
            with st.spinner("AI Agent thinking..."):
                time.sleep(1.5)  # Simulate thinking time

                # Run response graph
                response_graph = create_response_graph()

                for event in response_graph.stream(st.session_state.agent_state):
                    for key, value in event.items():
                        if isinstance(value, dict):
                            st.session_state.agent_state.update(value)

                # Update metrics if conversation completed
                if st.session_state.agent_state.get('churn_prevented'):
                    st.session_state.churn_prevented_count += 1
                    st.session_state.total_revenue_saved += st.session_state.agent_state.get('revenue_impact', 0)

                st.session_state.show_typing = False
                st.rerun()

    # RIGHT PANEL: Glass Box
    with col_right:
        st.markdown("### 🔍 AI Decision Transparency")

        with st.container():
            st.markdown('<div class="glass-box-container">', unsafe_allow_html=True)

            # Show current state
            st.markdown("#### Current State")

            # Row 1: Main metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Conversation Stage", st.session_state.agent_state['conversation_stage'].upper())
            with col2:
                st.metric("Current Plan", st.session_state.agent_state['current_plan'].upper())
            with col3:
                if st.session_state.agent_state.get('payment_risk_score') is not None:
                    payment_tier = st.session_state.agent_state.get('payment_risk_tier', 'N/A')
                    st.metric("Payment Risk", f"{st.session_state.agent_state['payment_risk_score']:.1f} ({payment_tier})")

            # Row 2: Additional metrics
            col4, col5, col6 = st.columns(3)
            with col4:
                st.metric("Risk Score", f"{st.session_state.agent_state['risk_score']:.2f}")
            with col5:
                if st.session_state.agent_state.get('payment_reliability'):
                    st.metric("Payment Reliability", st.session_state.agent_state['payment_reliability'].upper())
            with col6:
                if st.session_state.agent_state.get('current_intent'):
                    st.metric("Detected Intent", st.session_state.agent_state['current_intent'].replace('_', ' ').title())

            # Row 3: Medical metrics
            if st.session_state.agent_state.get('medical_urgency_score'):
                col7, col8, col9 = st.columns(3)
                with col7:
                    st.metric("Medical Urgency", f"{st.session_state.agent_state['medical_urgency_score']:.1f}/100")
                with col8:
                    if st.session_state.agent_state.get('medication_adherence_score'):
                        st.metric("Medication Adherence", f"{st.session_state.agent_state['medication_adherence_score']}%")
                with col9:
                    if st.session_state.agent_state.get('continuity_of_care_importance'):
                        st.metric("Care Importance", st.session_state.agent_state['continuity_of_care_importance'])

            # Row 4: Retention Priority (Autonomous AI Decision)
            # Note: We engage with ALL customers, but offer type varies by retention priority
            if st.session_state.agent_state.get('retention_priority_score') is not None:
                col10, col11, col12 = st.columns(3)
                with col10:
                    score = st.session_state.agent_state['retention_priority_score']
                    st.metric("🎯 Retention Priority", f"{score:.1f}/100",
                             help="AI score determining offer type - all customers get tailored outreach")
                with col11:
                    if st.session_state.agent_state.get('retention_decision'):
                        decision = st.session_state.agent_state['retention_decision'].replace('_', ' ').title()
                        st.metric("Outreach Strategy", decision,
                                 help="Offer type based on medical urgency + payment risk profile")
                with col12:
                    # Empty column for alignment consistency
                    pass

            st.divider()

            # Glass box panel
            glass_box_panel(st.session_state.agent_state)

            # Show success celebration
            if st.session_state.agent_state.get('churn_prevented'):
                st.success("🎉 SUCCESS: Customer retained! Churn prevented.")
                st.balloons()

            st.markdown('</div>', unsafe_allow_html=True)

else:
    # Welcome screen
    st.info("👈 Select a customer and click 'Simulate Payment Failure' to start the demo")

# Footer
st.divider()
st.caption("Built with ❤️ using Claude Sonnet 4.5, LangGraph, and Streamlit | CareLoop - Demo for Mars Veterinary Health")
