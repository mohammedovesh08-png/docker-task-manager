from flask import Flask, render_template, request, redirect
import os
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "db"),
        user=os.getenv("DB_USER", "taskuser"),
        password=os.getenv("DB_PASSWORD", "taskpass123"),
        database=os.getenv("DB_NAME", "taskdb")
    )

@app.route("/")
def home():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255) NOT NULL)")
    cursor.execute("SELECT * FROM tasks ORDER BY id DESC")
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title", "").strip()
    if title:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (title) VALUES (%s)", (title,))
        conn.commit()
        cursor.close()
        conn.close()
    return redirect("/")

@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
