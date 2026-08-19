import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_stock_prediction_model_error(mocker):
    mocker.patch(
        "app.views.load_model",
        side_effect=Exception("Model not found"),
    )

    client = APIClient()

    response = client.post(
        "/predict/",
        {"ticker": "AAPL"},
        format="json",
    )

    assert response.status_code == 400
    assert "Model not found" in response.data["detail"]