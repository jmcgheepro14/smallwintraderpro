
import math
import hashlib
from datetime import datetime

import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf

st.set_page_config(page_title="SmallWin Trader", page_icon="📈", layout="wide", initial_sidebar_state="collapsed")

# -----------------------------
# DESIGN
# -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
html, body, [class*="css"] {font-family: 'Inter', sans-serif;}
.stApp {
  background:
    radial-gradient(circle at 8% 4%, rgba(34,197,94,.23), transparent 28%),
    radial-gradient(circle at 92% 6%, rgba(14,165,233,.23), transparent 28%),
    radial-gradient(circle at 80% 92%, rgba(168,85,247,.13), transparent 30%),
    linear-gradient(135deg, #030712 0%, #0f172a 52%, #111827 100%);
  color:#f8fafc;
}
.main .block-container {max-width: 1320px; padding-top: 1.4rem;}
section[data-testid="stSidebar"] {background:#07111f; border-right:1px solid rgba(148,163,184,.18);}
h1,h2,h3 {font-weight:900; letter-spacing:-.04em; color:#f8fafc;}
p, label, span, div {color: inherit;}
.hero {
  padding: 36px; border-radius: 32px; margin-bottom: 22px;
  background: linear-gradient(135deg, rgba(15,23,42,.95), rgba(30,41,59,.88));
  border:1px solid rgba(148,163,184,.24);
  box-shadow: 0 30px 100px rgba(0,0,0,.42);
}
.hero-title {
  font-size: 3.35rem; line-height: .95; margin-bottom: 13px;
  background: linear-gradient(90deg, #fff, #67e8f9, #86efac);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero-sub {color:#cbd5e1; font-size:1.08rem; line-height:1.65; max-width:900px;}
.badge-row {display:flex; gap:10px; flex-wrap:wrap; margin-top:20px;}
.badge {padding:9px 14px; border-radius:999px; background:rgba(15,23,42,.72); border:1px solid rgba(148,163,184,.28); color:#e2e8f0; font-size:.9rem;}
.card, .glass-card {
  padding:24px; border-radius:26px; background:rgba(15,23,42,.80);
  border:1px solid rgba(148,163,184,.22); box-shadow:0 20px 70px rgba(0,0,0,.28); margin-bottom:18px;
}
.trade-card {
  padding:28px; border-radius:30px;
  background:linear-gradient(135deg, rgba(34,197,94,.17), rgba(6,182,212,.13)), rgba(15,23,42,.9);
  border:1px solid rgba(45,212,191,.38);
  box-shadow:0 25px 85px rgba(16,185,129,.12); margin-bottom:20px;
}
.warning-card {padding:20px; border-radius:22px; background:rgba(251,191,36,.12); border:1px solid rgba(251,191,36,.36); color:#fde68a; margin-bottom:18px;}
.danger-card {padding:20px; border-radius:22px; background:rgba(239,68,68,.12); border:1px solid rgba(248,113,113,.36); color:#fecaca; margin-bottom:18px;}
.success-card {padding:20px; border-radius:22px; background:rgba(34,197,94,.12); border:1px solid rgba(34,197,94,.36); color:#bbf7d0; margin-bottom:18px;}
.pill {display:inline-block; padding:8px 13px; border-radius:999px; font-weight:900; font-size:.78rem; letter-spacing:.04em; margin-bottom:10px;}
.pill-green {background:rgba(34,197,94,.18); border:1px solid rgba(34,197,94,.42); color:#bbf7d0;}
.pill-blue {background:rgba(6,182,212,.18); border:1px solid rgba(6,182,212,.42); color:#a5f3fc;}
.pill-red {background:rgba(239,68,68,.18); border:1px solid rgba(248,113,113,.42); color:#fecaca;}
.metric-grid {display:grid; grid-template-columns:repeat(auto-fit,minmax(155px,1fr)); gap:14px; margin-top:18px;}
.metric-card {padding:18px; border-radius:20px; background:rgba(2,6,23,.45); border:1px solid rgba(148,163,184,.20);}
.metric-label {color:#94a3b8; font-size:.82rem; margin-bottom:8px;}
.metric-value {color:#f8fafc; font-size:1.45rem; font-weight:900;}
.small-note {color:#cbd5e1; font-size:.94rem; line-height:1.65;}
.price {font-size:2.4rem; font-weight:900; color:#fff;}
div.stButton > button:first-child {
  background:linear-gradient(90deg,#22c55e,#06b6d4); color:#07111f; border:0; border-radius:16px;
  padding:.75rem 1.2rem; font-weight:900; box-shadow:0 10px 30px rgba(34,197,94,.22);
}
div.stButton > button:first-child:hover {transform:translateY(-1px); box-shadow:0 14px 35px rgba(6,182,212,.25);}
.stTabs [data-baseweb="tab-list"] {gap:8px; border-bottom:1px solid rgba(148,163,184,.20);}
.stTabs [data-baseweb="tab"] {border-radius:999px; padding:10px 18px; background:rgba(15,23,42,.55); color:#cbd5e1;}
.stTabs [aria-selected="true"] {background:linear-gradient(90deg,rgba(34,197,94,.28),rgba(6,182,212,.22)); color:#fff; border:1px solid rgba(45,212,191,.30);}
.auth-box {max-width: 520px; margin: 40px auto;}
.locked {filter: blur(1px); opacity:.55;}
</style>
""", unsafe_allow_html=True)

DISCLAIMER = "Educational use only. SmallWin Trader is not a broker, investment adviser, or guarantee of profit. Trade decisions are your responsibility."
BEGINNER_TICKERS = ["SOFI","RIVN","HOOD","BAC","F","PLTR","T","SNAP","PFE","CCL","AAL","WBD","UBER","LYFT","AMD","AAPL","NIO","LCID"]

# -----------------------------
# DEMO DATABASE
# -----------------------------
if "users" not in st.session_state:
    st.session_state.users = {}
if "user" not in st.session_state:
    st.session_state.user = None
if "journal" not in st.session_state:
    st.session_state.journal = []

def hash_pw(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

def current_user():
    if not st.session_state.user:
        return None
    return st.session_state.users.get(st.session_state.user)

def is_pro():
    u = current_user()
    return bool(u and u.get("plan") in ["Pro","Elite"])

# -----------------------------
# MARKET HELPERS
# -----------------------------
def money(v):
    try: return f"${float(v):,.2f}"
    except Exception: return "$0.00"

def safe_float(value, default=np.nan):
    try: return float(value)
    except Exception: return default

def flatten_columns(df):
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
    return df

@st.cache_data(ttl=60)
def get_data(ticker, period="5d", interval="15m"):
    data = yf.download(ticker, period=period, interval=interval, progress=False, auto_adjust=True, prepost=False, threads=False)
    return flatten_columns(data).dropna().copy()

def add_indicators(df):
    if df.empty: return df
    df = df.copy()
    df["EMA9"] = df["Close"].ewm(span=9, adjust=False).mean()
    df["EMA21"] = df["Close"].ewm(span=21, adjust=False).mean()
    delta = df["Close"].diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    rs = gain / loss.replace(0, np.nan)
    df["RSI"] = 100 - (100 / (1 + rs))
    tr = pd.concat([(df["High"]-df["Low"]), (df["High"]-df["Close"].shift()).abs(), (df["Low"]-df["Close"].shift()).abs()], axis=1).max(axis=1)
    df["ATR"] = tr.rolling(14).mean()
    typical = (df["High"] + df["Low"] + df["Close"]) / 3
    vol = df["Volume"].replace(0, np.nan)
    df["VWAP"] = (typical * vol).cumsum() / vol.cumsum()
    df["RelativeVolume"] = df["Volume"] / df["Volume"].rolling(20).mean().replace(0, np.nan)
    return df

def score_setup(df):
    if df.empty or len(df) < 30:
        return {"score":0,"bias":"Not enough data","reason":"Not enough recent data."}
    r, p = df.iloc[-1], df.iloc[-2]
    close, ema9, ema21, vwap, rsi, rv, atr = [safe_float(r[x]) for x in ["Close","EMA9","EMA21","VWAP","RSI","RelativeVolume","ATR"]]
    score, reasons = 0, []
    if close > vwap: score += 20; reasons.append("price is holding above VWAP")
    else: reasons.append("price is below VWAP")
    if ema9 > ema21: score += 20; reasons.append("short-term momentum is leading")
    else: reasons.append("EMA trend is not confirmed")
    if 45 <= rsi <= 70: score += 20; reasons.append("RSI is strong but not overextended")
    elif rsi > 70: score += 8; reasons.append("RSI is hot, wait for pullback")
    else: reasons.append("RSI is weak")
    if rv >= 1: score += 20; reasons.append("volume is active")
    else: reasons.append("volume is light")
    if close > p["Close"]: score += 10; reasons.append("latest candle is green")
    if not math.isnan(atr) and atr > 0: score += 10; reasons.append("ATR gives a usable stop")
    bias = "Strong setup" if score >= 80 else "Possible setup" if score >= 60 else "Wait" if score >= 40 else "Skip"
    return {"score":int(score), "bias":bias, "reason":", ".join(reasons)}

def trade_plan(ticker, df, account, risk_pct, max_cap_pct):
    r = df.iloc[-1]
    price, atr, vwap = safe_float(r["Close"]), safe_float(r["ATR"]), safe_float(r["VWAP"])
    if math.isnan(price) or price <= 0: return {}
    risk_dollars = account * risk_pct / 100
    max_capital = account * max_cap_pct / 100
    stop_distance = max(atr*.75 if not math.isnan(atr) else price*.015, price*.01)
    stop = price - stop_distance
    if not math.isnan(vwap): stop = min(stop, vwap - stop_distance*.15)
    risk_per_share = max(price-stop, .01)
    shares = max(0, min(math.floor(risk_dollars/risk_per_share), math.floor(max_capital/price)))
    return {"ticker":ticker, "price":round(price,2), "entry_low":round(price-risk_per_share*.25,2), "entry_high":round(price+risk_per_share*.15,2), "stop":round(stop,2), "target1":round(price+risk_per_share,2), "target2":round(price+risk_per_share*2,2), "shares":shares, "capital":round(shares*price,2), "max_loss":round(shares*risk_per_share,2), "risk_per_share":round(risk_per_share,2)}

def scan(tickers, account, risk_pct, max_cap_pct, limit=None):
    rows = []
    for t in tickers:
        try:
            df = add_indicators(get_data(t))
            if df.empty or len(df) < 30: continue
            s, p = score_setup(df), trade_plan(t, df, account, risk_pct, max_cap_pct)
            if not p: continue
            row = df.iloc[-1]
            rows.append({"Symbol":t, "Score":s["score"], "Bias":s["bias"], "Price":p["price"], "Shares":p["shares"], "Capital":p["capital"], "Entry Low":p["entry_low"], "Entry High":p["entry_high"], "Stop":p["stop"], "Target 1":p["target1"], "Target 2":p["target2"], "Max Loss":p["max_loss"], "RSI":round(safe_float(row["RSI"]),1), "Rel Vol":round(safe_float(row["RelativeVolume"]),2), "Why":s["reason"]})
        except Exception:
            continue
    out = pd.DataFrame(rows)
    if out.empty: return out
    out = out.sort_values(["Score","Shares","Rel Vol"], ascending=[False,False,False]).reset_index(drop=True)
    return out.head(limit) if limit else out

def render_plan(symbol, setup, plan, reason):
    pill = "pill-green" if setup["score"] >= 70 and plan["shares"] > 0 else "pill-red"
    label = "PRACTICE SETUP" if setup["score"] >= 70 and plan["shares"] > 0 else "WAIT OR SKIP"
    st.markdown(f"""
    <div class="trade-card">
      <span class="pill {pill}">{label}</span>
      <h2>{symbol} Trade Coach</h2>
      <p class="small-note">{reason}</p>
      <div class="metric-grid">
        <div class="metric-card"><div class="metric-label">Latest Price</div><div class="metric-value">{money(plan['price'])}</div></div>
        <div class="metric-card"><div class="metric-label">Score</div><div class="metric-value">{setup['score']}/100</div></div>
        <div class="metric-card"><div class="metric-label">Shares</div><div class="metric-value">{plan['shares']}</div></div>
        <div class="metric-card"><div class="metric-label">Capital Needed</div><div class="metric-value">{money(plan['capital'])}</div></div>
        <div class="metric-card"><div class="metric-label">Entry Zone</div><div class="metric-value">{money(plan['entry_low'])} - {money(plan['entry_high'])}</div></div>
        <div class="metric-card"><div class="metric-label">Stop Loss</div><div class="metric-value">{money(plan['stop'])}</div></div>
        <div class="metric-card"><div class="metric-label">Target 1</div><div class="metric-value">{money(plan['target1'])}</div></div>
        <div class="metric-card"><div class="metric-label">Target 2</div><div class="metric-value">{money(plan['target2'])}</div></div>
        <div class="metric-card"><div class="metric-label">Max Loss</div><div class="metric-value">{money(plan['max_loss'])}</div></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# AUTH SCREENS
# -----------------------------
def auth_screen():
    st.markdown('<div class="hero"><div class="hero-title">SmallWin Trader</div><div class="hero-sub">Learn trading with guided practice setups, small-account risk controls, paper journaling, and beginner-friendly education.</div><div class="badge-row"><div class="badge">Education first</div><div class="badge">Paper trading</div><div class="badge">Risk controls</div><div class="badge">Pro subscription demo</div></div></div>', unsafe_allow_html=True)
    left, right = st.columns([1,1])
    with left:
        st.markdown('<div class="card"><h2>Welcome back</h2><p class="small-note">Log in to view your dashboard, scanner, journal, and subscription status.</p></div>', unsafe_allow_html=True)
        with st.form("login"):
            email = st.text_input("Email")
            pw = st.text_input("Password", type="password")
            ok = st.form_submit_button("Log in")
        if ok:
            user = st.session_state.users.get(email.lower())
            if user and user["password"] == hash_pw(pw):
                st.session_state.user = email.lower()
                st.rerun()
            else:
                st.error("Login failed. Create an account first or check your password.")
    with right:
        st.markdown('<div class="card"><h2>Create account</h2><p class="small-note">This demo stores accounts in session only. Production should use Firebase, Supabase, Auth0, or your own backend.</p></div>', unsafe_allow_html=True)
        with st.form("signup"):
            name = st.text_input("Name")
            email2 = st.text_input("Email address")
            pw2 = st.text_input("Create password", type="password")
            experience = st.selectbox("Trading experience", ["Brand new", "Some practice", "Intermediate"])
            consent = st.checkbox("I agree this app is educational only and not financial advice.")
            created = st.form_submit_button("Create free account")
        if created:
            if not consent:
                st.warning("You must accept the educational-use disclaimer.")
            elif not email2 or not pw2:
                st.warning("Email and password are required.")
            else:
                st.session_state.users[email2.lower()] = {"name":name or "Trader", "email":email2.lower(), "password":hash_pw(pw2), "plan":"Free", "experience":experience, "created":str(datetime.now())}
                st.session_state.user = email2.lower()
                st.rerun()
    st.markdown('<div class="warning-card"><b>Launch note:</b> This is a working app prototype. For real paid launch, connect secure authentication and official app-store billing.</div>', unsafe_allow_html=True)

if not st.session_state.user:
    auth_screen()
    st.stop()

u = current_user()

# -----------------------------
# APP
# -----------------------------
with st.sidebar:
    st.markdown(f"## 👋 {u.get('name','Trader')}")
    st.caption(f"Plan: {u.get('plan','Free')}")
    if st.button("Log out"):
        st.session_state.user = None
        st.rerun()
    st.markdown("## ⚙️ Account")
    account = st.number_input("Practice account size", min_value=50.0, max_value=100000.0, value=500.0, step=50.0)
    risk_pct = st.slider("Max risk per trade %", .25, 5.0, 1.0, .25)
    max_cap_pct = st.slider("Max account used per trade %", 5, 100, 65, 5)
    st.markdown("## 👀 Watchlist")
    custom = st.text_area("Tickers", value=", ".join(BEGINNER_TICKERS), height=130)
    tickers = [x.strip().upper() for x in custom.replace("\n",",").split(",") if x.strip()]

st.markdown(f"""
<div class="hero">
  <div class="hero-title">SmallWin Trader</div>
  <div class="hero-sub">A subscription-ready beginner trading education app with login, account dashboard, Pro feature locks, checkout screens, paper trading, legal screens, and live stock practice tools.</div>
  <div class="badge-row">
    <div class="badge">Current plan: {u.get('plan','Free')}</div>
    <div class="badge">Max planned risk: {money(account*risk_pct/100)}</div>
    <div class="badge">Educational only</div>
    <div class="badge">Paper trading first</div>
  </div>
</div>
""", unsafe_allow_html=True)

tabs = st.tabs(["🏠 Dashboard","🏆 Best Setup","🔎 Scanner","🎓 Coach","📓 Journal","💳 Upgrade","👤 Account","⚖️ Legal"])

with tabs[0]:
    c1,c2,c3 = st.columns(3)
    c1.markdown(f'<div class="card"><span class="pill pill-green">ACCOUNT</span><h2>{money(account)}</h2><p class="small-note">Practice account size</p></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="card"><span class="pill pill-blue">RISK</span><h2>{money(account*risk_pct/100)}</h2><p class="small-note">Max planned risk per trade</p></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="card"><span class="pill pill-blue">PLAN</span><h2>{u.get("plan","Free")}</h2><p class="small-note">Subscription status</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="warning-card"><b>Beginner rule:</b> Your first job is not to make big money. Your first job is to follow the plan, use paper trading, and protect the account.</div>', unsafe_allow_html=True)

with tabs[1]:
    if st.button("Find my best setup"):
        with st.spinner("Scanning live market data..."):
            results = scan(tickers, account, risk_pct, max_cap_pct, limit=5 if not is_pro() else None)
        if results.empty:
            st.error("No setup found right now.")
        else:
            affordable = results[(results["Shares"] >= 1) & (results["Bias"].isin(["Strong setup","Possible setup"]))]
            if affordable.empty:
                st.warning("No clean affordable setup found. Skipping is part of trading.")
                st.dataframe(results, use_container_width=True, hide_index=True)
            else:
                best = affordable.iloc[0]
                df = add_indicators(get_data(best["Symbol"]))
                s = score_setup(df); p = trade_plan(best["Symbol"], df, account, risk_pct, max_cap_pct)
                render_plan(best["Symbol"], s, p, best["Why"])

with tabs[2]:
    if not is_pro():
        st.markdown('<div class="warning-card"><b>Free plan:</b> scanner is limited to 5 results. Upgrade to Pro for full watchlist scans and future alerts.</div>', unsafe_allow_html=True)
    if st.button("Scan watchlist"):
        with st.spinner("Scanning..."):
            results = scan(tickers, account, risk_pct, max_cap_pct, limit=5 if not is_pro() else None)
        if results.empty:
            st.error("No results returned.")
        else:
            st.dataframe(results, use_container_width=True, hide_index=True)
            st.download_button("Download CSV", results.to_csv(index=False), "smallwin_scan.csv")

with tabs[3]:
    ticker = st.text_input("Ticker to coach", "SOFI").upper()
    if st.button("Build trade plan"):
        df = add_indicators(get_data(ticker))
        if df.empty:
            st.error("Could not pull data.")
        else:
            s = score_setup(df); p = trade_plan(ticker, df, account, risk_pct, max_cap_pct)
            render_plan(ticker, s, p, s["reason"])
            st.line_chart(df[["Close","EMA9","EMA21","VWAP"]].tail(80))

with tabs[4]:
    with st.form("journal"):
        c1,c2,c3=st.columns(3)
        with c1:
            jt=st.text_input("Ticker")
            je=st.number_input("Entry", min_value=0.0, step=.01)
        with c2:
            js=st.number_input("Stop", min_value=0.0, step=.01)
            jtar=st.number_input("Target", min_value=0.0, step=.01)
        with c3:
            jsh=st.number_input("Shares", min_value=0, step=1)
            jr=st.selectbox("Result", ["Open","Win","Loss","Breakeven"])
        reason=st.text_area("Why did you take it?")
        sub=st.form_submit_button("Save paper trade")
    if sub:
        risk=max((je-js)*jsh,0); reward=max((jtar-je)*jsh,0)
        st.session_state.journal.append({"Time":datetime.now().strftime("%Y-%m-%d %H:%M"),"Ticker":jt.upper(),"Entry":je,"Stop":js,"Target":jtar,"Shares":jsh,"Risk $":round(risk,2),"Reward $":round(reward,2),"R/R":round(reward/risk,2) if risk else 0,"Result":jr,"Reason":reason})
        st.success("Saved.")
    if st.session_state.journal:
        st.dataframe(pd.DataFrame(st.session_state.journal), use_container_width=True, hide_index=True)
    else:
        st.info("No paper trades yet.")

with tabs[5]:
    st.markdown('<div class="card"><h2>Choose your plan</h2><p class="small-note">This is a demo checkout screen. Production should use Apple In-App Purchases, Google Play Billing, or Stripe for web.</p></div>', unsafe_allow_html=True)
    a,b,c=st.columns(3)
    with a:
        st.markdown('<div class="card"><span class="pill pill-green">FREE</span><h2>$0</h2><p class="small-note">Limited scanner, basic coach, paper journal, beginner lessons.</p></div>', unsafe_allow_html=True)
        if st.button("Use Free"):
            u["plan"]="Free"; st.success("Plan set to Free.")
    with b:
        st.markdown('<div class="trade-card"><span class="pill pill-blue">PRO</span><h2>$14.99/mo</h2><p class="small-note">Unlimited scans, full watchlist, Pro coach, exports, future alerts.</p></div>', unsafe_allow_html=True)
        if st.button("Start Pro demo checkout"):
            st.session_state.checkout = "Pro"
    with c:
        st.markdown('<div class="card"><span class="pill pill-blue">ELITE</span><h2>$29.99/mo</h2><p class="small-note">Advanced education, market recap, strategy tracking, community features.</p></div>', unsafe_allow_html=True)
        if st.button("Start Elite demo checkout"):
            st.session_state.checkout = "Elite"
    if st.session_state.get("checkout"):
        st.markdown('<div class="card"><h2>Secure Checkout Demo</h2><p class="small-note">Do not collect real card numbers in Streamlit. This screen shows where Apple Pay, Google Play Billing, or Stripe Checkout would launch.</p></div>', unsafe_allow_html=True)
        st.text_input("Name on card", placeholder="Demo only")
        st.text_input("Card number", placeholder="Do not enter real payment information")
        agree = st.checkbox("I agree to the subscription terms and educational-use disclaimer.")
        if st.button("Activate demo subscription"):
            if agree:
                u["plan"] = st.session_state.checkout
                st.session_state.checkout = None
                st.success("Demo subscription activated.")
                st.rerun()
            else:
                st.warning("Accept the terms first.")

with tabs[6]:
    st.markdown(f'<div class="card"><h2>Account</h2><p class="small-note">Email: {u["email"]}<br>Plan: {u["plan"]}<br>Experience: {u["experience"]}</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="warning-card"><b>Production needed:</b> replace demo login with Firebase/Supabase/Auth0, encrypted database storage, password reset, email verification, and real payment receipts.</div>', unsafe_allow_html=True)

with tabs[7]:
    legal = st.selectbox("Legal page", ["Risk Disclaimer","No Financial Advice","Privacy Policy","Terms of Service","Subscription Terms","Refund Policy"])
    copy = {
        "Risk Disclaimer":"Trading involves risk. You can lose money. App content is for education, paper trading, and risk-management practice only.",
        "No Financial Advice":"SmallWin Trader does not provide personalized investment, trading, tax, or financial advice.",
        "Privacy Policy":"Production apps should disclose account data, journal data, analytics, payments, retention, deletion, and support contacts.",
        "Terms of Service":"Users agree not to treat app content as a direct instruction to buy or sell securities.",
        "Subscription Terms":"Subscriptions renew automatically unless canceled. Mobile subscriptions should use Apple In-App Purchases or Google Play Billing.",
        "Refund Policy":"iOS refunds are handled by Apple. Android refunds are handled by Google Play. Web refunds follow your Stripe/web policy."
    }
    st.markdown(f'<div class="card"><h2>{legal}</h2><p class="small-note">{copy[legal]}</p></div>', unsafe_allow_html=True)

st.caption(DISCLAIMER)
