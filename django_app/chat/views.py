# django_app/chat/views.py
from .models import FriendRequest, ChatMessage
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@login_required
def chat_messages_api(request, user_id):
    friend = User.objects.get(id=user_id)
    messages = ChatMessage.objects.filter(
        sender__in=[request.user, friend],
        receiver__in=[request.user, friend]
    ).exclude(deleted_for=request.user).order_by("timestamp")
    data = [
        {
            "sender": msg.sender.username,
            "message": msg.message,
            "timestamp": msg.timestamp.strftime("%H:%M %d/%m/%Y"),
            "is_self": msg.sender == request.user,
        }
        for msg in messages
    ]
    return JsonResponse({"messages": data})

@login_required
def chat_dashboard(request):
    users = User.objects.exclude(username=request.user.username)
    friends = (
        User.objects.filter(
            sent_requests__to_user=request.user, sent_requests__is_accepted=True
        ) | User.objects.filter(
            received_requests__from_user=request.user, received_requests__is_accepted=True
        )
    ).distinct()
    users = users.exclude(id__in=friends.values_list('id', flat=True))
    pending_requests = request.user.received_requests.filter(is_accepted=False)
    return render(request, "chat/chat_dashboard.html", {
        "users": users,
        "friends": friends,
        "pending_requests": pending_requests, 
    })


@login_required
@csrf_exempt
def clear_chat(request, user_id):
    if request.method == "POST":
        friend = User.objects.get(id=user_id)
        messages = ChatMessage.objects.filter(
            sender__in=[request.user, friend], receiver__in=[request.user, friend]
        )
        for msg in messages:
            msg.deleted_for.add(request.user)
    return redirect("chat_with_user", user_id=user_id)

@login_required
def send_friend_request(request, to_user_id):
    to_user = User.objects.get(id=to_user_id)
    FriendRequest.objects.get_or_create(from_user=request.user, to_user=to_user)
    return redirect("chat_dashboard")

@login_required
def accept_friend_request(request, req_id):
    req = FriendRequest.objects.get(id=req_id, to_user=request.user)
    req.is_accepted = True
    req.save()
    return redirect("chat_dashboard")

@login_required
def chat_with_user(request, user_id):
    friend = User.objects.get(id=user_id)
    # Only allow if connected
    is_friend = FriendRequest.objects.filter(
        from_user=request.user, to_user=friend, is_accepted=True
    ).exists() or FriendRequest.objects.filter(
        from_user=friend, to_user=request.user, is_accepted=True
    ).exists()
    if not is_friend and request.user != friend:
        return redirect("chat_dashboard")
    # Get messages
    messages = ChatMessage.objects.filter(
    sender__in=[request.user, friend],
    receiver__in=[request.user, friend]
).exclude(deleted_for=request.user).order_by("timestamp")
    return render(request, "chat/chat_window.html", {"friend": friend, "messages": messages})

@login_required
def send_message(request, user_id):
    if request.method == "POST":
        friend = User.objects.get(id=user_id)
        ChatMessage.objects.create(
            sender=request.user, receiver=friend, message=request.POST["message"]
        )
    return redirect("chat_with_user", user_id=user_id)
