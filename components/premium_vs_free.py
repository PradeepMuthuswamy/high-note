import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

def show_premium_vs_free_tab(df):
    st.header("Premium vs Free User Comparison")

    # Original engagement metrics comparison
    engagement_metrics = ['posts', 'playlists', 'shouts']
    premium_avg = df[df['adopter'] == 1][engagement_metrics].mean()
    free_avg = df[df['adopter'] == 0][engagement_metrics].mean()

    fig = go.Figure(data=[
        go.Bar(name='Premium Users', x=engagement_metrics, y=premium_avg, marker_color='#FF6B6B'),
        go.Bar(name='Free Users', x=engagement_metrics, y=free_avg, marker_color='#4ECDC4')
    ])

    fig.update_layout(title="Average Engagement Metrics", barmode='group')
    st.plotly_chart(fig, use_container_width=True)

    # Additional visualizations
    col1, col2 = st.columns(2)

    with col1:
        # Radar Chart for Engagement
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=premium_avg,
            theta=engagement_metrics,
            fill='toself',
            name='Premium Users',
            line_color='#FF6B6B'
        ))
        fig.add_trace(go.Scatterpolar(
            r=free_avg,
            theta=engagement_metrics,
            fill='toself',
            name='Free Users',
            line_color='#4ECDC4'
        ))
        fig.update_layout(title="Engagement Metrics Radar")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Distribution Plot
        selected_metric = st.selectbox("Select metric to view distribution", engagement_metrics)
        fig = px.histogram(df, x=selected_metric, color='adopter',
                          color_discrete_map={0: '#4ECDC4', 1: '#FF6B6B'},
                          marginal="box",
                          title=f"{selected_metric} Distribution by User Type")
        st.plotly_chart(fig, use_container_width=True) 