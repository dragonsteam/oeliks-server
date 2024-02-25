from rest_framework import status
from rest_framework.test import APIClient

# AAA Arrange Act Assert

def test_get_ping():
    client = APIClient()
    response = client.get('/api/ping/')

    assert response.status_code == status.HTTP_200_OK