"""
PetDunning Enterprise - "The Churn Shield"
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
    page_title="PetDunning Enterprise | The Churn Shield",
    page_icon="🐾"
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
        min-height: 500px;
        max-height: 600px;
        overflow-y: auto;
    }
    .glass-box-container {
        background-color: #F8F9FA;
        border: 1px solid #E0E0E0;
        border-radius: 12px;
        padding: 20px;
        min-height: 500px;
        max-height: 600px;
        overflow-y: auto;
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
st.markdown('<div class="main-header">🐾 PetDunning Enterprise</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI-Powered Financial Triage for Veterinary Health Networks</div>', unsafe_allow_html=True)

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
            col1, col2 = st.columns(2)

            with col1:
                st.metric("Conversation Stage", st.session_state.agent_state['conversation_stage'].upper())
                st.metric("Risk Score", f"{st.session_state.agent_state['risk_score']:.2f}")

            with col2:
                st.metric("Current Plan", st.session_state.agent_state['current_plan'].upper())
                if st.session_state.agent_state.get('current_intent'):
                    st.metric("Detected Intent", st.session_state.agent_state['current_intent'])

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

    # Show workflow diagram
    st.markdown("### 🔄 How PetDunning Works")
    flowchart_visualization()

# Footer
st.divider()
st.caption("Built with ❤️ using Claude Sonnet 4.5, LangGraph, and Streamlit | Demo for Mars Veterinary Health")
