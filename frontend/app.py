"""
Indian Criminal Law Research Assistant
Single-file Streamlit app — no backend, no localhost dependency.
Uses Claude API directly + pandas for IPC CSV search.
"""

import streamlit as st
import pandas as pd
import requests
import json
import re
from pathlib import Path

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="IPC Legal Research Assistant",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS — dark law-library aesthetic ───────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Source+Serif+4:ital,wght@0,300;0,400;1,300&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Source Serif 4', Georgia, serif;
}

/* Dark parchment background */
.stApp {
    background: #0d0d0d;
    color: #e8dcc8;
}

/* Header */
h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
    color: #c9a84c !important;
    letter-spacing: 0.02em;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #111111 !important;
    border-right: 1px solid #2a2a2a;
}
[data-testid="stSidebar"] * { color: #c9a84c !important; }
[data-testid="stSidebar"] p, [data-testid="stSidebar"] label { color: #b0a080 !important; }

/* Input fields */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background: #1a1a1a !important;
    border: 1px solid #3a3020 !important;
    color: #e8dcc8 !important;
    border-radius: 4px;
    font-family: 'Source Serif 4', serif !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #8B6914 0%, #c9a84c 100%);
    color: #0d0d0d;
    font-family: 'Playfair Display', serif;
    font-weight: 700;
    border: none;
    border-radius: 4px;
    padding: 0.5rem 1.5rem;
    letter-spacing: 0.05em;
    transition: all 0.2s;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #c9a84c 0%, #e8c96c 100%);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(201, 168, 76, 0.3);
}

/* IPC section card */
.section-card {
    background: #161410;
    border: 1px solid #3a3020;
    border-left: 4px solid #c9a84c;
    border-radius: 4px;
    padding: 20px 24px;
    margin: 12px 0;
}
.section-number {
    font-family: 'Playfair Display', serif;
    font-size: 1.3rem;
    color: #c9a84c;
    font-weight: 700;
}
.section-offense {
    font-size: 0.95rem;
    color: #b0a080;
    font-style: italic;
    margin: 4px 0 8px;
}
.section-punishment {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    color: #e05555;
    background: #1a0a0a;
    padding: 4px 10px;
    border-radius: 3px;
    display: inline-block;
}

/* AI answer box */
.ai-answer {
    background: #121212;
    border: 1px solid #2a2a2a;
    border-top: 3px solid #c9a84c;
    border-radius: 4px;
    padding: 24px;
    margin: 16px 0;
    line-height: 1.8;
    color: #e8dcc8;
}

/* Chat message */
.chat-user {
    background: #1a1810;
    border: 1px solid #3a3020;
    border-radius: 4px;
    padding: 14px 18px;
    margin: 8px 0;
    color: #e8dcc8;
}
.chat-assistant {
    background: #111111;
    border: 1px solid #2a2a2a;
    border-radius: 4px;
    padding: 14px 18px;
    margin: 8px 0;
    color: #d0c8b0;
}

/* Dividers */
hr {
    border-color: #2a2a2a;
}

/* Expander */
.streamlit-expanderHeader {
    background: #161410 !important;
    color: #c9a84c !important;
    border: 1px solid #3a3020 !important;
}

/* Dataframe */
.stDataFrame {
    border: 1px solid #2a2a2a;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #111111;
    border-bottom: 1px solid #2a2a2a;
    gap: 0;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #7a6a4a;
    font-family: 'Playfair Display', serif;
    border-radius: 0;
    padding: 10px 24px;
    border-bottom: 2px solid transparent;
}
.stTabs [aria-selected="true"] {
    background: transparent;
    color: #c9a84c !important;
    border-bottom: 2px solid #c9a84c;
}

/* Metric */
[data-testid="stMetricValue"] { color: #c9a84c !important; }
[data-testid="stMetricLabel"] { color: #7a6a4a !important; }

/* Badge */
.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 3px;
    font-size: 0.75rem;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 500;
}
.badge-gold { background: #2a2010; color: #c9a84c; border: 1px solid #c9a84c; }
.badge-red  { background: #1a0808; color: #e05555; border: 1px solid #e05555; }
.badge-blue { background: #08101a; color: #5588cc; border: 1px solid #5588cc; }

/* Info/warning boxes */
.stInfo { background: #101820 !important; border-color: #5588cc !important; }
.stWarning { background: #18140a !important; border-color: #c9a84c !important; }
.stError { background: #180a0a !important; border-color: #e05555 !important; }
.stSuccess { background: #0a1810 !important; border-color: #55aa77 !important; }
</style>
""", unsafe_allow_html=True)


# ── Data loading ──────────────────────────────────────────────────────────────

@st.cache_data
def load_ipc_data():
    """Load IPC sections CSV — place ipc_sections.csv in same folder as app.py"""
    csv_path = Path("ipc_sections.csv")
    if not csv_path.exists():
        # Fallback: search common locations
        for p in [Path("data/ipc_sections.csv"), Path("../ipc_sections.csv")]:
            if p.exists():
                csv_path = p
                break
        else:
            return pd.DataFrame()
    df = pd.read_csv(csv_path)
    df.columns = [c.strip() for c in df.columns]
    # Normalise column names to lowercase
    df.columns = [c.lower().replace(" ", "_") for c in df.columns]
    return df

@st.cache_data
def load_ncrb_data():
    """Load NCRB crime statistics CSV"""
    for path in [Path("NCRB_CII_2023_Table_18A_2_0.csv"),
                 Path("data/NCRB_CII_2023_Table_18A_2_0.csv")]:
        if path.exists():
            df = pd.read_csv(path)
            df.columns = [c.strip() for c in df.columns]
            return df
    return pd.DataFrame()

ipc_df  = load_ipc_data()
ncrb_df = load_ncrb_data()


# ── Claude API helper ─────────────────────────────────────────────────────────

def call_claude(messages: list, system_prompt: str = "") -> str:
    """
    Call Claude API directly — no backend needed.
    API key read from st.secrets["ANTHROPIC_API_KEY"].
    """
    # Get API key from Streamlit secrets or env
    api_key = ""
    try:
        api_key = st.secrets["ANTHROPIC_API_KEY"]
    except Exception:
        import os
        api_key = os.environ.get("ANTHROPIC_API_KEY", "")

    if not api_key:
        return (
            "⚠️ **API key not configured.** "
            "Add `ANTHROPIC_API_KEY` to your Streamlit secrets "
            "(Settings → Secrets) or environment variables."
        )

    payload = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 2048,
        "messages": messages,
    }
    if system_prompt:
        payload["system"] = system_prompt

    try:
        resp = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json=payload,
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()
        return data["content"][0]["text"]
    except requests.exceptions.ConnectionError:
        return "❌ Network error: Could not reach Anthropic API. Check your internet connection."
    except requests.exceptions.Timeout:
        return "❌ Request timed out. Please try again."
    except requests.exceptions.HTTPError as e:
        if resp.status_code == 401:
            return "❌ Invalid API key. Please check your ANTHROPIC_API_KEY."
        return f"❌ API error ({resp.status_code}): {resp.text[:200]}"
    except Exception as e:
        return f"❌ Unexpected error: {str(e)}"


# ── IPC search ────────────────────────────────────────────────────────────────

def search_ipc(query: str, df: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
    """Keyword search across IPC description, offense, and section columns."""
    if df.empty:
        return df
    q_lower = query.lower()
    terms = [t.strip() for t in q_lower.split() if len(t.strip()) > 2]
    if not terms:
        return df.head(top_n)

    scores = pd.Series(0.0, index=df.index)
    text_cols = [c for c in df.columns if c in ("description", "offense", "section", "punishment")]

    for term in terms:
        for col in text_cols:
            if col in df.columns:
                col_text = df[col].fillna("").str.lower()
                weight = 3.0 if col == "offense" else (2.0 if col == "section" else 1.0)
                scores += col_text.str.contains(term, regex=False).astype(float) * weight

    # Check if query contains a section number like "302", "IPC 302"
    section_match = re.search(r'\b(\d{2,3}[A-Z]?)\b', query.upper())
    if section_match and "section" in df.columns:
        sec_num = section_match.group(1)
        mask = df["section"].fillna("").str.upper().str.contains(sec_num, regex=False)
        scores[mask] += 10  # strong boost for direct section match

    return df[scores > 0].assign(_score=scores).sort_values("_score", ascending=False).drop("_score", axis=1).head(top_n)


def render_ipc_card(row: pd.Series):
    """Render a single IPC section as a styled card."""
    section  = row.get("section", "N/A")
    offense  = row.get("offense", "")
    punish   = row.get("punishment", "")
    desc     = row.get("description", "")

    # Shorten description for display
    short_desc = ""
    if desc:
        lines = [l.strip() for l in desc.split("\n") if l.strip()]
        # Look for "Simple Words" summary
        for i, l in enumerate(lines):
            if "simple words" in l.lower() and i + 1 < len(lines):
                short_desc = lines[i + 1]
                break
        if not short_desc and lines:
            short_desc = lines[0][:300] + ("…" if len(lines[0]) > 300 else "")

    st.markdown(f"""
    <div class="section-card">
        <div class="section-number">⚖️ {section}</div>
        <div class="section-offense">{offense}</div>
        <div class="section-punishment">🔒 {punish}</div>
        <p style="color:#9a8a6a;margin-top:10px;font-size:0.9rem;line-height:1.6">{short_desc}</p>
    </div>
    """, unsafe_allow_html=True)


# ── System prompt for legal AI ────────────────────────────────────────────────

LEGAL_SYSTEM = """You are an expert Indian criminal law research assistant specialising in the 
Indian Penal Code (IPC), Code of Criminal Procedure (CrPC), and related legislation.

Guidelines:
- Cite specific IPC sections (e.g., IPC Section 302, Section 376, Section 420) when relevant.
- Explain legal concepts clearly for both lawyers and laypersons.
- When relevant sections from the IPC are provided in the query, use them as primary reference.
- Mention important case laws where applicable (Supreme Court, High Courts).
- Note if a provision has been amended or replaced by BNS 2023 (Bharatiya Nyaya Sanhita).
- Be precise about punishments, bailable/non-bailable status, cognisable/non-cognisable nature.
- Always add a disclaimer that this is legal information, not legal advice.
- Format responses with clear headings, bullet points, and section references.
- Keep responses informative yet concise (300–500 words unless a detailed analysis is requested)."""


# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## ⚖️ IPC Research\n### Assistant")
    st.markdown("---")

    # API key status
    has_key = False
    try:
        has_key = bool(st.secrets.get("ANTHROPIC_API_KEY", ""))
    except Exception:
        import os
        has_key = bool(os.environ.get("ANTHROPIC_API_KEY", ""))

    if has_key:
        st.markdown('<span class="badge badge-gold">✓ API Connected</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="badge badge-red">✗ API Key Missing</span>', unsafe_allow_html=True)
        st.caption("Add `ANTHROPIC_API_KEY` to Streamlit Secrets")

    st.markdown("---")

    # Dataset status
    st.markdown("**📊 Loaded Data**")
    col1, col2 = st.columns(2)
    col1.metric("IPC Sections", len(ipc_df) if not ipc_df.empty else "—")
    col2.metric("NCRB Records", len(ncrb_df) if not ncrb_df.empty else "—")

    if ipc_df.empty:
        st.warning("⚠️ `ipc_sections.csv` not found.\nPlace it in the same folder as `app.py`.")
    if ncrb_df.empty:
        st.caption("ℹ️ NCRB CSV not found (optional for stats tab).")

    st.markdown("---")

    # Quick section lookup
    st.markdown("**🔍 Quick Section Lookup**")
    quick_sec = st.text_input("Section number (e.g., 302)", placeholder="302", key="quick")
    if quick_sec.strip() and not ipc_df.empty:
        q = quick_sec.strip().upper().lstrip("IPC_ ")
        mask = ipc_df["section"].fillna("").str.upper().str.contains(q, regex=False)
        found = ipc_df[mask]
        if not found.empty:
            row = found.iloc[0]
            st.markdown(f"""
            <div style="background:#161410;padding:10px;border-left:3px solid #c9a84c;border-radius:3px;margin:6px 0">
                <b style="color:#c9a84c">{row.get('section','')}</b><br>
                <span style="color:#9a8a6a;font-size:0.8rem">{row.get('offense','')[:80]}…</span><br>
                <code style="color:#e05555;font-size:0.8rem">{row.get('punishment','')}</code>
            </div>""", unsafe_allow_html=True)
        else:
            st.caption("Section not found")

    st.markdown("---")

    # Common queries
    st.markdown("**💡 Common Queries**")
    suggestions = [
        "What is IPC Section 302?",
        "Bail conditions for murder",
        "Difference between culpable homicide and murder",
        "Punishment for theft under IPC",
        "What constitutes rape under IPC 376?",
        "IPC sections for cheating and fraud",
        "Rights of accused during arrest",
        "Cognisable vs non-cognisable offences",
    ]
    for s in suggestions:
        if st.button(s, key=f"sug_{s[:15]}", use_container_width=True):
            st.session_state["prefill_query"] = s
            st.rerun()


# ── Session state init ────────────────────────────────────────────────────────

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "prefill_query" not in st.session_state:
    st.session_state.prefill_query = ""


# ── Main content ──────────────────────────────────────────────────────────────

st.markdown("# ⚖️ Indian Criminal Law\n## Research Assistant")
st.markdown("*Powered by Claude AI · IPC Sections Database · NCRB Crime Statistics*")
st.divider()

tab_research, tab_sections, tab_stats, tab_chat = st.tabs([
    "🔬 AI Research", "📚 IPC Sections", "📊 Crime Statistics", "💬 Chat"
])


# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — AI RESEARCH
# ════════════════════════════════════════════════════════════════════════════

with tab_research:
    st.markdown("### Ask a Legal Question")
    st.caption("AI analysis with relevant IPC sections automatically referenced.")

    prefill = st.session_state.pop("prefill_query", "")
    query = st.text_area(
        "Enter your legal query:",
        value=prefill,
        height=120,
        placeholder="e.g. What is the punishment for murder under IPC? What sections apply to cybercrime?",
        key="main_query"
    )

    col_a, col_b, col_c = st.columns([2, 1, 1])
    with col_a:
        analyse = st.button("⚖️ Analyse", type="primary", use_container_width=True)
    with col_b:
        include_sections = st.toggle("Include matching IPC sections", value=True)
    with col_c:
        detailed = st.toggle("Detailed analysis", value=False)

    if analyse and query.strip():
        # Search IPC for relevant sections
        matched = pd.DataFrame()
        if include_sections and not ipc_df.empty:
            matched = search_ipc(query, ipc_df, top_n=6)

        # Build context for Claude
        ipc_context = ""
        if not matched.empty:
            sections_text = []
            for _, row in matched.iterrows():
                sections_text.append(
                    f"Section: {row.get('section','')}\n"
                    f"Offense: {row.get('offense','')}\n"
                    f"Punishment: {row.get('punishment','')}"
                )
            ipc_context = "\n\nRelevant IPC Sections from database:\n" + "\n---\n".join(sections_text)

        detail_instruction = (
            " Provide a comprehensive legal analysis with case law references, "
            "procedural details, and practical implications."
            if detailed else
            " Keep the response concise and focused."
        )

        messages = [{
            "role": "user",
            "content": query + ipc_context + detail_instruction
        }]

        with st.spinner("🔍 Researching legal provisions…"):
            answer = call_claude(messages, LEGAL_SYSTEM)

        # Display answer
        st.markdown(f'<div class="ai-answer">{answer}</div>', unsafe_allow_html=True)

        # Display matched sections
        if not matched.empty:
            st.markdown("---")
            st.markdown(f"**📚 {len(matched)} Relevant IPC Sections Found:**")
            for _, row in matched.iterrows():
                render_ipc_card(row)

        # Save to chat history
        st.session_state.chat_history.append({
            "role": "user", "content": query
        })
        st.session_state.chat_history.append({
            "role": "assistant", "content": answer
        })

    elif analyse and not query.strip():
        st.warning("Please enter a legal query.")


# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — IPC SECTIONS BROWSER
# ════════════════════════════════════════════════════════════════════════════

with tab_sections:
    st.markdown("### IPC Sections Database")

    if ipc_df.empty:
        st.error("IPC data not loaded. Ensure `ipc_sections.csv` is in the app folder.")
    else:
        col1, col2 = st.columns([3, 1])
        with col1:
            sec_search = st.text_input(
                "Search sections by keyword or section number:",
                placeholder="murder, theft, 302, assault, rape…",
                key="sec_search"
            )
        with col2:
            show_n = st.selectbox("Results", [10, 25, 50, 100], index=0)

        # Filters
        f1, f2 = st.columns(2)
        with f1:
            if "punishment" in ipc_df.columns:
                punish_filter = st.text_input("Filter by punishment keyword:", placeholder="death, life, fine…")
        with f2:
            pass

        # Apply search
        if sec_search.strip():
            results = search_ipc(sec_search, ipc_df, top_n=show_n)
        else:
            results = ipc_df.head(show_n)

        # Apply punishment filter
        if punish_filter.strip() if "punishment" in ipc_df.columns else False:
            results = results[
                results["punishment"].fillna("").str.lower().str.contains(punish_filter.lower(), regex=False)
            ]

        st.caption(f"Showing {len(results)} sections")

        view_mode = st.radio("View as:", ["Cards", "Table"], horizontal=True)

        if view_mode == "Cards":
            for _, row in results.iterrows():
                render_ipc_card(row)
        else:
            # Table view — show clean columns
            display_cols = [c for c in ["section", "offense", "punishment"] if c in results.columns]
            st.dataframe(
                results[display_cols],
                use_container_width=True,
                height=500,
                hide_index=True,
            )

        # Detailed view
        if not results.empty:
            st.markdown("---")
            st.markdown("**📄 View Full Description**")
            section_options = results["section"].tolist() if "section" in results.columns else []
            if section_options:
                chosen = st.selectbox("Select section:", section_options, key="detail_sec")
                row = results[results["section"] == chosen].iloc[0]
                with st.expander(f"Full text: {chosen}", expanded=True):
                    st.markdown(f"**Offense:** {row.get('offense', '')}")
                    st.markdown(f"**Punishment:** `{row.get('punishment', '')}`")
                    st.markdown("**Description:**")
                    st.markdown(row.get("description", "No description available."))

                    # Ask AI about this section
                    if st.button(f"🤖 Ask AI about {chosen}", key=f"ask_{chosen}"):
                        msg = [{
                            "role": "user",
                            "content": f"Explain {chosen} of the IPC in detail. "
                                       f"Offense: {row.get('offense','')}. "
                                       f"Punishment: {row.get('punishment','')}. "
                                       "Include: elements of the offence, landmark case laws, "
                                       "bailable/non-bailable status, and practical implications."
                        }]
                        with st.spinner("Analysing…"):
                            ai_resp = call_claude(msg, LEGAL_SYSTEM)
                        st.markdown(f'<div class="ai-answer">{ai_resp}</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — CRIME STATISTICS (NCRB)
# ════════════════════════════════════════════════════════════════════════════

with tab_stats:
    st.markdown("### Crime Statistics — NCRB 2023")

    if ncrb_df.empty:
        st.info(
            "NCRB statistics file not found.\n\n"
            "Place `NCRB_CII_2023_Table_18A_2_0.csv` in the same folder as `app.py` "
            "to enable crime statistics charts."
        )
        # Show placeholder
        st.markdown("""
        **Once the NCRB data is loaded, this tab will show:**
        - Crime incidence by state/UT
        - Year-on-year trend comparison
        - Top crime categories
        - State-wise ranking charts
        - Filterable data table with export
        """)
    else:
        st.caption(f"Source: NCRB Crime in India 2023 · {len(ncrb_df)} records")

        try:
            import plotly.express as px
            import plotly.graph_objects as go

            # Display raw data first so user can understand columns
            with st.expander("📋 View raw data columns", expanded=False):
                st.write("Columns:", list(ncrb_df.columns))
                st.dataframe(ncrb_df.head(10), use_container_width=True)

            # Auto-detect numeric columns for charting
            num_cols = ncrb_df.select_dtypes(include="number").columns.tolist()
            str_cols = ncrb_df.select_dtypes(include="object").columns.tolist()

            if num_cols and str_cols:
                c1, c2 = st.columns(2)
                with c1:
                    x_col = st.selectbox("Category (X axis):", str_cols, key="ncrb_x")
                with c2:
                    y_col = st.selectbox("Value (Y axis):", num_cols, key="ncrb_y")

                top_n = st.slider("Top N entries:", 5, 30, 15)

                chart_df = (
                    ncrb_df.groupby(x_col)[y_col]
                    .sum()
                    .reset_index()
                    .sort_values(y_col, ascending=False)
                    .head(top_n)
                )

                chart_type = st.radio("Chart type:", ["Bar", "Horizontal Bar", "Pie"], horizontal=True)

                if chart_type == "Bar":
                    fig = px.bar(chart_df, x=x_col, y=y_col, title=f"Top {top_n} by {y_col}",
                                 color=y_col, color_continuous_scale="YlOrBr")
                elif chart_type == "Horizontal Bar":
                    fig = px.bar(chart_df.sort_values(y_col), x=y_col, y=x_col,
                                 orientation="h", title=f"Top {top_n} by {y_col}",
                                 color=y_col, color_continuous_scale="YlOrBr")
                else:
                    fig = px.pie(chart_df, names=x_col, values=y_col,
                                 title=f"Distribution by {y_col}", hole=0.4)

                fig.update_layout(
                    paper_bgcolor="#0d0d0d",
                    plot_bgcolor="#0d0d0d",
                    font_color="#e8dcc8",
                    title_font_color="#c9a84c",
                    coloraxis_showscale=False,
                )
                st.plotly_chart(fig, use_container_width=True)

                # Download
                csv_out = chart_df.to_csv(index=False)
                st.download_button("📥 Download chart data as CSV", csv_out,
                                   "ncrb_filtered.csv", "text/csv")

        except ImportError:
            st.warning("Install `plotly` for charts: `pip install plotly`")
            st.dataframe(ncrb_df, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# TAB 4 — CHAT
# ════════════════════════════════════════════════════════════════════════════

with tab_chat:
    st.markdown("### Legal Research Chat")
    st.caption("Conversational interface — full chat history maintained.")

    # Display history
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(
                f'<div class="chat-user">🧑‍⚖️ <b>You:</b> {msg["content"]}</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="chat-assistant">⚖️ <b>Assistant:</b><br>{msg["content"]}</div>',
                unsafe_allow_html=True
            )

    # Input
    chat_input = st.text_area("Your message:", height=100, key="chat_input",
                               placeholder="Ask about any IPC section, criminal case, legal procedure…")
    c1, c2 = st.columns([1, 4])
    with c1:
        if st.button("Send", type="primary", key="send_chat", use_container_width=True):
            if chat_input.strip():
                # Add user message
                st.session_state.chat_history.append({
                    "role": "user", "content": chat_input.strip()
                })
                # Call Claude with full history
                with st.spinner("Thinking…"):
                    # Build context from IPC search
                    matched = search_ipc(chat_input, ipc_df, top_n=3) if not ipc_df.empty else pd.DataFrame()
                    ipc_ctx = ""
                    if not matched.empty:
                        ipc_ctx = "\n\nAuto-matched IPC sections:\n" + "\n".join(
                            f"- {r.get('section','')}: {r.get('offense','')} | {r.get('punishment','')}"
                            for _, r in matched.iterrows()
                        )
                    messages = st.session_state.chat_history.copy()
                    if ipc_ctx:
                        messages[-1]["content"] += ipc_ctx
                    answer = call_claude(messages, LEGAL_SYSTEM)

                st.session_state.chat_history.append({
                    "role": "assistant", "content": answer
                })
                st.rerun()
    with c2:
        if st.button("🗑️ Clear History", key="clear_chat", use_container_width=False):
            st.session_state.chat_history = []
            st.rerun()


# ── Footer ────────────────────────────────────────────────────────────────────

st.divider()
st.markdown(
    '<p style="text-align:center;color:#4a4030;font-size:0.8rem;font-family:\'JetBrains Mono\',monospace">'
    "⚖️ IPC Legal Research Assistant · For informational purposes only · Not legal advice"
    "</p>",
    unsafe_allow_html=True
)
