"""
Indian Criminal Law Research Assistant
Free AI: Google Gemini 1.5 Flash (100% free, 1M tokens/day)
Professional light theme — clean, authoritative, law-office aesthetic
"""

import streamlit as st
import pandas as pd
import requests
import re
import os
from pathlib import Path

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LexIPC — Indian Criminal Law Research",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS — PROFESSIONAL LIGHT THEME
# Aesthetic: Clean law-office — crisp whites, navy authority, gold accents
# Typography: Lora (serif headers) + DM Sans (UI text)
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;0,700;1,400&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

:root {
    --navy:      #1a2744;
    --navy-mid:  #2d3f6b;
    --navy-lite: #e8ecf5;
    --gold:      #b8860b;
    --gold-lite: #fdf6e3;
    --gold-soft: #f5e6c0;
    --red:       #c0392b;
    --red-lite:  #fdf0ee;
    --green:     #1a6b3a;
    --green-lite:#edf7f1;
    --gray-50:   #f8f9fb;
    --gray-100:  #f1f3f7;
    --gray-200:  #e2e6ef;
    --gray-400:  #8b95ad;
    --gray-600:  #4a5568;
    --gray-800:  #1e2533;
    --white:     #ffffff;
    --border:    #dde1ea;
    --shadow-sm: 0 1px 3px rgba(26,39,68,.08), 0 1px 2px rgba(26,39,68,.04);
    --shadow-md: 0 4px 12px rgba(26,39,68,.10), 0 2px 4px rgba(26,39,68,.06);
    --shadow-lg: 0 10px 30px rgba(26,39,68,.12);
    --radius:    8px;
    --radius-lg: 12px;
}

/* ── Reset & base ─────────────────────────────────── */
html, body { font-family: 'DM Sans', sans-serif !important; }

.stApp {
    background: var(--gray-50) !important;
    color: var(--gray-800) !important;
}

/* ── Sidebar ──────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: var(--navy) !important;
    border-right: none !important;
}
[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] .stCaption {
    color: rgba(255,255,255,0.75) !important;
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #ffffff !important;
    font-family: 'Lora', serif !important;
}
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.12) !important; }

/* Sidebar inputs */
[data-testid="stSidebar"] .stTextInput input {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    color: #ffffff !important;
    border-radius: var(--radius) !important;
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stSidebar"] .stTextInput input::placeholder { color: rgba(255,255,255,0.4) !important; }

/* Sidebar metrics */
[data-testid="stSidebar"] [data-testid="stMetricValue"] { color: #f5c842 !important; font-size: 1.4rem !important; }
[data-testid="stSidebar"] [data-testid="stMetricLabel"] { color: rgba(255,255,255,0.6) !important; }

/* Sidebar buttons */
[data-testid="stSidebar"] .stButton button {
    background: rgba(255,255,255,0.06) !important;
    color: rgba(255,255,255,0.85) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: var(--radius) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 400 !important;
    padding: 6px 12px !important;
    text-align: left !important;
    transition: all 0.15s ease !important;
}
[data-testid="stSidebar"] .stButton button:hover {
    background: rgba(255,255,255,0.12) !important;
    border-color: rgba(255,255,255,0.25) !important;
    color: #ffffff !important;
}

/* ── Headings ─────────────────────────────────────── */
h1 { font-family: 'Lora', serif !important; color: var(--navy) !important; font-size: 2rem !important; font-weight: 700 !important; }
h2 { font-family: 'Lora', serif !important; color: var(--navy) !important; font-size: 1.4rem !important; font-weight: 600 !important; }
h3 { font-family: 'Lora', serif !important; color: var(--navy-mid) !important; font-size: 1.15rem !important; font-weight: 600 !important; }

/* ── Main inputs ──────────────────────────────────── */
.stTextInput input,
.stTextArea textarea,
.stSelectbox > div > div {
    background: var(--white) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--gray-800) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    box-shadow: var(--shadow-sm) !important;
    transition: border-color 0.15s !important;
}
.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: var(--navy-mid) !important;
    box-shadow: 0 0 0 3px rgba(45,63,107,0.08) !important;
}

/* ── Primary buttons ─────────────────────────────── */
.stButton > button[kind="primary"],
.stButton > button[data-testid*="primary"] {
    background: var(--navy) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: var(--radius) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 10px 24px !important;
    letter-spacing: 0.02em !important;
    box-shadow: var(--shadow-sm) !important;
    transition: all 0.15s ease !important;
}
.stButton > button[kind="primary"]:hover {
    background: var(--navy-mid) !important;
    box-shadow: var(--shadow-md) !important;
    transform: translateY(-1px) !important;
}

/* Secondary buttons */
.stButton > button:not([kind="primary"]) {
    background: var(--white) !important;
    color: var(--navy) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    box-shadow: var(--shadow-sm) !important;
    transition: all 0.15s ease !important;
}
.stButton > button:not([kind="primary"]):hover {
    border-color: var(--navy-mid) !important;
    color: var(--navy-mid) !important;
}

/* ── Tabs ─────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--white) !important;
    border-bottom: 2px solid var(--gray-200) !important;
    border-radius: var(--radius-lg) var(--radius-lg) 0 0 !important;
    padding: 0 8px !important;
    gap: 0 !important;
    box-shadow: var(--shadow-sm) !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--gray-400) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    padding: 14px 22px !important;
    border-radius: 0 !important;
    border-bottom: 2.5px solid transparent !important;
    transition: all 0.15s !important;
}
.stTabs [data-baseweb="tab"]:hover { color: var(--navy) !important; }
.stTabs [aria-selected="true"] {
    color: var(--navy) !important;
    border-bottom: 2.5px solid var(--navy) !important;
    font-weight: 600 !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: var(--white) !important;
    border: 1px solid var(--gray-200) !important;
    border-top: none !important;
    border-radius: 0 0 var(--radius-lg) var(--radius-lg) !important;
    padding: 28px !important;
    box-shadow: var(--shadow-sm) !important;
}

/* ── Metrics ──────────────────────────────────────── */
[data-testid="stMetricValue"] { color: var(--navy) !important; font-family: 'Lora', serif !important; font-size: 1.6rem !important; }
[data-testid="stMetricLabel"] { color: var(--gray-400) !important; font-family: 'DM Sans', sans-serif !important; font-size: 0.8rem !important; }
[data-testid="metric-container"] {
    background: var(--white) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 16px 20px !important;
    box-shadow: var(--shadow-sm) !important;
}

/* ── Expander ─────────────────────────────────────── */
.streamlit-expanderHeader {
    background: var(--gray-50) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--navy) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
}

/* ── Dataframe ────────────────────────────────────── */
.stDataFrame { border-radius: var(--radius) !important; overflow: hidden !important; border: 1px solid var(--border) !important; }

/* ── Alerts ───────────────────────────────────────── */
.stSuccess { background: var(--green-lite) !important; border-color: var(--green) !important; border-left: 4px solid var(--green) !important; border-radius: var(--radius) !important; }
.stWarning { background: var(--gold-lite) !important; border-color: var(--gold) !important; border-left: 4px solid var(--gold) !important; border-radius: var(--radius) !important; }
.stError   { background: var(--red-lite) !important; border-color: var(--red) !important; border-left: 4px solid var(--red) !important; border-radius: var(--radius) !important; }
.stInfo    { background: var(--navy-lite) !important; border-color: var(--navy-mid) !important; border-left: 4px solid var(--navy-mid) !important; border-radius: var(--radius) !important; }

/* ── Custom components ────────────────────────────── */

/* Section card */
.ipc-card {
    background: var(--white);
    border: 1px solid var(--border);
    border-left: 4px solid var(--navy);
    border-radius: var(--radius);
    padding: 18px 22px;
    margin: 10px 0;
    box-shadow: var(--shadow-sm);
    transition: box-shadow 0.15s, transform 0.15s;
}
.ipc-card:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-1px);
}
.ipc-section-num {
    font-family: 'Lora', serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--navy);
    letter-spacing: 0.01em;
}
.ipc-offense {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.9rem;
    color: var(--gray-600);
    margin: 6px 0 10px;
    line-height: 1.5;
}
.ipc-punishment {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: var(--red-lite);
    color: var(--red);
    border: 1px solid rgba(192,57,43,0.2);
    border-radius: 20px;
    padding: 3px 12px;
    font-family: 'DM Mono', monospace;
    font-size: 0.78rem;
    font-weight: 500;
}
.ipc-summary {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.88rem;
    color: var(--gray-600);
    line-height: 1.65;
    margin-top: 10px;
    padding-top: 10px;
    border-top: 1px solid var(--gray-100);
}

/* AI answer box */
.ai-answer-box {
    background: var(--white);
    border: 1px solid var(--border);
    border-top: 4px solid var(--navy);
    border-radius: var(--radius-lg);
    padding: 28px 32px;
    margin: 16px 0;
    box-shadow: var(--shadow-md);
    font-family: 'DM Sans', sans-serif;
    font-size: 0.95rem;
    line-height: 1.8;
    color: var(--gray-800);
}
.ai-answer-box h1, .ai-answer-box h2, .ai-answer-box h3 {
    font-family: 'Lora', serif !important;
    color: var(--navy) !important;
    margin-top: 1.2em;
    margin-bottom: 0.5em;
}
.ai-answer-box strong { color: var(--navy); }
.ai-answer-box code {
    background: var(--gray-100);
    border: 1px solid var(--gray-200);
    border-radius: 4px;
    padding: 2px 6px;
    font-family: 'DM Mono', monospace;
    font-size: 0.85em;
    color: var(--red);
}

/* Answer header */
.answer-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 16px;
    padding-bottom: 14px;
    border-bottom: 1px solid var(--gray-100);
}
.answer-badge {
    background: var(--navy-lite);
    color: var(--navy);
    border: 1px solid rgba(26,39,68,0.15);
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.78rem;
    font-weight: 600;
    font-family: 'DM Sans', sans-serif;
    letter-spacing: 0.03em;
}

/* Chat messages */
.chat-bubble-user {
    background: var(--navy);
    color: #ffffff;
    border-radius: 12px 12px 4px 12px;
    padding: 12px 18px;
    margin: 8px 0 8px 40px;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.93rem;
    line-height: 1.6;
    box-shadow: var(--shadow-sm);
}
.chat-bubble-ai {
    background: var(--white);
    color: var(--gray-800);
    border: 1px solid var(--border);
    border-radius: 12px 12px 12px 4px;
    padding: 14px 18px;
    margin: 8px 40px 8px 0;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.93rem;
    line-height: 1.7;
    box-shadow: var(--shadow-sm);
}
.chat-label {
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 4px;
    font-family: 'DM Sans', sans-serif;
}

/* Status pill */
.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 4px 12px;
    border-radius: 20px;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.78rem;
    font-weight: 600;
}
.pill-connected { background: var(--green-lite); color: var(--green); border: 1px solid rgba(26,107,58,.2); }
.pill-missing   { background: var(--red-lite);   color: var(--red);   border: 1px solid rgba(192,57,43,.2); }
.pill-navy      { background: var(--navy-lite);  color: var(--navy);  border: 1px solid rgba(26,39,68,.15); }

/* Quick lookup card */
.lookup-card {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.12);
    border-left: 3px solid #f5c842;
    border-radius: var(--radius);
    padding: 10px 14px;
    margin: 8px 0;
}
.lookup-card .lc-sec { font-weight: 700; color: #f5c842; font-size: 0.9rem; font-family: 'Lora', serif; }
.lookup-card .lc-off { color: rgba(255,255,255,0.65); font-size: 0.78rem; margin: 3px 0; }
.lookup-card .lc-pun { color: #f08080; font-family: 'DM Mono', monospace; font-size: 0.75rem; }

/* Page header banner */
.page-header {
    background: linear-gradient(135deg, var(--navy) 0%, var(--navy-mid) 100%);
    border-radius: var(--radius-lg);
    padding: 28px 36px;
    margin-bottom: 24px;
    box-shadow: var(--shadow-lg);
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.page-header-title {
    font-family: 'Lora', serif;
    font-size: 1.7rem;
    font-weight: 700;
    color: #ffffff;
    margin: 0;
    letter-spacing: -0.01em;
}
.page-header-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.88rem;
    color: rgba(255,255,255,0.65);
    margin-top: 4px;
}
.page-header-pills { display: flex; gap: 8px; flex-wrap: wrap; }
.header-pill {
    background: rgba(255,255,255,0.1);
    border: 1px solid rgba(255,255,255,0.2);
    color: rgba(255,255,255,0.85);
    border-radius: 20px;
    padding: 4px 14px;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.78rem;
    font-weight: 500;
}

/* Disclaimer */
.disclaimer {
    background: var(--gold-lite);
    border: 1px solid var(--gold-soft);
    border-left: 4px solid var(--gold);
    border-radius: var(--radius);
    padding: 12px 16px;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.82rem;
    color: #7a5c00;
    line-height: 1.5;
    margin: 12px 0;
}

/* Section count badge */
.count-badge {
    background: var(--navy-lite);
    color: var(--navy);
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 0.78rem;
    font-weight: 600;
    font-family: 'DM Sans', sans-serif;
}

/* Radio buttons */
.stRadio label {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    color: var(--gray-600) !important;
}

/* Toggle */
.stToggle label {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    color: var(--gray-600) !important;
}

/* Caption */
.stCaption { color: var(--gray-400) !important; font-family: 'DM Sans', sans-serif !important; }

/* Spinner */
.stSpinner { color: var(--navy) !important; }

/* Download button */
.stDownloadButton button {
    background: var(--white) !important;
    color: var(--navy) !important;
    border: 1.5px solid var(--navy) !important;
    border-radius: var(--radius) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--gray-100); }
::-webkit-scrollbar-thumb { background: var(--gray-200); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--gray-400); }

</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────────────────────────────────────

@st.cache_data
def load_ipc_data() -> pd.DataFrame:
    for path in ["ipc_sections.csv", "data/ipc_sections.csv"]:
        p = Path(path)
        if p.exists():
            df = pd.read_csv(p)
            df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
            return df
    return pd.DataFrame()

@st.cache_data
def load_ncrb_data() -> pd.DataFrame:
    for path in ["NCRB_CII_2023_Table_18A_2_0.csv", "data/NCRB_CII_2023_Table_18A_2_0.csv"]:
        p = Path(path)
        if p.exists():
            df = pd.read_csv(p)
            df.columns = [c.strip() for c in df.columns]
            return df
    return pd.DataFrame()

ipc_df  = load_ipc_data()
ncrb_df = load_ncrb_data()


# ─────────────────────────────────────────────────────────────────────────────
# GEMINI API  (free — get key at aistudio.google.com)
# ─────────────────────────────────────────────────────────────────────────────

def get_api_key() -> str:
    try:
        return st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        return os.environ.get("GEMINI_API_KEY", "")

def call_gemini(messages: list, system_prompt: str = "") -> str:
    """
    Call Google Gemini 1.5 Flash — completely free (1M tokens/day).
    Get your free key at: aistudio.google.com → Get API Key
    Add to Streamlit Secrets as: GEMINI_API_KEY = "AIza..."
    """
    api_key = get_api_key()
    if not api_key:
        return (
            "**⚠️ Gemini API Key Not Configured**\n\n"
            "To enable AI responses:\n"
            "1. Go to [aistudio.google.com](https://aistudio.google.com) — it's **free**, no credit card needed\n"
            "2. Click **Get API Key** → Create API Key\n"
            "3. In Streamlit Cloud: **Settings → Secrets** → add:\n"
            "```\nGEMINI_API_KEY = \"AIza...\"\n```\n"
            "4. Redeploy the app\n\n"
            "*The IPC search above works without an API key.*"
        )

    # Build Gemini content format
    gemini_contents = []
    if system_prompt:
        # Gemini uses system instruction separately
        pass

    for msg in messages:
        role = "user" if msg["role"] == "user" else "model"
        gemini_contents.append({
            "role": role,
            "parts": [{"text": msg["content"]}]
        })

    payload = {
        "contents": gemini_contents,
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 2048,
            "topP": 0.85,
        },
        "safetySettings": [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]
    }

    if system_prompt:
        payload["systemInstruction"] = {"parts": [{"text": system_prompt}]}

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

    try:
        resp = requests.post(url, json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except requests.exceptions.ConnectionError:
        return "❌ Network error. Check your internet connection."
    except requests.exceptions.Timeout:
        return "❌ Request timed out. Please try again."
    except requests.exceptions.HTTPError:
        status = resp.status_code
        if status == 400:
            return "❌ Invalid API key. Please check your GEMINI_API_KEY in Streamlit Secrets."
        if status == 429:
            return "❌ Rate limit reached. Wait a moment and try again (free tier: 15 requests/min)."
        return f"❌ API error ({status}). Please try again."
    except (KeyError, IndexError):
        return "❌ Unexpected API response. Please try again."
    except Exception as e:
        return f"❌ Error: {str(e)}"


# ─────────────────────────────────────────────────────────────────────────────
# IPC SEARCH
# ─────────────────────────────────────────────────────────────────────────────

def search_ipc(query: str, df: pd.DataFrame, top_n: int = 6) -> pd.DataFrame:
    if df.empty or not query.strip():
        return df.head(top_n)

    q_lower = query.lower()
    terms = [t for t in q_lower.split() if len(t) > 2]
    scores = pd.Series(0.0, index=df.index)

    col_weights = {"offense": 3.0, "section": 2.5, "description": 1.0, "punishment": 0.5}
    for col, weight in col_weights.items():
        if col in df.columns:
            text = df[col].fillna("").str.lower()
            for term in terms:
                scores += text.str.contains(term, regex=False).astype(float) * weight

    # Direct section number match
    m = re.search(r'\b(\d{2,3}[A-Za-z]?)\b', query)
    if m and "section" in df.columns:
        sec = m.group(1).upper()
        scores[df["section"].fillna("").str.upper().str.contains(sec, regex=False)] += 15

    return (
        df[scores > 0]
        .assign(_s=scores)
        .sort_values("_s", ascending=False)
        .drop("_s", axis=1)
        .head(top_n)
    )


def render_ipc_card(row: pd.Series, compact: bool = False):
    section = row.get("section", "—")
    offense = row.get("offense", "")
    punish  = row.get("punishment", "")
    desc    = row.get("description", "")

    # Extract plain-language summary
    summary = ""
    if desc and not compact:
        lines = [l.strip() for l in str(desc).split("\n") if l.strip()]
        for i, l in enumerate(lines):
            if "simple words" in l.lower() and i + 1 < len(lines):
                summary = lines[i + 1][:280]
                break
        if not summary and lines:
            summary = lines[0][:240]

    st.markdown(f"""
    <div class="ipc-card">
        <div class="ipc-section-num">⚖ {section}</div>
        <div class="ipc-offense">{offense}</div>
        <span class="ipc-punishment">⚠ {punish}</span>
        {"" if not summary else f'<div class="ipc-summary">{summary}{"…" if len(summary)==280 else ""}</div>'}
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# LEGAL SYSTEM PROMPT
# ─────────────────────────────────────────────────────────────────────────────

LEGAL_SYSTEM = """You are LexIPC, an expert Indian criminal law research assistant.

Specialisation: Indian Penal Code (IPC), Code of Criminal Procedure (CrPC), Indian Evidence Act, 
Bharatiya Nyaya Sanhita 2023 (BNS), Bharatiya Nagarik Suraksha Sanhita 2023 (BNSS).

Response guidelines:
- Always cite specific IPC/BNS section numbers (e.g., "IPC Section 302", "BNS Section 101")
- Structure responses with clear headers using **bold** formatting
- Mention bailable/non-bailable and cognisable/non-cognisable status where relevant
- Include landmark Supreme Court / High Court cases where applicable
- Note if a provision has been replaced or amended by BNS 2023
- State punishments precisely (imprisonment duration, fine amounts)
- For complex queries, use numbered lists for clarity
- Always end with: "*Note: This is legal information for research purposes only, not legal advice.*"
- Keep responses focused and professional (aim for 250-450 words unless detailed analysis requested)
- Use plain language alongside legal terminology"""


# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "prefill" not in st.session_state:
    st.session_state.prefill = ""
if "last_answer" not in st.session_state:
    st.session_state.last_answer = None
if "last_matched" not in st.session_state:
    st.session_state.last_matched = pd.DataFrame()


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## ⚖️ LexIPC")
    st.markdown("*Indian Criminal Law Research*")
    st.markdown("---")

    # API status
    key_present = bool(get_api_key())
    status_class = "pill-connected" if key_present else "pill-missing"
    status_icon  = "●" if key_present else "○"
    status_text  = "Gemini AI Connected" if key_present else "API Key Missing"
    st.markdown(
        f'<div class="status-pill {status_class}">{status_icon} {status_text}</div>',
        unsafe_allow_html=True
    )
    if not key_present:
        st.markdown(
            '<div style="color:rgba(255,255,255,0.5);font-size:0.75rem;margin-top:6px">'
            'Free key → aistudio.google.com</div>',
            unsafe_allow_html=True
        )

    st.markdown("---")

    # Data stats
    st.markdown("**Dataset**")
    c1, c2 = st.columns(2)
    c1.metric("IPC Sections", f"{len(ipc_df):,}" if not ipc_df.empty else "—")
    c2.metric("NCRB Records", f"{len(ncrb_df):,}" if not ncrb_df.empty else "—")

    if ipc_df.empty:
        st.markdown(
            '<div style="color:#f5c842;font-size:0.78rem;margin-top:4px">⚠ ipc_sections.csv not found</div>',
            unsafe_allow_html=True
        )

    st.markdown("---")

    # Quick section lookup
    st.markdown("**Quick Section Lookup**")
    quick = st.text_input("", placeholder="Type section no. e.g. 302", key="quick_lookup",
                          label_visibility="collapsed")
    if quick.strip() and not ipc_df.empty:
        q = re.sub(r'[^0-9A-Za-z]', '', quick).upper()
        mask = ipc_df["section"].fillna("").str.upper().str.contains(q, regex=False)
        found = ipc_df[mask]
        if not found.empty:
            r = found.iloc[0]
            st.markdown(f"""
            <div class="lookup-card">
                <div class="lc-sec">⚖ {r.get('section','')}</div>
                <div class="lc-off">{str(r.get('offense',''))[:85]}{"…" if len(str(r.get('offense','')))>85 else ""}</div>
                <div class="lc-pun">⚠ {r.get('punishment','')}</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(
                '<div style="color:rgba(255,255,255,0.4);font-size:0.8rem">Section not found</div>',
                unsafe_allow_html=True
            )

    st.markdown("---")

    # Quick queries
    st.markdown("**Common Queries**")
    quick_queries = [
        "What is IPC Section 302?",
        "Punishment for theft (IPC 378–382)",
        "Culpable homicide vs murder",
        "IPC Section 376 — rape",
        "Cheating and fraud sections",
        "Rights of accused during arrest",
        "Bail — bailable vs non-bailable",
        "Dowry harassment — Section 498A",
        "Cybercrime under IPC",
        "Self-defence under IPC",
    ]
    for q in quick_queries:
        if st.button(q, key=f"q_{q[:12]}", use_container_width=True):
            st.session_state.prefill = q
            st.rerun()

    st.markdown("---")
    st.markdown(
        '<div style="color:rgba(255,255,255,0.3);font-size:0.72rem;line-height:1.5">'
        'LexIPC v2.0 · AI: Gemini 1.5 Flash (free)<br>'
        'For research purposes only. Not legal advice.'
        '</div>',
        unsafe_allow_html=True
    )


# ─────────────────────────────────────────────────────────────────────────────
# PAGE HEADER
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("""
<div class="page-header">
    <div>
        <div class="page-header-title">⚖️ Indian Criminal Law Research Assistant</div>
        <div class="page-header-sub">Powered by Google Gemini AI · IPC Sections Database · NCRB Crime Statistics 2023</div>
    </div>
    <div class="page-header-pills">
        <span class="header-pill">📚 IPC Database</span>
        <span class="header-pill">🤖 Gemini AI (Free)</span>
        <span class="header-pill">📊 NCRB 2023</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Tabs
tab_research, tab_sections, tab_stats, tab_chat = st.tabs([
    "  🔬  AI Research  ",
    "  📚  IPC Sections  ",
    "  📊  Crime Statistics  ",
    "  💬  Legal Chat  ",
])


# ═════════════════════════════════════════════════════════════════════════════
# TAB 1 — AI RESEARCH
# ═════════════════════════════════════════════════════════════════════════════

with tab_research:
    st.markdown("### Ask a Legal Question")
    st.markdown(
        '<div class="disclaimer">'
        '⚠️ <strong>Legal Information Only.</strong> '
        'Responses are for research and educational purposes. Always consult a qualified advocate for legal advice.'
        '</div>',
        unsafe_allow_html=True
    )

    prefill_val = st.session_state.pop("prefill", "")

    query = st.text_area(
        "Your legal query:",
        value=prefill_val,
        height=110,
        placeholder="e.g.  What is the punishment for murder under IPC?   What sections apply to cybercrime in India?   Explain the difference between robbery and dacoity.",
        key="main_query",
    )

    col_btn, col_t1, col_t2, col_t3 = st.columns([2, 1.4, 1.4, 1.4])
    with col_btn:
        analyse = st.button("⚖️  Analyse Query", type="primary", use_container_width=True, key="analyse_btn")
    with col_t1:
        inc_sections = st.toggle("Show IPC sections", value=True)
    with col_t2:
        detailed = st.toggle("Detailed analysis", value=False)
    with col_t3:
        show_sql = st.toggle("Show search info", value=False)

    if analyse:
        if not query.strip():
            st.warning("Please enter a legal query.")
        else:
            # IPC search
            matched = pd.DataFrame()
            if inc_sections and not ipc_df.empty:
                matched = search_ipc(query, ipc_df, top_n=6)

            # Build context
            ipc_ctx = ""
            if not matched.empty:
                rows_text = []
                for _, r in matched.iterrows():
                    rows_text.append(
                        f"• {r.get('section','')}: {r.get('offense','')}"
                        f" | Punishment: {r.get('punishment','')}"
                    )
                ipc_ctx = "\n\nMatching IPC Sections from database:\n" + "\n".join(rows_text)

            detail_note = (
                " Provide a comprehensive analysis including elements of the offence, "
                "relevant case laws (Supreme Court and High Court), procedural aspects under CrPC/BNSS, "
                "defences available, and practical implications."
                if detailed else ""
            )

            messages = [{"role": "user", "content": query + ipc_ctx + detail_note}]

            with st.spinner("Researching legal provisions…"):
                answer = call_gemini(messages, LEGAL_SYSTEM)

            st.session_state.last_answer = answer
            st.session_state.last_matched = matched

            # Save to chat
            st.session_state.chat_history.append({"role": "user", "content": query})
            st.session_state.chat_history.append({"role": "assistant", "content": answer})

    # Display result
    if st.session_state.last_answer:
        answer = st.session_state.last_answer
        matched = st.session_state.last_matched

        st.markdown(f"""
        <div class="ai-answer-box">
            <div class="answer-header">
                <span style="font-family:'Lora',serif;font-weight:700;color:var(--navy);font-size:1rem">
                    AI Legal Analysis
                </span>
                <span class="answer-badge">Gemini 1.5 Flash</span>
                {"<span class='answer-badge'>Detailed</span>" if detailed else ""}
            </div>
            {answer.replace(chr(10), '<br>')}
        </div>
        """, unsafe_allow_html=True)

        if show_sql and not matched.empty:
            st.caption(f"Search matched {len(matched)} IPC sections for this query.")

        if not matched.empty and inc_sections:
            st.markdown("---")
            n = len(matched)
            st.markdown(
                f'**Relevant IPC Sections** &nbsp;<span class="count-badge">{n} found</span>',
                unsafe_allow_html=True
            )
            for _, row in matched.iterrows():
                render_ipc_card(row)


# ═════════════════════════════════════════════════════════════════════════════
# TAB 2 — IPC SECTIONS BROWSER
# ═════════════════════════════════════════════════════════════════════════════

with tab_sections:
    st.markdown("### IPC Sections Database")

    if ipc_df.empty:
        st.error(
            "**IPC data not loaded.** "
            "Place `ipc_sections.csv` in the same folder as `app.py` and redeploy."
        )
    else:
        # Search bar
        col_s, col_n, col_v = st.columns([4, 1, 1])
        with col_s:
            sec_search = st.text_input(
                "",
                placeholder="🔍  Search by keyword or section number — e.g.  murder, 302, theft, fraud…",
                key="sec_search",
                label_visibility="collapsed",
            )
        with col_n:
            show_n = st.selectbox("Show", [10, 25, 50, 100], key="show_n", label_visibility="collapsed")
        with col_v:
            view_mode = st.selectbox("View", ["Cards", "Table"], key="view_mode", label_visibility="collapsed")

        # Punishment filter
        pf_col, _ = st.columns([2, 3])
        with pf_col:
            pun_filter = st.text_input(
                "",
                placeholder="Filter punishment: death, life, fine, 7 years…",
                key="pun_filter",
                label_visibility="collapsed",
            )

        # Apply search
        results = search_ipc(sec_search, ipc_df, top_n=show_n) if sec_search.strip() else ipc_df.head(show_n)

        # Apply punishment filter
        if pun_filter.strip() and "punishment" in results.columns:
            results = results[
                results["punishment"].fillna("").str.lower()
                .str.contains(pun_filter.lower(), regex=False)
            ]

        # Result count
        st.markdown(
            f'<div style="margin:8px 0 16px">'
            f'Showing <span class="count-badge">{len(results)}</span> sections'
            f'{"" if not sec_search else f" for <em>{sec_search}</em>"}'
            f'</div>',
            unsafe_allow_html=True
        )

        if view_mode == "Cards":
            for _, row in results.iterrows():
                render_ipc_card(row)
        else:
            disp_cols = [c for c in ["section", "offense", "punishment"] if c in results.columns]
            st.dataframe(
                results[disp_cols],
                use_container_width=True,
                height=520,
                hide_index=True,
                column_config={
                    "section":    st.column_config.TextColumn("Section", width=120),
                    "offense":    st.column_config.TextColumn("Offense / Description", width=500),
                    "punishment": st.column_config.TextColumn("Punishment", width=250),
                }
            )

        # Detail expander
        if not results.empty and "section" in results.columns:
            st.markdown("---")
            st.markdown("**View Full Section Details**")
            col_sel, col_ai = st.columns([3, 1])
            with col_sel:
                chosen = st.selectbox(
                    "Select a section:",
                    results["section"].tolist(),
                    key="chosen_section",
                    label_visibility="collapsed",
                )
            if chosen:
                row = results[results["section"] == chosen].iloc[0]
                with st.expander(f"📄 Full text — {chosen}", expanded=True):
                    c_a, c_b = st.columns(2)
                    c_a.markdown(f"**Offense:**\n{row.get('offense','—')}")
                    c_b.markdown(f"**Punishment:**\n`{row.get('punishment','—')}`")
                    st.markdown("---")
                    st.markdown("**Description:**")
                    st.markdown(str(row.get("description", "No description available.")))

                    if st.button(f"🤖 AI Analysis of {chosen}", key=f"ai_{chosen}"):
                        msgs = [{
                            "role": "user",
                            "content": (
                                f"Provide a detailed legal analysis of {chosen} of the IPC.\n"
                                f"Offense: {row.get('offense','')}\n"
                                f"Punishment: {row.get('punishment','')}\n\n"
                                "Cover: (1) Elements of the offence, (2) Landmark case laws, "
                                "(3) Bailable/non-bailable status, (4) Cognisable/non-cognisable, "
                                "(5) Common defences, (6) BNS 2023 equivalent if any."
                            )
                        }]
                        with st.spinner("Analysing…"):
                            ai_resp = call_gemini(msgs, LEGAL_SYSTEM)
                        st.markdown(f"""
                        <div class="ai-answer-box" style="margin-top:16px">
                            <div class="answer-header">
                                <span style="font-family:'Lora',serif;font-weight:700;color:var(--navy)">
                                    Analysis: {chosen}
                                </span>
                                <span class="answer-badge">Gemini 1.5 Flash</span>
                            </div>
                            {ai_resp.replace(chr(10), '<br>')}
                        </div>
                        """, unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# TAB 3 — CRIME STATISTICS
# ═════════════════════════════════════════════════════════════════════════════

with tab_stats:
    st.markdown("### NCRB Crime Statistics — India 2023")

    if ncrb_df.empty:
        st.info(
            "**NCRB data not loaded.**  \n"
            "Place `NCRB_CII_2023_Table_18A_2_0.csv` in the same folder as `app.py`.  \n"
            "This tab will show interactive charts once the file is present."
        )
        st.markdown("""
        **This tab will show:**
        - Crime incidence by State / UT
        - Category-wise crime distribution  
        - Top categories by volume
        - Filterable, downloadable data table
        """)
    else:
        import plotly.express as px
        import plotly.graph_objects as go

        st.caption(f"Source: NCRB Crime in India Report 2023 · {len(ncrb_df):,} records")

        with st.expander("📋 Data preview & column names"):
            st.write("**Columns:**", list(ncrb_df.columns))
            st.dataframe(ncrb_df.head(8), use_container_width=True, hide_index=True)

        num_cols = ncrb_df.select_dtypes(include="number").columns.tolist()
        str_cols = ncrb_df.select_dtypes(include="object").columns.tolist()

        if num_cols and str_cols:
            cc1, cc2, cc3 = st.columns(3)
            with cc1:
                x_col = st.selectbox("Category axis:", str_cols, key="ncrb_x")
            with cc2:
                y_col = st.selectbox("Value:", num_cols, key="ncrb_y")
            with cc3:
                top_n = st.slider("Top N:", 5, 30, 15, key="ncrb_n")

            chart_df = (
                ncrb_df.groupby(x_col)[y_col].sum()
                .reset_index()
                .sort_values(y_col, ascending=False)
                .head(top_n)
            )

            ct1, ct2, ct3 = st.columns(3)
            ct1.metric("Total Records", f"{ncrb_df[y_col].sum():,.0f}")
            ct2.metric("Categories", ncrb_df[x_col].nunique())
            ct3.metric(f"Top: {chart_df.iloc[0][x_col][:25] if len(chart_df)>0 else '—'}",
                       f"{chart_df.iloc[0][y_col]:,.0f}" if len(chart_df)>0 else "—")

            chart_type = st.radio(
                "Chart type:", ["Bar", "Horizontal Bar", "Pie", "Treemap"],
                horizontal=True, key="chart_type"
            )

            COLORS = ["#1a2744", "#2d3f6b", "#4a6fa5", "#b8860b", "#d4a017",
                      "#c0392b", "#1a6b3a", "#2e86ab", "#a23b72", "#f18f01"]

            if chart_type == "Bar":
                fig = px.bar(
                    chart_df, x=x_col, y=y_col,
                    title=f"Top {top_n} by {y_col}",
                    color=x_col, color_discrete_sequence=COLORS,
                )
                fig.update_layout(showlegend=False)
            elif chart_type == "Horizontal Bar":
                fig = px.bar(
                    chart_df.sort_values(y_col), x=y_col, y=x_col,
                    orientation="h", title=f"Top {top_n} by {y_col}",
                    color=x_col, color_discrete_sequence=COLORS,
                )
                fig.update_layout(showlegend=False)
            elif chart_type == "Pie":
                fig = px.pie(
                    chart_df, names=x_col, values=y_col,
                    title=f"Distribution by {y_col}", hole=0.45,
                    color_discrete_sequence=COLORS,
                )
            else:  # Treemap
                fig = px.treemap(
                    chart_df, path=[x_col], values=y_col,
                    title=f"Treemap — {y_col}",
                    color_discrete_sequence=COLORS,
                )

            fig.update_layout(
                paper_bgcolor="#ffffff",
                plot_bgcolor="#f8f9fb",
                font=dict(family="DM Sans, sans-serif", color="#1e2533"),
                title_font=dict(family="Lora, serif", size=16, color="#1a2744"),
                margin=dict(t=60, l=20, r=20, b=20),
                height=480,
            )
            fig.update_xaxes(gridcolor="#e2e6ef", tickfont=dict(size=11))
            fig.update_yaxes(gridcolor="#e2e6ef", tickfont=dict(size=11))
            st.plotly_chart(fig, use_container_width=True)

            # Download
            csv_dl = chart_df.to_csv(index=False)
            st.download_button(
                "📥 Download filtered data (CSV)",
                csv_dl, "ncrb_2023_filtered.csv", "text/csv"
            )

            # Full table
            with st.expander("📊 Full data table"):
                st.dataframe(ncrb_df, use_container_width=True, height=400, hide_index=True)


# ═════════════════════════════════════════════════════════════════════════════
# TAB 4 — LEGAL CHAT
# ═════════════════════════════════════════════════════════════════════════════

with tab_chat:
    st.markdown("### Legal Research Chat")
    st.caption("Full conversation history is maintained during your session.")

    # Chat history display
    chat_container = st.container()
    with chat_container:
        if not st.session_state.chat_history:
            st.markdown(
                '<div style="text-align:center;padding:40px 0;color:#8b95ad">'
                '<div style="font-size:2rem;margin-bottom:8px">⚖️</div>'
                '<div style="font-family:\'Lora\',serif;font-size:1rem;font-weight:600;color:#1a2744">Start a conversation</div>'
                '<div style="font-size:0.85rem;margin-top:4px">Ask any question about Indian criminal law</div>'
                '</div>',
                unsafe_allow_html=True
            )
        else:
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    st.markdown(
                        f'<div style="text-align:right">'
                        f'<div class="chat-label" style="color:#8b95ad;text-align:right">You</div>'
                        f'<div class="chat-bubble-user">{msg["content"]}</div>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f'<div>'
                        f'<div class="chat-label" style="color:#1a2744">⚖ LexIPC Assistant</div>'
                        f'<div class="chat-bubble-ai">{msg["content"].replace(chr(10),"<br>")}</div>'
                        f'</div>',
                        unsafe_allow_html=True
                    )

    st.markdown("---")

    # Input area
    chat_input = st.text_area(
        "",
        height=90,
        key="chat_input",
        placeholder="Type your legal question here…",
        label_visibility="collapsed",
    )

    btn_col, clear_col = st.columns([1, 5])
    with btn_col:
        send = st.button("Send →", type="primary", key="chat_send", use_container_width=True)
    with clear_col:
        if st.button("🗑 Clear chat", key="clear_chat"):
            st.session_state.chat_history = []
            st.rerun()

    if send and chat_input.strip():
        user_msg = chat_input.strip()
        st.session_state.chat_history.append({"role": "user", "content": user_msg})

        # Build messages with IPC context
        matched = search_ipc(user_msg, ipc_df, top_n=3) if not ipc_df.empty else pd.DataFrame()
        ipc_ctx = ""
        if not matched.empty:
            ipc_ctx = "\n\n[Auto-matched IPC Sections: " + "; ".join(
                f"{r.get('section','')}: {r.get('offense','')[:60]}"
                for _, r in matched.iterrows()
            ) + "]"

        messages_to_send = st.session_state.chat_history.copy()
        messages_to_send[-1]["content"] += ipc_ctx

        with st.spinner("Thinking…"):
            reply = call_gemini(messages_to_send, LEGAL_SYSTEM)

        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("---")
st.markdown(
    '<div style="text-align:center;color:#8b95ad;font-family:\'DM Sans\',sans-serif;'
    'font-size:0.78rem;padding:8px 0 4px">'
    '⚖️ LexIPC — Indian Criminal Law Research Assistant &nbsp;·&nbsp; '
    'Powered by Google Gemini 1.5 Flash (Free) &nbsp;·&nbsp; '
    'For educational & research use only — not legal advice'
    '</div>',
    unsafe_allow_html=True
)
