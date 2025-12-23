import os
import streamlit as st
import pandas as pd

# --------------------------------------------------
# OPTIONAL: Load .env automatically (if python-dotenv installed)
# If you don't want this, you can remove this block.
# pip install python-dotenv
# --------------------------------------------------
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass


# --------------------------------------------------
# ENV HELPERS
# --------------------------------------------------
def _env_int(key: str, default: int) -> int:
    val = os.getenv(key, "").strip()
    if not val:
        return default
    try:
        return int(float(val))
    except Exception:
        return default


def _env_float(key: str, default: float) -> float:
    val = os.getenv(key, "").strip()
    if not val:
        return default
    try:
        return float(val)
    except Exception:
        return default


def _parse_marks_csv(val: str):
    """
    Accepts: "589,550,480"
    Returns: (589, 550, 480) or None
    """
    if not val:
        return None
    parts = [p.strip() for p in val.split(",") if p.strip()]
    if len(parts) != 3:
        return None
    try:
        return (int(float(parts[0])), int(float(parts[1])), int(float(parts[2])))
    except Exception:
        return None


def load_default_marks():
    """
    Priority:
      1) PUBLIC_MARKS="589,550,480" and INTERNAL_MARKS="585,545,480"
      2) PUBLIC_M1/PUBLIC_M2/PUBLIC_M3 etc
      3) Hard defaults
    """
    hard_public = {"m1": 589, "m2": 550, "m3": 480}
    hard_internal = {"m1": 585, "m2": 545, "m3": 480}

    public_csv = _parse_marks_csv(os.getenv("PUBLIC_MARKS", "").strip())
    internal_csv = _parse_marks_csv(os.getenv("INTERNAL_MARKS", "").strip())

    if public_csv:
        public = {"m1": public_csv[0], "m2": public_csv[1], "m3": public_csv[2]}
    else:
        public = {
            "m1": _env_int("PUBLIC_M1", hard_public["m1"]),
            "m2": _env_int("PUBLIC_M2", hard_public["m2"]),
            "m3": _env_int("PUBLIC_M3", hard_public["m3"]),
        }

    if internal_csv:
        internal = {"m1": internal_csv[0], "m2": internal_csv[1], "m3": internal_csv[2]}
    else:
        internal = {
            "m1": _env_int("INTERNAL_M1", hard_internal["m1"]),
            "m2": _env_int("INTERNAL_M2", hard_internal["m2"]),
            "m3": _env_int("INTERNAL_M3", hard_internal["m3"]),
        }

    return public, internal


# --------------------------------------------------
# FIXED CONFIG (NON-EDITABLE)
# --------------------------------------------------
PRINCIPAL = 100_000
INTEREST_RATE = _env_float("INTEREST_RATE", 0.09)  # keep fixed by default (9%)
PUBLIC_SPLIT = 0.65
INTERNAL_SPLIT = 0.35

ANNUAL_FUND = round(PRINCIPAL * INTEREST_RATE)  # should be 9000 for 1,00,000 @ 9%
PUBLIC_POOL = round(ANNUAL_FUND * PUBLIC_SPLIT)
INTERNAL_POOL = ANNUAL_FUND - PUBLIC_POOL  # ensure total matches exactly

# --------------------------------------------------
# DEFAULT MARKS FROM ENV
# --------------------------------------------------
DEFAULT_PUBLIC_MARKS, DEFAULT_INTERNAL_MARKS = load_default_marks()


# --------------------------------------------------
# REWARD CALC
# --------------------------------------------------
def calc_rewards(pool_amount: int, marks: dict) -> pd.DataFrame:
    m1, m2, m3 = int(marks["m1"]), int(marks["m2"]), int(marks["m3"])
    total = m1 + m2 + m3

    if total <= 0:
        r1 = r2 = r3 = 0
    else:
        r1 = round(pool_amount * (m1 / total))
        r2 = round(pool_amount * (m2 / total))
        r3 = pool_amount - r1 - r2  # adjust to keep exact total

    return pd.DataFrame(
        {
            "Rank": ["🥇 1st", "🥈 2nd", "🥉 3rd"],
            "Marks": [m1, m2, m3],
            "Reward (₹)": [r1, r2, r3],
        }
    )


# --------------------------------------------------
# PAGE SETUP
# --------------------------------------------------
st.set_page_config(page_title="Performance Reward Distribution", page_icon="🎓", layout="wide")

# --------------------------------------------------
# BEAUTIFUL MODERN UI THEME
# --------------------------------------------------
st.markdown(
    """
<style>
html, body { margin: 0; padding: 0; }
body {
    background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
    font-family: 'Segoe UI', sans-serif;
}

/* Title */
.hero-title {
    text-align: center;
    font-size: 44px;
    font-weight: 900;
    color: #2c3e50;
    margin-bottom: -5px;
}
.hero-subtitle {
    text-align: center;
    font-size: 18px;
    color: #5c6b7a;
    margin-bottom: 28px;
}

/* Cards */
.card {
    background: white;
    padding: 22px;
    border-radius: 18px;
    width: 100%;
    border: 1px solid #e2e8f0;
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);
    transition: transform 0.2s ease;
}
.card:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.12);
}
.card-title { font-size: 20px; font-weight: 800; color: #1f2d3d; }
.card-desc { font-size: 14px; color: #576574; margin-top: 6px; }

/* Section Titles */
.section-title {
    font-size: 26px;
    font-weight: 800;
    margin-top: 30px;
    margin-bottom: 10px;
    color: #2c3e50;
}

/* Content Card */
.content-card {
    background: white;
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 4px 14px rgba(0,0,0,0.06);
}

/* Mini mark cards (for toggle OFF view) */
.marks-wrap {
    display: grid;
    grid-template-columns: 1fr;
    gap: 12px;
    margin-top: 8px;
}
.mark-card {
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 14px 14px;
    background: #ffffff;
    box-shadow: 0 2px 10px rgba(0,0,0,0.04);
}
.mark-label {
    font-size: 12px;
    color: #6b7b8b;
    margin-bottom: 4px;
}
.mark-value {
    font-size: 22px;
    font-weight: 900;
    color: #1f2d3d;
}

/* Table rounding */
[data-testid="stDataFrame"] { border-radius: 14px; overflow: hidden; border: 1px solid #e2e8f0; }
</style>
""",
    unsafe_allow_html=True,
)

# --------------------------------------------------
# HERO
# --------------------------------------------------
st.markdown('<div class="hero-title">🎓 Performance Reward Distribution</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Tagira High School, Ranital, Bhadrak, Odisha</div>', unsafe_allow_html=True)

# --------------------------------------------------
# TOP SUMMARY CARDS (FIXED)
# --------------------------------------------------
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(
        f"""
    <div class="card">
        <div class="card-title">🏦 Principal Amount</div>
        <h3>₹{PRINCIPAL:,.0f}</h3>
        <p class="card-desc">Permanently deposited in the school’s bank account.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        f"""
    <div class="card">
        <div class="card-title">📉 Interest Rate</div>
        <h3>{INTEREST_RATE*100:.0f}% per year</h3>
        <p class="card-desc">Revised yearly bank interest used for rewards.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        f"""
    <div class="card">
        <div class="card-title">💰 Annual Reward Fund</div>
        <h3>₹{ANNUAL_FUND:,.0f}</h3>
        <p class="card-desc">Split into two tests (₹{PUBLIC_POOL:,.0f} + ₹{INTERNAL_POOL:,.0f}).</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

# --------------------------------------------------
# PURPOSE
# --------------------------------------------------
st.markdown('<div class="section-title">🎯 Purpose of the Reward Scheme</div>', unsafe_allow_html=True)
st.markdown(
    """
<div class="content-card">
To encourage academic excellence, the school created a permanent education fund from which 
the annual interest is awarded to the top performers every year.

<br><br>
<ul>
    <li><b>Principal</b> remains untouched for life.</li>
    <li><b>Only yearly interest</b> is used for rewards.</li>
    <li><b>Split is fixed:</b> 65% Public Test + 35% Internal Test.</li>
    <li>Transparent, fair, and proportional reward system.</li>
</ul>
</div>
""",
    unsafe_allow_html=True,
)

# --------------------------------------------------
# FORMULA
# --------------------------------------------------
st.markdown('<div class="section-title">📐 Reward Calculation Formula</div>', unsafe_allow_html=True)
st.markdown(
    f"""
<div class="content-card">
Let:

• <b>M1, M2, M3</b> = Marks of 1st, 2nd, 3rd rank <br>
• <b>Total = M1 + M2 + M3</b> <br>
• <b>Pool = Test Pool Amount</b>

<br>
<b>Formulas:</b><br>
• Prize 1 = Pool × (M1 / Total)<br>
• Prize 2 = Pool × (M2 / Total)<br>
• Prize 3 = Pool × (M3 / Total)

<hr style="border:none;border-top:1px solid #eef2f7;margin:16px 0;">

<b>Split of Annual Fund (Fixed):</b><br><br>

🌍 <b>Public Pool (₹)</b> = {ANNUAL_FUND:,.0f} × 65% = <b>₹{PUBLIC_POOL:,.0f}</b><br>
🏫 <b>Internal Pool (₹)</b> = {ANNUAL_FUND:,.0f} × 35% = <b>₹{INTERNAL_POOL:,.0f}</b><br><br>

<b>Total (₹)</b> = <b>₹{ANNUAL_FUND:,.0f}</b>
</div>
""",
    unsafe_allow_html=True,
)

# --------------------------------------------------
# WINNER INPUTS (TOGGLE EDIT)
# --------------------------------------------------
st.markdown('<div class="section-title">🧮 Enter Winner Marks</div>', unsafe_allow_html=True)

top_left, top_right = st.columns([1, 3])
with top_left:
    enable_editing = st.toggle("Enable Editing", value=False)

with top_right:
    st.markdown(
        """
<div class="content-card">
<b>Only the marks are editable.</b> Principal, interest rate, annual fund, and 65/35 split are fixed.
</div>
""",
        unsafe_allow_html=True,
    )

# Store marks in session_state (so it stays after reruns)
if "public_marks" not in st.session_state:
    st.session_state.public_marks = DEFAULT_PUBLIC_MARKS.copy()
if "internal_marks" not in st.session_state:
    st.session_state.internal_marks = DEFAULT_INTERNAL_MARKS.copy()


def marks_input_block(title: str, pool_amount: int, key_prefix: str, state_key: str):
    """
    If enable_editing is ON -> show number_input widgets
    If OFF -> show pretty read-only mark cards (better UI)
    """
    st.markdown(
        f"""
<div class="content-card">
<h4 style="margin:0;">{title} (Pool = ₹{pool_amount:,.0f})</h4>
</div>
""",
        unsafe_allow_html=True,
    )

    marks = st.session_state[state_key]

    if enable_editing:
        # Editable inputs
        m1 = st.number_input(f"{key_prefix} - 1st Rank Marks", min_value=0, max_value=1000, value=int(marks["m1"]), step=1, key=f"{key_prefix}_m1")
        m2 = st.number_input(f"{key_prefix} - 2nd Rank Marks", min_value=0, max_value=1000, value=int(marks["m2"]), step=1, key=f"{key_prefix}_m2")
        m3 = st.number_input(f"{key_prefix} - 3rd Rank Marks", min_value=0, max_value=1000, value=int(marks["m3"]), step=1, key=f"{key_prefix}_m3")

        st.session_state[state_key] = {"m1": int(m1), "m2": int(m2), "m3": int(m3)}
    else:
        # Clean read-only display (no grey disabled inputs)
        st.markdown(
            f"""
<div class="marks-wrap">
  <div class="mark-card">
    <div class="mark-label">{key_prefix} - 1st Rank Marks</div>
    <div class="mark-value">{int(marks["m1"])}</div>
  </div>
  <div class="mark-card">
    <div class="mark-label">{key_prefix} - 2nd Rank Marks</div>
    <div class="mark-value">{int(marks["m2"])}</div>
  </div>
  <div class="mark-card">
    <div class="mark-label">{key_prefix} - 3rd Rank Marks</div>
    <div class="mark-value">{int(marks["m3"])}</div>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )


left, right = st.columns(2)
with left:
    marks_input_block("🌍 Public Test Winners", PUBLIC_POOL, "Public", "public_marks")

with right:
    marks_input_block("🏫 Internal Test Winners", INTERNAL_POOL, "Internal", "internal_marks")

# --------------------------------------------------
# REWARD TABLES
# --------------------------------------------------
st.markdown('<div class="section-title">🏆 Reward Distribution Tables</div>', unsafe_allow_html=True)

pub_df = calc_rewards(PUBLIC_POOL, st.session_state.public_marks)
int_df = calc_rewards(INTERNAL_POOL, st.session_state.internal_marks)

t1, t2 = st.columns(2)
with t1:
    st.markdown('<div class="content-card"><b>🌍 Public Test Reward Table</b></div>', unsafe_allow_html=True)
    st.dataframe(pub_df, use_container_width=True, hide_index=True)

with t2:
    st.markdown('<div class="content-card"><b>🏫 Internal Test Reward Table</b></div>', unsafe_allow_html=True)
    st.dataframe(int_df, use_container_width=True, hide_index=True)

# Totals check
pub_total = int(pub_df["Reward (₹)"].sum())
int_total = int(int_df["Reward (₹)"].sum())

st.markdown(
    f"""
<div class="content-card">
<b>Pool Totals Check:</b><br><br>
🌍 Public Total = <b>₹{pub_total:,.0f}</b> (Expected ₹{PUBLIC_POOL:,.0f})<br>
🏫 Internal Total = <b>₹{int_total:,.0f}</b> (Expected ₹{INTERNAL_POOL:,.0f})<br>
<hr style="border:none;border-top:1px solid #eef2f7;margin:16px 0;">
<b>Grand Total = ₹{(pub_total + int_total):,.0f}</b> (Expected ₹{ANNUAL_FUND:,.0f})
</div>
""",
    unsafe_allow_html=True,
)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown(
    """
<br><br>
<div style='text-align:center; color:#7f8c8d; font-size:14px; padding-top:20px;'>
    © 2025 • Designed & Developed by <b>RV Developers</b>
</div>
""",
    unsafe_allow_html=True,
)
