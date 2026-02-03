import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh
from datetime import datetime

API_URL = "http://localhost:8000/predict"  # FastAPI URL

st.set_page_config(
    page_title="NIFTY50 AI Dashboard",
    layout="wide",
)

# Auto refresh every 30 seconds
st_autorefresh(interval=30_000, key="refresh")

st.title("📈 NIFTY50 Live Market AI Dashboard")

# -------------------------
# AI SIGNAL PANEL
# -------------------------
st.subheader("🤖 AI Market Signal")

try:
    r = requests.get(API_URL, timeout=5)
    data = r.json()

    direction = data["direction"]
    confidence = data["confidence"]

    col1, col2 = st.columns(2)

    with col1:
        if direction == "UP":
            st.success("📈 MARKET BIAS: **BULLISH**")
        else:
            st.error("📉 MARKET BIAS: **BEARISH**")

    with col2:
        st.metric("Confidence", f"{confidence * 100:.1f}%")

except Exception as e:
    st.warning("⚠️ Prediction API not reachable")

# -------------------------
# LIVE CHART (TradingView)
# -------------------------
st.subheader("📊 Live NIFTY50 Chart")

tradingview_html = """
<!-- TradingView Widget -->
<div class="tradingview-widget-container">
  <div id="tradingview_12345"></div>
  <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
  <script type="text/javascript">
  new TradingView.widget(
  {
    "symbol": "NSE:NIFTY",
    "interval": "5",
    "timezone": "Asia/Kolkata",
    "theme": "dark",
    "style": "1",
    "locale": "en",
    "toolbar_bg": "#f1f3f6",
    "enable_publishing": false,
    "hide_side_toolbar": false,
    "container_id": "tradingview_12345"
  }
  );
  </script>
</div>
"""

st.components.v1.html(tradingview_html, height=550)

# -------------------------
# STRATEGY NOTES
# -------------------------
st.subheader("📌 AI Interpretation")

st.markdown("""
**How to use this signal**
- Confidence > **60%** → high probability bias
- Use with:
  - Support / Resistance
  - RSI & VWAP
  - Market structure
- Avoid trades during:
  - RBI announcements
  - Major global news
""")

st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
