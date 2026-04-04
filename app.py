from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

DATABASE = "clients.db"


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

    conn.close()


init_db()


programs = {
    "fat_loss": 0.8,
    "muscle_gain": 1.2,
    "beginner": 1.0
}


@app.route("/")
def home():
    return jsonify({"message": "ACEest Fitness API v2.2.4 FINAL"})


# ✅ ADD / UPDATE CLIENT
@app.route("/add-client", methods=["POST"])
def add_client():
    data = request.get_json()

    name = data.get("name")
    program = data.get("program")
    calories = data.get("calories")

    if not isinstance(name, str) or not name.strip():
        return {"error": "Invalid name"}, 400

    if program not in programs:
        return {"error": "Invalid program"}, 400

    if not isinstance(calories, int) or calories <= 0:
        return {"error": "Invalid calories"}, 400

    conn = get_db_connection()
    conn.execute(
        "INSERT OR REPLACE INTO clients (name, program, calories) VALUES (?, ?, ?)",
        (name.strip(), program, calories)
    )
    conn.commit()
    conn.close()

    return {"message": "Client saved"}, 201


# ✅ GET CLIENT
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


# ✅ SAVE PROGRESS
@app.route("/progress", methods=["POST"])
def save_progress():
    data = request.get_json()

    name = data.get("name")
    week = data.get("week")
    adherence = data.get("adherence")

    if not name or not week or not isinstance(adherence, int):
        return {"error": "Invalid data"}, 400

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO progress (name, week, adherence) VALUES (?, ?, ?)",
        (name, week, adherence)
    )
    conn.commit()
    conn.close()

    return {"message": "Progress saved"}, 201


# ✅ GET PROGRESS
@app.route("/progress/<name>")
def get_progress(name):
    conn = get_db_connection()
    rows = conn.execute(
        "SELECT week, adherence FROM progress WHERE name=?",
        (name,)
    ).fetchall()
    conn.close()

    if not rows:
        return {"message": "No progress found"}, 404

    return jsonify([dict(row) for row in rows])


# ✅ DELETE CLIENT (NEW IN FINAL)
@app.route("/client/<name>", methods=["DELETE"])
def delete_client(name):
    conn = get_db_connection()
    conn.execute("DELETE FROM clients WHERE name=?", (name,))
    conn.commit()
    conn.close()

    return {"message": "Client deleted"}


# ✅ CALCULATE CALORIES
@app.route("/calculate-calories", methods=["POST"])
def calculate_calories():
    data = request.get_json()

    program = data.get("program")
    base_calories = data.get("base_calories")

    if program not in programs:
        return {"error": "Invalid program"}, 400

    if not isinstance(base_calories, int):
        return {"error": "Invalid calories"}, 400

    return {
        "recommended_calories": base_calories * programs[program]
    }


if __name__ == "__main__":
    app.run(debug=True)