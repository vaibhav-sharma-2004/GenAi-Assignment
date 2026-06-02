import streamlit as st
import subprocess
import sys
import os
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Task4_data_query'))
from Task4_data_query.app import load_document, ask_question

st.set_page_config(page_title="Module 7 Assignment", layout="wide")
st.title("Module 7 Assignment")

tab1, tab2, tab3, tab4 = st.tabs([
    "Task 2 - LLM Chat",
    "Task 3 - Data Augmentation",
    "Task 4 - Document Q&A",
    "Task 5 - Data Extraction"
])

# ── Task 2: LLM Chat ──────────────────────────────────────────────────────────
with tab1:
    st.header("Task 2 - LLM Chat")
    st.write("Runs `task2_LLM_chat.py` — summarises user activity and extracts structured JSON insights using Gemini.")
    if st.button("Run LLM Chat", key="llm_chat"):
        with st.spinner("Running..."):
            result = subprocess.run(
                [sys.executable, 'task2_LLM_chat.py'],
                capture_output=True, text=True,
                cwd=os.path.dirname(__file__)
            )
        if result.stdout:
            st.subheader("Output")
            st.text(result.stdout)
        if result.stderr:
            st.subheader("Errors")
            st.error(result.stderr)

# ── Task 3: Data Augmentation ─────────────────────────────────────────────────
with tab2:
    st.header("Task 3 - Data Augmentation")
    st.write("Runs `task3_data_augmentation.py` — generates 10 synthetic customer records from `customers.csv` using Gemini.")
    if st.button("Run Data Augmentation", key="augmentation"):
        with st.spinner("Running..."):
            result = subprocess.run(
                [sys.executable, 'task3_data_augmentation.py'],
                capture_output=True, text=True,
                cwd=os.path.dirname(__file__)
            )
        if result.stdout:
            st.subheader("Output")
            st.text(result.stdout)
        if result.stderr:
            st.subheader("Errors")
            st.error(result.stderr)

# ── Task 4: Document Q&A ──────────────────────────────────────────────────────
with tab3:
    st.header("Task 4 - Document Q&A")
    st.write("Upload a PDF or DOCX file and ask a question about its content.")
    uploaded_file = st.file_uploader("Upload PDF or DOCX", type=["pdf", "docx"])
    question = st.text_input("Your question")
    if st.button("Ask", key="ask_doc"):
        if not uploaded_file:
            st.warning("Please upload a file.")
        elif not question.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Processing document..."):
                try:
                    suffix = ".pdf" if uploaded_file.name.endswith(".pdf") else ".docx"
                    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                        tmp.write(uploaded_file.read())
                        temp_path = tmp.name
                    document_text = load_document(temp_path)
                    answer = ask_question(document_text, question)
                    os.remove(temp_path)
                    st.subheader("Answer")
                    st.write(answer)
                except Exception as e:
                    st.error(f"Error: {e}")

# ── Task 5: Data Extraction ───────────────────────────────────────────────────
with tab4:
    import pandas as pd
    from task5_data_extraction import run_query

    st.header("Task 5 - Data Extraction")
    st.write("Ask a natural language question about the sales database. Gemini will generate and run the SQL query.")

    with st.expander("View Database Schema"):
        st.code("""Table: customer
  customer_id INTEGER PRIMARY KEY
  name        TEXT
  email       TEXT
  join_date   TEXT

Table: sales
  sale_id     INTEGER PRIMARY KEY
  customer_id INTEGER (FK → customer)
  product     TEXT
  amount      REAL
  sale_date   TEXT""")

    user_question = st.text_input("Enter your question (e.g. 'Who spent the most?')", key="task5_question")

    if st.button("Run Query", key="extraction"):
        if not user_question.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Generating SQL and querying database..."):
                try:
                    db_path = os.path.join(os.path.dirname(__file__), "sales_data.db")
                    generated_sql, column_names, results = run_query(user_question, db_path)

                    st.subheader("Generated SQL")
                    st.code(generated_sql, language="sql")

                    st.subheader("Query Results")
                    if results:
                        st.dataframe(pd.DataFrame(results, columns=column_names))
                    else:
                        st.info("No results found for this query.")
                except Exception as e:
                    st.error(f"Error: {e}")