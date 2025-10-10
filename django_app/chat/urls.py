# django_app/chat/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_dashboard, name='chat_dashboard'),
    path('send-request/<int:to_user_id>/', views.send_friend_request, name='send_friend_request'),
    path('accept-request/<int:req_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('<int:user_id>/', views.chat_with_user, name='chat_with_user'),
    path('<int:user_id>/send/', views.send_message, name='send_message'),
    path('<int:user_id>/clear/', views.clear_chat, name='clear_chat'),
    path('<int:user_id>/messages/', views.chat_messages_api, name='chat_messages_api'),

]
