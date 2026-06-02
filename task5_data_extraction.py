import sqlite3
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

customers = [
    (1, "John Doe",    "john@example.com",  "2024-01-10"),
    (2, "Alice Smith", "alice@example.com", "2024-02-15"),
    (3, "Bob Johnson", "bob@example.com",   "2024-03-20"),
]

sales = [
    (1, 1, "Laptop",   1200.50, "2026-05-26"),
    (2, 2, "Phone",     800.00, "2026-05-27"),
    (3, 1, "Keyboard",  150.75, "2026-05-28"),
    (4, 3, "Monitor",   400.00, "2026-05-25"),
    (5, 2, "Tablet",    650.00, "2026-05-28"),
]


def setup_database(db_path="sales_data.db"):
    """Creates and seeds the SQLite database. Returns (conn, cursor)."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customer (
            customer_id INTEGER PRIMARY KEY,
            name TEXT, email TEXT, join_date TEXT)
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            sale_id INTEGER PRIMARY KEY,
            customer_id INTEGER, product TEXT, amount REAL, sale_date TEXT,
            FOREIGN KEY(customer_id) REFERENCES customer(customer_id))
    """)
    cursor.execute("DELETE FROM customer")
    cursor.execute("DELETE FROM sales")
    cursor.executemany("INSERT INTO customer VALUES (?, ?, ?, ?)", customers)
    cursor.executemany("INSERT INTO sales VALUES (?, ?, ?, ?, ?)", sales)
    conn.commit()
    return conn, cursor


def run_query(user_question, db_path="sales_data.db"):
    """
    Takes a natural language question, generates SQL via Gemini,
    executes it, and returns (generated_sql, column_names, results).
    """
    conn, cursor = setup_database(db_path)

    prompt = f"""You are an expert SQL generator.

Database Schema:
Table customer(customer_id INTEGER PRIMARY KEY, name TEXT, email TEXT, join_date TEXT)
Table sales(sale_id INTEGER PRIMARY KEY, customer_id INTEGER, product TEXT, amount REAL, sale_date TEXT, FOREIGN KEY(customer_id) REFERENCES customer(customer_id))

Rules:
1. Generate ONLY SQLite SQL query.
2. Do not include explanations.
3. Do not use markdown.
4. Use valid SQLite syntax.

Natural Language Query: {user_question}"""

    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    generated_sql = response.text.strip().replace("```sql", "").replace("```", "").strip()

    cursor.execute(generated_sql)
    results = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    conn.close()

    return generated_sql, column_names, results


if __name__ == '__main__':
    user_question = input("Enter your question: ")
    generated_sql, column_names, results = run_query(user_question)

    print("\nGenerated SQL Query:")
    print(generated_sql)

    if not results:
        print("No results for the query.")
    else:
        header = " | ".join(column_names)
        print("\n" + header)
        print("-" * len(header))
        for row in results:
            print(" | ".join(str(v) for v in row))
        print("\nQuery executed successfully.")