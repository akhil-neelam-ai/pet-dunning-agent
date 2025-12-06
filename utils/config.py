"""
Configuration utilities for loading API keys
Supports both local .env files and Streamlit Cloud secrets
"""
import os
from dotenv import load_dotenv

# Load .env file for local development
load_dotenv()

def get_api_key():
    """
    Get the Anthropic API key from environment or Streamlit secrets
    """
    # Try to get from Streamlit secrets first (for cloud deployment)
    try:
        import streamlit as st
        if hasattr(st, 'secrets') and 'ANTHROPIC_API_KEY' in st.secrets:
            return st.secrets['ANTHROPIC_API_KEY']
    except:
        pass

    # Fall back to environment variable (for local development)
    return os.getenv('ANTHROPIC_API_KEY')
