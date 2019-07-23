from django.urls import path
from . import views

urlpatterns = [
    # ex: /accounts/signup
    path('signup/', views.SignUp.as_view(), name='signup'),
    ]
