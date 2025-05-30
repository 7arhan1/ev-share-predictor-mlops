# Unit Test for model.py
import unittest
import pandas as pd
import os
import pickle
from sklearn.linear_model import LinearRegression

class TestModel(unittest.TestCase):
    def setUp(self):
        # Load the model
        with open("model.pkl", "rb") as f:
            self.model = pickle.load(f)

    def test_model_type(self):
        self.assertIsInstance(self.model, LinearRegression)

    def test_prediction_output(self):
        sample_input = pd.DataFrame([[2030]], columns=["Year"])
        prediction = self.model.predict(sample_input)
        self.assertEqual(len(prediction), 1)
        self.assertIsInstance(prediction[0], float)

if __name__ == '__main__':
    unittest.main()
