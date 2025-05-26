import unittest
import pickle
import pandas as pd
import os

class TestModel(unittest.TestCase):
    def test_model_prediction(self):
        # Check if model file exists
        self.assertTrue(os.path.exists("model.pkl"), "model.pkl file not found!")

        # Load model
        with open("model.pkl", "rb") as file:
            model = pickle.load(file)

        # Dummy input (age, sex, bmi, children, smoker, region)
        input_data = pd.DataFrame([[30, 1, 25.3, 2, 1, 0]], 
                                  columns=["age", "sex", "bmi", "children", "smoker", "region"])

        # Run prediction
        prediction = model.predict(input_data)

        # Check prediction is a number and not empty
        self.assertIsInstance(prediction[0], float)
        self.assertGreaterEqual(prediction[0], 0)

if __name__ == '__main__':
    unittest.main()
