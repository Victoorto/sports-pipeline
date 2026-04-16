import streamlit as st
import polars as pl 
import plotly.express as px 
import plotly.graph_objects as go

#Page configuration 
st.set_page_config(
    page_title="Sports Analytics Pipeline",
    page_icon="⚽",
    layout="wide"
)

#Title
st.title("⚽ Sports Analytics Dashboard")
st.markdown("*Data powered by Football-Data.org | Build with Apache Kafka & Databricks*")

@st.cache_data
def load_data():
    wins = pl.read_csv("dashboard/data/football_wins_gold.csv")
    goals = pl.read_csv("dashboard/data/football_goals_gold.csv")
    results = pl.read_csv("dashboard/data/football_results_gold.csv")
    return wins, goals, results

df_wins, df_goals, df_results = load_data()

st.subheader("📊 Overview")

col1, col2, col3 = st.columns(3)

with col1:
    total_matches = df_goals["total_matches"].sum()
    st.metric("Total Matches", total_matches)

with col2:
    total_goals = df_goals["total_goals"].sum()
    st.metric("Total Goals", total_goals)

with col3:
    avg_goals = round(df_goals["avg_goals_per_match"].mean(), 2)
    st.metric("Avg Goals per Match", avg_goals)


col1, col2 = st.columns(2)

with col1:
    st.subheader("⚽ Goals by Competition")
    fig_goals = px.bar(
        df_goals,
        x="competition",
        y="total_goals",
        color="avg_goals_per_match",
        color_continuous_scale="RdYlGn",
        labels={"total_goals": "Total Goals", "competition": "Competition"}
    )
    st.plotly_chart(fig_goals, use_container_width=True)

with col2:
    st.subheader("🥇 Top 10 Teams by Wins")

    df_top10 = df_results.filter(
        pl.col("results") != "Draw"
    ).head(10).sort("total")

    fig_lollipop = go.Figure()

    # Lines lollipop
    fig_lollipop.add_trace(go.Bar(
        x=df_top10["total"],
        y=df_top10["results"],
        orientation="h",
        width=0.05,
        marker=dict(color="#636EFA"),
        showlegend=False
    ))

    # Circle lollipop
    fig_lollipop.add_trace(go.Scatter(
        x=df_top10["total"],
        y=df_top10["results"],
        mode="markers+text",
        marker=dict(size=16, color="#636EFA"),
        text=df_top10["total"],
        textposition="middle right",
        showlegend=False
    ))

    fig_lollipop.update_layout(
        xaxis_title="Total Wins",
        yaxis_title="Team",
        bargap=0.5
    )

    st.plotly_chart(fig_lollipop, use_container_width=True)

st.subheader("🔍 Explore Data")

competition_filter = st.selectbox(
    "Filter by Competition",
    options=["All"] + df_goals["competition"].to_list()
)

if competition_filter != "All":
    df_filtered = df_goals.filter(pl.col("competition") == competition_filter)
else:
    df_filtered = df_goals

st.dataframe(df_filtered, use_container_width=True)
