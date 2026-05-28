# app.py

import sqlite3
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

# -----------------------------
# Configure Gemini API
# -----------------------------
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# -----------------------------
# Create SQLite Database
# -----------------------------
conn = sqlite3.connect("sales_data.db")
cursor = conn.cursor()

# -----------------------------
# Create Tables
# -----------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS customer (
    customer_id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    join_date TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    sale_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product TEXT,
    amount REAL,
    sale_date TEXT,
    FOREIGN KEY(customer_id) REFERENCES customer(customer_id)
)
""")

# -----------------------------
# Insert Sample Data
# -----------------------------
cursor.execute("DELETE FROM customer")
cursor.execute("DELETE FROM sales")

customers = [
    (1, "John Doe", "john@example.com", "2024-01-10"),
    (2, "Alice Smith", "alice@example.com", "2024-02-15"),
    (3, "Bob Johnson", "bob@example.com", "2024-03-20")
]

sales = [
    (1, 1, "Laptop", 1200.50, "2026-05-26"),
    (2, 2, "Phone", 800.00, "2026-05-27"),
    (3, 1, "Keyboard", 150.75, "2026-05-28"),
    (4, 3, "Monitor", 400.00, "2026-05-25"),
    (5, 2, "Tablet", 650.00, "2026-05-28")
]

cursor.executemany(
    "INSERT INTO customer VALUES (?, ?, ?, ?)",
    customers
)

cursor.executemany(
    "INSERT INTO sales VALUES (?, ?, ?, ?, ?)",
    sales
)

conn.commit()

# -----------------------------
# User Natural Language Input
# -----------------------------
user_question = input("Enter your question: ")

# Example:
# highest sales amount done by a customer in last 3 days

# -----------------------------
# Prompt for LLM
# -----------------------------
prompt = f"""
You are an expert SQL generator.

Database Schema:

Table customer(
    customer_id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    join_date TEXT
)

Table sales(
    sale_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product TEXT,
    amount REAL,
    sale_date TEXT,
    FOREIGN KEY(customer_id) REFERENCES customer(customer_id)
)

Rules:
1. Generate ONLY SQLite SQL query.
2. Do not include explanations.
3. Do not use markdown.
4. Use valid SQLite syntax.

Natural Language Query:
{user_question}
"""

# -----------------------------
# Generate SQL Query
# -----------------------------
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

generated_sql = response.text.strip()

# Remove accidental markdown if present
generated_sql = generated_sql.replace("```sql", "").replace("```", "").strip()

print("\nGenerated SQL Query:")
print(generated_sql)

# -----------------------------
# Execute Generated Query
# -----------------------------
try:
    cursor.execute(generated_sql)
    results = cursor.fetchall()


    # No rows found
    if len(results) == 0:
        print("No results for the query.")

    else:
        column_names = [desc[0] for desc in cursor.description]

        # Single value result
        if len(column_names) == 1 and len(results) == 1:
            print(f"{column_names[0]}: {results[0][0]}")

        # Multiple rows / columns
        else:
            # Print headers
            header = " | ".join(column_names)

            print(header)
            print("-" * len(header))

            # Print rows
            for row in results:
                formatted_row = " | ".join(str(value) for value in row)
                print(formatted_row)

        print("\nQuery executed successfully.")

except Exception as e:
    print("\nError executing SQL query:")
    print(e)

finally:
    conn.close()