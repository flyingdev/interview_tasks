import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from django.test import TestCase

# Create your tests here.


class ApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_simulate(self):
        response = self.client.post(reverse('power-simulate'))

        assert response.status_code == status.HTTP_200_OK

        content = json.loads(response.content)

        assert 'active' in content.keys()
        assert 'reactive' in content.keys()

    def test_active_power(self):
        response = self.client.get(reverse('power-active-power'))

        assert response.status_code == status.HTTP_200_OK

        content = json.loads(response.content)

        assert 'active' in content.keys()

    def test_reactive_power(self):
        response = self.client.get(reverse('power-reactive-power'))

        assert response.status_code == status.HTTP_200_OK

        content = json.loads(response.content)

        assert 'reactive' in content.keys()
