import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# ============================================================
# MERCHANT GROWTH AI — PREMIUM DEMO
# ============================================================
st.set_page_config(
    page_title="Merchant Growth AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Design system
# -----------------------------
BG = "#07111F"
PANEL = "#0D1B2A"
PANEL_2 = "#102235"
BORDER = "rgba(148,163,184,.16)"
TEXT = "#F8FAFC"
MUTED = "#94A3B8"
GREEN = "#00D084"
GREEN_2 = "#16A86B"
CYAN = "#38BDF8"
YELLOW = "#FBBF24"
RED = "#FB7185"
PURPLE = "#A78BFA"

st.markdown(
    f"""
<style>
:root {{
    --bg:{BG};
    --panel:{PANEL};
    --panel2:{PANEL_2};
    --border:{BORDER};
    --text:{TEXT};
    --muted:{MUTED};
    --green:{GREEN};
}}
.stApp {{
    background:
        radial-gradient(circle at 85% 5%, rgba(0,208,132,.08), transparent 24%),
        radial-gradient(circle at 15% 0%, rgba(56,189,248,.06), transparent 22%),
        {BG};
    color: {TEXT};
}}
[data-testid="stHeader"] {{ background: transparent; }}
.block-container {{ max-width: 1500px; padding-top: 1.4rem; padding-bottom: 2rem; }}
[data-testid="stSidebar"] {{
    background: #06101C;
    border-right: 1px solid {BORDER};
}}
[data-testid="stSidebar"] * {{ color: #DDE7F2; }}
div[data-testid="stMetric"] {{
    background: linear-gradient(145deg, {PANEL_2}, {PANEL});
    border: 1px solid {BORDER};
    border-radius: 18px;
    padding: 18px 18px 14px;
    box-shadow: 0 12px 30px rgba(0,0,0,.18);
}}
div[data-testid="stMetricLabel"] {{ color: {MUTED}; }}
div[data-testid="stMetricValue"] {{ color: {TEXT}; font-size: 1.8rem; }}
div[data-testid="stMetricDelta"] {{ font-size: .78rem; }}
div.stButton > button {{
    border: 1px solid rgba(0,208,132,.32);
    background: linear-gradient(135deg, rgba(0,208,132,.18), rgba(0,208,132,.06));
    color: #DDFEF0;
    border-radius: 10px;
    font-weight: 700;
    min-height: 38px;
}}
div.stButton > button:hover {{
    border-color: {GREEN};
    background: rgba(0,208,132,.22);
    color: white;
}}
div[data-baseweb="select"] > div {{
    background: #0A1725;
    border-color: {BORDER};
    color: white;
}}
hr {{ border-color: {BORDER}; }}
.mini {{
    color:{MUTED}; font-size:.78rem; text-transform:uppercase;
    letter-spacing:.08em; font-weight:700;
}}
.hero {{
    border:1px solid rgba(0,208,132,.22);
    border-radius:24px;
    padding:28px 30px;
    background:
        linear-gradient(115deg, rgba(0,208,132,.12), rgba(56,189,248,.04) 48%, rgba(167,139,250,.05)),
        {PANEL};
    box-shadow:0 20px 55px rgba(0,0,0,.24);
}}
.hero h1 {{ margin:.2rem 0 .35rem; font-size:2rem; color:white; }}
.hero p {{ margin:0; color:#B6C4D3; }}
.badge {{
    display:inline-block; padding:5px 10px; border-radius:999px;
    background:rgba(0,208,132,.11); color:#7EF0BE;
    border:1px solid rgba(0,208,132,.22); font-size:.72rem; font-weight:800;
}}
.live-dot {{
    display:inline-block; width:8px; height:8px; border-radius:50%;
    background:{GREEN}; box-shadow:0 0 12px {GREEN}; margin-right:7px;
}}
.card {{
    background:linear-gradient(145deg, rgba(16,34,53,.96), rgba(9,24,38,.96));
    border:1px solid {BORDER}; border-radius:20px; padding:20px;
    margin:0 0 16px; box-shadow:0 14px 35px rgba(0,0,0,.14);
}}
.card-title {{ font-size:1.08rem; font-weight:800; color:white; margin-bottom:4px; }}
.card-sub {{ color:{MUTED}; font-size:.83rem; margin-bottom:15px; }}
.insight {{
    border:1px solid {BORDER}; border-left:3px solid {GREEN};
    background:rgba(0,208,132,.045); border-radius:13px; padding:13px 14px;
    margin:8px 0;
}}
.insight.warn {{ border-left-color:{YELLOW}; background:rgba(251,191,36,.045); }}
.insight.info {{ border-left-color:{CYAN}; background:rgba(56,189,248,.045); }}
.insight.danger {{ border-left-color:{RED}; background:rgba(251,113,133,.045); }}
.pill {{
    display:inline-block; padding:4px 9px; border-radius:999px;
    font-size:.68rem; font-weight:800; margin-bottom:7px;
}}
.pill-green {{ background:rgba(0,208,132,.12); color:#76F3BC; }}
.pill-yellow {{ background:rgba(251,191,36,.12); color:#FCD978; }}
.pill-red {{ background:rgba(251,113,133,.12); color:#FDA4AF; }}
.pill-blue {{ background:rgba(56,189,248,.12); color:#7DD3FC; }}
.action {{
    display:flex; justify-content:space-between; gap:12px; align-items:center;
    padding:13px 14px; border-radius:13px; border:1px solid {BORDER};
    background:rgba(255,255,255,.025); margin:8px 0;
}}
.action strong {{ color:white; }}
.action span {{ color:{MUTED}; font-size:.78rem; }}
.ai-box {{
    border:1px solid rgba(167,139,250,.25); border-radius:18px;
    background:linear-gradient(135deg, rgba(167,139,250,.08), rgba(56,189,248,.035));
    padding:18px;
}}
.score {{
    font-size:3rem; font-weight:900; line-height:1; color:white;
}}
.progress {{
    height:7px; border-radius:20px; background:#17283A; overflow:hidden; margin:5px 0 11px;
}}
.progress > div {{ height:100%; border-radius:20px; background:linear-gradient(90deg,{GREEN},{CYAN}); }}
.footer {{ color:#617286; font-size:.75rem; text-align:center; padding:20px 0 4px; }}
</style>
""",
    unsafe_allow_html=True,
)

# -----------------------------
# Session state
# -----------------------------
for key, default in {
    "reminders_sent": set(),
    "reorders_placed": set(),
    "discount_applied": False,
    "campaign_created": False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# -----------------------------
# Mock data
# -----------------------------
STORE_NAME = "Sri Lakshmi Kirana Store"
STORE_LOCATION = "Kakinada, Andhra Pradesh"

pending_payments = pd.DataFrame([
    {"id": 1, "customer": "Ramesh Traders", "amount": 1500, "due_in": "3 days"},
    {"id": 2, "customer": "Anitha Stores", "amount": 1800, "due_in": "1 day"},
    {"id": 3, "customer": "Venkat & Co.", "amount": 900, "due_in": "5 days"},
])

inventory = pd.DataFrame([
    {"id": 1, "item": "Rice (25kg bags)", "stock": 4, "reorder_qty": 20, "supplier": "Godavari Wholesale"},
    {"id": 2, "item": "Cooking Oil (5L)", "stock": 9, "reorder_qty": 15, "supplier": "Sri Balaji Distributors"},
    {"id": 3, "item": "Sugar (1kg packs)", "stock": 30, "reorder_qty": 0, "supplier": "—"},
])

days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
sales_values = [3100, 3000, 3700, 4100, 4700, 6500, 3300]
monthly_sales = 185000
todays_sales = 4320
pending_total = int(pending_payments["amount"].sum())

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.markdown("## ✦ MerchantAI")
    st.caption("AI business copilot for Paytm merchants")
    st.markdown(
        '<span class="badge"><span class="live-dot"></span>LIVE DEMO MODE</span>',
        unsafe_allow_html=True,
    )
    st.divider()

    merchant = st.selectbox("Merchant", [STORE_NAME, "Ravi Cafe", "Demo Merchant"])
    st.caption(STORE_LOCATION if merchant == STORE_NAME else "Bhimavaram, Andhra Pradesh")

    st.divider()
    st.markdown("**AI teammates**")
    st.markdown("🟢 💳 Billing AI — active")
    st.markdown("🟢 📦 Inventory AI — active")
    st.markdown("🟢 📊 Insights AI — active")
    st.markdown("🟢 🤖 Growth Copilot — active")

    st.divider()
    st.markdown("**Demo navigation**")
    section = st.radio(
        "Go to",
        ["Overview", "Analytics", "AI Insights", "Growth Opportunities",
         "Customers", "Products", "AI Copilot", "Campaigns"],
        label_visibility="collapsed",
    )

    st.divider()
    st.caption("Powered by Merchant Growth AI • prototype data")

# -----------------------------
# Hero
# -----------------------------
st.markdown(
    f"""
<div class="hero">
    <span class="badge">MERCHANT GROWTH AI • COMMAND CENTER</span>
    <h1>Good morning, {STORE_NAME.split()[0]} 👋</h1>
    <p><span class="live-dot"></span>Your AI business partner is monitoring sales, customers,
    products and growth opportunities in real time.</p>
</div>
""",
    unsafe_allow_html=True,
)

st.write("")

# -----------------------------
# Top metrics
# -----------------------------
m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Revenue / month", "₹1,85,000", "+12.4%")
m2.metric("Today's sales", "₹4,320", "+8.2%")
m3.metric("Orders", "154", "+18.4%")
m4.metric("Avg. order value", "₹1,202", "+4.1%")
m5.metric("Pending collection", f"₹{pending_total:,}", "3 invoices")

st.write("")

# -----------------------------
# Alert strip
# -----------------------------
st.markdown(
    """
<div class="card" style="padding:12px 16px;">
  <span class="pill pill-green">✦ AI MONITORING</span>
  &nbsp; <strong>4 growth opportunities detected</strong>
  <span style="color:#94A3B8;"> • 1 needs attention today • estimated upside ₹6,800</span>
</div>
""",
    unsafe_allow_html=True,
)

# ============================================================
# OVERVIEW
# ============================================================
if section == "Overview":

    left, right = st.columns([1.35, 1], gap="large")

    with left:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">📈 Revenue intelligence</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-sub">AI-tracked sales performance • last 7 days</div>', unsafe_allow_html=True)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=days, y=sales_values, mode="lines+markers",
            line=dict(color=GREEN, width=3),
            marker=dict(size=8, color=GREEN),
            fill="tozeroy",
            fillcolor="rgba(0,208,132,.08)",
            hovertemplate="<b>%{x}</b><br>Revenue ₹%{y:,}<extra></extra>",
        ))
        fig.update_layout(
            height=330, margin=dict(l=5, r=5, t=10, b=5),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94A3B8"), xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="rgba(148,163,184,.10)", tickprefix="₹"),
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        st.markdown(
            '<div class="insight"><span class="pill pill-green">AI INSIGHT</span><br>'
            '<strong>Saturday is your strongest sales window.</strong><br>'
            '<span style="color:#94A3B8;">Revenue reached ₹6,500 — 38% above your weekly average.</span></div>',
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">🩺 Business health</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-sub">AI health score based on current merchant signals</div>', unsafe_allow_html=True)
        st.markdown('<div class="score">78<span style="font-size:1rem;color:#94A3B8;"> / 100</span></div>', unsafe_allow_html=True)
        for label, value in [("Revenue trend", 82), ("Order trend", 74), ("Customer retention", 81), ("Inventory readiness", 69)]:
            st.markdown(
                f'<div style="display:flex;justify-content:space-between;font-size:.78rem;">'
                f'<span>{label}</span><span>{value}</span></div>'
                f'<div class="progress"><div style="width:{value}%"></div></div>',
                unsafe_allow_html=True,
            )
        st.markdown(
            '<div class="insight warn"><strong>Watch inventory</strong><br>'
            '<span style="color:#94A3B8;">Rice and cooking oil are approaching reorder thresholds.</span></div>',
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # Billing + Inventory
    a, b = st.columns(2, gap="large")

    with a:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">💳 Billing AI</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-sub">Recover pending payments with one tap.</div>', unsafe_allow_html=True)
        for _, row in pending_payments.iterrows():
            sent = row["id"] in st.session_state.reminders_sent
            c1, c2, c3 = st.columns([2.1, 1, 1])
            c1.markdown(f"**{row['customer']}**<br><span style='color:#94A3B8'>{row['due_in']}</span>", unsafe_allow_html=True)
            c2.markdown(f"**₹{row['amount']:,}**")
            if sent:
                c3.success("Sent", icon="✓")
            elif c3.button("Remind", key=f"bill_{row['id']}"):
                st.session_state.reminders_sent.add(row["id"])
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with b:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">📦 Inventory AI</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-sub">Prevent stock-outs before they affect sales.</div>', unsafe_allow_html=True)
        for _, row in inventory[inventory["reorder_qty"] > 0].iterrows():
            ordered = row["id"] in st.session_state.reorders_placed
            c1, c2, c3 = st.columns([1.6, 1.4, 1])
            c1.markdown(f"**{row['item']}**<br><span style='color:#FB7185'>Only {row['stock']} left</span>", unsafe_allow_html=True)
            c2.markdown(f"Reorder **{row['reorder_qty']}**<br><span style='color:#94A3B8'>{row['supplier']}</span>", unsafe_allow_html=True)
            if ordered:
                c3.success("Ordered", icon="✓")
            elif c3.button("Reorder", key=f"inv_{row['id']}"):
                st.session_state.reorders_placed.add(row["id"])
                st.rerun()
        st.markdown('<div class="insight"><strong>✓ Sugar stock healthy</strong><br><span style="color:#94A3B8">30 units available.</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # AI recommendation
    st.markdown('<div class="ai-box">', unsafe_allow_html=True)
    st.markdown("### 🤖 AI Growth Copilot")
    st.markdown(
        "**Today's recommendation:** Run a small Saturday bundle for slow-moving products. "
        "Based on your recent sales pattern, the estimated incremental revenue opportunity is **₹2,300–₹3,100**."
    )
    x, y, z = st.columns([1, 1, 2])
    if x.button("⚡ Create campaign", key="overview_campaign"):
        st.session_state.campaign_created = True
        st.rerun()
    y.button("Why this?", key="why_overview")
    if st.session_state.campaign_created:
        st.success("Campaign draft created for review.", icon="✓")
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# ANALYTICS
# ============================================================
elif section == "Analytics":
    st.markdown("## 📊 Analytics")
    st.caption("A simple decision layer over merchant sales data.")

    c1, c2, c3 = st.columns(3)
    c1.metric("Weekly revenue", "₹28,400", "+11.8%")
    c2.metric("Best day", "Saturday", "₹6,500")
    c3.metric("Growth opportunity", "₹6,800", "AI estimate")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=days, y=sales_values, marker_color=GREEN, name="Revenue"))
    fig.add_trace(go.Scatter(x=days, y=[sum(sales_values)/7]*7, mode="lines", line=dict(color=YELLOW, dash="dash"), name="Weekly average"))
    fig.update_layout(
        height=400, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94A3B8"), yaxis=dict(gridcolor="rgba(148,163,184,.1)", tickprefix="₹"),
        xaxis=dict(showgrid=False), legend=dict(orientation="h"), margin=dict(l=5,r=5,t=20,b=5)
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### What changed this week?")
    st.markdown(
        '<div class="insight"><strong>↑ Revenue</strong><br><span style="color:#94A3B8">Weekend demand is driving the largest increase.</span></div>'
        '<div class="insight info"><strong>→ Customers</strong><br><span style="color:#94A3B8">Returning customers contribute a large share of recent orders.</span></div>'
        '<div class="insight warn"><strong>↓ Inventory readiness</strong><br><span style="color:#94A3B8">Two fast-moving items are close to reorder levels.</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# AI INSIGHTS
# ============================================================
elif section == "AI Insights":
    st.markdown("## 💡 AI Insights")
    st.caption("Actionable explanations instead of raw charts.")

    insights = [
        ("MEDIUM", "Wednesday Sales Alert", "Wednesday revenue is 36% below your strongest weekday.", "Test a Wednesday-specific offer.", "warn"),
        ("LOW", "Peak-Hour Opportunity", "18:00–20:00 is your strongest recent revenue window.", "Consider staffing up or promoting a limited-time offer.", "info"),
        ("MEDIUM", "Product Decline", "Filter Coffee sales have decreased over the last 14 days.", "Bundle it with a growing complementary product.", "warn"),
        ("LOW", "Product Growth", "Ice Cream Sundae sales are showing strong recent momentum.", "Feature it prominently in a complementary bundle.", "green"),
    ]
    cols = st.columns(2)
    for i, (level, title, reason, action, tone) in enumerate(insights):
        with cols[i % 2]:
            st.markdown(
                f'<div class="card"><span class="pill pill-{"yellow" if tone=="warn" else "blue" if tone=="info" else "green"}">{level}</span>'
                f'<div class="card-title">{title}</div><div class="card-sub">{reason}</div>'
                f'<div class="insight"><strong>💡 Recommendation</strong><br><span style="color:#94A3B8">{action}</span></div></div>',
                unsafe_allow_html=True,
            )

# ============================================================
# GROWTH OPPORTUNITIES
# ============================================================
elif section == "Growth Opportunities":
    st.markdown("## 🚀 Growth Opportunities")
    st.caption("Prioritized actions detected from merchant activity.")

    opportunities = [
        ("01", "Weekend bundle", "High", "₹2,300–₹3,100", "Bundle slow-moving products with a weekend bestseller."),
        ("02", "Wednesday recovery", "Medium", "₹1,500–₹2,000", "Run a Wednesday-only offer to lift the weakest weekday."),
        ("03", "Peak-hour promotion", "Medium", "₹1,200–₹1,700", "Promote offers between 18:00 and 20:00."),
        ("04", "Inventory protection", "High", "Revenue protected", "Reorder rice and cooking oil before stock-out."),
    ]
    for num, title, priority, impact, action in opportunities:
        c1, c2, c3 = st.columns([.55, 3.2, 1.2])
        c1.markdown(f"### {num}")
        with c2:
            st.markdown(f"**{title}**")
            st.caption(action)
        c3.markdown(f"**{priority}**")
        st.markdown(f'<div class="insight"><strong>Estimated impact: {impact}</strong></div>', unsafe_allow_html=True)

# ============================================================
# CUSTOMERS
# ============================================================
elif section == "Customers":
    st.markdown("## 👥 Customer Intelligence")
    st.caption("Understand who is buying and where retention can improve.")

    a, b, c, d = st.columns(4)
    a.metric("Active customers", "86", "+9.4%")
    b.metric("Returning", "64%", "+3.0%")
    c.metric("At-risk", "11", "Needs attention")
    d.metric("New this month", "18", "+12.5%")

    customer_data = pd.DataFrame([
        ["Ramesh Traders", 12400, 8, "High"],
        ["Anitha Stores", 98
