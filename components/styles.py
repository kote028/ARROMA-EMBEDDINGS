import streamlit as st

def apply_custom_styles():
    """Inject luxury laboratory dark theme styling into Streamlit."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --color-bg: #111318;
        --color-surface: #191D24;
        --color-surface-hover: #222731;
        --color-surface-border: #2D333F;
        --color-gold: #C7A56B;
        --color-gold-light: #DFCA9B;
        --color-gold-dim: rgba(199, 165, 107, 0.15);
        --color-ivory: #F3EFE5;
        --color-grey: #A5A9B0;
        --color-accent-green: #4ADE80;
        --color-green-dim: rgba(74, 222, 128, 0.12);
    }

    /* Overall Background and typography */
    .stApp {
        background-color: var(--color-bg);
        color: var(--color-ivory);
        font-family: 'Inter', sans-serif;
    }

    h1, h2, h3, .brand-title {
        font-family: 'Cinzel', serif;
        letter-spacing: 0.04em;
        color: var(--color-ivory);
        font-weight: 600;
    }

    /* Top Header Bar */
    .scentlab-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1.5rem 0 2rem 0;
        border-bottom: 1px solid var(--color-surface-border);
        margin-bottom: 2rem;
    }
    .brand-container {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    .brand-mark {
        font-family: 'Cinzel', serif;
        font-size: 1.8rem;
        background: linear-gradient(135deg, var(--color-gold), var(--color-gold-light));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        letter-spacing: 0.08em;
    }
    .brand-tagline {
        font-size: 0.85rem;
        color: var(--color-grey);
        text-transform: uppercase;
        letter-spacing: 0.15em;
        margin-top: 2px;
    }

    /* Status Pill */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: var(--color-surface);
        padding: 0.4rem 0.9rem;
        border-radius: 9999px;
        border: 1px solid var(--color-surface-border);
        font-size: 0.78rem;
        color: var(--color-grey);
    }
    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: var(--color-accent-green);
        box-shadow: 0 0 8px var(--color-accent-green);
    }

    /* Hero Banner */
    .hero-container {
        padding: 2.8rem 2.2rem;
        background: linear-gradient(180deg, rgba(25, 29, 36, 0.8) 0%, rgba(17, 19, 24, 0.95) 100%);
        border: 1px solid var(--color-surface-border);
        border-radius: 16px;
        position: relative;
        overflow: hidden;
        margin-bottom: 2.5rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    }
    .hero-container::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, var(--color-gold), transparent);
    }
    .hero-heading {
        font-size: 2.2rem;
        margin-bottom: 0.8rem;
        color: var(--color-ivory);
    }
    .hero-sub {
        font-size: 1.05rem;
        color: var(--color-grey);
        line-height: 1.6;
        max-width: 780px;
    }

    /* Cards */
    .scent-card {
        background-color: var(--color-surface);
        border: 1px solid var(--color-surface-border);
        border-radius: 14px;
        padding: 1.6rem;
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .scent-card:hover {
        border-color: rgba(199, 165, 107, 0.5);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
        transform: translateY(-2px);
    }
    .card-icon {
        font-size: 1.8rem;
        color: var(--color-gold);
        margin-bottom: 0.8rem;
    }
    .card-title {
        font-family: 'Cinzel', serif;
        font-size: 1.2rem;
        color: var(--color-ivory);
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    .card-desc {
        font-size: 0.9rem;
        color: var(--color-grey);
        line-height: 1.5;
        margin-bottom: 1.2rem;
    }

    /* Result Panels */
    .result-container {
        background: var(--color-surface);
        border: 1px solid var(--color-surface-border);
        border-left: 3px solid var(--color-gold);
        border-radius: 12px;
        padding: 1.6rem;
        margin-top: 1.5rem;
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    .result-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid var(--color-surface-border);
        padding-bottom: 0.8rem;
        margin-bottom: 1rem;
    }
    .result-title {
        font-family: 'Cinzel', serif;
        font-size: 1.15rem;
        color: var(--color-gold-light);
    }
    .result-meta {
        font-size: 0.8rem;
        color: var(--color-grey);
        font-family: 'JetBrains Mono', monospace;
    }

    /* Tags */
    .tag-container {
        display: flex;
        flex-wrap: wrap;
        gap: 0.6rem;
        margin: 1rem 0;
    }
    .scent-tag {
        background: var(--color-gold-dim);
        border: 1px solid rgba(199, 165, 107, 0.4);
        color: var(--color-gold-light);
        padding: 0.35rem 0.85rem;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 500;
        letter-spacing: 0.03em;
        text-transform: capitalize;
    }
    .match-tag {
        background: var(--color-green-dim);
        border: 1px solid rgba(74, 222, 128, 0.4);
        color: var(--color-accent-green);
        padding: 0.3rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 500;
        text-transform: capitalize;
    }

    /* Code & SMILES blocks */
    .smiles-box {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        background: rgba(0, 0, 0, 0.35);
        border: 1px solid var(--color-surface-border);
        border-radius: 8px;
        padding: 0.6rem 0.9rem;
        color: #E2E8F0;
        word-break: break-all;
    }

    /* Streamlit widget modifications */
    div[data-testid="stTextInput"] input, div[data-testid="stTextArea"] textarea {
        background-color: #15181F !important;
        border: 1px solid #2D333F !important;
        color: #F3EFE5 !important;
        border-radius: 8px !important;
        font-family: 'Inter', sans-serif !important;
    }
    div[data-testid="stTextInput"] input:focus, div[data-testid="stTextArea"] textarea:focus {
        border-color: var(--color-gold) !important;
        box-shadow: 0 0 0 1px var(--color-gold) !important;
    }
    .stButton > button {
        background: linear-gradient(180deg, #D4B57D 0%, #C7A56B 100%) !important;
        color: #111318 !important;
        font-weight: 600 !important;
        font-family: 'Cinzel', serif !important;
        letter-spacing: 0.05em !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.6rem !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        background: linear-gradient(180deg, #E2CA99 0%, #D4B57D 100%) !important;
        box-shadow: 0 4px 15px rgba(199, 165, 107, 0.3) !important;
        transform: translateY(-1px) !important;
    }

    /* Secondary buttons */
    .secondary-btn button {
        background: transparent !important;
        border: 1px solid var(--color-surface-border) !important;
        color: var(--color-grey) !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 400 !important;
        font-size: 0.82rem !important;
    }
    .secondary-btn button:hover {
        border-color: var(--color-gold) !important;
        color: var(--color-ivory) !important;
    }

    /* Radio / Tabs nav styling */
    div[data-testid="stRadio"] > div {
        background: var(--color-surface);
        padding: 6px;
        border-radius: 12px;
        border: 1px solid var(--color-surface-border);
    }
    </style>
    """, unsafe_allow_html=True)
