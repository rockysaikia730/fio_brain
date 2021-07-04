from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('create/', views.UserView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('reset_password/', views.PasswordResetView.as_view()),
    path('validate-refresh-token-get-access-token/', views.VerifyRefreshTokenView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view())
]