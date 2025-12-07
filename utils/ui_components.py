"""
Custom Streamlit UI Components
"""
import streamlit as st
import time
from datetime import datetime


def gmail_style_message(message: dict, is_user: bool = False):
    """
    Render a message in Gmail-style format
    """
    if is_user:
        # User message (right-aligned, blue background)
        st.markdown(f"""
        <div style="display: flex; justify-content: flex-end; margin: 10px 0;">
            <div style="background-color: #D3E3FD; padding: 12px 16px; border-radius: 18px;
                        max-width: 70%; text-align: left; color: #000;">
                {message['content']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Assistant message (left-aligned, gray background)
        st.markdown(f"""
        <div style="display: flex; justify-content: flex-start; margin: 10px 0;">
            <div style="background-color: #F1F3F4; padding: 12px 16px; border-radius: 18px;
                        max-width: 70%; text-align: left; color: #000;">
                <div style="font-weight: 600; color: #1A73E8; margin-bottom: 4px;">
                    VCA Care Team
                </div>
                {message['content']}
            </div>
        </div>
        """, unsafe_allow_html=True)


def typing_indicator():
    """
    Show typing indicator animation
    """
    st.markdown("""
    <div style="display: flex; justify-content: flex-start; margin: 10px 0;">
        <div style="background-color: #F1F3F4; padding: 12px 16px; border-radius: 18px;">
            <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    </div>
    <style>
    .typing-indicator {
        display: flex;
        gap: 4px;
    }
    .typing-indicator span {
        width: 8px;
        height: 8px;
        background-color: #999;
        border-radius: 50%;
        animation: typing 1.4s infinite;
    }
    .typing-indicator span:nth-child(2) {
        animation-delay: 0.2s;
    }
    .typing-indicator span:nth-child(3) {
        animation-delay: 0.4s;
    }
    @keyframes typing {
        0%, 60%, 100% {
            transform: translateY(0);
            opacity: 0.7;
        }
        30% {
            transform: translateY(-10px);
            opacity: 1;
        }
    }
    </style>
    """, unsafe_allow_html=True)


def plan_comparison_table():
    """
    Render Premium vs Bridge plan comparison
    """
    st.markdown("""
    <style>
    .plan-table {
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
    }
    .plan-table th {
        background-color: #1A73E8;
        color: white;
        padding: 12px;
        text-align: left;
    }
    .plan-table td {
        padding: 10px 12px;
        border-bottom: 1px solid #E0E0E0;
    }
    .plan-table tr:hover {
        background-color: #F8F9FA;
    }
    .included {
        color: #0F9D58;
        font-weight: 600;
    }
    .not-included {
        color: #DB4437;
        font-weight: 600;
    }
    </style>

    <table class="plan-table">
        <thead>
            <tr>
                <th>Service</th>
                <th>$19.99 Access Plan (Current)</th>
                <th>$4.99 Digital Keeper Plan</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Unlimited Exams</td>
                <td class="included">✓ Included</td>
                <td class="not-included">✗ Excluded</td>
            </tr>
            <tr>
                <td>24/7 Live Chat</td>
                <td class="included">✓ Included</td>
                <td class="included">✓ Included</td>
            </tr>
            <tr>
                <td>Microchip & Membership</td>
                <td class="included">✓ Included</td>
                <td class="included">✓ Included</td>
            </tr>
            <tr>
                <td>Exclusive Member Benefits</td>
                <td class="included">✓ Included</td>
                <td class="included">✓ Included</td>
            </tr>
            <tr>
                <td>Medical Records Retention</td>
                <td class="included">✓ Included</td>
                <td class="included">✓ Included</td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)


def glass_box_panel(state: dict):
    """
    Render the "Glass Box" AI reasoning panel
    """
    st.markdown("### 🧠 AI Decision Log")

    # Show tool calls in reverse chronological order
    tool_calls = state.get('tool_calls', [])

    for i, call in enumerate(reversed(tool_calls)):
        agent = call.get('agent', 'unknown')
        timestamp = datetime.now().strftime("%H:%M:%S")

        with st.expander(f"🔸 {agent.upper()} - {timestamp}", expanded=(i == 0)):
            # Router
            if agent == 'router':
                st.markdown(f"**Decision:** `{call.get('decision')}`")
                st.markdown(f"**Risk Score:** `{call.get('risk_score', 0):.2f}`")

                # Payment History Display
                payment_check = call.get('payment_check', {})
                if payment_check:
                    st.markdown("---")
                    st.markdown("**💳 Payment History Analysis:**")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"- **Risk Score:** `{payment_check.get('risk_score', 'N/A'):.1f}/100`")
                        st.markdown(f"- **Risk Tier:** `{payment_check.get('risk_tier', 'N/A')}`")
                        st.markdown(f"- **Reliability:** `{payment_check.get('reliability', 'N/A').upper()}`")
                    with col2:
                        st.markdown(f"- **Failure Rate:** `{payment_check.get('failure_rate', 'N/A'):.1f}%`")
                        st.markdown(f"- **Late Rate:** `{payment_check.get('late_rate', 'N/A'):.1f}%`")
                        st.markdown(f"- **Total Payments:** `{payment_check.get('total_payments', 'N/A')}`")

                # Medical Check Display
                medical_check = call.get('medical_check', {})
                if medical_check:
                    st.markdown("---")
                    st.markdown("**🏥 Medical History Check:**")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"- **Urgency Score:** `{medical_check.get('urgency_score', 'N/A'):.1f}/100`")
                        st.markdown(f"- **Urgency Tier:** `{medical_check.get('urgency_tier', 'N/A')}`")
                    with col2:
                        st.markdown(f"- **Adherence:** `{medical_check.get('adherence_score', 'N/A')}%`")
                        st.markdown(f"- **Critical Meds:** `{medical_check.get('critical_medications', 0)}`")

                st.info(call.get('reasoning', ''))

            # Extractor
            elif agent == 'extractor':
                st.markdown(f"**Intent Detected:** `{call.get('intent')}`")
                st.markdown(f"**Confidence:** `{call.get('confidence', 0):.0%}`")
                st.success(call.get('reasoning', ''))

            # Negotiator
            elif agent == 'negotiator':
                st.markdown(f"**Strategy:** `{call.get('strategy')}`")
                st.markdown(f"**Message Preview:**")
                st.text(call.get('message_preview', ''))

            # Tool Executor
            elif 'tool' in call:
                st.markdown(f"**API Call:** `{call.get('tool')}`")
                st.json(call.get('result', {}))


def metric_card(label: str, value: str, delta: str = None, help_text: str = None):
    """
    Render a metric card
    """
    delta_html = ""
    if delta:
        delta_color = "#0F9D58" if not delta.startswith("-") else "#DB4437"
        delta_html = f'<div style="color: {delta_color}; font-size: 14px; margin-top: 4px;">{delta}</div>'

    help_html = ""
    if help_text:
        help_html = f'<div style="color: #666; font-size: 12px; margin-top: 8px;">{help_text}</div>'

    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px; border-radius: 10px; color: white; margin: 10px 0;">
        <div style="font-size: 14px; opacity: 0.9;">{label}</div>
        <div style="font-size: 32px; font-weight: 700; margin: 8px 0;">{value}</div>
        {delta_html}
        {help_html}
    </div>
    """, unsafe_allow_html=True)


def user_table(users_data: list):
    """
    Render a table of users with their status
    """
    import pandas as pd

    df = pd.DataFrame(users_data)
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Status": st.column_config.Column(
                width="small",
            ),
            "LTV": st.column_config.NumberColumn(
                format="$%d",
            ),
            "Risk": st.column_config.Column(
                width="small",
            )
        }
    )


def flowchart_visualization():
    """
    Render the agent workflow as a flowchart using mermaid
    """
    st.markdown("""
    ```mermaid
    graph TD
        A[Payment Failed] --> B[Risk Router]
        B --> C{High Medical Risk<br/>+ High LTV?}
        C -->|Yes| D[AI Negotiator]
        C -->|No| E[Standard Retry]
        D --> F[Generate Empathetic Message]
        F --> G[User Receives Email]
        G --> H[User Responds]
        H --> I[Intent Extractor]
        I --> J{What Intent?}
        J -->|Accept Bridge| K[Tool: Switch to $5 Plan]
        J -->|Decline| L[Tool: Offer Payment Update]
        J -->|Financial Hardship| D
        K --> M[Success: Churn Prevented]
        L --> N[User Decision]

        style B fill:#667eea,color:#fff
        style D fill:#764ba2,color:#fff
        style I fill:#f093fb,color:#fff
        style K fill:#0F9D58,color:#fff
        style M fill:#0F9D58,color:#fff
    ```
    """)
