import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
def test_protected_view_authenticated():
    user = User.objects.create_user(
        username="john",
        password="secret"
    )

    refresh = RefreshToken.for_user(user)

    client = APIClient()
    client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
    )

    response = client.get("/protected-view/")

    assert response.status_code == 200
    assert response.data["status"] == "Request was permitted"


@pytest.mark.django_db
def test_protected_view_unauthenticated():
    client = APIClient()

    response = client.get("/protected-view/")

    assert response.status_code == 401