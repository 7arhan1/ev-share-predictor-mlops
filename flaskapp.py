import pickle
import pandas as pd
from flask import Flask, request, render_template

app = Flask(__name__)

# Load the trained model
model = pickle.load(open("model.pkl", "rb"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    # Get the input year from the form
    year = float(request.form["year"])

    # Prepare data for prediction
    data = pd.DataFrame([[year]], columns=["Year"])

    # Make prediction
    #prediction = model.predict(data)
    prediction = 111
    formatted_prediction = f"Predicted EV stock share for {int(year)}: {round(float(prediction[0]), 2)}%"

    return render_template("result.html", prediction=formatted_prediction)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
