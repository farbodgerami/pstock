import numpy as np
import pandas as pd
import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_stock_prediction_success(mocker):
    """
    Test successful stock prediction request.
    """

    mock_model = mocker.Mock()

    mock_model.predict.return_value = np.array(
        [[100], [110], [120]]
    )

    mocker.patch(
        "app.views.load_model",
        return_value=mock_model,
    )

    dates = pd.date_range("2020-01-01", periods=300)

    df = pd.DataFrame(
        {
            "Date": dates,
            "Close": np.linspace(100, 200, 300),
        }
    )

    mocker.patch(
        "app.views.yf.download",
        return_value=df,
    )

    mocker.patch(
        "app.views.save_plot",
        return_value="/media/test.png",
    )

    client = APIClient()

    response = client.post(
        "/predict/",
        {"ticker": "AAPL"},
        format="json",
    )

    assert response.status_code == 200

    assert response.data["status"] == "success"
    assert "mse" in response.data
    assert "rmse" in response.data
    assert "r2" in response.data