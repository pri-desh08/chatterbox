from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from apps.notification.utilities import create_notification

from .forms import ChatterProfileForm

def chatterprofile(request, username):
    user = get_object_or_404(User, username=username)
    chatters = user.chatters.all()

    for chat in chatters:
        likes = chat.likes.filter(created_by_id=request.user.id)

        if likes.count() > 0:
            chat.liked = True
        else:
            chat.liked = False

        
    context = {
        'user': user,
        'chatters': chatters
    }

    return render(request, 'chatterprofile/chatterprofile.html', context)

@login_required
def edit_profile(request):
    if request.method =='POST':
        form = ChatterProfileForm(request.POST, request.FILES, instance=request.user.chatterprofile)

        if form.is_valid():
            form.save()

            return redirect('chatterprofile', username=request.user.username)
    else:
        form = ChatterProfileForm(instance=request.user.chatterprofile)

    context = {
        'user': request.user,
        'form': form
    }

    return render(request, 'chatterprofile/edit_profile.html', context)

@login_required
def follow_chatter(request, username):
    user = get_object_or_404(User, username=username)

    request.user.chatterprofile.follows.add(user.chatterprofile)

    create_notification(request, user, 'follower')

    return redirect('chatterprofile', username=username)

@login_required
def unfollow_chatter(request, username):
    user = get_object_or_404(User, username=username)

    request.user.chatterprofile.follows.remove(user.chatterprofile)

    return redirect('chatterprofile', username=username)

def followers(request, username): 
    user = get_object_or_404(User, username=username)

    return render(request, 'chatterprofile/followers.html',{'user': user} )

def follows(request, username): 
    user = get_object_or_404(User, username=username)

    return render(request, 'chatterprofile/follows.html',{'user': user} )
