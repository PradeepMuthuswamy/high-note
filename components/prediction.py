import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import plotly.graph_objects as go

def show_prediction_tab(df):
    st.header("Premium User Prediction Model")
    
    # Define features for the model
    features = ['friend_cnt', 'subscriber_friend_cnt', 'songsListened', 
                'lovedTracks', 'posts', 'playlists', 'shouts']
    
    # Prepare the data
    X = df[features]
    y = df['adopter']
    
    # Create and train the model
    @st.cache_resource
    def train_model(X, y):
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale the features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train the model
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train_scaled, y_train)
        
        return model, scaler, X_test_scaled, y_test

    model, scaler, X_test_scaled, y_test = train_model(X, y)
    
    # Model performance metrics
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    # Display metrics
    st.subheader("Model Performance")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Accuracy", f"{accuracy:.2%}")
    with col2:
        st.metric("Precision", f"{precision:.2%}")
    with col3:
        st.metric("Recall", f"{recall:.2%}")
    with col4:
        st.metric("F1 Score", f"{f1:.2%}")
    
    # Feature importance
    importance_df = pd.DataFrame({
        'Feature': features,
        'Importance': model.feature_importances_
    }).sort_values('Importance', ascending=False)
    
    st.subheader("Feature Importance")
    fig = px.bar(importance_df, x='Feature', y='Importance',
                 title="Feature Importance in Prediction Model",
                 color='Importance',
                 color_continuous_scale=['#4ECDC4', '#FF6B6B'])
    st.plotly_chart(fig, use_container_width=True)
    
    # User Prediction Interface
    st.subheader("Predict Premium User Likelihood")
    
    col1, col2 = st.columns(2)
    user_input = {}
    
    with col1:
        for feature in features[:4]:
            user_input[feature] = st.number_input(
                f"Enter {feature}",
                min_value=0,
                value=int(df[feature].mean())
            )
    
    with col2:
        for feature in features[4:]:
            user_input[feature] = st.number_input(
                f"Enter {feature}",
                min_value=0,
                value=int(df[feature].mean())
            )
    
    if st.button("Predict"):
        input_df = pd.DataFrame([user_input])
        input_scaled = scaler.transform(input_df)
        prediction = model.predict_proba(input_scaled)[0]
        
        st.subheader("Prediction Result")
        prob_premium = prediction[1]
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prob_premium * 100,
            title={'text': "Premium Subscription Likelihood"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#FF6B6B"},
                'steps': [
                    {'range': [0, 33], 'color': "#4ECDC4"},
                    {'range': [33, 66], 'color': "#FFD93D"},
                    {'range': [66, 100], 'color': "#FF6B6B"}
                ]
            }
        ))
        
        st.plotly_chart(fig, use_container_width=True)
        
        if prob_premium >= 0.7:
            st.success("This user is highly likely to become a premium subscriber!")
        elif prob_premium >= 0.4:
            st.warning("This user shows moderate potential for premium subscription.")
        else:
            st.error("This user is less likely to become a premium subscriber.") 