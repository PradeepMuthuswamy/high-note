import streamlit as st
import plotly.express as px
import pandas as pd

def show_core_metrics_tab(df, dict_df):
    st.header("Core Metrics Analysis")

    # Define core metrics
    core_metrics = ['male', 'friend_cnt', 'avg_friend_age', 'avg_friend_male',
                   'friend_country_cnt', 'subscriber_friend_cnt', 'songsListened',
                   'lovedTracks', 'posts', 'playlists', 'shouts']

    # Statistical Analysis
    st.subheader("📊 Statistical Overview")

    # Calculate statistics
    stats_data = []
    for metric in core_metrics:
        premium_data = df[df['adopter'] == 1][metric]
        free_data = df[df['adopter'] == 0][metric]

        premium_stats = premium_data.agg(['mean', 'median', 'std']).round(2)
        free_stats = free_data.agg(['mean', 'median', 'std']).round(2)

        stats_data.append({
            'Metric': metric,
            'Description': dict_df[dict_df['Variable'] == metric]['Description'].iloc[0] 
            if len(dict_df[dict_df['Variable'] == metric]['Description']) > 0 else 'No description available',
            'Premium Mean': premium_stats['mean'],
            'Premium Median': premium_stats['median'],
            'Premium Std': premium_stats['std'],
            'Free Mean': free_stats['mean'],
            'Free Median': free_stats['median'],
            'Free Std': free_stats['std']
        })

    stats_df = pd.DataFrame(stats_data)
    st.dataframe(stats_df, use_container_width=True)

    # Visualization
    st.subheader("📈 Metric Analysis")
    
    selected_metric = st.selectbox(
        "Select metric to analyze",
        core_metrics,
        format_func=lambda x: f"{x} ({stats_df[stats_df['Metric'] == x]['Description'].iloc[0]})"
    )

    col1, col2 = st.columns(2)

    with col1:
        fig = px.box(df, x='adopter', y=selected_metric,
                    color='adopter',
                    title=f"{selected_metric} by User Type",
                    color_discrete_map={0: '#4ECDC4', 1: '#FF6B6B'})
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.histogram(df, x=selected_metric,
                          color='adopter',
                          marginal="box",
                          title=f"{selected_metric} Distribution",
                          color_discrete_map={0: '#4ECDC4', 1: '#FF6B6B'})
        st.plotly_chart(fig, use_container_width=True) 