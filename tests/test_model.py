import unittest
import pandas as pd
import os
import pickle
from sklearn.linear_model import LinearRegression

class TestModel(unittest.TestCase):
    def setUp(self):
        # Get the absolute path to model.pkl relative to this test file
        base_dir = os.path.dirname(os.path.abspath(__file__))  # directory of this test file
        model_path = os.path.join(base_dir, '..', 'model.pkl')  # model.pkl expected one level up
        with open(model_path, "rb") as f:
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