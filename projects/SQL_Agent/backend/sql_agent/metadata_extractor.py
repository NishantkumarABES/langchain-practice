import psycopg2

DB_CONFIG = {
    "dbname": "SQL_Agent_DB",
    "user": "postgres",
    "password": "admin",
    "host": "localhost",
    "port": "5432"
}

def connect_to_db():
    """Establish connection to PostgreSQL"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def fetch_metadata():
    """Fetch database metadata (tables, columns, constraints, descriptions)"""
    conn = connect_to_db()
    if not conn:
        return {}

    cursor = conn.cursor()
    
    # Query to get all tables in the public schema
    cursor.execute("""
        SELECT table_name FROM information_schema.tables
        WHERE table_schema = 'public'
    """)
    tables = cursor.fetchall()

    metadata = {}

    for table in tables:
        table_name = table[0]
        
        # Fetch column details
        cursor.execute(f"""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = %s
        """, (table_name,))
        columns = cursor.fetchall()

        # Fetch constraints
        cursor.execute(f"""
            SELECT 
                tc.constraint_type, kcu.column_name
            FROM information_schema.table_constraints AS tc
            JOIN information_schema.key_column_usage AS kcu
            ON tc.constraint_name = kcu.constraint_name
            WHERE tc.table_name = %s
        """, (table_name,))
        constraints = cursor.fetchall()

        # Fetch table and column descriptions (if any)
        cursor.execute(f"""
            SELECT obj_description('{table_name}'::regclass, 'pg_class')
        """)
        table_description = cursor.fetchone()[0]

        column_details = {}
        for column_name, data_type, is_nullable in columns:
            column_details[column_name] = {
                "data_type": data_type,
                "is_nullable": is_nullable,
                "constraints": [
                    constraint_type for constraint_type, col in constraints if col == column_name
                ]
            }

        metadata[table_name] = {
            "description": table_description or "No description available",
            "columns": column_details
        }

    cursor.close()
    conn.close()

    return metadata



def metadata_to_text(metadata):
    """Convert JSON metadata to a structured text format for embedding."""
    structured_text = []

    for table, details in metadata.items():
        table_description = details.get("description", "No description available")
        structured_text.append(f"Table: {table}\nDescription: {table_description}\nColumns:")

        for column, col_details in details["columns"].items():
            col_type = col_details["data_type"]
            nullable = "NULLABLE" if col_details["is_nullable"] == "YES" else "NOT NULL"
            constraints = ", ".join(col_details["constraints"]) if col_details["constraints"] else "No constraints"
            
            structured_text.append(f"- {column} ({col_type}, {nullable}, {constraints})")
        
        structured_text.append("\n")  # Add spacing between tables
    
    return "\n".join(structured_text)

if __name__ == "__main__":
    json_metadata = fetch_metadata()
    text_metadata = metadata_to_text(json_metadata)
    with open("database_metadata.txt", "w") as txt_file:
        txt_file.write(text_metadata)
    print("✅ Database metadata extracted and saved to 'database_metadata.txt'")