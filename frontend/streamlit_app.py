import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go

API_URL = "https://blue-star-planet.trycloudflare.com"

st.title("Recommendation Scatter Plot")

@st.cache_data
def load_users():
    res = requests.get(f"{API_URL}/users")
    return res.json()

users = load_users()

user_list = [u["user_id"] for u in users]

selected_user = st.selectbox("Select User", user_list)

@st.cache_data
def load_user_data(user_id):
    res = requests.get(f"{API_URL}/data/{user_id}")
    return res.json()

if selected_user:

    data = load_user_data(selected_user)

    df = pd.DataFrame(data)

    top = df[df["group_name"].str.contains("Top")]
    near = df[df["group_name"]=="Near"]
    far = df[df["group_name"]=="Far"]
    random_pts = df[df["group_name"]=="Random"]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=random_pts["max_cosine"],
        y=random_pts["predicted_rating"],
        mode="markers",
        name="Random"
    ))

    fig.add_trace(go.Scatter(
        x=top["max_cosine"],
        y=top["predicted_rating"],
        mode="markers+text",
        text=top["display_label"],
        name="Top"
    ))

    fig.add_trace(go.Scatter(
        x=near["max_cosine"],
        y=near["predicted_rating"],
        mode="markers+text",
        text=near["display_label"],
        name="Near"
    ))

    fig.add_trace(go.Scatter(
        x=far["max_cosine"],
        y=far["predicted_rating"],
        mode="markers+text",
        text=far["display_label"],
        name="Far"
    ))

    st.plotly_chart(fig, use_container_width=True)