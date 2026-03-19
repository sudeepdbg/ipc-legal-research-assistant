"""
⚖️IPC Law Research Assistant
Single-file Streamlit app. Uses Groq API (free tier) for LLM responses.
No backend server needed – everything runs in the cloud.
"""

import streamlit as st
import pandas as pd
import re
import requests
from pathlib import Path

# ── Page configuration ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="LexIPC · Indian Criminal Law",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS – professional, clean, legal‑themed ────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,400;0,14..32,500;0,14..32,600;0,14..32,700;1,14..32,400&family=Merriweather:ital,wght@0,400;0,700;1,400&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #f9f7f4; color: #1e293b; }

/* ── Sidebar – dark, authoritative ── */
[data-testid="stSidebar"] {
    background: #0f172a !important;
    border-right: 1px solid #334155;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div { color: #cbd5e1; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #fbbf24 !important;
    font-family: 'Merriweather', serif !important;
}
[data-testid="stSidebar"] .stButton > button {
    background: #1e293b !important;
    color: #fbbf24 !important;
    border: 1px solid #334155 !important;
    border-radius: 6px !important;
    text-align: left !important;
    padding: 8px 12px !important;
    font-size: 0.85rem !important;
    width: 100% !important;
    transition: 0.1s ease;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: #2d3a4f !important;
    border-color: #fbbf24 !important;
}
[data-testid="stSidebar"] input {
    background: #1e293b !important;
    border: 1px solid #334155 !important;
    color: #e2e8f0 !important;
    border-radius: 6px !important;
}
[data-testid="stSidebar"] label { color: #94a3b8 !important; font-size: 0.8rem; }

/* ── Main area cards ── */
.ipc-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-left: 6px solid #fbbf24;
    border-radius: 8px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 4px 12px rgba(0,0,0,0.02);
}
.ipc-section-num {
    font-family: 'Merriweather', serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: #0f172a;
}
.ipc-offense {
    font-size: 0.9rem;
    color: #475569;
    font-style: italic;
    margin: 0.3rem 0 0.8rem;
}
.ipc-punish {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    background: #fee2e2;
    color: #b91c1c;
    padding: 0.2rem 0.8rem;
    border-radius: 4px;
    display: inline-block;
    border: 1px solid #fecaca;
}
.ipc-desc {
    font-size: 0.9rem;
    color: #334155;
    margin-top: 1rem;
    line-height: 1.6;
}

/* ── AI answer box ── */
.ai-box {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-top: 5px solid #fbbf24;
    border-radius: 8px;
    padding: 1.8rem 2rem;
    margin: 1.5rem 0;
    line-height: 1.8;
    color: #1e293b;
}

/* ── Chat bubbles ── */
.chat-user {
    background: #1e293b;
    color: #f8fafc;
    border-radius: 12px 12px 4px 12px;
    padding: 0.9rem 1.2rem;
    margin-left: 40px;
    font-size: 0.95rem;
    line-height: 1.6;
}
.chat-assistant {
    background: white;
    border: 1px solid #e2e8f0;
    border-left: 4px solid #fbbf24;
    border-radius: 4px 12px 12px 12px;
    padding: 0.9rem 1.2rem;
    margin-right: 40px;
    font-size: 0.95rem;
    line-height: 1.7;
    color: #1e293b;
}
.chat-label {
    font-size: 0.7rem;
    color: #64748b;
    margin: 0.8rem 0 0.2rem;
    font-family: 'JetBrains Mono', monospace;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: white;
    border-radius: 8px 8px 0 0;
    border: 1px solid #e2e8f0;
    border-bottom: none;
    padding: 0.5rem 0.5rem 0;
    gap: 0.2rem;
}
.stTabs [data-baseweb="tab"] {
    color: #64748b;
    font-weight: 500;
    font-size: 0.9rem;
    padding: 0.6rem 1.2rem;
    border-radius: 6px 6px 0 0;
}
.stTabs [aria-selected="true"] {
    color: #0f172a !important;
    border-bottom: 3px solid #fbbf24 !important;
    background: rgba(251,191,36,0.05);
}
.stTabs [data-baseweb="tab-panel"] {
    background: white;
    border: 1px solid #e2e8f0;
    border-top: none;
    border-radius: 0 0 8px 8px;
    padding: 2rem;
}

/* ── Metrics ── */
[data-testid="stMetricValue"] {
    color: #fbbf24 !important;
    font-family: 'Merriweather', serif;
    font-size: 2rem !important;
}
[data-testid="stMetricLabel"] { color: #64748b !important; font-size: 0.8rem; }

hr { border-color: #e2e8f0; }
</style>
""", unsafe_allow_html=True)


# ── Groq API integration ──────────────────────────────────────────────────────

def get_api_key() -> str:
    """Return Groq API key from Streamlit secrets or environment."""
    try:
        return st.secrets["GROQ_API_KEY"]
    except Exception:
        import os
        return os.environ.get("GROQ_API_KEY", "")

def call_ai(prompt: str, history: list = None, system: str = "") -> str:
    """Call Groq's Mixtral model (free, stable) with the given prompt and conversation history."""
    api_key = get_api_key()
    if not api_key:
        return "⚠️ **GROQ_API_KEY not configured.**\n\nGet a free key at [console.groq.com](https://console.groq.com) and add it to Streamlit Secrets."

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    if history:
        for m in history[-12:]:
            role = "assistant" if m["role"] == "assistant" else "user"
            messages.append({"role": role, "content": m["content"][:2000]})
    messages.append({"role": "user", "content": prompt})

    # Use Mixtral – widely available, fast, and free on Groq
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": messages,
        "max_tokens": 1500,
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    try:
        resp = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60,
        )
        if resp.status_code == 200:
            return resp.json()["choices"][0]["message"]["content"]
        elif resp.status_code == 401:
            return "🔐 Invalid API key. Please check your GROQ_API_KEY."
        elif resp.status_code == 429:
            return "⏳ Rate limit reached. Please wait a moment and try again."
        else:
            return f"❌ API error ({resp.status_code}): {resp.text[:200]}"
    except requests.exceptions.Timeout:
        return "⏱️ Request timed out. Please try again."
    except requests.exceptions.ConnectionError:
        return "🌐 Network error. Check your internet connection."
    except Exception as e:
        return f"⚠️ Unexpected error: {str(e)}"


# ── Data loading ──────────────────────────────────────────────────────────────

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


# ── IPC search logic ──────────────────────────────────────────────────────────

CRIMINAL_KEYWORDS = {
    "murder", "homicide", "manslaughter", "kidnapping", "abduction", "robbery",
    "dacoity", "theft", "extortion", "cheating", "fraud", "forgery", "rape",
    "assault", "hurt", "grievous", "obscene", "defamation", "sedition", "riot",
    "affray", "bribery", "corruption", "trespass", "mischief", "arson",
    "poisoning", "dowry", "cruelty", "stalking", "voyeurism", "acid", "terrorist",
    "waging", "counterfeit", "coinage", "arms", "weapon", "culpable", "abetment",
    "conspiracy", "attempt", "bail", "arrest", "custody", "remand", "cognisable",
    "non-cognisable", "warrant", "summons", "trial", "conviction", "sentence",
    "punishment", "fine", "imprisonment", "life", "death", "sections", "ipc",
    "crpc", "bns", "criminal", "offence", "offense", "penal", "code", "law",
    "legal", "court", "accused", "victim", "complaint", "fir", "chargesheet",
    "evidence",
}

def is_criminal_query(query: str) -> bool:
    q_lower = query.lower()
    if re.search(r'\b(ipc|section|sec\.?)\s*\d+', q_lower):
        return True
    words = set(re.findall(r'\b\w+\b', q_lower))
    return bool(words & CRIMINAL_KEYWORDS)

def search_ipc(query: str, df: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
    if df.empty or not query.strip():
        return pd.DataFrame()

    q_lower = query.lower()
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

    sec_match = re.search(r'\b(\d{2,3}[A-Z]?)\b', query.upper())
    if sec_match and "section" in df.columns:
        mask = df["section"].fillna("").str.upper().str.contains(sec_match.group(1), regex=False)
        scores[mask] += 20

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


# ── System prompt – criminal law only ─────────────────────────────────────────

LEGAL_SYSTEM = """You are LexIPC, an expert Indian criminal law assistant. Your domain is strictly the Indian Penal Code (IPC), Code of Criminal Procedure (CrPC), Bharatiya Nyaya Sanhita (BNS), and related criminal statutes.  
You do **not** answer civil law questions (property, family, contracts, etc.). If the user asks a civil law question, politely explain that you only handle criminal law.  

Format your answers with:
- Relevant IPC sections in **bold**
- Punishment, bailable/cognisable status
- Essential ingredients of the offence
- Landmark Supreme Court cases
- BNS 2023 equivalent if applicable

End with: ⚠️ Legal information only, not legal advice."""


# ── Session state ─────────────────────────────────────────────────────────────
if "chat_history"  not in st.session_state: st.session_state.chat_history  = []
if "prefill_query" not in st.session_state: st.session_state.prefill_query = ""


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 0 0 1rem;">
        <div style="font-family: 'Merriweather', serif; font-size: 2rem; color: #fbbf24; font-weight: 700;">
            ⚖️ LexIPC
        </div>
        <div style="color: #94a3b8; font-size: 0.8rem; margin-top: -0.2rem;">Indian Criminal Law Expert</div>
    </div>
    """, unsafe_allow_html=True)

    has_key = bool(get_api_key())
    if has_key:
        st.markdown("🟢 **Groq AI Connected (Mixtral)**")
    else:
        st.markdown("🔴 **API Key Required**")
        with st.expander("Setup instructions"):
            st.markdown("""
**Streamlit Cloud:**  
1. Go to App → Settings → Secrets  
2. Add:  
**Get a free key:** [console.groq.com](https://console.groq.com)
""")

    st.divider()

    st.markdown("**Dataset**")
    c1, c2 = st.columns(2)
    c1.metric("IPC Sections", len(ipc_df) if not ipc_df.empty else "—")
    c2.metric("NCRB Records", len(ncrb_df) if not ncrb_df.empty else "—")
    if ipc_df.empty:
        st.warning("Place `ipc_sections.csv` in the app folder.")

    st.divider()

    st.markdown("**Quick Section Lookup**")
    quick = st.text_input("sec_num", placeholder="e.g. 302, 376, 420", label_visibility="collapsed")
    if quick.strip() and not ipc_df.empty:
        num = quick.strip().upper().lstrip("IPC_ ")
        mask = ipc_df["section"].fillna("").str.upper().str.contains(num, regex=False)
        found = ipc_df[mask]
        if not found.empty:
            r = found.iloc[0]
            st.markdown(f"""
<div style="background:#1e293b; padding:0.8rem 1rem; border-left:3px solid #fbbf24; border-radius:6px;">
    <b style="color:#fbbf24">{r.get('section','')}</b><br>
    <span style="color:#94a3b8;">{str(r.get('offense',''))[:75]}…</span><br>
    <code style="color:#f87171;">{r.get('punishment','')}</code>
</div>
""", unsafe_allow_html=True)
        else:
            st.caption(f"Section '{quick}' not found")

    st.divider()
    st.markdown("**Common Criminal Law Queries**")
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
        if st.button(f"→ {label}", key=f"q_{hash(label)}", use_container_width=True):
            st.session_state.prefill_query = query_text
            st.rerun()

    st.divider()
    st.caption("⚖️ LexIPC v3.1 · Criminal law only · Not legal advice")
    st.caption("💡 Powered by Groq AI (Mixtral)")


# ── Main header ───────────────────────────────────────────────────────────────

ipc_badge = (
    f'<span style="display:inline-block; padding:0.3rem 0.9rem; border-radius:20px; font-size:0.75rem; background:rgba(251,191,36,0.12); color:#fbbf24; border:1px solid rgba(251,191,36,0.3);">📚 IPC ({len(ipc_df)})</span>'
    if not ipc_df.empty else
    '<span style="display:inline-block; padding:0.3rem 0.9rem; border-radius:20px; font-size:0.75rem; background:rgba(239,68,68,0.1); color:#ef4444; border:1px solid rgba(239,68,68,0.3);">⚠ IPC CSV Missing</span>'
)
ai_badge = (
    '<span style="display:inline-block; padding:0.3rem 0.9rem; border-radius:20px; font-size:0.75rem; background:rgba(34,197,94,0.12); color:#22c55e; border:1px solid rgba(34,197,94,0.3);">● Groq AI (Mixtral)</span>'
    if has_key else
    '<span style="display:inline-block; padding:0.3rem 0.9rem; border-radius:20px; font-size:0.75rem; background:rgba(239,68,68,0.1); color:#ef4444; border:1px solid rgba(239,68,68,0.3);">✗ API Key Missing</span>'
)
ncrb_badge = (
    '<span style="display:inline-block; padding:0.3rem 0.9rem; border-radius:20px; font-size:0.75rem; background:rgba(59,130,246,0.12); color:#3b82f6; border:1px solid rgba(59,130,246,0.3);">📊 NCRB 2023</span>'
    if not ncrb_df.empty else ""
)

st.markdown(f"""
<div style="background:linear-gradient(145deg, #0f172a 0%, #1e293b 100%); border-radius:12px; padding:2.5rem 3rem; margin-bottom:2rem;">
    <div style="font-family:'Merriweather',serif; font-size:2.5rem; color:#fbbf24; font-weight:700; line-height:1.2;">
        ⚖️ Indian Criminal Law Research Assistant
    </div>
    <div style="color:#94a3b8; font-size:0.9rem; margin:0.5rem 0 1rem;">
        IPC sections · NCRB statistics · AI‑powered analysis (criminal law only)
    </div>
    <div>{ai_badge} {ipc_badge} {ncrb_badge}</div>
</div>
""", unsafe_allow_html=True)


# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_ai, tab_ipc, tab_stats, tab_chat = st.tabs([
    "🔬 AI Research", "📚 IPC Sections", "📊 Crime Statistics", "💬 Legal Chat"
])


# ════════════════════════════════════════
# TAB 1 — AI RESEARCH
# ════════════════════════════════════════
with tab_ai:
    st.markdown("### Ask a Criminal Law Question")
    st.caption("Mixtral AI answers with IPC section references. Scope: **Indian criminal law only**.")

    prefill = st.session_state.prefill_query
    st.session_state.prefill_query = ""

    query = st.text_area(
        "Legal query",
        value=prefill,
        height=120,
        placeholder="Examples:\n• What is punishment for murder under IPC?\n• Explain bail conditions for rape accused",
        key="research_query",
        label_visibility="collapsed"
    )

    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        analyse = st.button("⚖️ Analyse Query", type="primary", use_container_width=True)
    with c2:
        auto_ipc = st.toggle("Auto-match IPC", value=True)
    with c3:
        detailed = st.toggle("Detailed analysis", value=False)

    if analyse:
        if not query.strip():
            st.warning("Please enter a legal query.")
        else:
            is_criminal = is_criminal_query(query)
            matched_df = pd.DataFrame()
            if auto_ipc and not ipc_df.empty and is_criminal:
                matched_df = search_ipc(query, ipc_df, top_n=6)

            ipc_ctx = ""
            if not matched_df.empty:
                parts = [f"{r['section']}: {r['offense']} | Punishment: {r['punishment']}" for _, r in matched_df.iterrows()]
                ipc_ctx = "\n\n[Relevant IPC sections:\n" + "\n".join(parts) + "]"

            detail_note = " Provide comprehensive analysis with case laws, procedural details, and sub‑sections." if detailed else " Keep response concise (under 500 words)."
            full_prompt = query + ipc_ctx + detail_note

            with st.spinner("Analysing legal provisions…"):
                answer = call_ai(full_prompt, system=LEGAL_SYSTEM)

            st.markdown(f'<div class="ai-box">{answer}</div>', unsafe_allow_html=True)

            if not matched_df.empty:
                st.markdown(f"---\n**📚 {len(matched_df)} Matching IPC Sections:**")
                for _, row in matched_df.iterrows():
                    render_ipc_card(row)
            elif auto_ipc and not is_criminal:
                st.info("ℹ️ No IPC sections matched – this appears to be a civil/property law query. LexIPC specialises in criminal law.")

            st.session_state.chat_history.extend([
                {"role": "user", "content": query},
                {"role": "assistant", "content": answer},
            ])


# ════════════════════════════════════════
# TAB 2 — IPC SECTIONS BROWSER
# ════════════════════════════════════════
with tab_ipc:
    if ipc_df.empty:
        st.error("⚠️ `ipc_sections.csv` not found. Please upload it.")
    else:
        st.markdown("### IPC Sections Database")
        s1, s2, s3 = st.columns([4, 1, 1])
        with s1:
            sec_q = st.text_input("Search", placeholder="Keyword or section number…", key="ipc_search", label_visibility="collapsed")
        with s2:
            show_n = st.selectbox("Show", [10, 25, 50, 100], index=0, label_visibility="collapsed")
        with s3:
            view = st.radio("View", ["Cards", "Table"], horizontal=True, label_visibility="collapsed")

        if sec_q:
            results = search_ipc(sec_q, ipc_df, top_n=show_n)
            if results.empty:
                # fallback to simple contains
                mask = pd.Series(False, index=ipc_df.index)
                for col in ["offense", "section", "description"]:
                    if col in ipc_df:
                        mask |= ipc_df[col].fillna("").str.lower().str.contains(sec_q.lower(), regex=False)
                results = ipc_df[mask].head(show_n)
        else:
            results = ipc_df.head(show_n)

        st.caption(f"Showing **{len(results)}** sections")

        if view == "Cards":
            for _, row in results.iterrows():
                render_ipc_card(row)
        else:
            cols = [c for c in ["section", "offense", "punishment"] if c in results.columns]
            st.dataframe(results[cols], use_container_width=True, height=500, hide_index=True)

        # Full detail view
        if not results.empty and "section" in results.columns:
            st.divider()
            chosen = st.selectbox("View full description for:", results["section"].tolist(), key="detail_sel")
            if chosen:
                row = results[results["section"] == chosen].iloc[0]
                with st.expander(f"📄 {chosen} — Full Text", expanded=True):
                    st.markdown(f"**Offense:** {row.get('offense','—')}")
                    st.markdown(f"**Punishment:** `{row.get('punishment','—')}`")
                    st.divider()
                    st.markdown(str(row.get("description", "No description available.")))
                    if st.button(f"🤖 AI Analysis of {chosen}", key=f"ai_{chosen}"):
                        p = f"Provide a detailed legal analysis of {chosen} IPC. Offense: {row.get('offense','')}. Punishment: {row.get('punishment','')}. Include all elements, landmark cases, bailable/cognisable, CrPC procedure, and BNS 2023 equivalent."
                        with st.spinner("Analysing…"):
                            r_text = call_ai(p, system=LEGAL_SYSTEM)
                        st.markdown(f'<div class="ai-box">{r_text}</div>', unsafe_allow_html=True)


# ════════════════════════════════════════
# TAB 3 — NCRB STATISTICS
# ════════════════════════════════════════
with tab_stats:
    st.markdown("### Crime Statistics — NCRB 2023")
    if ncrb_df.empty:
        st.info("Place `NCRB_CII_2023_Table_18A_2_0.csv` in the app folder to enable charts.")
        st.markdown("**Once loaded, this tab shows:** crime incidence by State/UT, interactive charts, and export.")
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
                x_col = r1.selectbox("Category", cat_cols, key="nx")
                y_col = r2.selectbox("Metric", num_cols, key="ny")
                top_n = r3.slider("Top N", 5, 30, 15, key="nn")
                ctype = st.radio("Chart", ["Bar", "Horizontal Bar", "Pie", "Treemap"], horizontal=True)

                cdf = (ncrb_df.groupby(x_col)[y_col].sum().reset_index().sort_values(y_col, ascending=False).head(top_n))
                cs = [[0, "#0f172a"], [0.5, "#b45309"], [1, "#fbbf24"]]

                if ctype == "Bar":
                    fig = px.bar(cdf, x=x_col, y=y_col, color=y_col, color_continuous_scale=cs)
                    fig.update_xaxes(tickangle=-45)
                elif ctype == "Horizontal Bar":
                    fig = px.bar(cdf.sort_values(y_col), x=y_col, y=x_col, orientation="h", color=y_col, color_continuous_scale=cs)
                elif ctype == "Pie":
                    fig = px.pie(cdf, names=x_col, values=y_col, hole=0.4, color_discrete_sequence=px.colors.sequential.YlOrBr_r)
                else:
                    fig = px.treemap(cdf, path=[x_col], values=y_col, color=y_col, color_continuous_scale=cs)

                fig.update_layout(
                    paper_bgcolor="white",
                    plot_bgcolor="white",
                    font=dict(family="Inter", color="#1e293b"),
                    coloraxis_showscale=False,
                    margin=dict(t=50, l=20, r=20, b=60),
                )
                st.plotly_chart(fig, use_container_width=True)
                st.download_button("📥 Download CSV", cdf.to_csv(index=False), "ncrb_data.csv", "text/csv")
        except ImportError:
            st.dataframe(ncrb_df, use_container_width=True)


# ════════════════════════════════════════
# TAB 4 — LEGAL CHAT
# ════════════════════════════════════════
with tab_chat:
    st.markdown("### Criminal Law Chat")
    st.caption("Full conversation history maintained during your session.")

    if not st.session_state.chat_history:
        st.markdown("""
<div style="text-align:center; padding:4rem 2rem; color:#94a3b8;">
    <div style="font-size:4rem;">⚖️</div>
    <p style="margin-top:1rem; font-size:1.1rem; color:#64748b;">Start a criminal law conversation</p>
    <p style="font-size:0.9rem;">Ask about IPC sections, bail, criminal procedure, case laws…</p>
</div>""", unsafe_allow_html=True)
    else:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown('<div class="chat-label" style="text-align:right;">YOU</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="chat-user">{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="chat-label">⚖️ LEXIPC</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="chat-assistant">{msg["content"]}</div>', unsafe_allow_html=True)

    st.divider()
    chat_q = st.text_area("chat_input", height=100, placeholder="Ask about any IPC section, offence, bail procedure…", key="chat_inp", label_visibility="collapsed")
    b1, b2 = st.columns([1, 5])
    send = b1.button("Send →", type="primary", key="send_chat", use_container_width=True)
    clear = b1.button("🗑 Clear", key="clear_chat", use_container_width=True)

    if send and chat_q.strip():
        ctx = ""
        if not ipc_df.empty:
            m = search_ipc(chat_q, ipc_df, top_n=3)
            if not m.empty:
                ctx = " [Relevant sections: " + "; ".join(f"{r['section']}: {str(r['offense'])[:50]}" for _, r in m.iterrows()) + "]"
        st.session_state.chat_history.append({"role": "user", "content": chat_q.strip()})
        history_for_api = [{"role": "model" if m["role"] == "assistant" else "user", "content": m["content"]} for m in st.session_state.chat_history[:-1]]
        with st.spinner("Researching…"):
            reply = call_ai(chat_q.strip() + ctx, history=history_for_api, system=LEGAL_SYSTEM)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.rerun()

    if clear:
        st.session_state.chat_history = []
        st.rerun()


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding:2rem; color:#94a3b8; font-size:0.75rem; border-top:1px solid #e2e8f0; margin-top:2rem;">
    ⚖️ LexIPC · Indian Criminal Law Research · For informational purposes only · Not legal advice
</div>
""", unsafe_allow_html=True)
