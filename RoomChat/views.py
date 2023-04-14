from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room
from .forms import RoomForm

# Create your views here.


def homePage(request):
  rooms = Room.objects.all()
  content = {'rooms' :rooms}
  return render(request, 'home.html',{'rooms' :rooms} )

def RoomChat(request, pk):
  room = Room.objects.get(id=pk)
 
  return render(request, 'ChatRoom.html', {'room':room})


def create_room(request):
  room = RoomForm()
  if request.method == 'POST':
    room = RoomForm(request.POST)
    if room.is_valid():
      room.save()
      return redirect("HomePage")
     
      
  context = {'room' : room}
  return render(request, 'form.html', context)