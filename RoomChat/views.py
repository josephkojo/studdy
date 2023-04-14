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
  form = RoomForm()
  if request.method == 'POST':
    form = RoomForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect("HomePage")
     
      
  context = {'form' : form}
  return render(request, 'form.html', context)


def updateRoom(request, pk):
  room = Room.objects.get(id=pk)
  form = RoomForm(instance=room)
  
  if request.method == 'POST':
    form = RoomForm(request.POST, instance=room)
    if form.is_valid():
      form.save()
      return  redirect("HomePage")
  
  context = {'form':form}
  return render(request,'form.html', context)
  