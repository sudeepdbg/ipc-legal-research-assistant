"""
⚖️ LexIPC — Indian Criminal Law Research Assistant
Single-file Streamlit app. No backend. No localhost dependency.
Uses Google Gemini API (free tier) + pandas IPC CSV search.

Fixes from v1:
  - Gemini 404: updated to gemini-1.5-flash (free, works reliably)
  - Sidebar buttons blank: fixed key generation + label rendering
  - Clean, professional UI with proper label visibility
"""

import streamlit as st
import pandas as pd
import requests
import json
import re
from pathlib import Path

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LexIPC · Indian Criminal Law Research",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Crimson+Pro:ital,wght@0,400;0,600;0,700;1,400&family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

/* ── Base ── */
html, body, [class*="css"] { font-family: 'IBM Plex Sans', sans-serif; }
.stApp { background: #f5f3ef; color: #1a1a2e; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #1a1a2e !important;
    border-right: 1px solid #2d2d4a;
}
[data-testid="stSidebar"] * { color: #e0ddd5 !important; }
[data-testid="stSidebar"] h1,[data-testid="stSidebar"] h2,[data-testid="stSidebar"] h3 {
    color: #e8c84a !important;
    font-family: 'Crimson Pro', serif !important;
}
[data-testid="stSidebar"] label { color: #9090a8 !important; font-size: 0.8rem !important; }
[data-testid="stSidebar"] .stTextInput input {
    background: #252540 !important;
    border: 1px solid #3a3a5a !important;
    color: #e0ddd5 !important;
    border-radius: 6px !important;
}
[data-testid="stSidebar"] .stButton > button {
    background: #252540 !important;
    color: #c0b090 !important;
    border: 1px solid #3a3a5a !important;
    border-radius: 6px !important;
    text-align: left !important;
    padding: 8px 12px !important;
    font-size: 0.82rem !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    width: 100% !important;
    transition: all 0.15s !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: #2f2f50 !important;
    border-color: #e8c84a !important;
    color: #e8c84a !important;
}

/* ── Header ── */
.lex-header {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    border-radius: 12px;
    padding: 32px 36px;
    margin-bottom: 24px;
    border: 1px solid #2d2d4a;
}
.lex-header h1 {
    font-family: 'Crimson Pro', serif;
    font-size: 2.4rem;
    color: #e8c84a;
    margin: 0 0 6px 0;
    letter-spacing: -0.01em;
}
.lex-header p { color: #9090a8; font-size: 0.9rem; margin: 0; }
.badge {
    display: inline-block;
    padding: 5px 14px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 500;
    margin: 6px 4px 0 0;
}
.badge-gold  { background: rgba(232,200,74,0.15); color: #e8c84a; border: 1px solid rgba(232,200,74,0.4); }
.badge-green { background: rgba(82,196,130,0.15); color: #52c482; border: 1px solid rgba(82,196,130,0.4); }
.badge-blue  { background: rgba(100,160,240,0.15); color: #64a0f0; border: 1px solid rgba(100,160,240,0.4); }
.badge-red   { background: rgba(240,80,80,0.15);  color: #f05050; border: 1px solid rgba(240,80,80,0.4);  }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: white;
    border-radius: 10px 10px 0 0;
    border: 1px solid #e0ddd5;
    border-bottom: none;
    padding: 6px 6px 0;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #6a6a8a;
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 0.88rem;
    font-weight: 500;
    border-radius: 8px 8px 0 0;
    padding: 10px 20px;
    border: none;
    border-bottom: 3px solid transparent;
}
.stTabs [aria-selected="true"] {
    color: #1a1a2e !important;
    border-bottom: 3px solid #e8c84a !important;
    font-weight: 600 !important;
    background: rgba(232,200,74,0.08) !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: white;
    border: 1px solid #e0ddd5;
    border-top: none;
    border-radius: 0 0 10px 10px;
    padding: 24px;
}

/* ── Main inputs & buttons ── */
.stTextArea textarea, .stTextInput input {
    border: 1.5px solid #d0cec8 !important;
    border-radius: 8px !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    background: #fafaf8 !important;
    color: #1a1a2e !important;
    transition: border-color 0.2s !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: #e8c84a !important;
    box-shadow: 0 0 0 3px rgba(232,200,74,0.15) !important;
}
.stButton > button {
    background: #1a1a2e !important;
    color: #e8c84a !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-weight: 600 !important;
    padding: 10px 24px !important;
    font-size: 0.9rem !important;
    transition: all 0.2s !important;
    letter-spacing: 0.02em !important;
}
.stButton > button:hover {
    background: #2d2d50 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(26,26,46,0.3) !important;
}

/* ── IPC Section Card ── */
.ipc-card {
    background: white;
    border: 1px solid #e0ddd5;
    border-left: 5px solid #e8c84a;
    border-radius: 8px;
    padding: 18px 22px;
    margin: 10px 0;
    transition: box-shadow 0.2s;
}
.ipc-card:hover { box-shadow: 0 4px 16px rgba(26,26,46,0.08); }
.ipc-section-num {
    font-family: 'Crimson Pro', serif;
    font-size: 1.25rem;
    color: #1a1a2e;
    font-weight: 700;
}
.ipc-offense {
    font-size: 0.9rem;
    color: #4a4a6a;
    font-style: italic;
    margin: 4px 0;
    line-height: 1.5;
}
.ipc-punish {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem;
    color: #c03030;
    background: #fff0f0;
    padding: 3px 10px;
    border-radius: 4px;
    display: inline-block;
    margin-top: 6px;
    border: 1px solid rgba(192,48,48,0.2);
}
.ipc-desc {
    font-size: 0.85rem;
    color: #6a6a8a;
    margin-top: 8px;
    line-height: 1.6;
}

/* ── AI Answer ── */
.ai-box {
    background: #f8f7f3;
    border: 1px solid #e0ddd5;
    border-top: 4px solid #e8c84a;
    border-radius: 8px;
    padding: 24px 28px;
    margin: 16px 0;
    line-height: 1.8;
    color: #1a1a2e;
}

/* ── Chat messages ── */
.chat-user {
    background: #1a1a2e;
    color: #e0ddd5;
    border-radius: 12px 12px 4px 12px;
    padding: 14px 18px;
    margin: 8px 0 8px 60px;
    font-size: 0.9rem;
    line-height: 1.6;
}
.chat-assistant {
    background: white;
    border: 1px solid #e0ddd5;
    border-left: 4px solid #e8c84a;
    border-radius: 4px 12px 12px 12px;
    padding: 14px 18px;
    margin: 8px 60px 8px 0;
    font-size: 0.9rem;
    line-height: 1.6;
    color: #1a1a2e;
}
.chat-label-user { text-align:right; font-size:0.75rem; color:#9090a8; margin-bottom:4px; }
.chat-label-bot  { font-size:0.75rem; color:#9090a8; margin-bottom:4px; }

/* ── Metrics ── */
[data-testid="stMetricValue"] { color: #e8c84a !important; font-family: 'Crimson Pro', serif !important; }
[data-testid="stMetricLabel"] { color: #9090a8 !important; font-size: 0.8rem !important; }

/* ── Misc ── */
.stSelectbox div[data-baseweb="select"] { background: #fafaf8 !important; }
div[data-testid="stExpander"] { border: 1px solid #e0ddd5 !important; border-radius: 8px !important; }
.stDataFrame { border: 1px solid #e0ddd5; border-radius: 8px; overflow: hidden; }
hr { border-color: #e0ddd5; }
</style>
""", unsafe_allow_html=True)


# ── Data loading ──────────────────────────────────────────────────────────────

@st.cache_data(show_spinner=False)
def load_ipc_data() -> pd.DataFrame:
    for p in ["ipc_sections.csv", "data/ipc_sections.csv", "../ipc_sections.csv"]:
        if Path(p).exists():
            df = pd.read_csv(p)
            df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
            return df
    return pd.DataFrame()

@st.cache_data(show_spinner=False)
def load_ncrb_data() -> pd.DataFrame:
    for p in ["NCRB_CII_2023_Table_18A_2_0.csv",
              "data/NCRB_CII_2023_Table_18A_2_0.csv"]:
        if Path(p).exists():
            df = pd.read_csv(p)
            df.columns = [c.strip() for c in df.columns]
            return df
    return pd.DataFrame()

ipc_df  = load_ipc_data()
ncrb_df = load_ncrb_data()


# ── Gemini API ────────────────────────────────────────────────────────────────
# FIX: Use gemini-1.5-flash — gemini-pro was deprecated and returns 404

GEMINI_MODELS = [
    "gemini-1.5-flash",      # Free tier, fast, reliable
    "gemini-2.0-flash",      # Newer free tier option
    "gemini-1.5-pro",        # Fallback
]

def get_gemini_key() -> str:
    try:
        return st.secrets.get("GEMINI_API_KEY", "") or st.secrets.get("GOOGLE_API_KEY", "")
    except Exception:
        import os
        return os.environ.get("GEMINI_API_KEY", os.environ.get("GOOGLE_API_KEY", ""))

def call_gemini(messages: list, system_prompt: str = "") -> str:
    """
    Call Google Gemini API directly via REST.
    Uses gemini-1.5-flash (free tier, no billing required).
    """
    api_key = get_gemini_key()
    if not api_key:
        return (
            "⚠️ **Gemini API key not configured.**\n\n"
            "Go to **Settings → Secrets** on Streamlit Cloud and add:\n"
            "```\nGEMINI_API_KEY = \"your-key-here\"\n```\n"
            "Get a free key at: https://aistudio.google.com/app/apikey"
        )

    # Build Gemini-format message list
    gemini_msgs = []
    if system_prompt:
        gemini_msgs.append({
            "role": "user",
            "parts": [{"text": f"[SYSTEM INSTRUCTIONS]\n{system_prompt}\n[END SYSTEM]\n\nAcknowledge these instructions briefly."}]
        })
        gemini_msgs.append({
            "role": "model",
            "parts": [{"text": "Understood. I'm LexIPC, your Indian criminal law research assistant. I'll follow all guidelines."}]
        })

    for m in messages:
        role = "user" if m["role"] == "user" else "model"
        gemini_msgs.append({"role": role, "parts": [{"text": m["content"]}]})

    payload = {
        "contents": gemini_msgs,
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 2048,
            "topP": 0.8,
        },
        "safetySettings": [
            {"category": "HARM_CATEGORY_HARASSMENT",       "threshold": "BLOCK_ONLY_HIGH"},
            {"category": "HARM_CATEGORY_HATE_SPEECH",      "threshold": "BLOCK_ONLY_HIGH"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT","threshold": "BLOCK_ONLY_HIGH"},
        ]
    }

    last_error = ""
    for model in GEMINI_MODELS:
        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{model}:generateContent?key={api_key}"
        )
        try:
            resp = requests.post(url, json=payload, timeout=60)
            if resp.status_code == 200:
                data = resp.json()
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        return parts[0].get("text", "No response text.")
                return "⚠️ Empty response from Gemini."
            elif resp.status_code == 404:
                last_error = f"Model {model} not found (404). Trying next..."
                continue  # try next model
            elif resp.status_code == 400:
                err = resp.json().get("error", {}).get("message", resp.text[:200])
                return f"❌ Bad request: {err}"
            elif resp.status_code == 403:
                return (
                    "❌ **API key error (403 Forbidden).**\n\n"
                    "Check your GEMINI_API_KEY is correct and has Generative Language API enabled."
                )
            else:
                last_error = f"HTTP {resp.status_code}: {resp.text[:200]}"
                continue
        except requests.exceptions.Timeout:
            return "❌ Request timed out. Please try again."
        except requests.exceptions.ConnectionError:
            return "❌ Could not reach Google API. Check internet connection."

    return f"❌ All Gemini models failed. Last error: {last_error}"


# ── IPC search ────────────────────────────────────────────────────────────────

def search_ipc(query: str, df: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
    if df.empty or not query.strip():
        return df.head(top_n)

    q_lower = query.lower()
    terms   = [t for t in q_lower.split() if len(t) > 2]
    scores  = pd.Series(0.0, index=df.index)

    text_cols = [c for c in ["description", "offense", "section", "punishment"] if c in df.columns]
    weights   = {"offense": 3.0, "section": 2.5, "punishment": 1.5, "description": 1.0}

    for term in terms:
        for col in text_cols:
            match = df[col].fillna("").str.lower().str.contains(term, regex=False)
            scores += match.astype(float) * weights.get(col, 1.0)

    # Boost exact section number match
    sec_match = re.search(r'\b(\d{2,3}[A-Z]?)\b', query.upper())
    if sec_match and "section" in df.columns:
        mask = df["section"].fillna("").str.upper().str.contains(sec_match.group(1), regex=False)
        scores[mask] += 15

    result = df[scores > 0].copy()
    result["_score"] = scores[scores > 0]
    return result.sort_values("_score", ascending=False).drop("_score", axis=1).head(top_n)


def render_ipc_card(row: pd.Series):
    section = row.get("section", "N/A")
    offense = row.get("offense", "—")
    punish  = row.get("punishment", "—")
    desc    = row.get("description", "")

    # Extract simple-words summary from description
    short = ""
    if desc:
        lines = [l.strip() for l in str(desc).split("\n") if l.strip()]
        for i, l in enumerate(lines):
            if "simple words" in l.lower() and i + 1 < len(lines):
                short = lines[i + 1][:280]
                break
        if not short and lines:
            short = lines[-1][:280]
        if short and not short.endswith((".", "…")):
            short += "…"

    st.markdown(f"""
    <div class="ipc-card">
        <div class="ipc-section-num">⚖️ {section}</div>
        <div class="ipc-offense">{offense}</div>
        <span class="ipc-punish">🔒 {punish}</span>
        {'<div class="ipc-desc">' + short + '</div>' if short else ''}
    </div>
    """, unsafe_allow_html=True)


# ── System prompt ─────────────────────────────────────────────────────────────

LEGAL_SYSTEM = """You are LexIPC, an expert Indian criminal law research assistant.
Specialise in: Indian Penal Code (IPC), Code of Criminal Procedure (CrPC), Evidence Act,
Bharatiya Nyaya Sanhita 2023 (BNS), and related Indian legislation.

Rules:
- Always cite specific IPC/BNS section numbers (e.g., "IPC Section 302", "BNS Section 101")
- Mention bailable/non-bailable and cognisable/non-cognisable status when relevant
- Reference landmark Supreme Court and High Court judgements where applicable
- Note if a provision has been replaced/amended by BNS 2023
- For procedural questions, cite CrPC sections
- Structure responses: short intro → key sections → punishment → procedure → case laws → note
- End every response with: "⚠️ This is legal information, not legal advice. Consult a qualified lawyer."
- Keep responses focused: 300–500 words unless detailed analysis is requested
- Use markdown formatting: **bold** for section numbers, bullet lists for elements"""


# ── Session state ─────────────────────────────────────────────────────────────

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "prefill" not in st.session_state:
    st.session_state.prefill = ""


# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    # Logo & title
    st.markdown("""
    <div style="padding:8px 0 16px">
        <div style="font-family:'Crimson Pro',serif;font-size:1.6rem;color:#e8c84a;font-weight:700">
            ⚖️ LexIPC
        </div>
        <div style="font-size:0.8rem;color:#6a6a8a;margin-top:2px">
            Indian Criminal Law Research
        </div>
    </div>
    """, unsafe_allow_html=True)

    # API key status
    gemini_key = get_gemini_key()
    if gemini_key:
        st.markdown('<span class="badge badge-green">● Gemini AI Connected</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="badge badge-red">✗ API Key Missing</span>', unsafe_allow_html=True)
        with st.expander("How to add API key"):
            st.markdown("""
            **Streamlit Cloud:**
            1. App Settings → Secrets
            2. Add: `GEMINI_API_KEY = "your-key"`

            **Get free key:**
            [aistudio.google.com](https://aistudio.google.com/app/apikey)
            """)

    st.divider()

    # Dataset metrics
    st.markdown("**Dataset**")
    c1, c2 = st.columns(2)
    c1.metric("IPC Sections", len(ipc_df) if not ipc_df.empty else "—")
    c2.metric("NCRB Records", len(ncrb_df) if not ncrb_df.empty else "—")

    if ipc_df.empty:
        st.warning("Place `ipc_sections.csv` in the app folder.")

    st.divider()

    # Quick section lookup
    st.markdown("**Quick Section Lookup**")
    quick = st.text_input(
        "Enter section number",        # actual label (shown)
        placeholder="e.g. 302, 376…",
        key="quick_lookup",
        label_visibility="collapsed"   # hides the label above, input still works
    )
    if quick.strip() and not ipc_df.empty:
        q = quick.strip().upper().lstrip("IPC_ ")
        mask = ipc_df["section"].fillna("").str.upper().str.contains(q, regex=False)
        found = ipc_df[mask]
        if not found.empty:
            r = found.iloc[0]
            st.markdown(f"""
            <div style="background:#252540;padding:12px;border-left:3px solid #e8c84a;border-radius:6px;margin:8px 0">
                <b style="color:#e8c84a;font-family:'Crimson Pro',serif">{r.get('section','')}</b><br>
                <span style="color:#9090a8;font-size:0.8rem;font-style:italic">{str(r.get('offense',''))[:80]}…</span><br>
                <code style="color:#f08080;font-size:0.78rem">{r.get('punishment','')}</code>
            </div>""", unsafe_allow_html=True)
        else:
            st.caption("Section not found")

    st.divider()

    # ── FIX: Common Queries — explicit labels, no blank buttons ──
    st.markdown("**Common Queries**")

    QUERIES = [
        ("Murder — IPC 302",             "What is IPC Section 302? Explain murder, its elements, punishment and important case laws."),
        ("Rape — IPC 376",               "Explain IPC Section 376 (rape). What are the elements, punishment and recent amendments?"),
        ("Theft & Robbery",              "What is the difference between theft, robbery and dacoity under IPC? Which sections apply?"),
        ("Bail conditions for murder",   "What are the bail conditions for a murder case? Is it bailable or non-bailable?"),
        ("Cheating — IPC 420",           "Explain cheating and dishonest inducement under IPC Section 420. What is the punishment?"),
        ("Culpable homicide vs murder",  "What is the difference between culpable homicide (IPC 299) and murder (IPC 302)?"),
        ("Cybercrime sections",          "Which IPC and IT Act sections apply to cybercrime in India?"),
        ("Rights of accused at arrest",  "What are the legal rights of a person at the time of arrest in India?"),
    ]

    for label, query_text in QUERIES:
        if st.button(f"→ {label}", key=f"sq_{label[:20]}", use_container_width=True):
            st.session_state.prefill = query_text
            st.rerun()

    st.divider()
    st.caption("LexIPC v2.0 · Legal info only · Not legal advice")


# ── Main content ──────────────────────────────────────────────────────────────

# Header
st.markdown(f"""
<div class="lex-header">
    <h1>⚖️ Indian Criminal Law Research Assistant</h1>
    <p>Powered by Google Gemini AI · IPC Sections Database · NCRB Crime Statistics 2023</p>
    <div style="margin-top:12px">
        {'<span class="badge badge-green">● Gemini AI (Free)</span>' if gemini_key else '<span class="badge badge-red">✗ API Key Required</span>'}
        {'<span class="badge badge-gold">📚 IPC Database (' + str(len(ipc_df)) + ' sections)</span>' if not ipc_df.empty else '<span class="badge badge-red">⚠ IPC CSV Missing</span>'}
        {'<span class="badge badge-blue">📊 NCRB 2023</span>' if not ncrb_df.empty else ''}
    </div>
</div>
""", unsafe_allow_html=True)

# Tabs
tab_ai, tab_ipc, tab_stats, tab_chat = st.tabs([
    "🔬 AI Research", "📚 IPC Sections", "📊 Crime Statistics", "💬 Legal Chat"
])


# ════════════════════════════════════════════════════════════════════════
# TAB 1 — AI RESEARCH
# ════════════════════════════════════════════════════════════════════════
with tab_ai:
    st.markdown("### Ask a Legal Question")
    st.caption("Gemini AI analyses your query and references relevant IPC sections automatically.")

    # Handle prefill from sidebar
    prefill_val = st.session_state.pop("prefill", "")

    query = st.text_area(
        "Enter your legal query",
        value=prefill_val,
        height=130,
        placeholder=(
            "e.g. What is the punishment for murder under IPC?\n"
            "What are the elements of rape? How to get bail in NDPS cases?"
        ),
        key="research_query",
        label_visibility="collapsed"
    )

    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        analyse_btn = st.button("⚖️ Analyse Query", type="primary", use_container_width=True)
    with col2:
        auto_ipc = st.toggle("Auto-match IPC sections", value=True)
    with col3:
        detailed = st.toggle("Detailed analysis", value=False)

    if analyse_btn:
        if not query.strip():
            st.warning("Please enter a legal query.")
        else:
            # Search IPC
            matched_df = pd.DataFrame()
            if auto_ipc and not ipc_df.empty:
                matched_df = search_ipc(query, ipc_df, top_n=6)

            # Build context for Gemini
            ipc_ctx = ""
            if not matched_df.empty:
                ctx_parts = []
                for _, row in matched_df.iterrows():
                    ctx_parts.append(
                        f"{row.get('section','')}: {row.get('offense','')} | "
                        f"Punishment: {row.get('punishment','')}"
                    )
                ipc_ctx = (
                    "\n\n[Auto-matched IPC Sections from database:\n"
                    + "\n".join(ctx_parts) + "]"
                )

            detail_note = (
                " Provide comprehensive analysis including case laws, procedural details, "
                "and practical implications. Use section headings."
                if detailed else
                " Keep response concise and focused (under 500 words)."
            )

            msgs = [{"role": "user", "content": query + ipc_ctx + detail_note}]

            with st.spinner("Researching legal provisions…"):
                answer = call_gemini(msgs, LEGAL_SYSTEM)

            st.markdown(f'<div class="ai-box">{answer}</div>', unsafe_allow_html=True)

            if not matched_df.empty:
                st.markdown(f"---\n**📚 {len(matched_df)} Matching IPC Sections:**")
                for _, row in matched_df.iterrows():
                    render_ipc_card(row)

            # Save to chat
            st.session_state.chat_history.extend([
                {"role": "user",      "content": query},
                {"role": "assistant", "content": answer},
            ])


# ════════════════════════════════════════════════════════════════════════
# TAB 2 — IPC SECTIONS BROWSER
# ════════════════════════════════════════════════════════════════════════
with tab_ipc:
    st.markdown("### IPC Sections Database")

    if ipc_df.empty:
        st.error(
            "⚠️ `ipc_sections.csv` not found.\n\n"
            "Place the CSV file in the same directory as `app.py`."
        )
        st.stop()

    # Search row
    s1, s2, s3 = st.columns([4, 1, 1])
    with s1:
        sec_q = st.text_input(
            "Search IPC sections",
            placeholder="Search by keyword or section number (e.g. murder, 302, theft, assault)…",
            key="ipc_search",
            label_visibility="collapsed"
        )
    with s2:
        show_n = st.selectbox("Show", [10, 25, 50], index=0, label_visibility="collapsed")
    with s3:
        view_mode = st.radio("View", ["Cards", "Table"], horizontal=False, label_visibility="collapsed")

    # Optional punishment filter
    punish_q = st.text_input(
        "Filter by punishment",
        placeholder="e.g. death, life imprisonment, fine…",
        key="punish_filter",
        label_visibility="collapsed"
    )

    # Apply search
    if sec_q.strip():
        results = search_ipc(sec_q, ipc_df, top_n=show_n)
    else:
        results = ipc_df.head(show_n)

    if punish_q.strip() and "punishment" in results.columns:
        results = results[
            results["punishment"].fillna("").str.lower().str.contains(
                punish_q.lower(), regex=False
            )
        ]

    st.caption(f"Showing **{len(results)}** sections")

    if view_mode == "Cards":
        for _, row in results.iterrows():
            render_ipc_card(row)
    else:
        disp_cols = [c for c in ["section", "offense", "punishment"] if c in results.columns]
        st.dataframe(results[disp_cols], use_container_width=True, height=480, hide_index=True)

    # Detailed view
    if not results.empty and "section" in results.columns:
        st.markdown("---")
        chosen = st.selectbox(
            "View full description for section:",
            results["section"].tolist(),
            key="detail_picker"
        )
        if chosen:
            row = results[results["section"] == chosen].iloc[0]
            with st.expander(f"📄 Full text: {chosen}", expanded=True):
                st.markdown(f"**Offense:** {row.get('offense', '—')}")
                st.markdown(f"**Punishment:** `{row.get('punishment', '—')}`")
                st.markdown("---")
                st.markdown(row.get("description", "No description available."))

                if st.button(f"🤖 Ask AI about {chosen}", key=f"ai_sec_{chosen}"):
                    msg_text = (
                        f"Explain {chosen} of IPC in detail. "
                        f"Offense: {row.get('offense','')}. "
                        f"Punishment: {row.get('punishment','')}. "
                        "Include: all elements, landmark cases, bailable/non-bailable, "
                        "cognisable/non-cognisable, CrPC procedure, and BNS equivalent if any."
                    )
                    with st.spinner("Analysing…"):
                        resp = call_gemini(
                            [{"role": "user", "content": msg_text}], LEGAL_SYSTEM
                        )
                    st.markdown(f'<div class="ai-box">{resp}</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════
# TAB 3 — NCRB CRIME STATISTICS
# ════════════════════════════════════════════════════════════════════════
with tab_stats:
    st.markdown("### Crime Statistics — NCRB 2023")

    if ncrb_df.empty:
        st.info(
            "📊 Place `NCRB_CII_2023_Table_18A_2_0.csv` in the app folder to enable charts."
        )
        st.markdown("""
        **Once loaded, this tab shows:**
        - Crime incidence by State/UT
        - Category-wise distribution charts
        - Year-on-year comparisons
        - Filterable data table with CSV export
        """)
    else:
        st.caption(f"Source: NCRB Crime in India 2023 · {len(ncrb_df):,} records")
        try:
            import plotly.express as px

            with st.expander("📋 Data preview & column info"):
                st.write("**Columns:**", list(ncrb_df.columns))
                st.dataframe(ncrb_df.head(8), use_container_width=True)

            num_cols = ncrb_df.select_dtypes(include="number").columns.tolist()
            str_cols = ncrb_df.select_dtypes(include="object").columns.tolist()

            if num_cols and str_cols:
                r1c1, r1c2, r1c3 = st.columns(3)
                with r1c1:
                    x_col = st.selectbox("Category (X axis)", str_cols, key="ncrb_x")
                with r1c2:
                    y_col = st.selectbox("Metric (Y axis)", num_cols, key="ncrb_y")
                with r1c3:
                    top_n = st.slider("Top N", 5, 30, 15, key="ncrb_topn")

                chart_type = st.radio(
                    "Chart type", ["Bar", "Horizontal Bar", "Pie", "Treemap"],
                    horizontal=True, key="ncrb_chart"
                )

                chart_df = (
                    ncrb_df.groupby(x_col)[y_col]
                    .sum().reset_index()
                    .sort_values(y_col, ascending=False)
                    .head(top_n)
                )

                color_scale = [[0, "#1a1a2e"], [0.5, "#8b6914"], [1, "#e8c84a"]]

                if chart_type == "Bar":
                    fig = px.bar(chart_df, x=x_col, y=y_col, title=f"Top {top_n} by {y_col}",
                                 color=y_col, color_continuous_scale=color_scale)
                    fig.update_xaxes(tickangle=-45)
                elif chart_type == "Horizontal Bar":
                    fig = px.bar(chart_df.sort_values(y_col), x=y_col, y=x_col,
                                 orientation="h", title=f"Top {top_n} by {y_col}",
                                 color=y_col, color_continuous_scale=color_scale)
                elif chart_type == "Pie":
                    fig = px.pie(chart_df, names=x_col, values=y_col, hole=0.4,
                                 title=f"Distribution by {y_col}",
                                 color_discrete_sequence=px.colors.sequential.YlOrBr_r)
                else:
                    fig = px.treemap(chart_df, path=[x_col], values=y_col,
                                     title=f"Treemap by {y_col}",
                                     color=y_col, color_continuous_scale=color_scale)

                fig.update_layout(
                    paper_bgcolor="white", plot_bgcolor="white",
                    font=dict(family="IBM Plex Sans, sans-serif", color="#1a1a2e"),
                    title_font=dict(family="Crimson Pro, serif", color="#1a1a2e"),
                    coloraxis_showscale=False,
                    margin=dict(t=60, l=20, r=20, b=60),
                )
                st.plotly_chart(fig, use_container_width=True)

                csv_dl = chart_df.to_csv(index=False)
                st.download_button(
                    "📥 Download filtered data (CSV)",
                    csv_dl, "ncrb_filtered.csv", "text/csv"
                )

        except ImportError:
            st.warning("`plotly` not installed. Run: `pip install plotly`")
            st.dataframe(ncrb_df, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════
# TAB 4 — LEGAL CHAT
# ════════════════════════════════════════════════════════════════════════
with tab_chat:
    st.markdown("### Legal Research Chat")
    st.caption("Full conversation history maintained during your session.")

    # Render history
    if not st.session_state.chat_history:
        st.markdown("""
        <div style="text-align:center;padding:48px 24px;color:#9090a8">
            <div style="font-size:2.5rem">⚖️</div>
            <p style="margin-top:8px">Start a conversation about Indian criminal law.</p>
            <p style="font-size:0.85rem">Ask about any IPC section, bail procedure, criminal offence, or case law.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown('<div class="chat-label-user">YOU</div>', unsafe_allow_html=True)
                st.markdown(
                    f'<div class="chat-user">{msg["content"]}</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown('<div class="chat-label-bot">⚖ LEXIPC ASSISTANT</div>', unsafe_allow_html=True)
                st.markdown(
                    f'<div class="chat-assistant">{msg["content"]}</div>',
                    unsafe_allow_html=True
                )

    st.markdown("---")

    # Input
    chat_q = st.text_area(
        "Your message",
        height=100,
        placeholder="Ask about any IPC section, criminal offence, bail, rights, procedure…",
        key="chat_input",
        label_visibility="collapsed"
    )

    b1, b2, b3 = st.columns([1, 1, 4])
    with b1:
        send = st.button("Send →", type="primary", key="send_btn", use_container_width=True)
    with b2:
        clear = st.button("🗑 Clear chat", key="clear_btn", use_container_width=True)

    if send and chat_q.strip():
        # Search IPC for context
        matched_ctx = search_ipc(chat_q, ipc_df, top_n=3) if not ipc_df.empty else pd.DataFrame()
        ctx_note = ""
        if not matched_ctx.empty:
            ctx_note = "\n\n[Relevant IPC sections: " + "; ".join(
                f"{r.get('section','')}: {r.get('offense','')[:50]}"
                for _, r in matched_ctx.iterrows()
            ) + "]"

        # Append user message
        st.session_state.chat_history.append({
            "role": "user", "content": chat_q.strip()
        })

        # Call Gemini with full history
        history_msgs = st.session_state.chat_history.copy()
        history_msgs[-1]["content"] += ctx_note

        with st.spinner("Thinking…"):
            reply = call_gemini(history_msgs, LEGAL_SYSTEM)

        st.session_state.chat_history.append({
            "role": "assistant", "content": reply
        })
        st.rerun()

    if clear:
        st.session_state.chat_history = []
        st.rerun()


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:24px;color:#9090a8;font-size:0.78rem;
            font-family:'IBM Plex Mono',monospace;border-top:1px solid #e0ddd5;margin-top:24px">
⚖️ LexIPC · Indian Criminal Law Research Assistant · For informational purposes only · Not legal advice<br>
Model: Gemini 1.5 Flash (Free) · Data: IPC Sections + NCRB 2023
</div>
""", unsafe_allow_html=True)
