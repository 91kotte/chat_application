from django.shortcuts import render #Used to render an HTML template with context data.
from django.contrib.auth.decorators import login_required #A decorator that ensures only authenticated users can access the chat_room view.
from django.contrib.auth.models import User #The default Django user model for authentication and user management.
from .models import Message #A model (defined in the app's models.py) that stores chat messages.
from django.db.models import Q #A Django ORM tool that allows complex query filtering using AND & OR conditions.
from datetime import datetime # Python’s built-in module for handling date and time.
from django.utils.timezone import make_aware #Converts a naive datetime object to a timezone-aware one.


@login_required #Ensures only logged-in users can access this view.
# Defines a function to handle a chat room, with
#request: The HTTP request object.
#room_name: The name of the chat room (likely the username of the person the user is chatting with).
def chat_room(request, room_name): 
    search_query = request.GET.get('search', '')  #Retrieves the search query parameter (search) from the URL, defaulting to an empty string if not provided.
    users = User.objects.exclude(id=request.user.id)  #Retrieves all users except the currently logged-in user.
    chats = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver__username=room_name)) |
        (Q(receiver=request.user) & Q(sender__username=room_name))
    ) #The logged-in user is the sender and room_name is the receiver. OR the logged-in user is the receiver and room_name is the sender.

    #If a search query exists, it filters messages where the content contains the search term.
    if search_query:
        chats = chats.filter(Q(content__icontains=search_query))  

    # Sorts messages in ascending order based on the timestamp.
    chats = chats.order_by('timestamp') 
    user_last_messages = [] #Initializes an empty list to store the last messages of each user.

    for user in users:
        last_message = Message.objects.filter(
            (Q(sender=request.user) & Q(receiver=user)) |
            (Q(receiver=request.user) & Q(sender=user))
        ).order_by('-timestamp').first() #Retrieves the latest message exchanged with each user (ordered by timestamp in descending order).

        user_last_messages.append({
            'user': user,
            'last_message': last_message
        })

    # Converts datetime.min (the smallest possible datetime) to a timezone-aware datetime.
    aware_min_datetime = make_aware(datetime.min)

    # Sort user_last_messages by the timestamp of the last_message in descending order
    # If a user has no messages, aware_min_datetime is used to push them to the bottom.
    user_last_messages.sort(
        key=lambda x: x['last_message'].timestamp if x['last_message'] else aware_min_datetime,
        reverse=True
    )
    
    return render(request, 'chat.html', {
        'room_name': room_name,
        'chats': chats,
        'users': users,
        'user_last_messages': user_last_messages,
        'search_query': search_query 
    })
