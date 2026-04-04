from flask import Flask, jsonify, request
import sqlite3
import os

app = Flask(__name__)

DATABASE = os.environ.get("DB_PATH", "clients.db")


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            program TEXT,
            calories INTEGER
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            week TEXT,
            adherence INTEGER
        )
    """)

    conn.commit()
    conn.close()


programs = {
    "fat_loss": 0.8,
    "muscle_gain": 1.2,
    "beginner": 1.0
}


@app.route("/")
def home():
    return jsonify({"message": "ACEest Fitness API v2.0.1"})


@app.route("/health")
def health():
    return jsonify({"status": "ok", "app": "ACEest Fitness API"}), 200


@app.route("/add-client", methods=["POST"])
def add_client():
    data = request.get_json()

    name = data.get("name")
    program = data.get("program")
    calories = data.get("calories")

    if not name or program not in programs:
        return {"error": "Invalid data"}, 400

    conn = get_db_connection()
    conn.execute(
        "INSERT OR REPLACE INTO clients (name, program, calories) VALUES (?, ?, ?)",
        (name, program, calories)
    )
    conn.commit()
    conn.close()

    return {"message": "Client saved"}, 201


@app.route("/client/<name>")
def get_client(name):
    conn = get_db_connection()
    row = conn.execute(
        "SELECT * FROM clients WHERE name=?",
        (name,)
    ).fetchone()
    conn.close()

    if not row:
        return {"error": "Client not found"}, 404

    return jsonify(dict(row))


@app.route("/progress", methods=["POST"])
def save_progress():
    data = request.get_json()

    name = data.get("name")
    week = data.get("week")
    adherence = data.get("adherence")

    if not name or not week or adherence is None:
        return {"error": "Invalid data"}, 400

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO progress (name, week, adherence) VALUES (?, ?, ?)",
        (name, week, adherence)
    )
    conn.commit()
    conn.close()

    return {"message": "Progress saved"}, 201


@app.route("/calculate-calories", methods=["POST"])
def calculate_calories():
    data = request.get_json()

    program = data.get("program")
    base_calories = data.get("base_calories")

    if program not in programs:
        return {"error": "Invalid program"}, 400

    return jsonify({
        "recommended_calories": base_calories * programs[program]
    })


if __name__ == "__main__":
    init_db()
    app.run(debug=False)