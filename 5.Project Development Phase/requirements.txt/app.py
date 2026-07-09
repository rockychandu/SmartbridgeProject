from flask import Flask, render_template, request
import sqlite3
import joblib
from datetime import datetime

app = Flask(__name__)

model = joblib.load("crop_model.pkl")


def create_database():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prediction_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nitrogen REAL,
            phosphorous REAL,
            potassium REAL,
            temperature REAL,
            humidity REAL,
            ph REAL,
            rainfall REAL,
            recommended_crop TEXT,
            date TEXT
        )
    """)

    conn.commit()
    conn.close()


create_database()


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():

    try:
        nitrogen = float(request.form["nitrogen"])
        phosphorous = float(request.form["phosphorous"])
        potassium = float(request.form["potassium"])
        temperature = float(request.form["temperature"])
        humidity = float(request.form["humidity"])
        ph = float(request.form["ph"])
        rainfall = float(request.form["rainfall"])

        data = [[
            nitrogen,
            phosphorous,
            potassium,
            temperature,
            humidity,
            ph,
            rainfall
        ]]

        prediction = model.predict(data)[0]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO prediction_history
            (
                nitrogen,
                phosphorous,
                potassium,
                temperature,
                humidity,
                ph,
                rainfall,
                recommended_crop,
                date
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            nitrogen,
            phosphorous,
            potassium,
            temperature,
            humidity,
            ph,
            rainfall,
            prediction,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()
        conn.close()

        return render_template(
            "index.html",
            prediction_text=f"Recommended Crop: {prediction.capitalize()}"
        )

    except Exception as e:
        return render_template(
            "index.html",
            prediction_text=f"Error: {e}"
        )


if __name__ == "__main__":
    app.run(debug=True)