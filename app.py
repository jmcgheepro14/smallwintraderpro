import math
from datetime import datetime
import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf

st.set_page_config(
    page_title="SmallWin Trader Pro",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp {
    background:
        radial-gradient(circle at top left, rgba(34,197,94,.22), transparent 30%),
        radial-gradient(circle at top right, rgba(6,182,212,.18), transparent 28%),
        linear-gradient(135deg, #07111f 0%, #0f172a 48%, #111827 100%);
    color: #f8fafc;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #07111f 0%, #111827 100%);
    border-right: 1px solid rgba(148,163,184,.18);
}

.main .block-container { padding-top: 2rem; max-width: 1320px; }

h1, h2, h3 { color: #f8fafc; font-weight: 800; letter-spacing: -.03em; }

.hero {
    padding: 34px;
    border-radius: 30px;
    background:
        linear-gradient(135deg, rgba(15,23,42,.94), rgba(30,41,59,.88)),
        linear-gradient(90deg, rgba(34,197,94,.15), rgba(6,182,212,.15));
    border: 1px solid rgba(148,163,184,.25);
    box-shadow: 0 25px 80px rgba(0,0,0,.38);
    margin-bottom: 24px;
}

.hero-title {
    font-size: 3.35rem;
    line-height: 1;
    margin-bottom: 12px;
    background: linear-gradient(90deg, #ffffff, #67e8f9, #86efac);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-sub {
    color: #cbd5e1;
    font-size: 1.08rem;
    max-width: 840px;
    line-height: 1.65;
}

.badge-row { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 20px; }

.badge {
    padding: 9px 14px;
    border-radius: 999px;
    background: rgba(15,23,42,.72);
    border: 1px solid rgba(148,163,184,.28);
    color: #e2e8f0;
    font-size: .9rem;
}

.glass-card {
    padding: 24px;
    border-radius: 24px;
    background: rgba(15,23,42,.78);
    border: 1px solid rgba(148,163,184,.22);
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
    padding: 20px;
    border-radius: 22px;
    background: rgba(251,191,36,.12);
    border: 1px solid rgba(251,191,36,.36);
    color: #fde68a;
    margin-bottom: 18px;
}

.danger-card {
    padding: 20px;
    border-radius: 22px;
    background: rgba(239,68,68,.12);
    border: 1px solid rgba(248,113,113,.36);
    color: #fecaca;
    margin-bottom: 18px;
}

.success-pill, .skip-pill {
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

.metric-label { color: #94a3b8; font-size: .82rem; margin-bottom: 8px; }
.metric-value { color: #f8fafc; font-size: 1.45rem; font-weight: 800; }
.small-note { color: #cbd5e1; font-size: .94rem; line-height: 1.6; }

div.stButton > button:first-child {
    background: linear-gradient(90deg, #22c55e, #06b6d4);
    color: #07111f;
    border: 0;
    border-radius: 16px;
    padding: .75rem 1.2rem;
    font-weight: 800;
    box-shadow: 0 10px 30px rgba(34,197,94,.22);
}

div.stButton > button:first-child:hover {
    transform: translateY(-1px);
    box-shadow: 0 14px 35px rgba(6,182,212,.25);
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

[data-testid="stDataFrame"] {
    border-radius: 18px;
    overflow: hidden;
    border: 1px solid rgba(148,163,184,.18);
}

.lesson-box {
    padding: 22px;
    border-radius: 22px;
    background: rgba(30,41,59,.72);
    border: 1px solid rgba(148,163,184,.22);
    margin-bottom: 14px;
}
</style>
""", unsafe_allow_html=True)

DISCLAIMER = "SmallWin Trader Pro is an educational trading practice tool. It is not financial advice, not a broker, and not a guarantee of profit. Use paper trading first and verify prices in your brokerage app."

BEGINNER_TICKERS = ["SOFI", "RIVN", "HOOD", "BAC", "F", "PLTR", "T", "SNAP", "PFE", "CCL", "AAL", "WBD", "UBER", "LYFT", "AMD", "AAPL", "NIO", "LCID"]

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

    if score >= 80:
        bias = "Strong setup"
    elif score >= 60:
        bias = "Possible setup"
    elif score >= 40:
        bias = "Wait"
    else:
        bias = "Skip"

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
        "target_1_profit": round(shares * risk_per_share, 2),
        "target_2_profit": round(shares * risk_per_share * 2, 2),
        "risk_per_share": round(risk_per_share, 2),
    }

def scan_watchlist(tickers, account_size, risk_percent, max_capital_percent):
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
                "ATR": round(safe_float(last["ATR"]), 2),
                "Rel Vol": round(safe_float(last["RelativeVolume"]), 2),
                "Why": setup["reason"],
            })
        except Exception:
            continue

    result = pd.DataFrame(rows)
    if result.empty:
        return result
    return result.sort_values(by=["Score", "Shares", "Rel Vol"], ascending=[False, False, False]).reset_index(drop=True)

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
    <div class="hero-title">SmallWin Trader Pro</div>
    <div class="hero-sub">
        A beginner-friendly trading coach that scans live stocks, builds simple practice plans,
        teaches entries and exits, and keeps risk small while you learn.
    </div>
    <div class="badge-row">
        <div class="badge">📍 Entry zones</div>
        <div class="badge">🛑 Stop losses</div>
        <div class="badge">🎯 Profit targets</div>
        <div class="badge">📓 Paper journal</div>
        <div class="badge">🧠 Beginner lessons</div>
    </div>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## ⚙️ Account Setup")
    account_size = st.number_input("Account size", min_value=50.0, max_value=100000.0, value=500.0, step=50.0)
    risk_percent = st.slider("Max risk per trade %", min_value=.25, max_value=5.0, value=1.0, step=.25)
    max_capital_percent = st.slider("Max account used per trade %", min_value=5, max_value=100, value=65, step=5)

    st.markdown("## 👀 Watchlist")
    custom_watchlist = st.text_area("Tickers", value=", ".join(BEGINNER_TICKERS), height=140)
    tickers = [x.strip().upper() for x in custom_watchlist.replace("\n", ",").split(",") if x.strip()]

    st.markdown(f"""
    <div class="glass-card">
        <b>Beginner guardrail</b>
        <p class="small-note">At {risk_percent:.2f}% risk, your max planned loss per trade is <b>{money(account_size * risk_percent / 100)}</b>.</p>
    </div>
    """, unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏆 Best Setup", "🔎 Scanner", "🎓 Trade Coach", "📓 Journal", "📚 Lessons"])

with tab1:
    st.markdown('<div class="glass-card"><h3>Find one realistic beginner setup</h3><p class="small-note">This filters for setups that fit your account size instead of showing trades that require too much money.</p></div>', unsafe_allow_html=True)
    if st.button("Find best setup now"):
        with st.spinner("Scanning live stock data..."):
            results = scan_watchlist(tickers, account_size, risk_percent, max_capital_percent)
        if results.empty:
            st.markdown('<div class="danger-card">No setup came back right now. Try again during regular market hours.</div>', unsafe_allow_html=True)
        else:
            affordable = results[(results["Shares"] >= 1) & (results["Bias"].isin(["Strong setup", "Possible setup"]))]
            if affordable.empty:
                st.markdown('<div class="warning-card">No clean affordable setup found. Skipping bad trades is part of trading.</div>', unsafe_allow_html=True)
                st.dataframe(results, use_container_width=True, hide_index=True)
            else:
                best = affordable.iloc[0]
                df = add_indicators(get_data(best["Symbol"]))
                setup = score_setup(df)
                plan = build_trade_plan(best["Symbol"], df, account_size, risk_percent, max_capital_percent)
                render_trade_card(best["Symbol"], setup, plan, best["Why"])
                st.markdown('<div class="warning-card"><b>Beginner rule:</b> Do not enter just because the app found it. Wait for price to hold above VWAP, avoid chasing, and place the stop loss immediately.</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="glass-card"><h3>Live beginner scanner</h3><p class="small-note">Ranks stocks by trend, VWAP, EMA alignment, RSI, volume, affordability, and risk control.</p></div>', unsafe_allow_html=True)
    if st.button("Scan watchlist"):
        with st.spinner("Scanning watchlist..."):
            results = scan_watchlist(tickers, account_size, risk_percent, max_capital_percent)
        if results.empty:
            st.markdown('<div class="danger-card">No results came back. Check tickers or try again during market hours.</div>', unsafe_allow_html=True)
        else:
            st.dataframe(results, use_container_width=True, hide_index=True)
            st.download_button("Download scan results", data=results.to_csv(index=False).encode("utf-8"), file_name="smallwin_scan_results.csv", mime="text/csv")

with tab3:
    st.markdown('<div class="glass-card"><h3>Build a trade plan for any ticker</h3><p class="small-note">Use this when you want to practice with a specific stock.</p></div>', unsafe_allow_html=True)
    ticker = st.text_input("Ticker", value="SOFI").upper()
    if st.button("Coach this ticker"):
        with st.spinner(f"Building plan for {ticker}..."):
            df = add_indicators(get_data(ticker))
        if df.empty:
            st.markdown('<div class="danger-card">Could not pull data for that ticker.</div>', unsafe_allow_html=True)
        else:
            setup = score_setup(df)
            plan = build_trade_plan(ticker, df, account_size, risk_percent, max_capital_percent)
            render_trade_card(ticker, setup, plan, setup["reason"])
            st.markdown('<div class="glass-card"><h3>Price, EMA, and VWAP chart</h3></div>', unsafe_allow_html=True)
            st.line_chart(df[["Close", "EMA9", "EMA21", "VWAP"]].tail(80))
            if setup["score"] < 70:
                st.markdown('<div class="warning-card">This is not clean enough for a beginner yet. Waiting is better than forcing a trade.</div>', unsafe_allow_html=True)

with tab4:
    st.markdown('<div class="glass-card"><h3>Paper trade journal</h3><p class="small-note">Your first goal is not profit. Your first goal is proving you can follow your plan.</p></div>', unsafe_allow_html=True)

    if "journal" not in st.session_state:
        st.session_state["journal"] = []

    with st.form("journal_form"):
        c1, c2, c3 = st.columns(3)
        with c1:
            j_ticker = st.text_input("Ticker")
            j_entry = st.number_input("Entry price", min_value=0.0, value=0.0, step=.01)
        with c2:
            j_stop = st.number_input("Stop loss", min_value=0.0, value=0.0, step=.01)
            j_target = st.number_input("Target", min_value=0.0, value=0.0, step=.01)
        with c3:
            j_shares = st.number_input("Shares", min_value=0, value=0, step=1)
            j_result = st.selectbox("Result", ["Open", "Win", "Loss", "Breakeven"])
        j_reason = st.text_area("Why did you take this trade?")
        submitted = st.form_submit_button("Save practice trade")

    if submitted:
        risk = max((j_entry - j_stop) * j_shares, 0)
        reward = max((j_target - j_entry) * j_shares, 0)
        rr = round(reward / risk, 2) if risk > 0 else 0
        st.session_state["journal"].append({
            "Time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Ticker": j_ticker.upper(),
            "Entry": j_entry,
            "Stop": j_stop,
            "Target": j_target,
            "Shares": j_shares,
            "Risk $": round(risk, 2),
            "Reward $": round(reward, 2),
            "R/R": rr,
            "Result": j_result,
            "Reason": j_reason,
        })
        st.success("Practice trade saved.")

    if st.session_state["journal"]:
        st.dataframe(pd.DataFrame(st.session_state["journal"]), use_container_width=True, hide_index=True)
    else:
        st.info("No paper trades logged yet.")

with tab5:
    lessons = [
        ("Scanner vs. trade", "The scanner finds candidates. You still need confirmation, entry timing, stop loss, and discipline."),
        ("Small wins are the goal", "With a small account, a $5 to $20 practice win is more realistic than forcing huge gains."),
        ("Stop loss first", "Before you enter, know exactly where the trade is wrong. If the stop is too wide, skip it."),
        ("Do not chase", "If a stock already ran hard, wait for a pullback. Beginners usually lose by buying too high."),
        ("Paper trade first", "Practice until you can follow the plan without moving stops or revenge trading."),
    ]
    for title, body in lessons:
        st.markdown(f'<div class="lesson-box"><h3>{title}</h3><p class="small-note">{body}</p></div>', unsafe_allow_html=True)

st.markdown("---")
st.caption(DISCLAIMER)
