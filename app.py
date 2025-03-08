from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

data_file = "data.json"

def read_data():
    try:
        with open(data_file, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"employees": [], "feedback": []}

def write_data(data):
    with open(data_file, "w") as file:
        json.dump(data, file, indent=4)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/employees", methods=["GET", "POST"])
def employees():
    data = read_data()
    if request.method == "POST":
        new_employee = request.json
        new_employee["id"] = len(data["employees"]) + 1
        data["employees"].append(new_employee)
        write_data(data)
        return jsonify(new_employee)
    return jsonify(data["employees"])

@app.route("/api/feedback", methods=["GET", "POST"])
def feedback():
    data = read_data()
    if request.method == "POST":
        new_feedback = request.json
        data["feedback"].append(new_feedback)
        write_data(data)
        return jsonify(new_feedback)
    return jsonify(data["feedback"])

if __name__ == "__main__":
    app.run(debug=True)