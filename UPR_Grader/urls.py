from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name='Login'),
    path('register/', views.register_page, name='Register'),
    path('home/', views.home_page, name='Home'),
    path('courses/', views.courses_page, name='Enrolled_Courses')
    path('home/', views.home_page, name='Home'),
    path('settings/', views.settings_page, name='Settings'),
]


