from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

DATABASE = "clients.db"


# ---------------- DB HELPERS ----------------
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

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


# ---------------- CONSTANTS ----------------
PROGRAMS = {
    "fat_loss": 0.8,
    "muscle_gain": 1.2,
    "beginner": 1.0
}


# ---------------- UTILS ----------------
def validate_client(data):
    name = data.get("name")
    program = data.get("program")
    calories = data.get("calories")

    if not isinstance(name, str) or not name.strip():
        return "Invalid name"

    if program not in PROGRAMS:
        return "Invalid program"

    if not isinstance(calories, int) or calories <= 0:
        return "Invalid calories"

    return None


def validate_progress(data):
    name = data.get("name")
    week = data.get("week")
    adherence = data.get("adherence")

    if not name or not week:
        return "Missing fields"

    if not isinstance(adherence, int) or not (0 <= adherence <= 100):
        return "Invalid adherence"

    return None


# ---------------- ROUTES ----------------

@app.route("/")
def home():
    return jsonify({"message": "ACEest API v3.2.4 FINAL"})


# 🔹 CREATE / UPDATE CLIENT
@app.route("/clients", methods=["POST"])
def create_client():
    data = request.get_json()

    error = validate_client(data)
    if error:
        return {"error": error}, 400

    conn = get_db()
    conn.execute(
        "INSERT OR REPLACE INTO clients (name, program, calories) VALUES (?, ?, ?)",
        (data["name"].strip(), data["program"], data["calories"])
    )
    conn.commit()
    conn.close()

    return {"message": "Client saved"}, 201


# 🔹 GET ALL CLIENTS
@app.route("/clients", methods=["GET"])
def get_clients():
    conn = get_db()
    rows = conn.execute("SELECT * FROM clients").fetchall()
    conn.close()

    return jsonify([dict(row) for row in rows])


# 🔹 GET CLIENT BY NAME
@app.route("/clients/<name>", methods=["GET"])
def get_client(name):
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM clients WHERE name=?",
        (name,)
    ).fetchone()
    conn.close()

    if not row:
        return {"error": "Client not found"}, 404

    return jsonify(dict(row))


# 🔹 DELETE CLIENT
@app.route("/clients/<name>", methods=["DELETE"])
def delete_client(name):
    conn = get_db()
    conn.execute("DELETE FROM clients WHERE name=?", (name,))
    conn.commit()
    conn.close()

    return {"message": "Client deleted"}


# 🔹 ADD PROGRESS
@app.route("/progress", methods=["POST"])
def add_progress():
    data = request.get_json()

    error = validate_progress(data)
    if error:
        return {"error": error}, 400

    conn = get_db()
    conn.execute(
        "INSERT INTO progress (name, week, adherence) VALUES (?, ?, ?)",
        (data["name"], data["week"], data["adherence"])
    )
    conn.commit()
    conn.close()

    return {"message": "Progress saved"}, 201


# 🔹 GET PROGRESS
@app.route("/progress/<name>", methods=["GET"])
def get_progress(name):
    conn = get_db()
    rows = conn.execute(
        "SELECT week, adherence FROM progress WHERE name=?",
        (name,)
    ).fetchall()
    conn.close()

    if not rows:
        return {"message": "No progress found"}, 404

    return jsonify([dict(row) for row in rows])


# 🔹 CALCULATE CALORIES
@app.route("/calculate-calories", methods=["POST"])
def calculate_calories():
    data = request.get_json()

    program = data.get("program")
    base_calories = data.get("base_calories")

    if program not in PROGRAMS:
        return {"error": "Invalid program"}, 400

    if not isinstance(base_calories, int):
        return {"error": "Invalid calories"}, 400

    return {
        "recommended_calories": base_calories * PROGRAMS[program]
    }


if __name__ == "__main__":
    app.run(debug=True)