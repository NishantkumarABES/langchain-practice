import os
import psycopg2
from langchain.tools import Tool

def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

# 1️⃣ List all tables in the database
def list_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tables

# 2️⃣ Get schema for a given table
def get_table_schema(table_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_name = %s;
    """, (table_name,))
    
    schema = {col[0]: {"data_type": col[1], "nullable": col[2]} for col in cursor.fetchall()}
    conn.close()
    return schema

# 3️⃣ Get sample data from a table
def get_sample_data(table_name, limit=5):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name} LIMIT %s;", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows

# Convert functions into LangChain tools
list_tables_tool = Tool(
    name="ListTables",
    func=list_tables,
    description="Returns a list of all table names in the database."
)

get_schema_tool = Tool(
    name="GetTableSchema",
    func=get_table_schema,
    description="Returns the schema (columns, types, constraints) for a given table."
)

get_sample_tool = Tool(
    name="GetSampleData",
    func=get_sample_data,
    description="Returns sample rows from a table to help understand the data."
)


