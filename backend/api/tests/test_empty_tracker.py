import pandas as pd
import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_stock_prediction_no_data(mocker):
    mock_model = mocker.Mock()

    mocker.patch(
        "app.views.load_model",
        return_value=mock_model,
    )

    mocker.patch(
        "app.views.yf.download",
        return_value=pd.DataFrame(),
    )

    client = APIClient()

    response = client.post(
        "/predict/",
        {"ticker": "INVALID"},
        format="json",
    )

    assert response.status_code == 404