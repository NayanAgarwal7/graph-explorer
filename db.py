import sqlite3
import json

DATABASE_NAME = "graphs.db"

def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection

def init_db():
    connection = get_connection()

    with open("schema.sql", "r", encoding="utf-8") as schema_file:
        connection.executescript(schema_file.read())

    connection.commit()
    connection.close()

def save_graph(name, graph):
    connection = get_connection()

    graph_json = json.dumps(graph)

    connection.execute(
        """
        INSERT INTO graphs (name, graph_data)
        VALUES (?, ?)
        ON CONFLICT(name) DO UPDATE SET
            graph_data = excluded.graph_data
        """,
        (name, graph_json)
    )

    connection.commit()
    connection.close()

def load_graph(name):
    connection = get_connection()

    row = connection.execute(
        "SELECT graph_data FROM graphs WHERE name = ?",
        (name,)
    ).fetchone()

    connection.close()

    if row is None:
        return None

    return json.loads(row["graph_data"])

def list_graphs():
    connection = get_connection()

    rows = connection.execute(
        "SELECT id, name, created_at FROM graphs ORDER BY created_at DESC"
    ).fetchall()

    connection.close()

    return [dict(row) for row in rows]