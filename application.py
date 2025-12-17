import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for

application = Flask(__name__)

# Absolute path for EB
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "tasks.db")

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Create tasks table if it doesn't exist"""
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@application.route("/", methods=["GET", "POST"])
def index():
    init_db()  # Ensure table exists before queries
    conn = get_db_connection()

    if request.method == "POST":
        task = request.form["task"]
        if task.strip():
            conn.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
            conn.commit()

    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    return render_template("index.html", tasks=tasks)

@application.route("/delete/<int:id>")
def delete(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))
