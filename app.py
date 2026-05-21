
import math
from datetime import datetime
import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf

st.set_page_config(page_title='SmallWin Trader', page_icon='📈', layout='wide', initial_sidebar_state='expanded')

CSS = '''
<style>
.stApp{background:linear-gradient(135deg,#07111f,#0f172a 50%,#111827);color:#f8fafc}.main .block-container{padding-top:2rem;max-width:1300px}h1,h2,h3{color:#f8fafc;font-weight:800}.hero{padding:34px;border-radius:30px;background:linear-gradient(135deg,rgba(15,23,42,.96),rgba(30,41,59,.9));border:1px solid rgba(148,163,184,.25);box-shadow:0 25px 80px rgba(0,0,0,.38);margin-bottom:24px}.hero-title{font-size:3.2rem;font-weight:900;background:linear-gradient(90deg,#fff,#67e8f9,#86efac);-webkit-background-clip:text;-webkit-text-fill-color:transparent}.hero-sub,.small-note,.legal-text{color:#cbd5e1;line-height:1.65}.badge{display:inline-block;margin:6px;padding:9px 14px;border-radius:999px;background:rgba(15,23,42,.72);border:1px solid rgba(148,163,184,.28);color:#e2e8f0}.glass-card,.pricing-card,.lesson-box{padding:24px;border-radius:24px;background:rgba(15,23,42,.78);border:1px solid rgba(148,163,184,.22);box-shadow:0 20px 60px rgba(0,0,0,.25);margin-bottom:18px}.pricing-card-pro{padding:24px;border-radius:24px;background:linear-gradient(135deg,rgba(34,197,94,.18),rgba(6,182,212,.14)),rgba(15,23,42,.9);border:1px solid rgba(45,212,191,.42);box-shadow:0 20px 60px rgba(0,0,0,.25);margin-bottom:18px}.trade-card{padding:28px;border-radius:28px;background:linear-gradient(135deg,rgba(34,197,94,.16),rgba(6,182,212,.13)),rgba(15,23,42,.88);border:1px solid rgba(45,212,191,.36);box-shadow:0 20px 75px rgba(16,185,129,.10);margin-bottom:20px}.warning-card{padding:20px;border-radius:22px;background:rgba(251,191,36,.12);border:1px solid rgba(251,191,36,.36);color:#fde68a;margin-bottom:18px}.danger-card{padding:20px;border-radius:22px;background:rgba(239,68,68,.12);border:1px solid rgba(248,113,113,.36);color:#fecaca;margin-bottom:18px}.success-pill,.skip-pill,.pro-pill{display:inline-block;padding:8px 13px;border-radius:999px;font-weight:800;margin-bottom:10px;font-size:.82rem}.success-pill{background:rgba(34,197,94,.18);border:1px solid rgba(34,197,94,.42);color:#bbf7d0}.skip-pill{background:rgba(239,68,68,.18);border:1px solid rgba(248,113,113,.42);color:#fecaca}.pro-pill{background:rgba(6,182,212,.18);border:1px solid rgba(6,182,212,.42);color:#a5f3fc}.metric-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(155px,1fr));gap:14px;margin-top:20px}.metric-card{padding:18px;border-radius:20px;background:rgba(2,6,23,.45);border:1px solid rgba(148,163,184,.20)}.metric-label{color:#94a3b8;font-size:.82rem;margin-bottom:8px}.metric-value{color:#f8fafc;font-size:1.35rem;font-weight:800}div.stButton>button:first-child{background:linear-gradient(90deg,#22c55e,#06b6d4);color:#07111f;border:0;border-radius:16px;padding:.75rem 1.2rem;font-weight:800}
</style>
'''
st.markdown(CSS, unsafe_allow_html=True)

DISCLAIMER='SmallWin Trader is educational only. It is not financial advice, not a broker, not a registered investment adviser, and not a guarantee of profit. Use paper trading first and verify prices in your brokerage app.'
TICKERS=['SOFI','RIVN','HOOD','BAC','F','PLTR','T','SNAP','PFE','CCL','AAL','WBD','UBER','LYFT','AMD','AAPL','NIO','LCID']

def money(v):
    try:return f'${float(v):,.2f}'
    except Exception:return '$0.00'
def sf(v,d=np.nan):
    try:return float(v)
    except Exception:return d
def flatten(df):
    if isinstance(df.columns,pd.MultiIndex):df.columns=[c[0] if isinstance(c,tuple) else c for c in df.columns]
    return df
@st.cache_data(ttl=60)
def get_data(ticker, period='5d', interval='15m'):
    df=yf.download(ticker,period=period,interval=interval,progress=False,auto_adjust=True,prepost=False,threads=False)
    return flatten(df).dropna().copy()
def add_ind(df):
    if df.empty:return df
    df=df.copy();df['EMA9']=df['Close'].ewm(span=9,adjust=False).mean();df['EMA21']=df['Close'].ewm(span=21,adjust=False).mean()
    delta=df['Close'].diff();gain=delta.clip(lower=0).rolling(14).mean();loss=(-delta.clip(upper=0)).rolling(14).mean();rs=gain/loss.replace(0,np.nan);df['RSI']=100-(100/(1+rs))
    tr=pd.concat([(df['High']-df['Low']),(df['High']-df['Close'].shift()).abs(),(df['Low']-df['Close'].shift()).abs()],axis=1).max(axis=1);df['ATR']=tr.rolling(14).mean()
    tp=(df['High']+df['Low']+df['Close'])/3;vol=df['Volume'].replace(0,np.nan);df['VWAP']=(tp*vol).cumsum()/vol.cumsum();df['RelativeVolume']=df['Volume']/df['Volume'].rolling(20).mean().replace(0,np.nan)
    return df
def score(df):
    if df.empty or len(df)<30:return {'score':0,'bias':'Not enough data','reason':'Not enough recent data.'}
    r=df.iloc[-1];p=df.iloc[-2];s=0;re=[]
    if sf(r['Close'])>sf(r['VWAP']):s+=20;re.append('holding above VWAP')
    else:re.append('below VWAP')
    if sf(r['EMA9'])>sf(r['EMA21']):s+=20;re.append('short-term momentum is leading')
    else:re.append('EMA trend is not confirmed')
    rsi=sf(r['RSI']);rv=sf(r['RelativeVolume']);atr=sf(r['ATR'])
    if 45<=rsi<=70:s+=20;re.append('RSI is strong but not overextended')
    elif rsi>70:s+=8;re.append('RSI is hot, wait for pullback')
    else:re.append('RSI is weak')
    if rv>=1:s+=20;re.append('volume is active')
    else:re.append('volume is light')
    if sf(r['Close'])>sf(p['Close']):s+=10;re.append('latest candle is green')
    if not math.isnan(atr) and atr>0:s+=10;re.append('ATR gives a usable stop')
    return {'score':int(s),'bias':'Strong setup' if s>=80 else 'Possible setup' if s>=60 else 'Wait' if s>=40 else 'Skip','reason':', '.join(re)}
def build_plan(ticker,df,acct,risk_pct,max_cap_pct):
    r=df.iloc[-1];price=sf(r['Close']);atr=sf(r['ATR']);vwap=sf(r['VWAP'])
    if math.isnan(price) or price<=0:return {}
    risk_d=acct*risk_pct/100;max_cap=acct*max_cap_pct/100;stop_dist=max(atr*.75 if not math.isnan(atr) else price*.015,price*.01);stop=price-stop_dist
    if not math.isnan(vwap):stop=min(stop,vwap-(stop_dist*.15))
    rps=max(price-stop,.01);shares=max(0,min(math.floor(risk_d/rps),math.floor(max_cap/price)))
    return {'ticker':ticker,'price':round(price,2),'entry_low':round(price-rps*.25,2),'entry_high':round(price+rps*.15,2),'stop_loss':round(stop,2),'target_1':round(price+rps,2),'target_2':round(price+rps*2,2),'shares':shares,'capital_needed':round(shares*price,2),'max_loss':round(shares*rps,2)}
def scan(tickers,acct,risk,maxcap,limit=None):
    rows=[]
    for t in tickers:
        try:
            df=add_ind(get_data(t))
            if df.empty or len(df)<30:continue
            sc=score(df);pl=build_plan(t,df,acct,risk,maxcap)
            if not pl:continue
            last=df.iloc[-1];rows.append({'Symbol':t,'Score':sc['score'],'Bias':sc['bias'],'Price':pl['price'],'Shares':pl['shares'],'Capital':pl['capital_needed'],'Stop':pl['stop_loss'],'Target 1':pl['target_1'],'Target 2':pl['target_2'],'Max Loss':pl['max_loss'],'RSI':round(sf(last['RSI']),1),'ATR':round(sf(last['ATR']),2),'Rel Vol':round(sf(last['RelativeVolume']),2),'Why':sc['reason']})
        except Exception:continue
    out=pd.DataFrame(rows)
    if out.empty:return out
    out=out.sort_values(by=['Score','Shares','Rel Vol'],ascending=[False,False,False]).reset_index(drop=True)
    return out.head(limit) if limit else out
def render_card(symbol,sc,pl,why):
    pill='success-pill' if sc['score']>=70 and pl['shares']>=1 else 'skip-pill';text='BEGINNER PRACTICE SETUP' if sc['score']>=70 and pl['shares']>=1 else 'WAIT OR SKIP'
    st.markdown(f'''<div class="trade-card"><div class="{pill}">{text}</div><h2>{symbol} Trade Coach</h2><p class="small-note">{why}</p><div class="metric-grid"><div class="metric-card"><div class="metric-label">Latest Price</div><div class="metric-value">{money(pl['price'])}</div></div><div class="metric-card"><div class="metric-label">AI Score</div><div class="metric-value">{sc['score']}/100</div></div><div class="metric-card"><div class="metric-label">Shares</div><div class="metric-value">{pl['shares']}</div></div><div class="metric-card"><div class="metric-label">Capital Needed</div><div class="metric-value">{money(pl['capital_needed'])}</div></div><div class="metric-card"><div class="metric-label">Entry Zone</div><div class="metric-value">{money(pl['entry_low'])} - {money(pl['entry_high'])}</div></div><div class="metric-card"><div class="metric-label">Stop Loss</div><div class="metric-value">{money(pl['stop_loss'])}</div></div><div class="metric-card"><div class="metric-label">Target 1</div><div class="metric-value">{money(pl['target_1'])}</div></div><div class="metric-card"><div class="metric-label">Target 2</div><div class="metric-value">{money(pl['target_2'])}</div></div><div class="metric-card"><div class="metric-label">Max Loss</div><div class="metric-value">{money(pl['max_loss'])}</div></div></div></div>''',unsafe_allow_html=True)

if 'plan_mode' not in st.session_state: st.session_state['plan_mode']='Free'
with st.sidebar:
    st.markdown('## ⚙️ Account Setup')
    acct=st.number_input('Account size',50.0,100000.0,500.0,50.0)
    risk=st.slider('Max risk per trade %',.25,5.0,1.0,.25)
    maxcap=st.slider('Max account used per trade %',5,100,65,5)
    st.markdown('## 💳 Demo Access')
    st.session_state['plan_mode']=st.radio('Plan mode',['Free','Pro'],horizontal=True)
    st.markdown('## 👀 Watchlist')
    custom=st.text_area('Tickers',value=', '.join(TICKERS),height=140)
    tickers=[x.strip().upper() for x in custom.replace('\n',',').split(',') if x.strip()]
    st.markdown(f'<div class="glass-card"><b>Beginner guardrail</b><p class="small-note">At {risk:.2f}% risk, max planned loss is <b>{money(acct*risk/100)}</b>.</p><p class="small-note">Demo plan: <b>{st.session_state["plan_mode"]}</b></p></div>',unsafe_allow_html=True)

st.markdown('''<div class="hero"><div class="hero-title">SmallWin Trader</div><div class="hero-sub">A beginner-friendly trading coach that scans live stocks, builds simple practice plans, teaches entries and exits, and keeps risk small while users learn. Built for an education-first subscription model.</div><div><span class="badge">📍 Entry zones</span><span class="badge">🛑 Stop losses</span><span class="badge">🎯 Profit targets</span><span class="badge">💳 Subscription ready</span><span class="badge">⚖️ Legal pages included</span><span class="badge">📱 Store prep notes</span></div></div>''',unsafe_allow_html=True)

tab1,tab2,tab3,tab4,tab5,tab6,tab7=st.tabs(['🏆 Best Setup','🔎 Scanner','🎓 Trade Coach','📓 Journal','💳 Pricing','⚖️ Legal','🚀 Store Prep'])
with tab1:
    st.markdown('<div class="glass-card"><h3>Find one realistic beginner setup</h3><p class="small-note">Filters for setups that fit account size.</p></div>',unsafe_allow_html=True)
    if st.button('Find best setup now'):
        with st.spinner('Scanning live stock data...'):
            res=scan(tickers,acct,risk,maxcap,5 if st.session_state['plan_mode']=='Free' else None)
        if res.empty: st.markdown('<div class="danger-card">No setup came back right now.</div>',unsafe_allow_html=True)
        else:
            aff=res[(res['Shares']>=1)&(res['Bias'].isin(['Strong setup','Possible setup']))]
            if aff.empty:
                st.markdown('<div class="warning-card">No clean affordable setup found. Skipping bad trades is part of trading.</div>',unsafe_allow_html=True); st.dataframe(res,use_container_width=True,hide_index=True)
            else:
                b=aff.iloc[0];df=add_ind(get_data(b['Symbol']));sc=score(df);pl=build_plan(b['Symbol'],df,acct,risk,maxcap);render_card(b['Symbol'],sc,pl,b['Why'])
with tab2:
    st.markdown('<div class="glass-card"><h3>Live beginner scanner</h3><p class="small-note">Ranks stocks by trend, VWAP, EMA alignment, RSI, volume, affordability, and risk control.</p></div>',unsafe_allow_html=True)
    if st.session_state['plan_mode']=='Free': st.markdown('<div class="warning-card"><b>Free plan:</b> scanner limited to first 5 results.</div>',unsafe_allow_html=True)
    if st.button('Scan watchlist'):
        with st.spinner('Scanning watchlist...'):
            res=scan(tickers,acct,risk,maxcap,5 if st.session_state['plan_mode']=='Free' else None)
        if res.empty: st.markdown('<div class="danger-card">No results came back.</div>',unsafe_allow_html=True)
        else: st.dataframe(res,use_container_width=True,hide_index=True); st.download_button('Download scan results',data=res.to_csv(index=False).encode(),file_name='smallwin_scan_results.csv',mime='text/csv')
with tab3:
    st.markdown('<div class="glass-card"><h3>Build a trade plan for any ticker</h3></div>',unsafe_allow_html=True)
    t=st.text_input('Ticker',value='SOFI').upper()
    if st.button('Coach this ticker'):
        with st.spinner(f'Building plan for {t}...'):
            df=add_ind(get_data(t))
        if df.empty: st.markdown('<div class="danger-card">Could not pull data for that ticker.</div>',unsafe_allow_html=True)
        else:
            sc=score(df);pl=build_plan(t,df,acct,risk,maxcap);render_card(t,sc,pl,sc['reason']);st.line_chart(df[['Close','EMA9','EMA21','VWAP']].tail(80))
with tab4:
    st.markdown('<div class="glass-card"><h3>Paper trade journal</h3><p class="small-note">Practice before risking real money.</p></div>',unsafe_allow_html=True)
    if 'journal' not in st.session_state: st.session_state['journal']=[]
    with st.form('journal_form'):
        c1,c2,c3=st.columns(3)
        with c1: jt=st.text_input('Ticker'); je=st.number_input('Entry price',min_value=0.0,value=0.0,step=.01)
        with c2: js=st.number_input('Stop loss',min_value=0.0,value=0.0,step=.01); jta=st.number_input('Target',min_value=0.0,value=0.0,step=.01)
        with c3: jsh=st.number_input('Shares',min_value=0,value=0,step=1); jr=st.selectbox('Result',['Open','Win','Loss','Breakeven'])
        why=st.text_area('Why did you take this trade?'); sub=st.form_submit_button('Save practice trade')
    if sub:
        rk=max((je-js)*jsh,0);rw=max((jta-je)*jsh,0);rr=round(rw/rk,2) if rk>0 else 0
        st.session_state['journal'].append({'Time':datetime.now().strftime('%Y-%m-%d %H:%M'),'Ticker':jt.upper(),'Entry':je,'Stop':js,'Target':jta,'Shares':jsh,'Risk $':round(rk,2),'Reward $':round(rw,2),'R/R':rr,'Result':jr,'Reason':why});st.success('Practice trade saved.')
    st.dataframe(pd.DataFrame(st.session_state['journal']),use_container_width=True,hide_index=True) if st.session_state['journal'] else st.info('No paper trades logged yet.')
with tab5:
    st.markdown('<div class="glass-card"><h3>Subscription model</h3><p class="small-note">For mobile stores, use Apple In-App Purchases and Google Play Billing. For web, use Stripe.</p></div>',unsafe_allow_html=True)
    c1,c2,c3=st.columns(3)
    c1.markdown('<div class="pricing-card"><div class="success-pill">FREE</div><h2>$0</h2><p class="small-note">Limited scanner, basic coach, paper journal, beginner lessons.</p></div>',unsafe_allow_html=True)
    c2.markdown('<div class="pricing-card-pro"><div class="pro-pill">PRO</div><h2>$14.99/mo</h2><p class="small-note">Unlimited scans, full watchlist, advanced coaching, exports, future alerts.</p></div>',unsafe_allow_html=True)
    c3.markdown('<div class="pricing-card"><div class="pro-pill">ELITE</div><h2>$29.99/mo</h2><p class="small-note">AI lessons, market recap, priority alerts, community, backtesting.</p></div>',unsafe_allow_html=True)
with tab6:
    st.markdown('<div class="glass-card"><h3>Legal and compliance center</h3><p class="small-note">Placeholder legal pages included. Have an attorney review before launch.</p></div>',unsafe_allow_html=True)
    sec=st.selectbox('Choose legal page',['Risk Disclaimer','Terms of Service','Privacy Policy','Subscription Terms','Refund Policy','No Financial Advice'])
    text={'Risk Disclaimer':'Trading involves risk. You can lose money. Setups are not guarantees or instructions to buy or sell.','Terms of Service':'All content is educational only. Market data may be delayed, incomplete, inaccurate, or unavailable.','Privacy Policy':'The app may collect account info, subscription status, usage data, watchlists, and journal entries. Do not collect brokerage passwords.','Subscription Terms':'Paid plans may renew automatically. iOS should use Apple In-App Purchases. Android should use Google Play Billing.','Refund Policy':'iOS refunds are handled by Apple. Android refunds are handled by Google Play. Web refunds follow the posted web policy.','No Financial Advice':'SmallWin Trader does not provide personalized investment advice, brokerage services, or recommendations.'}[sec]
    st.markdown(f'<div class="glass-card legal-text"><h3>{sec}</h3><p>{text}</p></div>',unsafe_allow_html=True)
with tab7:
    st.markdown('<div class="glass-card"><h3>Apple App Store and Google Play readiness</h3><p class="small-note">Use this checklist before submitting a real mobile version.</p></div>',unsafe_allow_html=True)
    for title,body in [('Required before launch','Business email, support URL, privacy policy URL, terms URL, subscription disclosure page, and no misleading income claims.'),('Mobile subscription rules','Use Apple In-App Purchases for iOS and Google Play Billing for Android digital subscriptions.'),('Finance app wording','Use educational setup, practice trade, example entry zone, risk-management plan, and paper trading.'),('Technical next step','For real stores, rebuild frontend in React Native or Flutter and connect a secure backend, auth, and official billing.')]: st.markdown(f'<div class="lesson-box"><h3>{title}</h3><p class="small-note">{body}</p></div>',unsafe_allow_html=True)
st.markdown('---'); st.caption(DISCLAIMER)
