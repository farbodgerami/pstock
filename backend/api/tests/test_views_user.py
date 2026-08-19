import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_register_user():
    client = APIClient()

    response = client.post(
        "/register/",
        {
            "username": "john",
            "email": "john@test.com",
            "password": "secret123",
        },
        format="json",
    )

    assert response.status_code == 200
    assert User.objects.filter(username="john").exists()


@pytest.mark.django_db
def test_register_duplicate_user():
    User.objects.create_user(
        username="john",
        email="john@test.com",
        password="secret",
    )

    client = APIClient()

    response = client.post(
        "/register/",
        {
            "username": "john",
            "email": "john@test.com",
            "password": "secret123",
        },
        format="json",
    )

    assert response.status_code == 400