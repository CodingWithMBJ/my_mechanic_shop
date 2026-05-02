from app import create_app
from app.models import db, Customer, Mechanic, Inventory, ServiceTicket
from app.utils.util import encode_token
from datetime import date
import unittest


class TestServiceTicket(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()

            customer = Customer(
                name="Test Customer",
                email="customer@test.com",
                phone_number="123-456-7890",
                password="test"
            )

            mechanic = Mechanic(
                name="Test Mechanic",
                email="mechanic@test.com",
                phone="123-456-7890",
                salary=70000
            )

            part = Inventory(
                name="Brake Pads",
                price=79.99
            )

            db.session.add_all([customer, mechanic, part])
            db.session.commit()

            ticket = ServiceTicket(
                vin="1HGCM82633A004352",
                service_date=date(2026, 5, 1),
                service_desc="Brake replacement",
                customer_id=1
            )

            db.session.add(ticket)
            db.session.commit()

        self.token = encode_token(1)
        self.headers = {"Authorization": "Bearer " + self.token}

    def test_create_ticket(self):
        payload = {
            "vin": "2HGCM82633A004999",
            "service_date": "2026-05-02",
            "service_desc": "Oil change",
            "customer_id": 1
        }

        response = self.client.post('/service-tickets/', json=payload)
        self.assertEqual(response.status_code, 201)

    def test_invalid_create_ticket(self):
        payload = {
            "vin": "BADVIN"
        }

        response = self.client.post('/service-tickets/', json=payload)
        self.assertEqual(response.status_code, 400)

    def test_get_tickets(self):
        response = self.client.get('/service-tickets/', headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_get_my_tickets(self):
        response = self.client.get('/service-tickets/my-tickets', headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_assign_mechanic(self):
        response = self.client.put('/service-tickets/1/assign-mechanic/1')
        self.assertEqual(response.status_code, 200)

    def test_remove_mechanic(self):
        self.client.put('/service-tickets/1/assign-mechanic/1')

        response = self.client.put('/service-tickets/1/remove-mechanic/1')
        self.assertEqual(response.status_code, 200)

    def test_edit_ticket_mechanics(self):
        payload = {
            "add_ids": [1],
            "remove_ids": []
        }

        response = self.client.put(
            '/service-tickets/1/edit',
            json=payload,
            headers=self.headers
        )

        self.assertEqual(response.status_code, 200)

    def test_add_part(self):
        response = self.client.put(
            '/service-tickets/1/add-part/1',
            headers=self.headers
        )

        self.assertEqual(response.status_code, 200)

    def test_add_same_part_negative(self):
        self.client.put('/service-tickets/1/add-part/1', headers=self.headers)

        response = self.client.put(
            '/service-tickets/1/add-part/1',
            headers=self.headers
        )

        self.assertEqual(response.status_code, 400)