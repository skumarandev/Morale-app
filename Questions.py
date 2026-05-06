import streamlit as st
import sqlite3

DB_PATH = 'survey_results.db'


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS text_responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            motivation TEXT NOT NULL,
            expectations TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


def save_text_response(motivation: str, expectations: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO text_responses (motivation, expectations)
        VALUES (?, ?)
    ''', (motivation, expectations))
    conn.commit()
    conn.close()


def main():
    st.set_page_config(page_title='Text Survey', layout='centered')
    init_db()

    st.title('Team Motivation Survey')
    st.markdown('Please answer the following questions about your motivation and what you want out of Xanite.')

    with st.form('text_survey_form'):
        motivation = st.text_area(
            'What motivates you in the context of the team/EQ?',
            height=160,
            placeholder='Share what energizes you and keeps you engaged in the team.'
        )

        expectations = st.text_area(
            'What do you want out of this project (project in this case = Xanite in general)?',
            height=160,
            placeholder='Share your goals, hopes, or outcomes you want from Xanite.'
        )

        submitted = st.form_submit_button('Submit')

    if submitted:
        if not motivation.strip() or not expectations.strip():
            st.error('Please answer both questions before submitting.')
        else:
            save_text_response(motivation.strip(), expectations.strip())
            st.success('Thank you! Your answers have been saved.')

if st.button("Go to Admin Page"):
    st.switch_page("pages/SavedData.py")    

if __name__ == '__main__':
    main()
