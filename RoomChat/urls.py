from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePage, name="HomePage"),
    path('room/<str:pk>/', views.RoomChat, name="ChatRoom"),
    path('create_room/', views.create_room, name="CreateRoom")
    
]
