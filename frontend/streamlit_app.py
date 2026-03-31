import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go

API_URL = "http://127.0.0.1:8000"

st.title("Recommendation Scatter Plot")

# Load users
users = requests.get(f"{API_URL}/users").json()
user_list = [u['user_id'] for u in users]

selected_user = st.selectbox("Select User", user_list)

if selected_user:
    data = requests.get(f"{API_URL}/data/{selected_user}").json()
    df = pd.DataFrame(data)

    top_order = ['Top1','Top2','Top3','Top4','Top5']

    top = df[df['group_name'].isin(top_order)]
    near = df[df['group_name'] == 'Near']
    far = df[df['group_name'] == 'Far']
    random_pts = df[df['group_name'] == 'Random']

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=random_pts['max_cosine'],
        y=random_pts['predicted_rating'],
        mode='markers',
        name='Random'
    ))

    fig.add_trace(go.Scatter(
        x=top['max_cosine'],
        y=top['predicted_rating'],
        mode='markers+text',
        text=top['display_label'],
        name='Top 5'
    ))

    fig.add_trace(go.Scatter(
        x=near['max_cosine'],
        y=near['predicted_rating'],
        mode='markers+text',
        text=near['display_label'],
        name='Near'
    ))

    fig.add_trace(go.Scatter(
        x=far['max_cosine'],
        y=far['predicted_rating'],
        mode='markers+text',
        text=far['display_label'],
        name='Far'
    ))

    st.plotly_chart(fig, use_container_width=True)