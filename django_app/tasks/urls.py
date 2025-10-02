from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add-task/', views.add_task, name='add_task'),
    path('signup/', views.signup_view, name='signup'),
]
