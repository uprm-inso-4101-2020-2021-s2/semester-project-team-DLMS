from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name='Login'),
    path('register/', views.register_page, name='Register'),
    path('home/', views.home_page, name='Home'),
    path('courses/', views.courses_page, name='Enrolled_Courses'),
    path('settings/', views.settings_page, name='Settings'),
    path('list/', views.courses_list, name='List'),
    path('edit/<id>/', views.edit_courses, name='Edit'),
    path('delete/<id>/', views.delete_courses, name='Delete'),
    path('curriculum/', views.curriculum_page, name="Curriculum")
]


