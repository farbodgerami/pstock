from django.shortcuts import render

# Create your views here.

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
    def post(self, request):
        data = request.data
   
        try:
            user = User.objects.create(
                username=data["username"],
                email=data["email"],
                password=make_password(data["password"]),
            )

            serializer = UserSerializer(user, many=False)
            # login(request, user)
            return Response(serializer.data)
        except Exception as e:
            message = {"detail": "Username or Email adress already exists"}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        response = {"status": "Request was permitted"}
        return Response(response)


class StockPrediction(APIView):
    def post(self, request):
        try:
            # load ML Model
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

            # preparing test data
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
            # Revert the scaled prices to original price
            y_predicted = scaler.inverse_transform(y_predicted.reshape(-1, 1)).flatten()
            y_test = scaler.inverse_transform(y_test.reshape(-1, 1)).flatten()

            # plot the final prediction

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
