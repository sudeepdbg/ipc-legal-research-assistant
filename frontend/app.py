"""
⚖️ LexIPC — Indian Criminal Law Research Assistant
Single-file Streamlit app. No backend. No localhost.

Uses google-generativeai SDK (official, handles all versioning).
Fixes: 404 API error, </div> raw text in header, irrelevant search results.
"""

import streamlit as st
import pandas as pd
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

html, body, [class*="css"] { font-family: 'IBM Plex Sans', sans-serif; }
.stApp { background: #f5f3ef; color: #1a1a2e; }

/* ── Sidebar ── */
[data-testid="stSidebar"] { background: #1a1a2e !important; border-right: 1px solid #2d2d4a; }
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div { color: #c0bdb0 !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #e8c84a !important; font-family: 'Crimson Pro', serif !important; }
[data-testid="stSidebar"] label { color: #7a7a9a !important; font-size: 0.8rem !important; }
[data-testid="stSidebar"] input {
    background: #252540 !important; border: 1px solid #3a3a5a !important;
    color: #e0ddd5 !important; border-radius: 6px !important;
}
[data-testid="stSidebar"] .stButton > button {
    background: #252540 !important; color: #c0b090 !important;
    border: 1px solid #3a3a5a !important; border-radius: 6px !important;
    text-align: left !important; padding: 9px 14px !important;
    font-size: 0.83rem !important; width: 100% !important;
    transition: all 0.15s !important; margin: 2px 0 !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: #2f2f55 !important; border-color: #e8c84a !important; color: #e8c84a !important;
}
[data-testid="stMetricValue"] { color: #e8c84a !important; font-family: 'Crimson Pro', serif !important; font-size: 1.8rem !important; }
[data-testid="stMetricLabel"] { color: #7a7a9a !important; font-size: 0.78rem !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: white; border-radius: 10px 10px 0 0;
    border: 1px solid #e0ddd5; border-bottom: none; padding: 6px 6px 0; gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent; color: #6a6a8a;
    font-family: 'IBM Plex Sans', sans-serif; font-size: 0.88rem; font-weight: 500;
    border-radius: 8px 8px 0 0; padding: 10px 20px;
    border: none; border-bottom: 3px solid transparent;
}
.stTabs [aria-selected="true"] {
    color: #1a1a2e !important; border-bottom: 3px solid #e8c84a !important;
    font-weight: 600 !important; background: rgba(232,200,74,0.08) !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: white; border: 1px solid #e0ddd5; border-top: none;
    border-radius: 0 0 10px 10px; padding: 28px;
}

/* ── Inputs & buttons ── */
.stTextArea textarea, .stTextInput > div > div > input {
    border: 1.5px solid #d0cec8 !important; border-radius: 8px !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    background: #fafaf8 !important; color: #1a1a2e !important;
}
.stTextArea textarea:focus, .stTextInput > div > div > input:focus {
    border-color: #e8c84a !important; box-shadow: 0 0 0 3px rgba(232,200,74,0.15) !important;
}
.stButton > button {
    background: #1a1a2e !important; color: #e8c84a !important;
    border: none !important; border-radius: 8px !important;
    font-family: 'IBM Plex Sans', sans-serif !important; font-weight: 600 !important;
    padding: 10px 24px !important; font-size: 0.9rem !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: #2d2d50 !important; transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(26,26,46,0.3) !important;
}

/* ── Cards ── */
.ipc-card {
    background: white; border: 1px solid #e0ddd5; border-left: 5px solid #e8c84a;
    border-radius: 8px; padding: 18px 22px; margin: 10px 0;
    box-shadow: 0 2px 8px rgba(26,26,46,0.04);
}
.ipc-section-num { font-family: 'Crimson Pro', serif; font-size: 1.3rem; color: #1a1a2e; font-weight: 700; }
.ipc-offense { font-size: 0.9rem; color: #4a4a6a; font-style: italic; margin: 4px 0 8px; line-height: 1.5; }
.ipc-punish {
    font-family: 'IBM Plex Mono', monospace; font-size: 0.78rem; color: #c03030;
    background: #fff0f0; padding: 3px 10px; border-radius: 4px; display: inline-block;
    border: 1px solid rgba(192,48,48,0.2);
}
.ipc-desc { font-size: 0.85rem; color: #5a5a7a; margin-top: 10px; line-height: 1.65; }

/* ── AI Answer ── */
.ai-box {
    background: #f8f7f3; border: 1px solid #e0ddd5; border-top: 4px solid #e8c84a;
    border-radius: 8px; padding: 24px 28px; margin: 16px 0;
    line-height: 1.8; color: #1a1a2e; font-size: 0.92rem;
}

/* ── Chat ── */
.chat-you-label { text-align:right; font-size:0.73rem; color:#9090a8; margin: 12px 0 3px; font-family:'IBM Plex Mono',monospace; }
.chat-bot-label  { font-size:0.73rem; color:#9090a8; margin: 12px 0 3px; font-family:'IBM Plex Mono',monospace; }
.chat-user {
    background: #1a1a2e; color: #e0ddd5; border-radius: 12px 12px 4px 12px;
    padding: 14px 18px; margin-left: 60px; font-size: 0.9rem; line-height: 1.6;
}
.chat-assistant {
    background: white; border: 1px solid #e0ddd5; border-left: 4px solid #e8c84a;
    border-radius: 4px 12px 12px 12px; padding: 14px 18px; margin-right: 60px;
    font-size: 0.9rem; line-height: 1.7; color: #1a1a2e;
}

/* ── Misc ── */
hr { border-color: #e0ddd5; }
div[data-testid="stExpander"] { border: 1px solid #e0ddd5 !important; border-radius: 8px !important; }
</style>
""", unsafe_allow_html=True)


# ── Gemini via official SDK ───────────────────────────────────────────────────

def get_api_key() -> str:
    try:
        k = st.secrets.get("GEMINI_API_KEY", "") or st.secrets.get("GOOGLE_API_KEY", "")
        if k:
            return k
    except Exception:
        pass
    import os
    return os.environ.get("GEMINI_API_KEY", os.environ.get("GOOGLE_API_KEY", ""))


def call_gemini(prompt: str, history: list = None, system: str = "") -> str:
    """
    Call Gemini using the official google-generativeai SDK.
    Handles all endpoint versioning automatically.
    Model: gemini-1.5-flash (free tier, fast, reliable).
    """
    api_key = get_api_key()
    if not api_key:
        return (
            "⚠️ **Gemini API key not set.**\n\n"
            "Add to Streamlit Secrets (Settings → Secrets):\n"
            "```\nGEMINI_API_KEY = \"AIza...\"\n```\n"
            "Get a free key at: https://aistudio.google.com/app/apikey"
        )

    try:
        import google.generativeai as genai
    except ImportError:
        return (
            "❌ `google-generativeai` package not installed.\n\n"
            "Ensure `requirements.txt` contains:\n```\ngoogle-generativeai\n```"
        )

    try:
        genai.configure(api_key=api_key)

        # Try models in order — all free tier
        models_to_try = [
            "gemini-1.5-flash",
            "gemini-2.0-flash-exp",
            "gemini-1.5-flash-latest",
        ]

        generation_config = genai.GenerationConfig(
            temperature=0.3,
            max_output_tokens=2048,
        )

        safety_settings = {
            "HARASSMENT": "BLOCK_ONLY_HIGH",
            "HATE_SPEECH": "BLOCK_ONLY_HIGH",
            "DANGEROUS": "BLOCK_ONLY_HIGH",
        }

        last_err = ""
        for model_name in models_to_try:
            try:
                model = genai.GenerativeModel(
                    model_name=model_name,
                    system_instruction=system if system else None,
                    generation_config=generation_config,
                )

                # Build message list for multi-turn
                if history:
                    chat = model.start_chat(history=[
                        {"role": m["role"], "parts": [m["content"]]}
                        for m in history[:-1]   # all but last
                    ])
                    response = chat.send_message(prompt)
                else:
                    response = model.generate_content(prompt)

                return response.text

            except Exception as e:
                last_err = str(e)
                if "404" in last_err or "not found" in last_err.lower():
                    continue  # try next model
                # Non-404 error — return immediately
                break

        # All models failed
        if "API_KEY" in last_err or "api key" in last_err.lower() or "403" in last_err:
            return (
                "❌ **Invalid API key.**\n\n"
                "Check your `GEMINI_API_KEY` in Streamlit Secrets.\n"
                "Make sure the Generative Language API is enabled in Google Cloud Console."
            )
        return f"❌ Gemini API error: {last_err[:300]}"

    except Exception as e:
        return f"❌ Unexpected error: {str(e)[:300]}"


# ── Data loading ──────────────────────────────────────────────────────────────

@st.cache_data(show_spinner=False)
def load_ipc_data() -> pd.DataFrame:
    for p in ["ipc_sections.csv", "data/ipc_sections.csv"]:
        if Path(p).exists():
            df = pd.read_csv(p)
            df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
            return df
    return pd.DataFrame()


@st.cache_data(show_spinner=False)
def load_ncrb_data() -> pd.DataFrame:
    for p in ["NCRB_CII_2023_Table_18A_2_0.csv", "data/NCRB_CII_2023_Table_18A_2_0.csv"]:
        if Path(p).exists():
            df = pd.read_csv(p)
            df.columns = [c.strip() for c in df.columns]
            return df
    return pd.DataFrame()


ipc_df  = load_ipc_data()
ncrb_df = load_ncrb_data()


# ── IPC search ────────────────────────────────────────────────────────────────

# Criminal law keywords — avoid matching civil/property queries
CRIMINAL_KEYWORDS = {
    "murder", "homicide", "manslaughter", "kidnapping", "abduction",
    "robbery", "dacoity", "theft", "burglary", "extortion", "cheating",
    "fraud", "forgery", "rape", "assault", "hurt", "grievous",
    "obscene", "defamation", "sedition", "riot", "affray", "bribery",
    "corruption", "trespass", "mischief", "arson", "poisoning", "dowry",
    "cruelty", "stalking", "voyeurism", "acid", "terrorist", "waging",
    "counterfeit", "coinage", "arms", "weapon", "culpable", "abetment",
    "conspiracy", "attempt", "bail", "arrest", "custody", "remand",
    "cognisable", "non-cognisable", "warrant", "summons", "trial",
    "conviction", "sentence", "punishment", "fine", "imprisonment",
    "life", "death", "sections", "ipc", "crpc", "bns", "criminal",
    "offence", "offense", "penal", "code", "law", "legal", "court",
    "accused", "victim", "complaint", "fir", "chargesheet", "evidence",
}


def is_criminal_query(query: str) -> bool:
    """Check if query is about criminal law (vs civil/property/family law)."""
    q_lower = query.lower()
    # Check for IPC section numbers
    if re.search(r'\b(ipc|section|sec\.?)\s*\d+', q_lower):
        return True
    # Check for criminal keywords
    words = set(re.findall(r'\b\w+\b', q_lower))
    return bool(words & CRIMINAL_KEYWORDS)


def search_ipc(query: str, df: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
    """
    Smart IPC keyword search.
    Returns empty DataFrame for clearly non-criminal queries (eviction, title suit etc.)
    """
    if df.empty or not query.strip():
        return pd.DataFrame()

    q_lower = query.lower()
    # Extract search terms — skip very short or common words
    stop = {"the", "a", "an", "in", "for", "is", "of", "to", "and", "or", "with",
            "that", "this", "it", "he", "she", "they", "have", "has", "had",
            "where", "what", "how", "who", "when", "which", "need", "find",
            "want", "can", "tell", "me", "my", "do"}
    terms = [t for t in re.findall(r'\b[a-z]+\b', q_lower) if len(t) > 3 and t not in stop]

    if not terms:
        return pd.DataFrame()

    text_cols = [c for c in ["offense", "description", "section", "punishment"] if c in df.columns]
    weights   = {"offense": 4.0, "section": 3.0, "punishment": 1.5, "description": 1.0}
    scores    = pd.Series(0.0, index=df.index)

    for term in terms:
        for col in text_cols:
            match = df[col].fillna("").str.lower().str.contains(term, regex=False)
            scores += match.astype(float) * weights.get(col, 1.0)

    # Boost direct section number match (e.g. "302", "376")
    sec_match = re.search(r'\b(\d{2,3}[A-Z]?)\b', query.upper())
    if sec_match and "section" in df.columns:
        mask = df["section"].fillna("").str.upper().str.contains(sec_match.group(1), regex=False)
        scores[mask] += 20

    # Minimum score threshold to avoid garbage results
    min_score = 2.0
    result = df[scores >= min_score].copy()
    if result.empty:
        return pd.DataFrame()

    result["_score"] = scores[scores >= min_score]
    return result.sort_values("_score", ascending=False).drop("_score", axis=1).head(top_n)


def render_ipc_card(row: pd.Series):
    section = str(row.get("section", "N/A"))
    offense = str(row.get("offense", "—"))
    punish  = str(row.get("punishment", "—"))
    desc    = str(row.get("description", ""))

    short = ""
    if desc:
        lines = [l.strip() for l in desc.split("\n") if l.strip()]
        for i, l in enumerate(lines):
            if "simple words" in l.lower() and i + 1 < len(lines):
                short = lines[i + 1][:300]
                break
        if not short and lines:
            short = lines[-1][:300]
        if short and not short.endswith((".", "…")):
            short += "…"

    desc_html = f'<div class="ipc-desc">{short}</div>' if short else ""
    st.markdown(f"""
    <div class="ipc-card">
        <div class="ipc-section-num">⚖️ {section}</div>
        <div class="ipc-offense">{offense}</div>
        <span class="ipc-punish">🔒 {punish}</span>
        {desc_html}
    </div>
    """, unsafe_allow_html=True)


# ── System prompt ─────────────────────────────────────────────────────────────

LEGAL_SYSTEM = """You are LexIPC, an expert Indian criminal law research assistant.
You specialise in: Indian Penal Code (IPC), Code of Criminal Procedure (CrPC), Indian Evidence Act,
Bharatiya Nyaya Sanhita 2023 (BNS), and related Indian criminal legislation.

IMPORTANT SCOPE RULE:
- You only answer questions about CRIMINAL law (IPC, CrPC, BNS, criminal procedure, bail, arrest, trial).
- If asked about civil law (eviction, title suits, property disputes, rent, divorce, contract), 
  politely clarify this is outside your scope and suggest they consult the relevant act 
  (Transfer of Property Act, CPC, Rent Control Acts, etc.).

Response format:
1. Identify the relevant IPC/BNS sections with exact numbers
2. State punishment (imprisonment, fine, bailable/non-bailable, cognisable/non-cognisable)
3. Key elements that must be proven
4. Landmark case laws (Supreme Court / High Court)
5. BNS 2023 equivalent if applicable
6. ⚠️ Always end with: "This is legal information, not legal advice. Consult a qualified advocate."

Use **bold** for section numbers. Keep answers focused and accurate."""


# ── Session state ─────────────────────────────────────────────────────────────
if "chat_history"  not in st.session_state: st.session_state.chat_history  = []
if "prefill_query" not in st.session_state: st.session_state.prefill_query = ""


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:4px 0 14px">
        <div style="font-family:'Crimson Pro',serif;font-size:1.7rem;color:#e8c84a;font-weight:700;letter-spacing:-0.01em">
            ⚖️ LexIPC
        </div>
        <div style="font-size:0.78rem;color:#6a6a8a;margin-top:2px">Indian Criminal Law Research</div>
    </div>
    """, unsafe_allow_html=True)

    # API status
    has_key = bool(get_api_key())
    if has_key:
        st.markdown("🟢 **Gemini AI Connected**")
    else:
        st.markdown("🔴 **API Key Required**")
        with st.expander("Setup instructions"):
            st.markdown("""
**Streamlit Cloud:**
1. App → Settings → Secrets
2. Add:
```
GEMINI_API_KEY = "AIza..."
```
**Get free key:**  
[aistudio.google.com](https://aistudio.google.com/app/apikey)
""")

    st.divider()

    # Dataset stats
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
        "sec_num",
        placeholder="Type section number e.g. 302, 376, 420…",
        key="quick_lookup",
        label_visibility="collapsed"
    )
    if quick.strip() and not ipc_df.empty:
        num = quick.strip().upper().lstrip("IPC_ ")
        mask = ipc_df["section"].fillna("").str.upper().str.contains(num, regex=False)
        found = ipc_df[mask]
        if not found.empty:
            r = found.iloc[0]
            st.markdown(f"""
<div style="background:#252540;padding:12px 14px;border-left:3px solid #e8c84a;
            border-radius:6px;margin:6px 0;font-size:0.82rem">
    <b style="color:#e8c84a">{r.get('section','')}</b><br>
    <span style="color:#a09888;font-style:italic">{str(r.get('offense',''))[:75]}…</span><br>
    <code style="color:#f08080">{r.get('punishment','')}</code>
</div>""", unsafe_allow_html=True)
        else:
            st.caption(f"Section '{quick}' not found")

    st.divider()

    # Common queries — explicit labels with proper button keys
    st.markdown("**Common Queries**")
    QUERIES = [
        ("Murder — IPC 302",            "What is IPC Section 302? Explain elements of murder, punishment, and key case laws like K.M. Nanavati v State."),
        ("Rape — IPC 376",              "Explain IPC Section 376 on rape. What are the elements, punishment, amendments after Nirbhaya case?"),
        ("Theft, Robbery & Dacoity",    "What is the difference between theft (IPC 378), robbery (IPC 390) and dacoity (IPC 391)? What are punishments?"),
        ("Bail for non-bailable cases", "How to get bail in non-bailable offences? What is Section 437 and 439 CrPC? When can bail be denied?"),
        ("Cheating — IPC 420",          "Explain IPC Section 420 cheating. What must be proved? What is the punishment?"),
        ("Culpable homicide vs murder",  "Difference between culpable homicide (IPC 299) and murder (IPC 302)? What is the exception clause?"),
        ("Cybercrime laws India",       "Which IPC sections and IT Act provisions apply to cybercrime — hacking, online fraud, morphing?"),
        ("Rights at time of arrest",    "What are the legal rights of an arrested person under Article 22, Section 41 CrPC and D.K. Basu guidelines?"),
    ]
    for label, query_text in QUERIES:
        if st.button(f"→ {label}", key=f"q_{hash(label) % 100000}", use_container_width=True):
            st.session_state.prefill_query = query_text
            st.rerun()

    st.divider()
    st.caption("⚖️ LexIPC v2.1 · Legal info only · Not legal advice")


# ── Main ──────────────────────────────────────────────────────────────────────

# ── Header (pure HTML — no stray </div> possible) ──
ipc_badge = (
    f'<span style="display:inline-block;padding:5px 14px;border-radius:20px;font-size:0.75rem;'
    f'font-family:IBM Plex Mono,monospace;background:rgba(232,200,74,0.15);'
    f'color:#e8c84a;border:1px solid rgba(232,200,74,0.4);margin:4px 4px 0 0">'
    f'📚 IPC Database ({len(ipc_df)} sections)</span>'
    if not ipc_df.empty else
    '<span style="display:inline-block;padding:5px 14px;border-radius:20px;font-size:0.75rem;'
    'font-family:IBM Plex Mono,monospace;background:rgba(240,80,80,0.15);'
    'color:#f05050;border:1px solid rgba(240,80,80,0.4);margin:4px 4px 0 0">'
    '⚠ IPC CSV Missing</span>'
)
gemini_badge = (
    '<span style="display:inline-block;padding:5px 14px;border-radius:20px;font-size:0.75rem;'
    'font-family:IBM Plex Mono,monospace;background:rgba(82,196,130,0.15);'
    'color:#52c482;border:1px solid rgba(82,196,130,0.4);margin:4px 4px 0 0">'
    '● Gemini AI (Free)</span>'
    if has_key else
    '<span style="display:inline-block;padding:5px 14px;border-radius:20px;font-size:0.75rem;'
    'font-family:IBM Plex Mono,monospace;background:rgba(240,80,80,0.15);'
    'color:#f05050;border:1px solid rgba(240,80,80,0.4);margin:4px 4px 0 0">'
    '✗ API Key Required</span>'
)
ncrb_badge = (
    '<span style="display:inline-block;padding:5px 14px;border-radius:20px;font-size:0.75rem;'
    'font-family:IBM Plex Mono,monospace;background:rgba(100,160,240,0.15);'
    'color:#64a0f0;border:1px solid rgba(100,160,240,0.4);margin:4px 4px 0 0">'
    '📊 NCRB 2023</span>'
    if not ncrb_df.empty else ""
)

st.markdown(f"""
<div style="background:linear-gradient(135deg,#1a1a2e 0%,#16213e 50%,#0f3460 100%);
            border-radius:12px;padding:32px 36px;margin-bottom:24px;
            border:1px solid #2d2d4a">
    <div style="font-family:'Crimson Pro',serif;font-size:2.4rem;
                color:#e8c84a;margin:0 0 6px;letter-spacing:-0.01em;font-weight:700">
        ⚖️ Indian Criminal Law Research Assistant
    </div>
    <div style="color:#7a7a9a;font-size:0.88rem;margin-bottom:14px">
        Powered by Google Gemini AI · IPC Sections Database · NCRB Crime Statistics 2023
    </div>
    <div>{gemini_badge}{ipc_badge}{ncrb_badge}</div>
</div>
""", unsafe_allow_html=True)

# ── Tabs ──
tab_ai, tab_ipc, tab_stats, tab_chat = st.tabs([
    "🔬 AI Research", "📚 IPC Sections", "📊 Crime Statistics", "💬 Legal Chat"
])


# ════════════════════════════════════════
# TAB 1 — AI RESEARCH
# ════════════════════════════════════════
with tab_ai:
    st.markdown("### Ask a Legal Question")
    st.caption("Gemini AI answers with IPC section references. Scope: Indian criminal law only.")

    prefill_val = st.session_state.prefill_query
    st.session_state.prefill_query = ""

    query = st.text_area(
        "Legal query",
        value=prefill_val,
        height=130,
        placeholder=(
            "Examples:\n"
            "• What is punishment for murder under IPC?\n"
            "• Explain bail conditions for rape accused\n"
            "• What sections apply to cybercrime and online fraud?"
        ),
        key="research_query",
        label_visibility="collapsed"
    )

    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        analyse_btn = st.button("⚖️ Analyse Query", type="primary", use_container_width=True)
    with c2:
        auto_ipc = st.toggle("Auto-match IPC sections", value=True)
    with c3:
        detailed = st.toggle("Detailed analysis", value=False)

    if analyse_btn:
        if not query.strip():
            st.warning("Please enter a legal query.")
        else:
            # Check if query is criminal law
            is_criminal = is_criminal_query(query)

            # Search IPC sections
            matched_df = pd.DataFrame()
            if auto_ipc and not ipc_df.empty and is_criminal:
                matched_df = search_ipc(query, ipc_df, top_n=6)

            # Build Gemini prompt
            ipc_ctx = ""
            if not matched_df.empty:
                parts = [
                    f"{r.get('section','')}: {r.get('offense','')} | Punishment: {r.get('punishment','')}"
                    for _, r in matched_df.iterrows()
                ]
                ipc_ctx = "\n\n[Relevant IPC sections from database:\n" + "\n".join(parts) + "]"

            detail_note = (
                " Provide comprehensive analysis with case laws, procedural details, and sub-sections."
                if detailed else " Keep response focused and concise (under 500 words)."
            )

            full_prompt = query + ipc_ctx + detail_note

            with st.spinner("Analysing legal provisions…"):
                answer = call_gemini(full_prompt, system=LEGAL_SYSTEM)

            st.markdown(f'<div class="ai-box">{answer}</div>', unsafe_allow_html=True)

            if not matched_df.empty:
                st.markdown(f"---\n**📚 {len(matched_df)} Matching IPC Sections:**")
                for _, row in matched_df.iterrows():
                    render_ipc_card(row)
            elif auto_ipc and not is_criminal:
                st.info(
                    "ℹ️ No IPC sections matched — this appears to be a civil/property law query. "
                    "LexIPC specialises in criminal law (IPC/CrPC/BNS)."
                )

            # Save to chat history
            st.session_state.chat_history.extend([
                {"role": "user",      "content": query},
                {"role": "assistant", "content": answer},
            ])


# ════════════════════════════════════════
# TAB 2 — IPC SECTIONS BROWSER
# ════════════════════════════════════════
with tab_ipc:
    st.markdown("### IPC Sections Database")

    if ipc_df.empty:
        st.error("⚠️ `ipc_sections.csv` not found. Place it in the same folder as `app.py`.")
    else:
        s1, s2, s3 = st.columns([4, 1, 1])
        with s1:
            sec_q = st.text_input(
                "Search",
                placeholder="Search by keyword or section number (e.g. murder, 302, theft, rape)…",
                key="ipc_search",
                label_visibility="collapsed"
            )
        with s2:
            show_n = st.selectbox("Show", [10, 25, 50, 100], index=0, label_visibility="collapsed")
        with s3:
            view = st.radio("View", ["Cards", "Table"], horizontal=False, label_visibility="collapsed")

        punish_q = st.text_input(
            "Punishment filter",
            placeholder="Filter by punishment type (e.g. death, life, fine)…",
            key="punish_f",
            label_visibility="collapsed"
        )

        if sec_q.strip():
            results = search_ipc(sec_q, ipc_df, top_n=show_n)
            if results.empty:
                # Fallback: simple contains search
                mask = pd.Series(False, index=ipc_df.index)
                for col in [c for c in ["offense", "section", "description"] if c in ipc_df.columns]:
                    mask |= ipc_df[col].fillna("").str.lower().str.contains(sec_q.lower(), regex=False)
                results = ipc_df[mask].head(show_n)
        else:
            results = ipc_df.head(show_n)

        if punish_q.strip() and "punishment" in results.columns:
            results = results[
                results["punishment"].fillna("").str.lower().str.contains(punish_q.lower(), regex=False)
            ]

        st.caption(f"Showing **{len(results)}** sections")

        if view == "Cards":
            for _, row in results.iterrows():
                render_ipc_card(row)
        else:
            disp = [c for c in ["section", "offense", "punishment"] if c in results.columns]
            st.dataframe(results[disp], use_container_width=True, height=500, hide_index=True)

        # Full detail view
        if not results.empty and "section" in results.columns:
            st.divider()
            chosen = st.selectbox("View full text for:", results["section"].tolist(), key="detail_sel")
            if chosen:
                row = results[results["section"] == chosen].iloc[0]
                with st.expander(f"📄 {chosen} — Full Description", expanded=True):
                    st.markdown(f"**Offense:** {row.get('offense','—')}")
                    st.markdown(f"**Punishment:** `{row.get('punishment','—')}`")
                    st.divider()
                    st.markdown(str(row.get("description", "No description available.")))

                    if st.button(f"🤖 AI Analysis of {chosen}", key=f"ai_{chosen}"):
                        p = (
                            f"Provide a detailed legal analysis of {chosen} IPC. "
                            f"Offense: {row.get('offense','')}. Punishment: {row.get('punishment','')}. "
                            "Include: all elements, landmark Supreme Court cases, bailable/non-bailable, "
                            "cognisable/non-cognisable, CrPC procedure, and BNS 2023 equivalent."
                        )
                        with st.spinner("Analysing…"):
                            r_text = call_gemini(p, system=LEGAL_SYSTEM)
                        st.markdown(f'<div class="ai-box">{r_text}</div>', unsafe_allow_html=True)


# ════════════════════════════════════════
# TAB 3 — NCRB STATISTICS
# ════════════════════════════════════════
with tab_stats:
    st.markdown("### Crime Statistics — NCRB 2023")
    if ncrb_df.empty:
        st.info("Place `NCRB_CII_2023_Table_18A_2_0.csv` in the app folder to enable charts.")
        st.markdown("""
**Once loaded, this tab shows:**
- Crime incidence by State/UT  
- Category-wise distribution  
- Interactive charts with filters  
- CSV export
        """)
    else:
        st.caption(f"Source: NCRB Crime in India 2023 · {len(ncrb_df):,} records")
        try:
            import plotly.express as px
            with st.expander("📋 Data columns & preview"):
                st.write("Columns:", list(ncrb_df.columns))
                st.dataframe(ncrb_df.head(8), use_container_width=True)

            num_cols = ncrb_df.select_dtypes(include="number").columns.tolist()
            cat_cols = ncrb_df.select_dtypes(include="object").columns.tolist()

            if num_cols and cat_cols:
                r1, r2, r3 = st.columns(3)
                x_col   = r1.selectbox("Category", cat_cols, key="nx")
                y_col   = r2.selectbox("Metric",   num_cols, key="ny")
                top_n   = r3.slider("Top N", 5, 30, 15, key="nn")
                ctype   = st.radio("Chart", ["Bar","Horizontal Bar","Pie","Treemap"], horizontal=True)

                cdf = (ncrb_df.groupby(x_col)[y_col].sum().reset_index()
                       .sort_values(y_col, ascending=False).head(top_n))
                cs  = [[0,"#1a1a2e"],[0.5,"#8b6914"],[1,"#e8c84a"]]

                if ctype == "Bar":
                    fig = px.bar(cdf, x=x_col, y=y_col, color=y_col, color_continuous_scale=cs)
                    fig.update_xaxes(tickangle=-45)
                elif ctype == "Horizontal Bar":
                    fig = px.bar(cdf.sort_values(y_col), x=y_col, y=x_col,
                                 orientation="h", color=y_col, color_continuous_scale=cs)
                elif ctype == "Pie":
                    fig = px.pie(cdf, names=x_col, values=y_col, hole=0.4,
                                 color_discrete_sequence=px.colors.sequential.YlOrBr_r)
                else:
                    fig = px.treemap(cdf, path=[x_col], values=y_col,
                                     color=y_col, color_continuous_scale=cs)

                fig.update_layout(
                    paper_bgcolor="white", plot_bgcolor="white",
                    font=dict(family="IBM Plex Sans", color="#1a1a2e"),
                    coloraxis_showscale=False, margin=dict(t=50,l=20,r=20,b=60),
                )
                st.plotly_chart(fig, use_container_width=True)
                st.download_button("📥 Download CSV", cdf.to_csv(index=False),
                                   "ncrb_data.csv", "text/csv")
        except ImportError:
            st.dataframe(ncrb_df, use_container_width=True)


# ════════════════════════════════════════
# TAB 4 — LEGAL CHAT
# ════════════════════════════════════════
with tab_chat:
    st.markdown("### Legal Research Chat")
    st.caption("Full conversation history maintained during your session.")

    # Render history
    if not st.session_state.chat_history:
        st.markdown("""
<div style="text-align:center;padding:56px 24px;color:#9090a8">
    <div style="font-size:3rem">⚖️</div>
    <p style="margin-top:10px;font-size:1rem;color:#6a6a8a">Start a legal research conversation</p>
    <p style="font-size:0.85rem">Ask about IPC sections, bail, criminal procedure, case laws…</p>
</div>""", unsafe_allow_html=True)
    else:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown('<div class="chat-you-label">YOU</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="chat-user">{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="chat-bot-label">⚖ LEXIPC</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="chat-assistant">{msg["content"]}</div>', unsafe_allow_html=True)

    st.divider()
    chat_q = st.text_area(
        "chat_input",
        height=100,
        placeholder="Ask about any IPC section, offence, bail procedure, rights, case law…",
        key="chat_inp",
        label_visibility="collapsed"
    )

    b1, b2 = st.columns([1, 5])
    send  = b1.button("Send →", type="primary", key="send_chat", use_container_width=True)
    clear = b1.button("🗑 Clear",               key="clear_chat", use_container_width=True)

    if send and chat_q.strip():
        # IPC context
        ctx = ""
        if not ipc_df.empty:
            m = search_ipc(chat_q, ipc_df, top_n=3)
            if not m.empty:
                ctx = " [Relevant sections: " + "; ".join(
                    f"{r.get('section','')}: {str(r.get('offense',''))[:50]}"
                    for _, r in m.iterrows()
                ) + "]"

        st.session_state.chat_history.append({"role": "user", "content": chat_q.strip()})

        # Build history for multi-turn
        history_for_api = [
            {"role": "model" if m["role"] == "assistant" else "user", "content": m["content"]}
            for m in st.session_state.chat_history[:-1]
        ]

        with st.spinner("Researching…"):
            reply = call_gemini(chat_q.strip() + ctx, history=history_for_api, system=LEGAL_SYSTEM)

        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.rerun()

    if clear:
        st.session_state.chat_history = []
        st.rerun()


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:20px;color:#9090a8;font-size:0.76rem;
            font-family:'IBM Plex Mono',monospace;border-top:1px solid #e0ddd5;margin-top:28px">
    ⚖️ LexIPC · Indian Criminal Law Research · For informational purposes only · Not legal advice
</div>
""", unsafe_allow_html=True)
