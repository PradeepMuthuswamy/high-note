import streamlit as st
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import os

# Import components
from components.premium_vs_free import show_premium_vs_free_tab
from components.geography import show_geography_tab
from components.chat_analysis import show_chat_analysis_tab
from components.usage_patterns import show_usage_patterns_tab
from components.core_metrics import show_core_metrics_tab
from components.prediction import show_prediction_tab
# Import other components...

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Page config
st.set_page_config(page_title="High Note User Analysis", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_excel("High Note data.xlsx")
    dict_df = pd.read_excel("High Note data dictionary.xlsx")
    return df, dict_df

df, dict_df = load_data()

# Main title and metrics
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

# Create tabs
tabs = st.tabs(["🎯 Premium vs Free Users", "🌍 User Geography", "📊 Usage Patterns", 
                "🔍 Core Metrics Analysis (B-M)", "🤖 Prediction Model", "💬 Analysis Chat"])

# Show content for each tab
with tabs[0]:
    show_premium_vs_free_tab(df)
    
with tabs[1]:
    show_geography_tab(df)
    
with tabs[2]:
    show_usage_patterns_tab(df)
    
with tabs[3]:
    show_core_metrics_tab(df, dict_df)
    
with tabs[4]:
    show_prediction_tab(df)
    
with tabs[5]:
    show_chat_analysis_tab(df, dict_df, client)

# Data Dictionary
with st.expander("📚 Data Dictionary"):
    st.dataframe(dict_df[['Variable', 'Description', 'Notes']])