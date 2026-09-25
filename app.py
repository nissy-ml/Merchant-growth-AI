import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# ----------------------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Merchant Growth AI",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------------
# THEME / CSS (matches the pitch deck: navy + forest green)
# ----------------------------------------------------------------------------
NAVY = "#0F2A47"
GREEN = "#1F6F4A"
GREEN_LIGHT = "#DFF0E6"
GREEN_DARK = "#17573A"
TEXT_MUTED = "#5B6B78"

st.markdown(f"""
<style>
    .main {{ background-color: #FFFFFF; }}
    .block-container {{ padding-top: 1.5rem; }}

    .mg-header {{
        background-color: {NAVY};
        padding: 1.4rem 1.8rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 1.4rem;
    }}
    .mg-header h1 {{ margin: 0; font-size: 1.6rem; }}
    .mg-header p {{ margin: 0.2rem 0 0 0; color: #B9CBE0; font-size: 0.95rem; }}

    .mg-badge {{
        display: inline-block;
        background-color: rgba(255,255,255,0.12);
        border-radius: 6px;
        padding: 0.25rem 0.7rem;
        font-size: 0.75rem;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }}

    .mg-card {{
        background-color: white;
        border: 1px solid #E1E6E9;
        border-radius: 12px;
        padding: 1.1rem 1.2rem;
        margin-bottom: 0.9rem;
    }}

    .mg-section-title {{
        font-size: 1.15rem;
        font-weight: 700;
        color: #132A3A;
        margin-bottom: 0.6rem;
    }}

    .mg-banner {{
        background-color: {GREEN_LIGHT};
        color: {GREEN_DARK};
        border-radius: 10px;
        padding: 0.9rem 1.1rem;
        font-weight: 600;
        margin-top: 0.6rem;
    }}

    .mg-pill {{
        display:inline-block;
        background-color:{GREEN_LIGHT};
        color:{GREEN_DARK};
        border-radius:20px;
        padding:0.15rem 0.6rem;
        font-size:0.75rem;
        font-weight:700;
    }}

    div.stButton > button {{
        background-color: {GREEN};
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.4rem 0.9rem;
        font-weight: 600;
    }}
    div.stButton > button:hover {{
        background-color: {GREEN_DARK};
        color: white;
    }}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# SESSION STATE (so button clicks "stick" during the demo)
# ----------------------------------------------------------------------------
if "reminders_sent" not in st.session_state:
    st.session_state.reminders_sent = set()
if "reorders_placed" not in st.session_state:
    st.session_state.reorders_placed = set()
if "discount_applied" not in st.session_state:
    st.session_state.discount_applied = False

# ----------------------------------------------------------------------------
# MOCK DATA — Sri Lakshmi Kirana Store
# ----------------------------------------------------------------------------
STORE_NAME = "Sri Lakshmi Kirana Store"
STORE_LOCATION = "Kakinada, Andhra Pradesh"

pending_payments = pd.DataFrame([
    {"id": 1, "customer": "Ramesh Traders", "amount": 1500, "due_in": "3 days"},
    {"id": 2, "customer": "Anitha Stores",   "amount": 1800, "due_in": "1 day"},
    {"id": 3, "customer": "Venkat & Co.",    "amount": 900,  "due_in": "5 days"},
])

inventory = pd.DataFrame([
    {"id": 1, "item": "Rice (25kg bags)", "stock": 4,  "reorder_qty": 20, "supplier": "Godavari Wholesale"},
    {"id": 2, "item": "Cooking Oil (5L)",  "stock": 9,  "reorder_qty": 15, "supplier": "Sri Balaji Distributors"},
    {"id": 3, "item": "Sugar (1kg packs)", "stock": 30, "reorder_qty": 0,  "supplier": "—"},
])

days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
sales_values = [3100, 3000, 3700, 4100, 4700, 6500, 3300]

monthly_sales = 185000
todays_sales = 4320
pending_total = int(pending_payments["amount"].sum())

# ----------------------------------------------------------------------------
# HEADER
# ----------------------------------------------------------------------------
st.markdown(f"""
<div class="mg-header">
    <div class="mg-badge">TRACK 1 — MERCHANT GROWTH AI</div>
    <h1>{STORE_NAME}</h1>
    <p>{STORE_LOCATION} &nbsp;•&nbsp; all 3 AI teammates active</p>
</div>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# SIDEBAR
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🧭 Merchant Growth AI")
    st.caption("The AI business partner for every Paytm merchant")
    st.divider()
    st.markdown("**Team:** Merchmatrix AI")
    st.caption("Nissy Keerthana Kunche")
    st.caption("Beulah Rani Oleti")
    st.divider()
    st.markdown("**AI Teammates**")
    st.markdown("📄 Billing AI — active")
    st.markdown("📦 Inventory AI — active")
    st.markdown("📊 Insights AI — active")
    st.divider()
    st.caption("This is a working prototype using sample data to demonstrate the product experience.")

# ----------------------------------------------------------------------------
# TOP METRICS
# ----------------------------------------------------------------------------
c1, c2, c3 = st.columns(3)
c1.metric("Monthly sales", f"₹{monthly_sales:,}", "+12.4% vs last month")
c2.metric("Today's sales", f"₹{todays_sales:,}")
c3.metric("Pending payments", f"₹{pending_total:,}")

st.write("")

# ----------------------------------------------------------------------------
# TWO COLUMN LAYOUT: Billing / Inventory  |  Insights / Growth
# ----------------------------------------------------------------------------
left, right = st.columns([1, 1.15], gap="large")

with left:
    # ---- Billing AI ----
    st.markdown('<div class="mg-card">', unsafe_allow_html=True)
    st.markdown('<div class="mg-section-title">💳 Billing teammate</div>', unsafe_allow_html=True)
    st.caption("Tracks pending payments and lets you resend a reminder in one tap.")
    for _, row in pending_payments.iterrows():
        c1, c2, c3, c4 = st.columns([2.2, 1.2, 1, 1.4])
        c1.write(f"**{row['customer']}**")
        c2.write(f"₹{row['amount']:,}")
        c3.write(f"due {row['due_in']}")
        if row["id"] in st.session_state.reminders_sent:
            c4.markdown('<span class="mg-pill">✓ Sent</span>', unsafe_allow_html=True)
        else:
            if c4.button("Resend", key=f"remind_{row['id']}"):
                st.session_state.reminders_sent.add(row["id"])
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # ---- Inventory AI ----
    st.markdown('<div class="mg-card">', unsafe_allow_html=True)
    st.markdown('<div class="mg-section-title">📦 Inventory teammate</div>', unsafe_allow_html=True)
    st.caption("Flags low stock and suggests reorder quantity + preferred supplier.")
    low_stock = inventory[inventory["reorder_qty"] > 0]
    for _, row in low_stock.iterrows():
        c1, c2, c3 = st.columns([2.3, 2.2, 1.3])
        c1.write(f"**{row['item']}**  \n:red[only {row['stock']} left]")
        c2.write(f"Reorder {row['reorder_qty']} units\nfrom {row['supplier']}")
        if row["id"] in st.session_state.reorders_placed:
            c3.markdown('<span class="mg-pill">✓ Ordered</span>', unsafe_allow_html=True)
        else:
            if c3.button("Reorder", key=f"reorder_{row['id']}"):
                st.session_state.reorders_placed.add(row["id"])
                st.rerun()
    ok_item = inventory[inventory["reorder_qty"] == 0].iloc[0]
    st.caption(f"✅ {ok_item['item']} — stock healthy ({ok_item['stock']} units)")
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    # ---- Insights AI ----
    st.markdown('<div class="mg-card">', unsafe_allow_html=True)
    st.markdown('<div class="mg-section-title">📊 Insights teammate</div>', unsafe_allow_html=True)
    st.caption("Sales up 12% this week vs last week — best day: Sat")

    fig = go.Figure(go.Bar(
        x=days, y=sales_values,
        marker_color=[GREEN if d != "Sat" else GREEN_DARK for d in days],
        text=[f"₹{v:,}" for v in sales_values],
        textposition="outside",
    ))
    fig.update_layout(
        height=300,
        margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor="white",
        paper_bgcolor="white",
        yaxis=dict(showgrid=True, gridcolor="#EDEDED"),
        xaxis=dict(showgrid=False),
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

    # ---- Growth Suggestions ----
    st.markdown('<div class="mg-card">', unsafe_allow_html=True)
    st.markdown('<div class="mg-section-title">⚡ Growth suggestions</div>', unsafe_allow_html=True)
    if st.session_state.discount_applied:
        st.markdown(
            '<div class="mg-banner">✅ 5% weekend discount is live on slow movers.</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="mg-banner">⚡ Run a 5% weekend discount on slow movers — '
            '+₹2,300 potential.</div>',
            unsafe_allow_html=True,
        )
        if st.button("Apply discount", key="apply_discount"):
            st.session_state.discount_applied = True
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# FOOTER
# ----------------------------------------------------------------------------
st.write("")
st.caption("Merchmatrix AI • Merchant Growth AI — working prototype (sample data)")
