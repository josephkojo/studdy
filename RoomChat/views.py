from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Room, Topic,Message
from .forms import RoomForm
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Create your views here.
def registerUser(request):
  page = 'login'
  if request.user.is_authenticated:
    return redirect('HomePage')
  if request.method == 'POST':
    username = request.POST.get('username').lower()
    password = request.POST.get('password')
    try:
      user = User.objects.get(username=username)
    except:
      messages.error(request, "user does not exist")
    user = authenticate(request, username=username, password=password)
    if user is not None:
      login(request, user)
      return redirect('HomePage')
    else:
      messages.error(request, "username or password does not exist")
      
    
  context = {'page': page}
  return render(request, 'login_register.html', context)

def newAccount(request):
  form = UserCreationForm()
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save(commit=False)
      user.username = user.username.lower()
      user.save()
      login(request, user)
      return redirect('HomePage')
    else:
      messages.error(request, 'an error occured during the registeration of the user')
  context = {'form': form}
  return render(request, 'login_register.html', context)
 

def logoutUser(request):
    logout(request)

    return redirect('HomePage')


def homePage(request):
  q = request.GET.get('q')  if request.GET.get('q') != None else ''
  rooms = Room.objects.filter(
    Q(topic__name__icontains=q) |
    Q(name__icontains=q) |
    Q(description__icontains=q)
)

  topic = Topic.objects.all()
  room_count = rooms.count()
  
  room_messages = Message.objects.filter(room__topic__name__icontains=q)
  content = {'rooms': rooms}
  return render(request, 'home.html', {'rooms': rooms, 'topic': topic, 'room_count': room_count,
                                      'message_room': room_messages, 'message_room': room_messages})


def RoomChat(request, pk):
  room = Room.objects.get(id=pk)
  room_message = room.message_set.all().order_by('-created')  
  participant = room.participant.all()
  if request.method == 'POST':
    message = Message.objects.create(
      user= request.user,
      room=room,
      body = request.POST.get('main')
    )
    room.participant.add(request.user)
    return redirect('ChatRoom', pk=room.id)
  return render(request, 'ChatRoom.html', {'room':room, 'room_messages':room_message, 'participate':participant})


@login_required(login_url='login')
def create_room(request):
  form = RoomForm()
  if request.method == 'POST':
    form = RoomForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect("HomePage")
     
      
  context = {'form' : form}
  return render(request, 'form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
  room = Room.objects.get(id=pk)
  form = RoomForm(instance=room)
  if request.user != room.Host:
    return HttpResponse('you are not allowed here')
  if request.method == 'POST':
    form = RoomForm(request.POST, instance=room)
    if form.is_valid():
      form.save()
      return  redirect("HomePage")
  
  context = {'form':form}
  return render(request,'form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
  room = Room.objects.get(id=pk)
  if request.user != room.Host:
    return HttpResponse('You are not allowed here')
  if request.method == 'POST':
    room.delete()
    return redirect("HomePage")
  return render(request, 'delete.html', {'obj' :room})


@login_required(login_url='login')
def deleteMessage(request, pk):
  message = Message.objects.get(id=pk)
  if request.user != message.user:
    return HttpResponse('You are not allowed here')
  if request.method == 'POST':
    message.delete()
    return redirect("HomePage")
  return render(request, 'delete.html', {'obj' :message})
  