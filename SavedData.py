import streamlit as st
import sqlite3
import pandas as pd

# 1. Connect to the SQLite database
# If the file doesn't exist, this will create an empty one
conn = sqlite3.connect('survey_results.db')

# 2. Fetch data directly into a pandas DataFrame
query = "SELECT * FROM responses"
df = pd.read_sql(query, conn)

# 3. Close the connection
conn.close()

# 4. Display in Streamlit
st.title("Database Records")
st.dataframe(df) # Renders an interactive table
