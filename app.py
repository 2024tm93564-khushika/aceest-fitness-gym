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
            name TEXT NOT NULL,
            program TEXT NOT NULL,
            calories INTEGER NOT NULL
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
    return jsonify({"message": "ACEest Fitness API v2.1"})


# ✅ ADD CLIENT WITH VALIDATION
@app.route("/add-client", methods=["POST"])
def add_client():
    data = request.get_json()

    name = data.get("name")
    program = data.get("program")
    calories = data.get("calories")

    # Validation
    if not name or not isinstance(name, str):
        return jsonify({"error": "Invalid name"}), 400

    if program not in programs:
        return jsonify({"error": "Invalid program"}), 400

    if not isinstance(calories, int) or calories <= 0:
        return jsonify({"error": "Invalid calories"}), 400

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO clients (name, program, calories) VALUES (?, ?, ?)",
        (name.strip(), program, calories)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Client added successfully"}), 201


# ✅ GET CLIENTS
@app.route("/clients")
def get_clients():
    conn = get_db_connection()
    clients = conn.execute("SELECT * FROM clients").fetchall()
    conn.close()

    return jsonify([dict(row) for row in clients])


# ✅ CALORIE CALCULATION
@app.route("/calculate-calories", methods=["POST"])
def calculate_calories():
    data = request.get_json()

    program = data.get("program")
    base_calories = data.get("base_calories")

    if program not in programs:
        return jsonify({"error": "Invalid program"}), 400

    if not isinstance(base_calories, int) or base_calories <= 0:
        return jsonify({"error": "Invalid calories"}), 400

    return jsonify({
        "recommended_calories": base_calories * programs[program]
    })


if __name__ == "__main__":
    app.run(debug=True)