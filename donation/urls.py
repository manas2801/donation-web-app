from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('donate/', views.donate, name='donate'),
    path('register/', views.register, name='register'),
    path('complete-payment/<int:id>/', views.complete_payment, name='complete_payment'),
]