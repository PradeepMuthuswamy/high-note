import streamlit as st
import pandas as pd
import time

def get_numeric_data_context(df):
    # Get only numeric columns
    numeric_df = df.select_dtypes(include=['int64', 'float64'])
    
    # Create a JSON-like string with key statistics and sample data
    data_stats = {
        'numerical_stats': numeric_df.describe().to_dict(),
        'correlations': numeric_df.corr()['adopter'].to_dict(),
        'sample_data': numeric_df.head(5).to_dict('records'),
        'column_info': {col: {
            'dtype': str(numeric_df[col].dtype),
            'unique_values': len(numeric_df[col].unique()),
            'missing_values': numeric_df[col].isnull().sum()
        } for col in numeric_df.columns}
    }
    return data_stats

def show_chat_analysis_tab(df, dict_df, client):
    st.header("Chat with High Note Analysis Assistant")
    
    # Initialize chat history and processed suggestions in session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "processed_suggestions" not in st.session_state:
        st.session_state.processed_suggestions = set()
    
    # Create a container for chat messages
    chat_container = st.container()
    
    with chat_container:
        # Display chat messages from history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Function to generate analysis insights
    def generate_analysis_response(prompt):
        # Get data context
        data_context = get_numeric_data_context(df)
        
        total_users = len(df)
        premium_users = len(df[df['adopter'] == 1])
        premium_rate = (premium_users / total_users) * 100
        avg_tenure = df['tenure'].mean()
        
        # Create a context string with key metrics and data insights
        context = f"""
        Key metrics about High Note:
        - Total Users: {total_users:,}
        - Premium Users: {premium_users:,}
        - Premium Conversion Rate: {premium_rate:.1f}%
        - Average User Tenure: {avg_tenure:.1f} months
        
        Data Dictionary:
        {dict_df[['Variable', 'Description']].to_dict('records')}
        
        Statistical Context:
        1. Correlation with Premium Adoption:
        {dict(sorted(data_context['correlations'].items(), key=lambda x: abs(x[1]), reverse=True))}
        
        2. Key Metrics Statistics:
        {data_context['numerical_stats']}
        
        3. Sample User Data:
        {data_context['sample_data']}
        """
        
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"""You are a data analysis assistant for High Note, a music streaming service. 
                    You have access to detailed user data and statistics. 
                    
                    Context about the data:
                    {context}
                    
                    Your role is to:
                    1. Provide data-driven insights and recommendations
                    2. Use specific numbers and statistics from the data
                    3. Identify actionable patterns and trends
                    4. Suggest concrete steps for improvement
                    5. Focus on practical, implementable solutions
                    
                    Format your responses with:
                    - Clear sections
                    - Bullet points for key findings
                    - Specific metrics when relevant
                    - Actionable recommendations
                    
                    Always maintain a professional, analytical tone."""},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating response: {str(e)}"

    # Chat input
    if prompt := st.chat_input("Ask about High Note's user analysis..."):
        with chat_container:
            # Display user message
            st.chat_message("user").markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Generate and display assistant response
            with st.chat_message("assistant"):
                with st.spinner('Analyzing data and generating response...'):
                    response = generate_analysis_response(prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})

    # Add helpful prompt suggestions
    st.markdown("### Suggested Questions:")
    
    # Create two columns for suggestions
    col1, col2 = st.columns(2)
    
    suggestions = [
        "What are the strongest predictors of premium conversion based on the correlation data?",
        "Based on the user statistics, what are the key characteristics of our most engaged users?",
        "What patterns do you see in the sample data that could inform our targeting strategy?",
        "How do social network metrics correlate with premium adoption?",
        "What specific metrics should we focus on improving to increase premium conversion?",
        "Can you analyze the geographic distribution and suggest region-specific strategies?",
        "What user behaviors show the strongest correlation with premium adoption?",
        "Based on the data, what would be the most effective retention strategies?"
    ]
    
    # Display suggestions in two columns
    for i, suggestion in enumerate(suggestions):
        if suggestion in st.session_state.processed_suggestions:
            continue
            
        with col1 if i % 2 == 0 else col2:
            if st.button(f"📝 {suggestion}", key=f"suggestion_{i}"):
                with chat_container:
                    # Display user message
                    st.chat_message("user").markdown(suggestion)
                    st.session_state.messages.append({"role": "user", "content": suggestion})
                    
                    # Generate and display assistant response
                    with st.chat_message("assistant"):
                        with st.spinner('Analyzing data and generating response...'):
                            response = generate_analysis_response(suggestion)
                            st.markdown(response)
                            st.session_state.messages.append({"role": "assistant", "content": response})
                st.session_state.processed_suggestions.add(suggestion)

    # Add clear chat button at the bottom
    if st.button("🗑️ Clear Chat History", key="clear_chat"):
        st.session_state.messages = []
        st.session_state.processed_suggestions = set()
        st.rerun() 