import os
from datetime import date, timedelta

import altair as alt
import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title="Listen AI Dashboard", layout="wide")

GATEWAY_URL = os.getenv("GATEWAY_URL", "http://localhost:8000")

if "token" not in st.session_state:
    st.session_state.token = None

st.title("Social Listening Dashboard")
st.caption("Track sentiment, keywords, trends, and example posts by keyword filters.")

with st.sidebar:
    st.subheader("Authentication")
    username = st.text_input("Username", value="admin")
    password = st.text_input("Password", type="password", value="admin123")

    if st.button("Login", use_container_width=True):
        try:
            resp = requests.post(
                f"{GATEWAY_URL}/auth/login",
                json={"username": username, "password": password},
                timeout=10,
            )
            if resp.status_code == 200:
                st.session_state.token = resp.json().get("token")
                st.success("Login successful")
            else:
                st.error(resp.json().get("error", "Login failed"))
        except Exception as exc:
            st.error(f"Gateway error: {exc}")

    if st.session_state.token:
        st.success("Authenticated")

col1, col2 = st.columns(2)
with col1:
    include_input = st.text_input("Include keywords (comma-separated)", "listen ai, dashboard")
with col2:
    exclude_input = st.text_input("Exclude keywords (comma-separated)", "spam")

range_col1, range_col2, range_col3 = st.columns([2, 2, 1])
with range_col1:
    from_date = st.date_input("From date", value=date.today() - timedelta(days=30))
with range_col2:
    to_date = st.date_input("To date", value=date.today())
with range_col3:
    sample_size = st.number_input("Example posts", min_value=1, max_value=20, value=5)

run_clicked = st.button("Analyze", type="primary")

if run_clicked:
    if not st.session_state.token:
        st.warning("Please login first.")
    else:
        include_keywords = [k.strip() for k in include_input.split(",") if k.strip()]
        exclude_keywords = [k.strip() for k in exclude_input.split(",") if k.strip()]

        payload = {
            "includeKeywords": include_keywords,
            "excludeKeywords": exclude_keywords,
            "fromDate": from_date.strftime("%Y-%m-%d"),
            "toDate": to_date.strftime("%Y-%m-%d"),
            "sampleSize": int(sample_size),
        }

        try:
            with st.spinner("Building dashboard..."):
                resp = requests.post(
                    f"{GATEWAY_URL}/api/dashboard",
                    json=payload,
                    headers={"Authorization": f"Bearer {st.session_state.token}"},
                    timeout=30,
                )

            if resp.status_code != 200:
                st.error(resp.json().get("error", "Request failed"))
                st.stop()

            data = resp.json()
            sentiment = data.get("sentimentPercentage", {})

            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Mentions", data.get("mentionCount", 0))
            m2.metric("Positive %", sentiment.get("positive", 0))
            m3.metric("Neutral %", sentiment.get("neutral", 0))
            m4.metric("Negative %", sentiment.get("negative", 0))

            st.subheader("Top Keywords")
            top_keywords = data.get("topKeywords", [])
            if top_keywords:
                kw_df = pd.DataFrame(top_keywords)
                st.dataframe(kw_df, use_container_width=True)
            else:
                st.info("No keywords found for this filter.")

            st.subheader("Post Trend")
            trends = data.get("trends", [])
            if trends:
                trends_df = pd.DataFrame(trends)
                chart = (
                    alt.Chart(trends_df)
                    .mark_line(point=True)
                    .encode(x="date:T", y="count:Q")
                    .properties(height=300)
                )
                st.altair_chart(chart, use_container_width=True)
            else:
                st.info("No trend data found.")

            st.subheader("Example Posts")
            examples = data.get("examplePosts", [])
            if not examples:
                st.info("No posts found for your keyword filters.")
            for post in examples:
                st.markdown(
                    f"**[{post.get('platform', 'unknown')}] @{post.get('author', 'user')}** "
                    f"({post.get('created_at', '')})  \\n"
                    f"Sentiment: **{post.get('sentiment', 'neutral')}**  \\n"
                    f"{post.get('content', '')}"
                )
                st.divider()

        except Exception as exc:
            st.error(f"Error: {exc}")
