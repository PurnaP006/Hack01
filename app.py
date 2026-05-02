import streamlit as st
import anthropic

# Retrieve the key from secrets
client = anthropic.Anthropic(
    api_key=st.secrets["ANTHROPIC_API_KEY"]
)
# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="StudyMate AI",
    page_icon="🎓",
    layout="centered",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Outfit:wght@300;400;600;700&display=swap');

:root {
    --blue-deep:   #040d2a;
    --blue-dark:   #071035;
    --blue-mid:    #0a1a52;
    --blue-card:   #0d2060;
    --blue-border: #1a3580;
    --blue-accent: #2d6fff;
    --blue-bright: #4d8fff;
    --blue-glow:   #1a4dcc;
    --blue-light:  #a8c4ff;
    --white:       #eef3ff;
    --muted:       #6b85c0;
}

*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
    background: var(--blue-deep) !important;
    color: var(--white);
}

.stApp {
    background:
        radial-gradient(ellipse 80% 50% at 20% 10%, rgba(45,111,255,0.18) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 80%, rgba(10,26,82,0.9) 0%, transparent 70%),
        var(--blue-deep) !important;
    min-height: 100vh;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem !important; max-width: 780px !important; }

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
}
.hero-badge {
    display: inline-block;
    background: rgba(45,111,255,0.15);
    border: 1px solid rgba(45,111,255,0.4);
    color: var(--blue-bright);
    border-radius: 999px;
    padding: 4px 16px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 1rem;
    font-family: 'Plus Jakarta Sans', sans-serif;
}
.hero h1 {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 3rem !important;
    font-weight: 800 !important;
    background: linear-gradient(135deg, #fff 30%, var(--blue-bright) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 0.5rem !important;
    line-height: 1.1 !important;
}
.hero p { color: var(--muted); font-size: 1.05rem; margin: 0; }

.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--blue-border), transparent);
    margin: 1.5rem 0;
}

/* ── Input card ── */
.input-card {
    background: rgba(13,32,96,0.5);
    border: 1px solid var(--blue-border);
    border-radius: 18px;
    padding: 1.5rem;
    backdrop-filter: blur(10px);
    margin-bottom: 1.2rem;
}
.input-label {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 600;
    font-size: 0.85rem;
    color: var(--blue-light);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.5rem;
}

/* ── Task buttons ── */
.stButton > button {
    background: rgba(13,32,96,0.7) !important;
    color: var(--white) !important;
    border: 1.5px solid var(--blue-border) !important;
    border-radius: 14px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    padding: 0.65rem 1rem !important;
    transition: all 0.22s ease !important;
    text-align: left !important;
    white-space: pre-wrap !important;
    line-height: 1.4 !important;
}
.stButton > button:hover {
    border-color: var(--blue-accent) !important;
    background: rgba(45,111,255,0.18) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(45,111,255,0.2) !important;
}

/* Generate button override */
div[data-testid="stVerticalBlock"] > div:has(> div[data-testid="stButton"]:last-child) .stButton > button,
.generate-btn .stButton > button {
    background: linear-gradient(135deg, var(--blue-accent), var(--blue-glow)) !important;
    border: none !important;
    box-shadow: 0 4px 20px rgba(45,111,255,0.35) !important;
    font-size: 1rem !important;
    padding: 0.75rem 2rem !important;
    text-align: center !important;
}

/* ── Inputs ── */
textarea, .stTextArea textarea {
    background: rgba(4,13,42,0.8) !important;
    border: 1.5px solid var(--blue-border) !important;
    border-radius: 12px !important;
    color: var(--white) !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.95rem !important;
}
textarea:focus, .stTextArea textarea:focus {
    border-color: var(--blue-accent) !important;
    box-shadow: 0 0 0 3px rgba(45,111,255,0.15) !important;
}
div[data-baseweb="select"] > div {
    background: rgba(4,13,42,0.8) !important;
    border: 1.5px solid var(--blue-border) !important;
    border-radius: 12px !important;
    color: var(--white) !important;
}
div[data-baseweb="select"] > div:hover { border-color: var(--blue-accent) !important; }

.stSlider > div > div > div > div { background: var(--blue-accent) !important; }

/* ── Stats chips ── */
.stat-chips { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 1rem; }
.chip {
    background: rgba(45,111,255,0.12);
    border: 1px solid rgba(45,111,255,0.3);
    border-radius: 999px;
    padding: 3px 12px;
    font-size: 0.75rem;
    color: var(--blue-light);
    font-weight: 500;
}

/* ── Result ── */
.result-wrapper {
    background: rgba(7,16,53,0.8);
    border: 1px solid var(--blue-border);
    border-radius: 18px;
    padding: 1.5rem;
    margin-top: 1.2rem;
    position: relative;
    overflow: hidden;
}
.result-wrapper::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--blue-accent), var(--blue-bright), transparent);
}
.result-label {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 0.75rem;
    font-weight: 700;
    color: var(--blue-accent);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.8rem;
}
.result-text { color: var(--white); font-size: 0.97rem; line-height: 1.75; white-space: pre-wrap; }

/* Download button */
a[data-testid="stDownloadButton"] button {
    background: rgba(45,111,255,0.15) !important;
    border: 1px solid var(--blue-accent) !important;
    color: var(--blue-bright) !important;
    border-radius: 10px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    margin-top: 0.8rem;
}
a[data-testid="stDownloadButton"] button:hover {
    background: rgba(45,111,255,0.28) !important;
}

.footer {
    text-align: center;
    color: var(--muted);
    font-size: 0.78rem;
    padding: 2rem 0 1rem;
}

.stSpinner > div { border-top-color: var(--blue-accent) !important; }
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">✦ AI-Powered · Hackathon Edition</div>
    <h1>StudyMate AI</h1>
    <p>Your intelligent assistant for everyday student tasks</p>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)

# ── Task selection (session state) ───────────────────────────────────────────
TASKS = {
    "summarize": ("📝", "Summarize Notes",       "Turn long text into key points"),
    "quiz":      ("❓", "Generate Quiz",          "Create practice questions"),
    "explain":   ("💡", "Explain a Concept",      "Simplify complex ideas"),
    "draft":     ("✉️", "Draft Essay / Email",    "Write polished documents"),
}

if "task" not in st.session_state:
    st.session_state.task = "summarize"

st.markdown("#### 🗂️ Choose your task")
col1, col2 = st.columns(2)
task_keys = list(TASKS.keys())

for i, key in enumerate(task_keys):
    icon, label, desc = TASKS[key]
    col = col1 if i % 2 == 0 else col2
    with col:
        btn_label = f"{icon} {label}\n{desc}"
        if st.button(btn_label, key=f"btn_{key}", use_container_width=True):
            st.session_state.task = key
            st.rerun()

task = st.session_state.task
icon, label, _ = TASKS[task]

# Show active task indicator
st.markdown(f"""
<div style="margin: 1rem 0 0.4rem; color: var(--blue-light); font-size:0.85rem; font-weight:600;">
    ▶ Active: {icon} <span style="color:#fff;">{label}</span>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Input section ─────────────────────────────────────────────────────────────
st.markdown(f'<div class="input-card"><div class="input-label">{icon} {label}</div></div>', unsafe_allow_html=True)

user_input = ""
extra = {}

if task == "summarize":
    user_input = st.text_area("Your text", height=210,
        placeholder="Paste lecture notes, an article, chapter text, or anything you want summarized…")
    extra["style"] = st.selectbox("Summary format", ["Bullet points", "Short paragraph", "Key facts only"])

elif task == "quiz":
    user_input = st.text_area("Study material", height=210,
        placeholder="Paste a chapter, topic overview, or any content to generate questions from…")
    c1, c2 = st.columns(2)
    with c1:
        extra["num_q"] = st.slider("Number of questions", 3, 10, 5)
    with c2:
        extra["q_type"] = st.selectbox("Question type", ["Multiple choice", "True / False", "Short answer"])

elif task == "explain":
    user_input = st.text_area("Concept to explain", height=150,
        placeholder="e.g. Photosynthesis, the Pythagorean theorem, supply and demand, recursion…")
    extra["level"] = st.selectbox("Explain it like I am a…",
        ["5-year-old", "Middle schooler", "High schooler", "University student"])

elif task == "draft":
    extra["doc_type"] = st.selectbox("Document type",
        ["Short essay", "Email to professor", "Apology / excuse letter", "Scholarship letter", "Book report intro"])
    user_input = st.text_area("Describe your requirements", height=170,
        placeholder="e.g. Essay on climate change, 300 words, persuasive tone, for a science class…")


# ── Prompt builder ────────────────────────────────────────────────────────────
def build_prompt(task, user_input, extra):
    if task == "summarize":
        return (
            f"Summarize the following text as {extra['style'].lower()}. "
            f"Be concise and retain only the most important information.\n\nTEXT:\n{user_input}"
        )
    elif task == "quiz":
        return (
            f"Create exactly {extra['num_q']} {extra['q_type'].lower()} questions from the material below. "
            f"Number each question. For multiple choice, include options A–D and mark the correct answer at the end.\n\n"
            f"MATERIAL:\n{user_input}"
        )
    elif task == "explain":
        return (
            f"Explain the following concept to a {extra['level'].lower()} in a clear, engaging way. "
            f"Use simple language, relatable real-life examples, and analogies.\n\nCONCEPT:\n{user_input}"
        )
    elif task == "draft":
        return (
            f"Write a well-structured, polished {extra['doc_type'].lower()} for a student. "
            f"Requirements: {user_input}\n\nMake it natural, professional, and ready to submit."
        )


# ── Generate ──────────────────────────────────────────────────────────────────
st.markdown("")
generate = st.button("✨ Generate with AI", use_container_width=True)

if generate:
    if not user_input.strip():
        st.warning("⚠️ Please enter some text before generating.")
    else:
        with st.spinner("🔵 AI is thinking…"):
            try:
                client = anthropic.Anthropic()
                prompt = build_prompt(task, user_input, extra)
                message = client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=1024,
                    messages=[{"role": "user", "content": prompt}],
                )
                result = message.content[0].text
                word_count = len(result.split())

                st.markdown(f"""
                <div class="stat-chips">
                    <span class="chip">📄 {word_count} words</span>
                    <span class="chip">✅ Generated successfully</span>
                </div>
                <div class="result-wrapper">
                    <div class="result-label">✦ AI Output</div>
                    <div class="result-text">{result}</div>
                </div>
                """, unsafe_allow_html=True)

                st.download_button(
                    "⬇️ Download as .txt",
                    data=result,
                    file_name=f"studymate_{task}.txt",
                    mime="text/plain",
                    use_container_width=True,
                )

            except Exception as e:
                st.error(f"❌ Something went wrong: {e}")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="divider" style="margin-top:2.5rem;"></div>
<div class="footer">
    🎓 StudyMate AI &nbsp;·&nbsp; Built with Streamlit & Claude &nbsp;·&nbsp; Hackathon Edition 🚀
</div>
""", unsafe_allow_html=True)
