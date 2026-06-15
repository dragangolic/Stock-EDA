import yfinance as yf
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import date, timedelta

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Stock Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Import fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* Dark card panels for metrics */
[data-testid="metric-container"] {
    background: #1E2130;
    border: 1px solid #2D3250;
    border-radius: 12px;
    padding: 16px 20px;
}
[data-testid="metric-container"] label { color: #8892B0 !important; font-size: 0.78rem; letter-spacing: 0.08em; text-transform: uppercase; }
[data-testid="metric-container"] [data-testid="stMetricValue"] { font-size: 1.6rem; font-weight: 700; color: #E6F1FF; }
[data-testid="metric-container"] [data-testid="stMetricDelta"] { font-size: 0.85rem; }

/* Sidebar */
[data-testid="stSidebar"] { background: #0D1117; border-right: 1px solid #21262D; }

/* Chart containers */
.chart-container { background: #161B22; border-radius: 12px; padding: 4px; border: 1px solid #21262D; }

/* Section headers */
.section-header { font-size: 1.1rem; font-weight: 600; color: #8892B0; letter-spacing: 0.04em; text-transform: uppercase; margin-bottom: 4px; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar controls ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Controls")
    st.markdown("---")

    ticker1 = st.text_input("Ticker 1", value="GOOGL").upper().strip()
    ticker2 = st.text_input("Ticker 2", value="AAPL").upper().strip()

    st.markdown("#### Date Range")
    end_date   = st.date_input("End date",   value=date.today())
    start_date = st.date_input("Start date", value=date.today() - timedelta(days=365 * 5))

    chart_type = st.selectbox("Chart type", ["Candlestick", "Line", "Area"])
    show_ma    = st.checkbox("Show moving averages (50d / 200d)", value=True)

    st.markdown("---")
    st.markdown("<small style='color:#555'>Data via Yahoo Finance · Built with Streamlit</small>", unsafe_allow_html=True)

# ── Data fetching ─────────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def load_data(symbol, start, end):
    t  = yf.Ticker(symbol)
    df = t.history(start=str(start), end=str(end))
    info = {}
    try:
        info = t.info
    except Exception:
        pass
    return df, info

def pct_change(df):
    if df.empty or len(df) < 2:
        return 0.0
    return ((df["Close"].iloc[-1] - df["Close"].iloc[-2]) / df["Close"].iloc[-2]) * 100

# ── Build chart ───────────────────────────────────────────────────────────────
def build_chart(df, ticker, chart_type, show_ma):
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        row_heights=[0.72, 0.28],
        vertical_spacing=0.03,
    )

    # Price chart
    if chart_type == "Candlestick":
        fig.add_trace(go.Candlestick(
            x=df.index, open=df["Open"], high=df["High"],
            low=df["Low"], close=df["Close"],
            name="Price",
            increasing_line_color="#00E5A0",
            decreasing_line_color="#FF4B6E",
        ), row=1, col=1)
    elif chart_type == "Area":
        fig.add_trace(go.Scatter(
            x=df.index, y=df["Close"], name="Price",
            fill="tozeroy", line=dict(color="#7B8CDE", width=1.5),
            fillcolor="rgba(123,140,222,0.12)",
        ), row=1, col=1)
    else:  # Line
        fig.add_trace(go.Scatter(
            x=df.index, y=df["Close"], name="Price",
            line=dict(color="#7B8CDE", width=1.8),
        ), row=1, col=1)

    # Moving averages
    if show_ma and len(df) > 50:
        df = df.copy()
        df["MA50"]  = df["Close"].rolling(50).mean()
        df["MA200"] = df["Close"].rolling(200).mean()
        fig.add_trace(go.Scatter(x=df.index, y=df["MA50"],  name="50d MA",
                                 line=dict(color="#F6C90E", width=1, dash="dot")), row=1, col=1)
    if show_ma and len(df) > 200:
        fig.add_trace(go.Scatter(x=df.index, y=df["MA200"], name="200d MA",
                                 line=dict(color="#FF7B7B", width=1, dash="dot")), row=1, col=1)

    # Volume bars
    colors = ["#00E5A0" if c >= o else "#FF4B6E"
              for c, o in zip(df["Close"], df["Open"])]
    fig.add_trace(go.Bar(
        x=df.index, y=df["Volume"], name="Volume",
        marker_color=colors, opacity=0.7,
    ), row=2, col=1)

    fig.update_layout(
        paper_bgcolor="#161B22",
        plot_bgcolor="#161B22",
        font=dict(family="Inter", color="#8892B0"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, bgcolor="rgba(0,0,0,0)"),
        xaxis_rangeslider_visible=False,
        margin=dict(l=10, r=10, t=20, b=10),
        height=480,
    )
    fig.update_xaxes(gridcolor="#21262D", showline=False, zeroline=False)
    fig.update_yaxes(gridcolor="#21262D", showline=False, zeroline=False)
    return fig

# ── Stock card renderer ───────────────────────────────────────────────────────
def render_stock(ticker, start_date, end_date, chart_type, show_ma):
    df, info = load_data(ticker, start_date, end_date)

    if df.empty:
        st.error(f"No data found for **{ticker}**. Check the ticker symbol.")
        return

    price    = df["Close"].iloc[-1]
    delta    = pct_change(df)
    vol      = df["Volume"].iloc[-1]
    hi52     = df["High"].rolling(252).max().iloc[-1]
    lo52     = df["Low"].rolling(252).min().iloc[-1]
    name     = info.get("longName", ticker)

    # Header
    st.markdown(f"### {name} &nbsp;<span style='color:#555;font-size:0.9rem'>({ticker})</span>", unsafe_allow_html=True)
    if info.get("sector"):
        st.caption(f"{info['sector']} · {info.get('industry','')}")

    # KPI row
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Last Close",    f"${price:,.2f}", f"{delta:+.2f}%")
    c2.metric("Volume",        f"{vol/1e6:.1f}M")
    c3.metric("52-wk High",    f"${hi52:,.2f}")
    c4.metric("52-wk Low",     f"${lo52:,.2f}")

    # Chart
    st.plotly_chart(build_chart(df, ticker, chart_type, show_ma),
                    use_container_width=True, config={"displayModeBar": False})

# ── Main layout ───────────────────────────────────────────────────────────────
st.markdown("# 📈 Stock Dashboard")
st.caption(f"Comparing **{ticker1}** and **{ticker2}** · {start_date} → {end_date}")
st.markdown("---")

tab1, tab2, tab3 = st.tabs([f"📊 {ticker1}", f"📊 {ticker2}", "⚖️ Compare"])

with tab1:
    render_stock(ticker1, start_date, end_date, chart_type, show_ma)

with tab2:
    render_stock(ticker2, start_date, end_date, chart_type, show_ma)

with tab3:
    st.markdown("### Closing Price — Side by Side")
    df1, _ = load_data(ticker1, start_date, end_date)
    df2, _ = load_data(ticker2, start_date, end_date)

    if not df1.empty and not df2.empty:
        # Normalise to 100 for fair comparison
        norm1 = (df1["Close"] / df1["Close"].iloc[0]) * 100
        norm2 = (df2["Close"] / df2["Close"].iloc[0]) * 100

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df1.index, y=norm1, name=ticker1,
                                 line=dict(color="#7B8CDE", width=2)))
        fig.add_trace(go.Scatter(x=df2.index, y=norm2, name=ticker2,
                                 line=dict(color="#00E5A0", width=2)))
        fig.update_layout(
            paper_bgcolor="#161B22", plot_bgcolor="#161B22",
            font=dict(family="Inter", color="#8892B0"),
            yaxis_title="Indexed to 100",
            legend=dict(orientation="h", bgcolor="rgba(0,0,0,0)"),
            margin=dict(l=10, r=10, t=10, b=10),
            height=420,
        )
        fig.update_xaxes(gridcolor="#21262D")
        fig.update_yaxes(gridcolor="#21262D")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        # Quick stats table
        st.markdown("### Key Stats")
        rows = []
        for sym, df in [(ticker1, df1), (ticker2, df2)]:
            rows.append({
                "Ticker":       sym,
                "Last Price":   f"${df['Close'].iloc[-1]:,.2f}",
                "1d Change":    f"{pct_change(df):+.2f}%",
                "Period High":  f"${df['High'].max():,.2f}",
                "Period Low":   f"${df['Low'].min():,.2f}",
                "Avg Volume":   f"{df['Volume'].mean()/1e6:.1f}M",
            })
        st.dataframe(pd.DataFrame(rows).set_index("Ticker"), use_container_width=True)

        