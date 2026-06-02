from .views import UserCrud, ProtectedView, StockPrediction
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("register/", UserCrud.as_view()),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("protected-view/", ProtectedView.as_view()),
    path("predict/", StockPrediction.as_view(), name="stock_prediction"),
]
