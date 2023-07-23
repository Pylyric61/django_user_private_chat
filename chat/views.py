from django.shortcuts import render, redirect
from chat.models import Room, Message
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def home(request):
    if request.user.is_authenticated:
        chats = Message.objects.filter(user=request.user.username)
        chatrooms = []
        for chat in chats:
            Rname = Room.objects.get(id=chat.roomid)
            chatrooms.append(Rname.name)
        return render(request, 'home.html',{ 'chatrooms' : list(set(chatrooms))})
    else:
        return render(request, 'home.html')


def room(request, room):
    username = request.user.username
    room_details = Room.objects.filter(name=room)
    return render(request, 'room.html', {'username' : username, 'room_details' : room_details, 'room' : room})
    
    
def checkview(request):
    room = request.POST["room_name"]
    if len(room) == 0:
        return render(request, 'home.html')
    username = request.user.username
    if Room.objects.filter(name=room).exists():
        return redirect("/" + room + '/')
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect("/" + room + '/')


def send(request, room):
    message = request.POST['message']
    if len(message) == 0:
        return HttpResponse('Message is empty')
    username = request.POST['username']
    if username !=  request.user.username:
        auth.logout(request)
        messages.info(request, "Authentication is required")
        return HttpResponse('Authentication is required')
    room_details = Room.objects.get(name=room)
    new_message = Message.objects.create(value = message, user=username.strip("/"), roomid=room_details.id)
    new_message.save()
    return HttpResponse('Message sent successfully.')


def getMessage(request, room):
    room_details = Room.objects.get(name=room)
    messages = Message.objects.filter(roomid=room_details.id)
    return JsonResponse({'messages': list(messages.values())})
    

def getrooms(request, room=None):
    chats = Message.objects.filter(user=request.user.username)
    chatrooms = []
    for chat in chats:
        Rname = Room.objects.get(id=chat.roomid)
        chatrooms.append(Rname.name)
    return JsonResponse({"chatrooms": list(set(chatrooms))})


def register(request):
    if request.method == 'POST':
        if len(request.POST['username'])<=1:
            messages.info(request, 'username is required')
            return redirect('register')
        username = request.POST['username']
        if len(request.POST['email'])<=1:
            messages.info(request, 'email is required')
            return redirect('register')
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST["password2"]
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'email already registered')
                return  redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'username already registered')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                return render(request,'login.html', {'messages' : ["Successfully registered"]})
        else:
            messages.info(request, 'Password is not match')
            return redirect('register')
    else:
        return render(request, 'register.html')    
    return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            auth.login(request, user=user)            
            return redirect("/")
        else:
            messages.info(request, "Creadentials not found")
            return redirect('login')
    else:
        return render(request, 'login.html')
    
def director(request, room):
    return redirect('login')

def roomdirect(request, room):
    return redirect(room)

def logout(request):
    auth.logout(request)
    return redirect('/')

