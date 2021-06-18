from django.urls import path
from . import views
urlpatterns = [
    path('create/', views.UserView.as_view()),
    path('reset_password/', views.PasswordResetView.as_view())
]