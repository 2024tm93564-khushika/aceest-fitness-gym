from flask import Flask, jsonify

app = Flask(__name__)

# Extracted from v1.0
programs = {
    "fat_loss": {
        "name": "Fat Loss",
        "workout": "Back Squat, Bench Press, Cardio",
        "diet": "Egg whites, Chicken breast, Fish"
    },
    "muscle_gain": {
        "name": "Muscle Gain",
        "workout": "Squat, Deadlift, Bench Press",
        "diet": "Eggs, Rice, Chicken, Milk"
    },
    "beginner": {
        "name": "Beginner",
        "workout": "Basic circuit training",
        "diet": "Balanced diet"
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


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)