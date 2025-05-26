import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Load dataset
df = pd.read_csv("ev_data.csv")

# Features and Target
X = df[["Year"]]
y = df["Share"]

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Linear Regression Model
model = LinearRegression()
model.fit(X_train, y_train)

# Save trained model to .pkl
with open("model.pkl", "wb") as file:
    pickle.dump(model, file)

print("✅ Model trained and saved as model.pkl")
