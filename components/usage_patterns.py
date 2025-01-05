import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def show_usage_patterns_tab(df):
    st.header("Usage Pattern Analysis")

    # Original time series analysis
    time_metrics = ['songsListened', 'lovedTracks', 'playlists']
    selected_metric = st.selectbox("Select Usage Metric", time_metrics)

    fig = go.Figure()

    for adopter, name, color in [(1, 'Premium Users', '#FF6B6B'), (0, 'Free Users', '#4ECDC4')]:
        user_group = df[df['adopter'] == adopter]
        values = [
            user_group[f'delta1_{selected_metric}'].mean(),
            user_group[selected_metric].mean(),
            user_group[f'delta2_{selected_metric}'].mean()
        ]

        fig.add_trace(go.Scatter(
            x=['Pre', 'Current', 'Post'],
            y=values,
            name=name,
            line=dict(color=color)
        ))

    fig.update_layout(
        title=f"{selected_metric} Evolution Over Time",
        xaxis_title="Time Period",
        yaxis_title="Average Value",
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)

    # Additional usage pattern visualizations
    col1, col2 = st.columns(2)

    with col1:
        # Distribution comparison
        fig = px.histogram(df, x=selected_metric,
                          color='adopter',
                          marginal="box",
                          title=f"{selected_metric} Distribution",
                          color_discrete_map={0: '#4ECDC4', 1: '#FF6B6B'})
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Correlation heatmap
        correlation_metrics = time_metrics + ['posts', 'shouts']
        corr_matrix = df[correlation_metrics].corr()
        fig = px.imshow(corr_matrix,
                       labels=dict(color="Correlation"),
                       color_continuous_scale="RdBu",
                       title="Usage Metrics Correlation")
        st.plotly_chart(fig, use_container_width=True) 