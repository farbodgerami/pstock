from django.shortcuts import render

 
from django.contrib.auth.models import User
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from .serializers import UserSerializer, StockPredictionSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .utils import save_plot
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

from datetime import datetime
import os
from django.conf.urls.static import static
from django.conf import settings
from keras.models import load_model
from sklearn.metrics import mean_squared_error, r2_score


class UserCrud(APIView):
    """
    API endpoint for creating a new user account.

    Accepts a username, email address, and password from the request body,
    securely hashes the password, creates a Django User instance, and
    returns the serialized user data.

    Returns:
        Response: Serialized user data with HTTP 200 on successful creation,
        or an error message with HTTP 400 if the username or email already
        exists or user creation fails.
    """
    def post(self, request):
        """
        Create a new user account.

        Args:
            request: Django REST Framework HTTP request containing
                `username`, `email`, and `password` in the request body.

        Returns:
            Response: Serialized user information on success, or an error
            response with HTTP 400 on failure.
        """
        data = request.data
   
        try:
            user = User.objects.create(
                username=data["username"],
                email=data["email"],
                password=make_password(data["password"]),
            )

            serializer = UserSerializer(user, many=False)
    
            return Response(serializer.data)
        except Exception as e:
            message = {"detail": "Username or Email adress already exists"}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


class ProtectedView(APIView):
    """
    Protected API endpoint accessible only to authenticated users.

    Uses the IsAuthenticated permission class to ensure that only users
    with valid authentication credentials can access the endpoint.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Verify that the current user is authenticated.

        Args:
            request: Django REST Framework HTTP request from an authenticated
                user.

        Returns:
            Response: A confirmation message indicating that the request
            was permitted.
        """
        response = {"status": "Request was permitted"}
        return Response(response)


class StockPrediction(APIView):
    """
    API endpoint for stock price analysis and prediction.

    Downloads approximately ten years of historical stock data using
    yfinance, generates closing-price and moving-average plots, prepares
    the data for a pre-trained Keras machine-learning model, and generates
    predicted stock prices.

    The endpoint calculates prediction performance using Mean Squared Error
    (MSE), Root Mean Squared Error (RMSE), and R² score. Generated plots are
    saved using the application's `save_plot` utility and their paths are
    returned in the API response.

    The request must contain a stock ticker symbol in the `ticker` field.

    Returns:
        Response: A JSON response containing the generated plot paths and
        prediction metrics on success, or an HTTP 400/404 error response
        when processing fails or no historical data is available.
    """

    def post(self, request):
        """
        Generate stock-price predictions for the requested ticker.

        Args:
            request: Django REST Framework HTTP request containing a `ticker`
                field with the stock symbol to analyze.

        Returns:
            Response: Contains the status, generated plot paths, MSE, RMSE,
            and R² prediction metrics.

        Raises:
            Exception: Any unexpected error during model loading, data
                retrieval, preprocessing, prediction, or plot generation
                is caught and returned as an HTTP 400 response.
        """
        try:
           
            model = load_model("stock_prediction_model.keras")
            data = request.data
            ticker = data["ticker"]

            now = datetime.now()
            start = datetime(now.year - 10, now.month, now.day)
            end = now
            df = yf.download(ticker, start, end)
            print(df)
            try:
                if df.empty:
                    raise Exception("No data found for the given thicker")
            except Exception as e:
                return Response(str(e), status=status.HTTP_404_NOT_FOUND)
            df = df.reset_index()
            "generate Basic Plot"
            plt.switch_backend("AGG")
            plt.figure(figsize=(12, 6))
            plt.plot(df.Close, label="Closing Price")
            plt.title(f"Closing price of {ticker}")
            plt.xlabel("Days")
            plt.ylabel("Price")
            plt.legend()
            plot_img_path = f"{ticker}_plot.png"
            plot_img = save_plot(plot_img_path)

            ma100 = df.Close.rolling(100).mean()
            plt.switch_backend("AGG")
            plt.figure(figsize=(12, 6))
            plt.plot(df.Close, label="Closing Price")
            plt.plot(ma100, "r", label="100 DMA")
            plt.title(f"Closing price of {ticker}")
            plt.xlabel("Days")
            plt.ylabel("Price")
            plt.legend()
            plot_img_dma = f"{ticker}_dma_plot.png"
            plot_100_img = save_plot(plot_img_dma)

            ma200 = df.Close.rolling(200).mean()
            plt.switch_backend("AGG")
            plt.figure(figsize=(12, 6))
            plt.plot(df.Close, label="Closing Price")
            plt.plot(ma200, "g", label="200 DMA")
            plt.title(f"Closing price of {ticker}")
            plt.xlabel("Days")
            plt.ylabel("Price")
            plt.legend()
            plot_img_200_dma = f"{ticker}_dma_200_plot.png"
            plot_200_img = save_plot(plot_img_200_dma)

            data_training = pd.DataFrame(df.Close[0 : int(len(df) * 0.7)])
            data_testing = pd.DataFrame(df.Close[int(len(df) * 0.7) :])
            scaler = MinMaxScaler(feature_range=(0, 1))

           
            past_100_days = data_training.tail(100)
            final_df = pd.concat([past_100_days, data_testing], ignore_index=True)
            input_data = scaler.fit_transform(final_df)

            x_test = []
            y_test = []
            for i in range(100, input_data.shape[0]):
                x_test.append(input_data[i - 100 : i])
                y_test.append(input_data[i, 0])
            x_test, y_test = np.array(x_test), np.array(y_test)

            y_predicted = model.predict(x_test)
            
            y_predicted = scaler.inverse_transform(y_predicted.reshape(-1, 1)).flatten()
            y_test = scaler.inverse_transform(y_test.reshape(-1, 1)).flatten()

       
            ma200 = df.Close.rolling(200).mean()
            plt.switch_backend("AGG")
            plt.figure(figsize=(12, 6))
            plt.plot(y_test, "b", label="Original Price")
            plt.plot(y_predicted, "r", label="Predicted Price")
            plt.title(f"Final Prediction for {ticker}")
            plt.xlabel("Days")
            plt.ylabel("Price")
            plt.legend()
            plot_img_inal_predition = f"{ticker}_final_predition_plot.png"
            plot_final_predition_img = save_plot(plot_img_inal_predition)
            mse = mean_squared_error(y_test, y_predicted)
            rmse = np.sqrt(mse)
            r2 = r2_score(y_test, y_predicted)

            return Response(
                {
                    "status": "success",
                    "plot_img": plot_img,
                    "plot_100_img": plot_100_img,
                    "plot_200_img": plot_200_img,
                    "plot_final_predition_img": plot_final_predition_img,
                    "mse": mse,
                    "r2": r2,
                    "rmse": rmse,
                }
            )

        except Exception as e:
            message = {"detail": str(e)}
            print(message)
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
