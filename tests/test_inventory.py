from app import create_app
from app.models import db, Inventory
import unittest


class TestInventory(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()

            part = Inventory(
                name="Brake Pads",
                price=79.99
            )

            db.session.add(part)
            db.session.commit()

    def test_create_inventory(self):
        payload = {
            "name": "Premium Pads",
            "price": 99.99
        }

        response = self.client.post('/inventory/', json=payload)
        self.assertEqual(response.status_code, 201)

    def test_get_inventory(self):
        response = self.client.get('/inventory/')
        self.assertEqual(response.status_code, 200)

    def test_get_single_inventory(self):
        response = self.client.get('/inventory/1')
        self.assertEqual(response.status_code, 200)

    def test_update_inventory(self):
        payload = {
            "name": "Updated Pads",
            "price": 120.00
        }

        response = self.client.put('/inventory/1', json=payload)
        self.assertEqual(response.status_code, 200)

    def test_delete_inventory(self):
        response = self.client.delete('/inventory/1')
        self.assertEqual(response.status_code, 200)