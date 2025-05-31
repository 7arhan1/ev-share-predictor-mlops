import os
import pickle
import pandas as pd
from flask import Flask, request, render_template

app = Flask(__name__)

# Get absolute path to model.pkl relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")

# Load the trained model
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    year = float(request.form["year"])
    data = pd.DataFrame([[year]], columns=["Year"])

    # Uncomment this for actual prediction:
    prediction = model.predict(data)
    formatted_prediction = f"Predicted EV stock share for {int(year)}: {round(float(prediction[0]), 2)}%"
    return render_template("result.html", prediction=456.00)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")