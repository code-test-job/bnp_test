#pip install httpx
import unittest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestLongCalculation(unittest.TestCase):
    def test_valid_param(self):
        response = client.get("/long-calculation?param=10")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"result": "3628800"})

    def test_negative_param(self):
        response = client.get("/long-calculation?param=-10")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
                         "error": "Parameter must be a positive integer"})


if __name__ == "__main__":
    unittest.main()
