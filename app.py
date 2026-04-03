from flask import Flask, jsonify, request, Response
import csv
import io

app = Flask(__name__)

# Programs (same as v1.1)
programs = {
    "fat_loss": {
        "name": "Fat Loss",
        "workout": "Back Squat, Bench Press, Cardio",
        "diet": "Egg whites, Chicken breast, Fish",
        "calorie_factor": 0.8
    },
    "muscle_gain": {
        "name": "Muscle Gain",
        "workout": "Squat, Deadlift, Bench Press",
        "diet": "Eggs, Rice, Chicken, Milk",
        "calorie_factor": 1.2
    },
    "beginner": {
        "name": "Beginner",
        "workout": "Basic circuit training",
        "diet": "Balanced diet",
        "calorie_factor": 1.0
    }
}

# v1.1.2: in-memory client storage
clients = []

@app.route("/")
def home():
    return "Welcome to ACEest Fitness & Gym"

@app.route("/programs")
def get_programs():
    return jsonify(programs)

@app.route("/programs/<program_name>")
def get_program(program_name):
    program = programs.get(program_name.lower())
    if program:
        return jsonify(program)
    return {"error": "Program not found"}, 404


# v1.1 feature
@app.route("/calculate-calories", methods=["POST"])
def calculate_calories():
    data = request.get_json()

    program_name = data.get("program")
    base_calories = data.get("base_calories")

    if not program_name or base_calories is None:
        return {"error": "Missing data"}, 400

    program = programs.get(program_name.lower())

    if not program:
        return {"error": "Invalid program"}, 400

    result = base_calories * program["calorie_factor"]

    return {
        "program": program_name,
        "recommended_calories": result
    }


# v1.1.2: add client
@app.route("/add-client", methods=["POST"])
def add_client():
    data = request.get_json()

    name = data.get("name")
    program = data.get("program")
    calories = data.get("calories")

    if not name or not program or calories is None:
        return {"error": "Missing fields"}, 400

    client = {
        "name": name,
        "program": program,
        "calories": calories
    }

    clients.append(client)

    return {"message": "Client added successfully"}, 201


# v1.1.2: view clients
@app.route("/clients")
def get_clients():
    return jsonify(clients)


# v1.1.2: export CSV
@app.route("/export-csv")
def export_csv():
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["name", "program", "calories"])
    writer.writeheader()

    for client in clients:
        writer.writerow(client)

    return Response(output.getvalue(), mimetype="text/csv")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)