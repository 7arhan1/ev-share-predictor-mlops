# Integration Test for flaskapp + model
import unittest
from flaskapp import app

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Predict Electric Vehicle Stock Share", response.data)

    def test_prediction_endpoint(self):
        response = self.app.post('/predict', data=dict(year=2030))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Predicted EV stock share", response.data)

if __name__ == '__main__':
    unittest.main()
