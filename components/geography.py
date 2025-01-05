import streamlit as st
import plotly.express as px

def show_geography_tab(df):
    st.header("Geographic Analysis")

    col1, col2 = st.columns(2)
    with col1:
        country_dist = df.groupby('good_country')['adopter'].mean().reset_index()
        fig = px.bar(country_dist, x='good_country', y='adopter',
                     title="Premium Adoption by Region",
                     color='adopter',
                     color_continuous_scale=['#4ECDC4', '#FF6B6B'])
        st.plotly_chart(fig, use_container_width=True)

    with col2:
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
        fig = px.box(df, x='adopter', y='friend_country_cnt',
                     color='adopter',
                     title="Friend Countries Distribution",
                     color_discrete_map={0: '#4ECDC4', 1: '#FF6B6B'})
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        fig = px.violin(df, x='adopter', y='friend_country_cnt',
                        color='adopter',
                        box=True,
                        title="Friend Countries Distribution (Detailed)",
                        color_discrete_map={0: '#4ECDC4', 1: '#FF6B6B'})
        st.plotly_chart(fig, use_container_width=True) 