from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

DATABASE = "clients.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# Initialize DB
def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            program TEXT,
            calories INTEGER
        )
    """)
    conn.close()


init_db()


programs = {
    "fat_loss": {"calorie_factor": 0.8},
    "muscle_gain": {"calorie_factor": 1.2},
    "beginner": {"calorie_factor": 1.0}
}


@app.route("/")
def home():
    return "ACEest Fitness & Gym API with Database"


@app.route("/add-client", methods=["POST"])
def add_client():
    data = request.get_json()

    name = data.get("name")
    program = data.get("program")
    calories = data.get("calories")

    if not name or not program or calories is None:
        return {"error": "Missing fields"}, 400

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO clients (name, program, calories) VALUES (?, ?, ?)",
        (name, program, calories)
    )
    conn.commit()
    conn.close()

    return {"message": "Client added to database"}, 201


@app.route("/clients")
def get_clients():
    conn = get_db_connection()
    clients = conn.execute("SELECT * FROM clients").fetchall()
    conn.close()

    return jsonify([dict(row) for row in clients])


@app.route("/calculate-calories", methods=["POST"])
def calculate_calories():
    data = request.get_json()

    program = data.get("program")
    base_calories = data.get("base_calories")

    if not program or base_calories is None:
        return {"error": "Missing data"}, 400

    factor = programs.get(program, {}).get("calorie_factor")

    if not factor:
        return {"error": "Invalid program"}, 400

    return {
        "recommended_calories": base_calories * factor
    }


if __name__ == "__main__":
    app.run(debug=True)