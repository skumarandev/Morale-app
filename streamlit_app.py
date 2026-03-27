import streamlit as st
import sqlite3

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('survey_results.db')
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
    conn.commit()
    conn.close()

def save_response(data):
    conn = sqlite3.connect('survey_results.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO responses 
        (clarity, energy, psychological_safety, work_life_balance, confidence, efficiency)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', data)
    conn.commit()
    conn.close()

# --- APP UI ---
def main():
    st.set_page_config(page_title="Team Health Survey", layout="centered")
    init_db()

    st.title("Team Health Check")
    st.info("ℹ️ All answers will be saved anonymously")

    # Define the survey questions based on your image
    questions = [
        {"key": "clarity", "label": "Clarity", "desc": "I clearly understand what is expected of me on this team"},
        {"key": "energy", "label": "Energy", "desc": "I am energized by the work I do"},
        {"key": "psychological_safety", "label": "Psychological Safety", "desc": "I feel safe and do not fear making mistakes, raising issues, taking risks, or asking for help"},
        {"key": "work_life_balance", "label": "Work-life Balance", "desc": "My typical workload allows me to achieve an acceptable level of work-life balance"},
        {"key": "confidence", "label": "Confidence", "desc": "I'm confident our team will be successful"},
        {"key": "efficiency", "label": "Efficiency", "desc": "Tools, resources, processes, procedures allow me to effectively meet my customers' needs"},
    ]

    responses = []

    # Display Scale Legend
    cols = st.columns([1, 1, 1])
    cols[0].markdown(":red[**Unfavorable (1-6)**]")
    cols[1].markdown(":orange[**Neutral (7-8)**]")
    cols[2].markdown(":green[**Favorable (9-10)**]")

    st.divider()

    # Generate Form
    with st.form("survey_form"):
        for q in questions:
            st.markdown(f"### {q['label']}")
            st.caption(q['desc'])
            # Create a horizontal radio row 1-10
            val = st.radio(
                f"Select rating for {q['label']}",
                options=list(range(1, 11)),
                horizontal=True,
                index=7, # Default to 8 (Neutral)
                key=q['key'],
                label_visibility="collapsed"
            )
            responses.append(val)
            st.write("") # Spacer

        # Submit button
        col1, col2 = st.columns([1, 5])
        with col1:
            submit = st.form_submit_button("Submit", type="primary")
        with col2:
            if st.form_submit_button("Cancel"):
                st.rerun()

    if submit:
        save_response(tuple(responses))
        st.success("Thank you! Your feedback has been recorded anonymously.")
        st.balloons()

if __name__ == "__main__":
    main()
