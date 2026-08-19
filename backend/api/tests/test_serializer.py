from app.serializers import UserSerializer, StockPredictionSerializer


def test_user_serializer():
    serializer = UserSerializer(
        data={
            "username": "john",
            "email": "john@test.com",
            "password": "123456",
        }
    )

    assert serializer.is_valid()


def test_stock_prediction_serializer():
    serializer = StockPredictionSerializer(
        data={"ticker": "AAPL"}
    )

    assert serializer.is_valid()


def test_stock_prediction_serializer_invalid():
    serializer = StockPredictionSerializer(
        data={"ticker": ""}
    )

    assert not serializer.is_valid()