# theme_manager.py
import streamlit as st

THEMES = {
    "Karanlık": {"bg": "#1a1a1a", "text": "#ffffff", "secondary": "#2a2a2a"},
    "Açık": {"bg": "#ffffff", "text": "#000000", "secondary": "#f0f0f0"},
    "Retro": {"bg": "#2d2d2d", "text": "#ffd700", "secondary": "#3a3a3a"}
}

def apply_theme(theme_name):
    theme = THEMES.get(theme_name, THEMES["Karanlık"])
    st.markdown(f"""
    <style>
        .stApp {{
            background-color: {theme['bg']} !important;
            color: {theme['text']} !important;
        }}
        .css-1d391kg, .st-bb, .st-at {{
            background-color: {theme['secondary']} !important;
        }}
        .st-b7, .st-c2 {{
            color: {theme['text']} !important;
        }}
        /* Özel bileşenler için ek stiller */
        .game-card {{
            background: {theme['secondary']} !important;
            border: 1px solid {theme['text']} !important;
        }}
    </style>
    """, unsafe_allow_html=True)