import math
from datetime import datetime
import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf

st.set_page_config(
    page_title="SmallWin Trader",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(34,197,94,.20), transparent 30%),
        radial-gradient(circle at top right, rgba(6,182,212,.18), transparent 28%),
        radial-gradient(circle at bottom right, rgba(168,85,247,.14), transparent 30%),
        linear-gradient(135deg, #07111f 0%, #0f172a 48%, #111827 100%);
    color: #f8fafc;
}

.main .block-container {
    padding-top: 2rem;
    max-width: 1250px;
}

h1, h2, h3, p, label {
    color: #f8fafc !important;
}

.hero {
    padding: 34px;
    border-radius: 30px;
    background:
        linear-gradient(135deg, rgba(15,23,42,.94), rgba(30,41,59,.90));
    border: 1px solid rgba(148,163,184,.25);
    box-shadow: 0 25px 80px rgba(0,0,0,.38);
    margin-bottom: 24px;
}

.hero-title {
    font-size: 3.1rem;
    line-height: 1;
    margin-bottom: 12px;
    font-weight: 800;
    background: linear-gradient(90deg, #ffffff, #67e8f9, #86efac);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-sub {
    color: #cbd5e1 !important;
    font-size: 1.08rem;
    max-width: 900px;
    line-height: 1.65;
}

.badge-row {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 20px;
}

.badge {
    padding: 9px 14px;
    border-radius: 999px;
    background: rgba(15,23,42,.72);
    border: 1px solid rgba(148,163,184,.28);
    color: #e2e8f0;
    font-size: .9rem;
}

.glass-card {
    padding: 26px;
    border-radius: 26px;
    background: rgba(15,23,42,.80);
    border: 1px solid rgba(148,163,184,.24);
    box-shadow: 0 20px 60px rgba(0,0,0,.25);
    margin-bottom: 18px;
}

.trade-card {
    padding: 28px;
    border-radius: 28px;
    background:
        linear-gradient(135deg, rgba(34,197,94,.16), rgba(6,182,212,.13)),
        rgba(15,23,42,.88);
    border: 1px solid rgba(45,212,191,.36);
    box-shadow: 0 20px 75px rgba(16,185,129,.10);
    margin-bottom: 20px;
}

.warning-card {
    padding: 18px;
    border-radius: 20px;
    background: rgba(251,191,36,.14);
    border: 1px solid rgba(251,191,36,.40);
    color: #fde68a !important;
    margin-bottom: 18px;
}

.success-pill, .pro-pill, .skip-pill {
    display: inline-block;
    padding: 8px 13px;
    border-radius: 999px;
    font-weight: 800;
    margin-bottom: 10px;
    font-size: .82rem;
    letter-spacing: .03em;
}

.success-pill {
    background: rgba(34,197,94,.18);
    border: 1px solid rgba(34,197,94,.42);
    color: #bbf7d0;
}

.pro-pill {
    background: rgba(6,182,212,.18);
    border: 1px solid rgba(6,182,212,.42);
    color: #a5f3fc;
}

.skip-pill {
    background: rgba(239,68,68,.18);
    border: 1px solid rgba(248,113,113,.42);
    color: #fecaca;
}

.metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(155px, 1fr));
    gap: 14px;
    margin-top: 20px;
}

.metric-card {
    padding: 18px;
    border-radius: 20px;
    background: rgba(2,6,23,.45);
    border: 1px solid rgba(148,163,184,.20);
}

.metric-label {
    color: #94a3b8 !important;
    font-size: .82rem;
    margin-bottom: 8px;
}

.metric-value {
    color: #f8fafc !important;
    font-size: 1.45rem;
    font-weight: 800;
}

.small-note {
    color: #cbd5e1 !important;
    font-size: .94rem;
    line-height: 1.6;
}

/* FIXED BUTTONS */
div.stButton > button {
    background: linear-gradient(90deg, #22c55e, #06b6d4) !important;
    color: #04111f !important;
    border: none !important;
    border-radius: 16px !important;
    padding: .75rem 1.2rem !important;
    font-weight: 900 !important;
    font-size: 1rem !important;
    box-shadow: 0 10px 30px rgba(34,197,94,.24) !important;
}

div.stButton > button:hover {
    color: #000000 !important;
    background: linear-gradient(90deg, #86efac, #67e8f9) !important;
    transform: translateY(-1px);
}

div.stButton > button:disabled {
    background: #334155 !important;
    color: #cbd5e1 !important;
    opacity: 1 !important;
}

/* Inputs */
.stTextInput input,
.stPasswordInput input,
.stNumberInput input,
textarea,
.stSelectbox div[data-baseweb="select"] {
    background-color: #f8fafc !important;
    color: #0f172a !important;
    border-radius: 12px !important;
}

.stCheckbox label span {
    color: #f8fafc !important;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    border-bottom: 1px solid rgba(148,163,184,.20);
}

.stTabs [data-baseweb="tab"] {
    border-radius: 999px;
    padding: 10px 18px;
    background: rgba(15,23,42,.55);
    color: #cbd5e1;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(90deg, rgba(34,197,94,.28), rgba(6,182,212,.22));
    color: #ffffff;
    border: 1px solid rgba(45,212,191,.30);
}
</style>
""", unsafe_allow_html=True)

DISCLAIMER = "SmallWin Trader is an educational paper-trading and risk-management app. It is not financial advice, not a broker, and not a guarantee of profit."

BEGINNER_TICKERS = ["SOFI", "RIVN", "HOOD", "BAC", "F", "PLTR", "T", "SNAP", "PFE", "CCL", "AAL", "WBD", "UBER", "LYFT", "AMD", "AAPL"]

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "plan" not in st.session_state:
    st.session_state.plan = "Free"
if "journal" not in st.session_state:
    st.session_state.journal = []

def money(value):
    try:
        return f"${float(value):,.2f}"
    except Exception:
        return "$0.00"

def safe_float(value, default=np.nan):
    try:
        return float(value)
    except Exception:
        return default

def flatten_columns(df):
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
    return df

@st.cache_data(ttl=60)
def get_data(ticker, period="5d", interval="15m"):
    data = yf.download(ticker, period=period, interval=interval, progress=False, auto_adjust=True, prepost=False, threads=False)
    data = flatten_columns(data)
    return data.dropna().copy()

def add_indicators(df):
    if df.empty:
        return df
    df = df.copy()
    df["EMA9"] = df["Close"].ewm(span=9, adjust=False).mean()
    df["EMA21"] = df["Close"].ewm(span=21, adjust=False).mean()
    delta = df["Close"].diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    rs = gain / loss.replace(0, np.nan)
    df["RSI"] = 100 - (100 / (1 + rs))
    high_low = df["High"] - df["Low"]
    high_close = (df["High"] - df["Close"].shift()).abs()
    low_close = (df["Low"] - df["Close"].shift()).abs()
    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    df["ATR"] = true_range.rolling(14).mean()
    typical_price = (df["High"] + df["Low"] + df["Close"]) / 3
    volume = df["Volume"].replace(0, np.nan)
    df["VWAP"] = (typical_price * volume).cumsum() / volume.cumsum()
    df["RelativeVolume"] = df["Volume"] / df["Volume"].rolling(20).mean().replace(0, np.nan)
    return df

def score_setup(df):
    if df.empty or len(df) < 30:
        return {"score": 0, "bias": "Not enough data", "reason": "Not enough recent data to grade this setup."}
    row = df.iloc[-1]
    prev = df.iloc[-2]
    close = safe_float(row["Close"])
    ema9 = safe_float(row["EMA9"])
    ema21 = safe_float(row["EMA21"])
    vwap = safe_float(row["VWAP"])
    rsi = safe_float(row["RSI"])
    rel_vol = safe_float(row["RelativeVolume"])
    atr = safe_float(row["ATR"])
    score = 0
    reasons = []
    if close > vwap:
        score += 20
        reasons.append("holding above VWAP")
    else:
        reasons.append("below VWAP")
    if ema9 > ema21:
        score += 20
        reasons.append("short-term momentum is leading")
    else:
        reasons.append("EMA trend is not confirmed")
    if 45 <= rsi <= 70:
        score += 20
        reasons.append("RSI is strong but not overextended")
    elif rsi > 70:
        score += 8
        reasons.append("RSI is hot, wait for pullback")
    else:
        reasons.append("RSI is weak")
    if rel_vol >= 1.0:
        score += 20
        reasons.append("volume is active")
    else:
        reasons.append("volume is light")
    if close > prev["Close"]:
        score += 10
        reasons.append("latest candle is green")
    if not math.isnan(atr) and atr > 0:
        score += 10
        reasons.append("ATR gives a usable stop")
    bias = "Strong setup" if score >= 80 else "Possible setup" if score >= 60 else "Wait" if score >= 40 else "Skip"
    return {"score": int(score), "bias": bias, "reason": ", ".join(reasons)}

def build_trade_plan(ticker, df, account_size, risk_percent, max_capital_percent):
    row = df.iloc[-1]
    price = safe_float(row["Close"])
    atr = safe_float(row["ATR"])
    vwap = safe_float(row["VWAP"])
    if math.isnan(price) or price <= 0:
        return {}
    risk_dollars = account_size * (risk_percent / 100)
    max_trade_capital = account_size * (max_capital_percent / 100)
    stop_distance = max(atr * .75 if not math.isnan(atr) else price * .015, price * .01)
    stop_loss = price - stop_distance
    if not math.isnan(vwap):
        stop_loss = min(stop_loss, vwap - (stop_distance * .15))
    risk_per_share = max(price - stop_loss, .01)
    shares_by_risk = math.floor(risk_dollars / risk_per_share)
    shares_by_capital = math.floor(max_trade_capital / price)
    shares = max(0, min(shares_by_risk, shares_by_capital))
    return {
        "ticker": ticker,
        "price": round(price, 2),
        "entry_low": round(price - risk_per_share * .25, 2),
        "entry_high": round(price + risk_per_share * .15, 2),
        "stop_loss": round(stop_loss, 2),
        "target_1": round(price + risk_per_share, 2),
        "target_2": round(price + risk_per_share * 2, 2),
        "shares": shares,
        "capital_needed": round(shares * price, 2),
        "max_loss": round(shares * risk_per_share, 2),
    }

def scan_watchlist(tickers, account_size, risk_percent, max_capital_percent, limit=None):
    rows = []
    for ticker in tickers:
        try:
            df = add_indicators(get_data(ticker))
            if df.empty or len(df) < 30:
                continue
            setup = score_setup(df)
            plan = build_trade_plan(ticker, df, account_size, risk_percent, max_capital_percent)
            if not plan:
                continue
            last = df.iloc[-1]
            rows.append({
                "Symbol": ticker,
                "Score": setup["score"],
                "Bias": setup["bias"],
                "Price": plan["price"],
                "Shares": plan["shares"],
                "Capital": plan["capital_needed"],
                "Stop": plan["stop_loss"],
                "Target 1": plan["target_1"],
                "Target 2": plan["target_2"],
                "Max Loss": plan["max_loss"],
                "RSI": round(safe_float(last["RSI"]), 1),
                "Rel Vol": round(safe_float(last["RelativeVolume"]), 2),
                "Why": setup["reason"],
            })
        except Exception:
            continue
    result = pd.DataFrame(rows)
    if result.empty:
        return result
    result = result.sort_values(by=["Score", "Shares", "Rel Vol"], ascending=[False, False, False]).reset_index(drop=True)
    return result.head(limit) if limit else result

def render_trade_card(symbol, setup, plan, reason):
    pill_class = "success-pill" if setup["score"] >= 70 and plan["shares"] >= 1 else "skip-pill"
    pill_text = "BEGINNER PRACTICE SETUP" if setup["score"] >= 70 and plan["shares"] >= 1 else "WAIT OR SKIP"
    st.markdown(f"""
    <div class="trade-card">
        <div class="{pill_class}">{pill_text}</div>
        <h2>{symbol} Trade Coach</h2>
        <p class="small-note">{reason}</p>
        <div class="metric-grid">
            <div class="metric-card"><div class="metric-label">Latest Price</div><div class="metric-value">{money(plan['price'])}</div></div>
            <div class="metric-card"><div class="metric-label">AI Score</div><div class="metric-value">{setup['score']}/100</div></div>
            <div class="metric-card"><div class="metric-label">Shares</div><div class="metric-value">{plan['shares']}</div></div>
            <div class="metric-card"><div class="metric-label">Capital Needed</div><div class="metric-value">{money(plan['capital_needed'])}</div></div>
            <div class="metric-card"><div class="metric-label">Entry Zone</div><div class="metric-value">{money(plan['entry_low'])} - {money(plan['entry_high'])}</div></div>
            <div class="metric-card"><div class="metric-label">Stop Loss</div><div class="metric-value">{money(plan['stop_loss'])}</div></div>
            <div class="metric-card"><div class="metric-label">Target 1</div><div class="metric-value">{money(plan['target_1'])}</div></div>
            <div class="metric-card"><div class="metric-label">Target 2</div><div class="metric-value">{money(plan['target_2'])}</div></div>
            <div class="metric-card"><div class="metric-label">Max Loss</div><div class="metric-value">{money(plan['max_loss'])}</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div class="hero-title">SmallWin Trader</div>
    <div class="hero-sub">Learn trading with guided practice setups, small-account risk controls, paper journaling, and beginner-friendly education.</div>
    <div class="badge-row">
        <div class="badge">Education first</div>
        <div class="badge">Paper trading</div>
        <div class="badge">Risk controls</div>
        <div class="badge">Subscription demo</div>
    </div>
</div>
""", unsafe_allow_html=True)

if not st.session_state.logged_in:
    left, right = st.columns(2)

    with left:
        st.markdown('<div class="glass-card"><h2>Welcome back</h2><p class="small-note">Log in to view your dashboard, scanner, journal, and subscription status.</p></div>', unsafe_allow_html=True)
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Log in", key="login_button"):
            if email and password:
                st.session_state.logged_in = True
                st.session_state.user_name = email.split("@")[0].title()
                st.rerun()
            else:
                st.error("Enter an email and password.")

    with right:
        st.markdown('<div class="glass-card"><h2>Create account</h2><p class="small-note">This demo stores accounts in this session only. Production should use Firebase, Supabase, Auth0, or your own backend.</p></div>', unsafe_allow_html=True)
        name = st.text_input("Name", key="signup_name")
        signup_email = st.text_input("Email address", key="signup_email")
        signup_password = st.text_input("Create password", type="password", key="signup_password")
        experience = st.selectbox("Trading experience", ["Brand new", "Beginner", "Some experience", "Advanced"])
        legal_ok = st.checkbox("I agree this app is educational only and not financial advice.")
        if st.button("Create free account", key="create_account_button"):
            if name and signup_email and signup_password and legal_ok:
                st.session_state.logged_in = True
                st.session_state.user_name = name
                st.session_state.plan = "Free"
                st.rerun()
            else:
                st.error("Fill out all fields and accept the educational disclaimer.")

    st.markdown('<div class="warning-card"><b>Launch note:</b> For real payments, do not collect card numbers here. Use Stripe Checkout for web, Apple In-App Purchases for iOS, and Google Play Billing for Android.</div>', unsafe_allow_html=True)
    st.stop()

with st.sidebar:
    st.markdown(f"## Hi, {st.session_state.user_name or 'Trader'}")
    st.session_state.plan = st.radio("Plan", ["Free", "Pro"], index=0 if st.session_state.plan == "Free" else 1)
    account_size = st.number_input("Account size", min_value=50.0, max_value=100000.0, value=500.0, step=50.0)
    risk_percent = st.slider("Max risk per trade %", min_value=.25, max_value=5.0, value=1.0, step=.25)
    max_capital_percent = st.slider("Max account used per trade %", min_value=5, max_value=100, value=65, step=5)
    custom_watchlist = st.text_area("Watchlist", value=", ".join(BEGINNER_TICKERS), height=120)
    tickers = [x.strip().upper() for x in custom_watchlist.replace("\n", ",").split(",") if x.strip()]
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.rerun()

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Dashboard", "Scanner", "Trade Coach", "Journal", "Subscribe", "Legal"])

with tab1:
    st.markdown(f'<div class="glass-card"><h2>Dashboard</h2><p class="small-note">Current plan: <b>{st.session_state.plan}</b>. Max planned risk per trade: <b>{money(account_size * risk_percent / 100)}</b>.</p></div>', unsafe_allow_html=True)
    if st.button("Find best beginner setup"):
        with st.spinner("Scanning..."):
            results = scan_watchlist(tickers, account_size, risk_percent, max_capital_percent, limit=5 if st.session_state.plan == "Free" else None)
        if results.empty:
            st.warning("No clean setup found right now.")
        else:
            affordable = results[(results["Shares"] >= 1) & (results["Bias"].isin(["Strong setup", "Possible setup"]))]
            if affordable.empty:
                st.warning("No affordable clean setup found.")
                st.dataframe(results, use_container_width=True)
            else:
                best = affordable.iloc[0]
                df = add_indicators(get_data(best["Symbol"]))
                setup = score_setup(df)
                plan = build_trade_plan(best["Symbol"], df, account_size, risk_percent, max_capital_percent)
                render_trade_card(best["Symbol"], setup, plan, best["Why"])

with tab2:
    if st.session_state.plan == "Free":
        st.markdown('<div class="warning-card">Free plan is limited to 5 scan results. Switch to Pro in the sidebar or Subscribe tab for full demo access.</div>', unsafe_allow_html=True)
    if st.button("Scan watchlist"):
        with st.spinner("Scanning watchlist..."):
            results = scan_watchlist(tickers, account_size, risk_percent, max_capital_percent, limit=5 if st.session_state.plan == "Free" else None)
        if results.empty:
            st.warning("No results came back.")
        else:
            st.dataframe(results, use_container_width=True, hide_index=True)

with tab3:
    ticker = st.text_input("Ticker to coach", value="SOFI").upper()
    if st.button("Build trade plan"):
        df = add_indicators(get_data(ticker))
        if df.empty:
            st.error("Could not pull data.")
        else:
            setup = score_setup(df)
            plan = build_trade_plan(ticker, df, account_size, risk_percent, max_capital_percent)
            render_trade_card(ticker, setup, plan, setup["reason"])
            st.line_chart(df[["Close", "EMA9", "EMA21", "VWAP"]].tail(80))

with tab4:
    with st.form("journal_form"):
        j_ticker = st.text_input("Ticker")
        j_entry = st.number_input("Entry", min_value=0.0, step=.01)
        j_stop = st.number_input("Stop", min_value=0.0, step=.01)
        j_target = st.number_input("Target", min_value=0.0, step=.01)
        j_shares = st.number_input("Shares", min_value=0, step=1)
        j_notes = st.text_area("Notes")
        submitted = st.form_submit_button("Save journal entry")
    if submitted:
        risk = max((j_entry - j_stop) * j_shares, 0)
        reward = max((j_target - j_entry) * j_shares, 0)
        st.session_state.journal.append({
            "Time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Ticker": j_ticker.upper(),
            "Entry": j_entry,
            "Stop": j_stop,
            "Target": j_target,
            "Shares": j_shares,
            "Risk": round(risk, 2),
            "Reward": round(reward, 2),
            "Notes": j_notes,
        })
    if st.session_state.journal:
        st.dataframe(pd.DataFrame(st.session_state.journal), use_container_width=True, hide_index=True)
    else:
        st.info("No journal entries yet.")

with tab5:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="glass-card"><div class="success-pill">FREE</div><h2>$0</h2><p class="small-note">Limited scanner, basic coach, journal, and lessons.</p></div>', unsafe_allow_html=True)
        if st.button("Keep Free"):
            st.session_state.plan = "Free"
            st.success("Free plan active.")
    with c2:
        st.markdown('<div class="glass-card"><div class="pro-pill">PRO</div><h2>$14.99/mo</h2><p class="small-note">Unlimited scans, full watchlist, advanced coaching, and future alerts.</p></div>', unsafe_allow_html=True)
        if st.button("Start Pro Demo"):
            st.session_state.plan = "Pro"
            st.success("Pro demo active. Real launch should connect Apple, Google, or Stripe billing.")
    st.markdown('<div class="warning-card">Payment setup for production: Stripe Checkout for web, Apple In-App Purchases for iOS, Google Play Billing for Android. Never collect raw card numbers directly inside this app.</div>', unsafe_allow_html=True)

with tab6:
    st.markdown(f'<div class="glass-card"><h2>Legal</h2><p class="small-note">{DISCLAIMER}</p><p class="small-note">Trading involves risk. Users can lose money. App content is general educational information only and should not be treated as personalized investment advice.</p></div>', unsafe_allow_html=True)
