from rest_framework import status
from rest_framework.test import APIClient


def test_user_registration():
    client = APIClient()
    response = client.post('/api/register/', {"phone": "123"})

    assert response.status_code == status.HTTP_200_OK