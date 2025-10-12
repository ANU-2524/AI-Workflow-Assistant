from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add-task/', views.add_task, name='add_task'),
    path('signup/', views.signup_view, name='signup'),
    path('edit-task/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete-task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('assistant/', views.speak_assistant, name='speak_assistant'),
    path('', views.dashboard, name='dashboard'),
]
