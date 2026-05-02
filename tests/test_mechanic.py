from app import create_app
from app.models import db, Mechanic
import unittest


class TestMechanic(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()

            mechanic = Mechanic(
                name="Test Mechanic",
                email="mechanic@test.com",
                phone="123-456-7890",
                salary=70000
            )

            db.session.add(mechanic)
            db.session.commit()

    def test_create_mechanic(self):
        payload = {
            "name": "Nasir",
            "email": "nasir@example.com",
            "phone": "6515551022",
            "salary": 80000
        }

        response = self.client.post('/mechanics/', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["name"], "Nasir")

    def test_get_mechanics(self):
        response = self.client.get('/mechanics/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_get_single_mechanic(self):
        response = self.client.get('/mechanics/1')
        self.assertEqual(response.status_code, 200)

    def test_update_mechanic(self):
        payload = {
            "name": "Updated",
            "email": "updated@test.com",
            "phone": "999-999-9999",
            "salary": 90000
        }

        response = self.client.put('/mechanics/1', json=payload)
        self.assertEqual(response.status_code, 200)

    def test_delete_mechanic(self):
        response = self.client.delete('/mechanics/1')
        self.assertEqual(response.status_code, 200)