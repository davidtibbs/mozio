from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Provider, ServiceArea


class ProviderModelTest(TestCase):
    def setUp(self):
        self.provider = Provider.objects.create(
            name="Alenxandru",
            email="Alenxandru@example.com",
            phone_number="+1231234567",
            language="English",
            currency="USD",
        )

    def test_provider_str(self):
        self.assertEqual(str(self.provider), "Alenxandru")


class ServiceAreaTest(APITestCase):
    def setUp(self):
        self.provider = Provider.objects.create(
            name="Alenxandru",
            email="Alenxandru@example.com",
            phone_number="+1231234567",
            language="English",
            currency="USD",
        )
        self.service_area = ServiceArea.objects.create(
            provider=self.provider,
            name="New Service Area",
            price=100.00,
            geojson={
                "type": "Polygon",
                "coordinates": [
                    [
                        [30.0, 10.0],
                        [40.0, 40.0],
                        [20.0, 40.0],
                        [10.0, 20.0],
                        [30.0, 10.0],
                    ]
                ],
            },
        )

    def test_service_area_str(self):
        self.assertEqual(str(self.service_area), "New Service Area")

    def test_contains_valid_point(self):
        response = self.client.get(
            "/api/service-areas/contains/", data={"lat": 20.0, "lng": 30.0}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Expect the created area

    def test_contains_invalid_point(self):
        response = self.client.get(
            "/api/service-areas/contains/", data={"lat": -10.0, "lng": -20.0}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # Expect no areas
