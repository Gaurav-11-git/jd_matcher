import streamlit as st
import pandas as pd

# Sample data
data = {
    'Category': ['A', 'B', 'C', 'D'],
    'Percentage': [75, 50, 90, 65]
}

# Create DataFrame
df = pd.DataFrame(data)

# Function to create bar representation
def bar_chart(percentage):
    return f'<div style="background-color: skyblue; width: {percentage}%; height: 20px;"></div>'

# Apply bar chart function to Percentage column
df['Percentage'] = df['Percentage'].apply(bar_chart)

# Display DataFrame with bars
st.title("Percentage Data with Horizontal Bars")
st.write("Here is the tabular data with horizontal bars:")
st.write(df.to_html(escape=False), unsafe_allow_html=True)
