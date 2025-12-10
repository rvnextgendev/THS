import streamlit as st
import pandas as pd

# --------------------------------------------------
# PAGE SETUP
# --------------------------------------------------
st.set_page_config(
    page_title="Performance Reward Distribution",
    page_icon="🎓",
    layout="wide"
)

# --------------------------------------------------
# BEAUTIFUL MODERN UI THEME
# --------------------------------------------------
st.markdown("""
<style>

html, body {
    margin: 0;
    padding: 0;
}

body {
    background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
    font-family: 'Segoe UI', sans-serif;
}

/* Title Styling */
.hero-title {
    text-align: center;
    font-size: 46px;
    font-weight: 900;
    color: #2c3e50;
    margin-bottom: -5px;
}

.hero-subtitle {
    text-align: center;
    font-size: 20px;
    color: #5c6b7a;
    margin-bottom: 35px;
}

/* Cards */
.card {
    background: white;
    padding: 25px;
    border-radius: 18px;
    width: 100%;
    border: 1px solid #e2e8f0;
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);
    transition: transform 0.2s ease;
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.12);
}

.card-title {
    font-size: 22px;
    font-weight: 800;
    color: #1f2d3d;
}

.card-desc {
    font-size: 15px;
    color: #576574;
}

/* Section Titles */
.section-title {
    font-size: 28px;
    font-weight: 800;
    margin-top: 35px;
    margin-bottom: 10px;
    color: #2c3e50;
}

/* Content Card */
.content-card {
    background: white;
    padding: 25px;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 4px 14px rgba(0,0,0,0.06);
}

.dataframe {
    border-radius: 10px !important;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HERO SECTION
# --------------------------------------------------
st.markdown('<div class="hero-title">🎓 Performance Reward Distribution</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Tagira High School, Ranital, Bhadrak, Odisha</div>', unsafe_allow_html=True)

# --------------------------------------------------
# TOP SUMMARY CARDS
# --------------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
        <div class="card-title">🏦 Principal Amount</div>
        <h3>₹1,00,000</h3>
        <p class="card-desc">Permanently deposited in the school’s bank account.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <div class="card-title">📉 Interest Rate</div>
        <h3>9% per year</h3>
        <p class="card-desc">Revised yearly bank interest used for rewards.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
        <div class="card-title">💰 Annual Reward Fund</div>
        <h3>₹9,000</h3>
        <p class="card-desc">Interest amount used for student rewards.</p>
    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# PURPOSE SECTION
# --------------------------------------------------
st.markdown('<div class="section-title">🎯 Purpose of the Reward Scheme</div>', unsafe_allow_html=True)

st.markdown("""
<div class="content-card">
To encourage academic excellence, the school created a permanent education fund from which 
the annual interest (₹9,000) is awarded to the top 3 performers every year.

<br>

<ul>
    <li>Principal amount remains untouched for life.</li>
    <li>Only yearly interest is used for student motivation.</li>
    <li>Transparent, fair, and proportional reward system.</li>
    <li>Supports long-term academic growth in the Ranital–Bhadrak region.</li>
</ul>

</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# FORMULA SECTION
# --------------------------------------------------
st.markdown('<div class="section-title">📐 Reward Calculation Formula</div>', unsafe_allow_html=True)

st.markdown("""
<div class="content-card">

Let:

• <b>M1, M2, M3</b> = Marks of 1st, 2nd, 3rd rank <br>
• <b>Total = M1 + M2 + M3</b> <br>
• <b>Reward Pool = ₹9,000</b>

<br>
<b>Formulas:</b><br>
• First Prize = 9000 × (M1 / Total)<br>
• Second Prize = 9000 × (M2 / Total)<br>
• Third Prize = 9000 × (M3 / Total)

</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# EXAMPLE SECTION (OUT OF 600)
# --------------------------------------------------
st.markdown('<div class="section-title">📝 Example (Marks out of 600)</div>', unsafe_allow_html=True)

st.markdown("""
<div class="content-card">

<ul>
<li><b>1st Rank:</b> 589</li>
<li><b>2nd Rank:</b> 550</li>
<li><b>3rd Rank:</b> 480</li>
</ul>

<b>Total Marks = 1619</b>

</div>
""", unsafe_allow_html=True)

# Marks and rewards for ₹9,000 fund
df = pd.DataFrame({
    "Rank": ["🥇 1st", "🥈 2nd", "🥉 3rd"],
    "Marks (out of 600)": [589, 550, 480],
    "Final Reward (₹)": [3274, 3057, 2668]
})

st.dataframe(df, use_container_width=True, hide_index=True)

st.markdown("""
<div class="content-card">
<b>Final Distribution (₹9,000 Fund):</b><br><br>

🥇 1st Rank → <b>₹3,274</b><br>
🥈 2nd Rank → <b>₹3,057</b><br>
🥉 3rd Rank → <b>₹2,668</b><br><br>

<span style="font-size:13px; color:#7f8c8d;">
(Values are rounded to the nearest rupee; a difference of ₹1 may remain due to rounding.)
</span>

</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown("""
<br><br>
<div style='text-align:center; color:#7f8c8d; font-size:14px; padding-top:20px;'>
    © 2025 • Designed & Developed by <b>RV Developers</b>
</div>
""", unsafe_allow_html=True)
