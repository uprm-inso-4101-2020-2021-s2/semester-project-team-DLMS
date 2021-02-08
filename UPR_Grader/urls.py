from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name='Login'),
    path('register/', views.register_page, name='Register'),
]


