import streamlit as st
import sqlite3
import pandas as pd
import numpy as np

DB_PATH = 'survey_results.db'

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            clarity INTEGER,
            energy INTEGER,
            psychological_safety INTEGER,
            work_life_balance INTEGER,
            confidence INTEGER,
            efficiency INTEGER
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS text_responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            motivation TEXT,
            expectations TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


def table_exists(conn, name: str) -> bool:
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (name,))
    return cur.fetchone() is not None


# 1. Check if user is already logged in
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# 2. Define the login check logic
def check_password():
    """Returns True if the user had the correct password."""
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == "12345":
            st.session_state["authenticated"] = True
            del st.session_state["password"]  # Clear password from state
        else:
            st.session_state["authenticated"] = False
            st.error("😕 Access code incorrect")

    if not st.session_state["authenticated"]:
        # Display login input
        st.text_input("Enter Access Code", type="password", on_change=password_entered, key="password")
        return False
    else:
        return True


# 3. Main App Logic
if check_password():
    st.success("Access Granted!")
    st.title("Protected Dashboard")
    init_db()

    conn = sqlite3.connect(DB_PATH)

    if table_exists(conn, 'responses'):
        df = pd.read_sql("SELECT * FROM responses", conn)
    else:
        df = pd.DataFrame(columns=["id", "clarity", "energy", "psychological_safety", "work_life_balance", "confidence", "efficiency"])

    if not df.empty:
        cols_to_average = df.iloc[:, 1:7].apply(pd.to_numeric, errors='coerce')
        df["average"] = cols_to_average.mean(axis=1)

        conditions = [
            (df["average"] < 7),
            (df["average"] >= 7) & (df["average"] < 9)
        ]
        choices = [1, 2]
        df["morale"] = np.select(conditions, choices, default=3)

        average_morale_of_team = df["morale"].mean()
        st.write("Average Morale of Team:", average_morale_of_team)
    else:
        st.info("No numeric survey responses have been recorded yet.")

    st.header("Numeric Responses")
    st.dataframe(df, hide_index=True)

    if table_exists(conn, 'text_responses'):
        df_text = pd.read_sql("SELECT * FROM text_responses ORDER BY created_at DESC", conn)
    else:
        df_text = pd.DataFrame(columns=["id", "motivation", "expectations", "created_at"])

    st.header("Text Survey Responses")
    if df_text.empty:
        st.info("No text survey answers have been recorded yet.")
    else:
        st.dataframe(df_text, hide_index=True)

    if st.button("Log out"):
        st.session_state["authenticated"] = False
        st.rerun()

    delete_col1, delete_col2 = st.columns(2)
    with delete_col1:
        if st.button("Delete numeric survey responses"):
            c = conn.cursor()
            c.execute('DELETE FROM responses')
            conn.commit()
            conn.close()
            st.success("Numeric survey responses deleted.")
            st.rerun()
    with delete_col2:
        if st.button("Delete text survey responses"):
            c = conn.cursor()
            c.execute('DELETE FROM text_responses')
            conn.commit()
            conn.close()
            st.success("Text survey responses deleted.")
            st.rerun()

    conn.close()

