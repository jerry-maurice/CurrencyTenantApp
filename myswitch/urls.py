from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # ex: /dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    # ex: /transfer
    path('transfer/', views.transfer, name='transfer'),
    # ex: /profile
    path('profile/', views.profile, name='profile'),
    # ex: /support
    path('support/', views.support, name='support'),
    # ex: /transactions
    path('transactions/', views.transactions, name='transactions'),
    # ex: /users
    path('users/', views.userInfo, name='userInfo'),
    # ex: /usersProfile
    path('<int:user_id>/users-profile/', views.usersProfile, name='usersProfile'),
    # ex: /rates
    path('rates/', views.rateManagement, name='rateManagement'),
    # ex: /usersProfile
    path('<int:rate_id>/rate/', views.rateManagementSingle, name='rateManagementSingle'),
    path('authenticateUser/', views.authenticateUser, name='authenticateUser'),
    path('logout/', views.logout_view, name='logout_view'),
    ]
