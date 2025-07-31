import unittest
import requests

BASE_URL = "http://74.225.221.182:5000"

class TestIBCommRAGAPI(unittest.TestCase):

    def test_save_message(self):
        url = f"{BASE_URL}/save_message/"
        payload = {
            "group_id": "group123",
            "message": "Hello world",
            "sender": "user1"
        }
        response = requests.post(url, json=payload)
        self.assertEqual(response.status_code, 200)

    def test_query_vector_db(self):
        url = f"{BASE_URL}/query/"
        payload = {
            "group_id": "420",
            "text": "What is this about?"
        }
        response = requests.post(url, json=payload)
        self.assertEqual(response.status_code, 200)

    def test_delete_group(self):
        url = f"{BASE_URL}/delete_group/"
        payload = {
            "groupid": "group123"
        }
        response = requests.delete(url, json=payload)
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
