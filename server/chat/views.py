from django.shortcuts import render

def index(request):
    return render(request, 'index.html', {})


def room(request, room):
    return render(request, 'chatroom.html', {
        'room': room
    })
