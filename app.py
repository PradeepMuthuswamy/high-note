import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Page config
st.set_page_config(page_title="High Note User Analysis", layout="wide")


# Load data
@st.cache_data
def load_data():
    df = pd.read_excel("High Note data.xlsx")
    dict_df = pd.read_excel("High Note data dictionary.xlsx")
    return df, dict_df


df, dict_df = load_data()

# Main title
st.title("🎵 High Note User Analysis Dashboard")

# Top metrics
total_users = len(df)
premium_users = len(df[df['adopter'] == 1])
premium_rate = (premium_users / total_users) * 100

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Users", f"{total_users:,}")
with col2:
    st.metric("Premium Users", f"{premium_users:,}")
with col3:
    st.metric("Premium Conversion Rate", f"{premium_rate:.1f}%")
with col4:
    avg_tenure = df['tenure'].mean()
    st.metric("Average User Tenure", f"{avg_tenure:.1f} months")

# Main tabs
tabs = st.tabs(["🎯 Premium vs Free Users", "🌍 User Geography", "📊 Usage Patterns", "🔍 Core Metrics Analysis (B-M)"])

# Tab 1: Premium vs Free Users
with tabs[0]:
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

# Tab 2: Geographic Analysis
with tabs[1]:
    st.header("Geographic Analysis")

    col1, col2 = st.columns(2)
    with col1:
        # Original visualization
        country_dist = df.groupby('good_country')['adopter'].mean().reset_index()
        fig = px.bar(country_dist, x='good_country', y='adopter',
                     title="Premium Adoption by Region",
                     color='adopter',
                     color_continuous_scale=['#4ECDC4', '#FF6B6B'])
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Add pie chart
        country_counts = df[df['adopter'] == 1]['good_country'].value_counts()
        fig = px.pie(values=country_counts.values,
                     names=country_counts.index,
                     title="Premium Users Distribution by Country Type",
                     color_discrete_sequence=['#FF6B6B', '#4ECDC4'])
        st.plotly_chart(fig, use_container_width=True)

    # Add friend country analysis
    st.subheader("Friend Network Geographic Analysis")
    col3, col4 = st.columns(2)

    with col3:
        # Box plot of friend countries
        fig = px.box(df, x='adopter', y='friend_country_cnt',
                     color='adopter',
                     title="Friend Countries Distribution",
                     color_discrete_map={0: '#4ECDC4', 1: '#FF6B6B'})
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        # Violin plot
        fig = px.violin(df, x='adopter', y='friend_country_cnt',
                        color='adopter',
                        box=True,
                        title="Friend Countries Distribution (Detailed)",
                        color_discrete_map={0: '#4ECDC4', 1: '#FF6B6B'})
        st.plotly_chart(fig, use_container_width=True)

# Tab 3: Usage Patterns
with tabs[2]:
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

    # Cumulative analysis
    st.subheader("Cumulative Usage Analysis")
    col3, col4 = st.columns(2)

    with col3:
        # Scatter plot
        fig = px.scatter(df, x=selected_metric, y='posts',
                         color='adopter',
                         title=f"{selected_metric} vs Posts",
                         color_discrete_map={0: '#4ECDC4', 1: '#FF6B6B'})
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        # Box plot comparison
        fig = px.box(df, x='adopter', y=selected_metric,
                     color='adopter',
                     title=f"{selected_metric} by User Type",
                     color_discrete_map={0: '#4ECDC4', 1: '#FF6B6B'})
        st.plotly_chart(fig, use_container_width=True)

# Tab 4: Core Metrics Analysis
with tabs[3]:
    st.header("Core Metrics Analysis (Columns B-M)")

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

        premium_mode = premium_data.mode().iloc[0] if not premium_data.empty else None
        free_mode = free_data.mode().iloc[0] if not free_data.empty else None

        premium_stats = premium_data.agg(['mean', 'median', 'std', 'min', 'max']).round(2)
        free_stats = free_data.agg(['mean', 'median', 'std', 'min', 'max']).round(2)

        stats_data.append({
            'Metric': metric,
            'Description': dict_df[dict_df['Variable'] == metric]['Description'].values[0]
            if len(dict_df[dict_df['Variable'] == metric]['Description'].values) > 0
            else 'No description available',
            'Premium Mean': premium_stats['mean'],
            'Premium Median': premium_stats['median'],
            'Premium Mode': premium_mode,
            'Premium Std': premium_stats['std'],
            'Free Mean': free_stats['mean'],
            'Free Median': free_stats['median'],
            'Free Mode': free_mode,
            'Free Std': free_stats['std']
        })

    stats_df = pd.DataFrame(stats_data)
    st.dataframe(stats_df)

    # Distribution Analysis
    st.subheader("Distribution Analysis")
    selected_core_metric = st.selectbox("Select Core Metric", core_metrics,
                                        format_func=lambda
                                            x: f"{x} ({stats_df[stats_df['Metric'] == x]['Description'].iloc[0]})")

    col1, col2 = st.columns(2)

    with col1:
        # Distribution plot
        fig = px.histogram(df, x=selected_core_metric, color='adopter',
                           marginal="box",
                           title=f"{selected_core_metric} Distribution",
                           color_discrete_map={0: '#4ECDC4', 1: '#FF6B6B'})
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Box plot with violin
        fig = px.violin(df, x='adopter', y=selected_core_metric,
                        color='adopter', box=True,
                        title=f"{selected_core_metric} Distribution by User Type",
                        color_discrete_map={0: '#4ECDC4', 1: '#FF6B6B'})
        st.plotly_chart(fig, use_container_width=True)

    # Correlation Analysis
    st.subheader("Correlation Analysis")
    correlation_matrix = df[core_metrics].corr()
    fig = px.imshow(correlation_matrix,
                    title="Core Metrics Correlation Matrix",
                    color_continuous_scale="RdBu")
    st.plotly_chart(fig, use_container_width=True)

# Key Insights and Recommendations
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.header("📊 Key Insights")
    st.markdown("""
    **1. User Engagement**
    - Premium users show significantly higher engagement across all metrics
    - Strong correlation between social activity (posts, shouts) and premium status
    - Premium users maintain more diverse friend networks

    **2. Geographic Patterns**
    - Clear differences in adoption rates across regions
    - Premium users have more geographically diverse networks
    - Strong network effects in premium adoption

    **3. Usage Patterns**
    - Premium users show higher activity levels pre-conversion
    - Strong correlation between different engagement metrics
    - Distinct behavioral patterns between user groups
    """)

with col2:
    st.header("💡 Recommendations")
    st.markdown("""
    **1. Targeting Strategy**
    - Focus on users with high social engagement
    - Target users with existing premium connections
    - Identify users with diverse geographic networks

    **2. Engagement Initiatives**
    - Promote social features and interactions
    - Encourage playlist creation and sharing
    - Create community-focused events

    **3. Geographic Focus**
    - Prioritize high-conversion regions
    - Leverage existing premium networks
    - Create region-specific campaigns

    **4. Retention Strategy**
    - Monitor post-conversion engagement
    - Develop premium-exclusive features
    - Build community engagement programs
    """)

# Data Dictionary
with st.expander("📚 Data Dictionary"):
    st.dataframe(dict_df[['Variable', 'Description', 'Notes']])