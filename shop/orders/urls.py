from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('accounts/login/', views.auth_login, name='login'),
    path('login2/', views.auth_login2, name='login2'),
    path('confirmation/<int:order_id>/', views.confirmation, name='confirmation'),
    path('checkout/', views.checkout, name='checkout'),
    path('register/', views.register, name='register'),
]
