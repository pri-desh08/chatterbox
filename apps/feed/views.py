from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Chatter

@login_required
def feed(request):
    userids = [request.user.id]

    for chatter in request.user.chatterprofile.follows.all():
        userids.append(chatter.user.id)

    chatters = Chatter.objects.filter(created_by_id__in=userids)

    for chat in chatters:
        likes = chat.likes.filter(created_by_id=request.user.id)

        if likes.count() > 0:
            chat.liked = True
        else:
            chat.liked = False
            
    return render(request, 'feed/feed.html', {'chats': chatters})


@login_required
def search(request):
    query = request.GET.get('query', '')

    if len(query) > 0:
        chatters = User.objects.filter(username__icontains=query)
        chats = Chatter.objects.filter(body__icontains=query)
    else:
        chatters = []
        chats = []

    context = {
        'query': query,
        'chatters': chatters,
        'chats': chats
    }

    return render(request, 'feed/search.html', {'chatter':chatters})

    #return render(request, 'feed/search.html', context)