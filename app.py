from flask import Flask, jsonify, request

app = Flask(__name__)

# v1.1 update: added calorie_factor
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


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)