import streamlit as st
from core.challenge_engine import get_challenge
from core.simulator import NetworkSimulator

def start_challenge(challenge_id):
    c = get_challenge(challenge_id)
    st.session_state.challenge = c
    st.session_state.simulator = NetworkSimulator(c)
    st.session_state.hints_used = 0
    st.session_state.hint_index = 0
    st.session_state.last_score = None
    st.session_state.coach = None

def ensure_session():
    if "challenge" not in st.session_state:
        start_challenge("route_01")

def simulator():
    return st.session_state.simulator
