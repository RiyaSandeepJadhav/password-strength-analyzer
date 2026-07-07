from flask import Flask, render_template, request, jsonify

from analyzer import analyze_password
from generator import generate_password
from database import (
    init_db,
    save_password,
    password_exists
)

app = Flask(__name__)

# Initialize SQLite database
init_db()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.get_json()

    password = data.get("password", "").strip()

    if password == "":
        return jsonify({
            "success": False,
            "message": "Password cannot be empty."
        })

    result = analyze_password(password)

    # Check password reuse
    if password_exists(password):
        result["reuse"] = True
        result["suggestions"].append(
            "This password has already been used before."
        )
    else:
        result["reuse"] = False
        save_password(password)

    result["success"] = True

    return jsonify(result)


@app.route("/generate", methods=["GET"])
def generate():

    password = generate_password(16)

    return jsonify({
        "password": password
    })


if __name__ == "__main__":
    app.run(debug=True)