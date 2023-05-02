from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.registerUser, name='login'),
    path('register/', views.newAccount, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('', views.homePage, name="HomePage"),
    path('room/<str:pk>/', views.RoomChat, name="ChatRoom"),
    path('create_room/', views.create_room, name="CreateRoom"),
    path('update_room/<str:pk>/', views.updateRoom,name="updateRoom"),
    path('delete_room/<str:pk>/', views.deleteRoom, name="deleteRoom"),
    path('delete_message/<str:pk>/', views.deleteMessage, name="delete_message")
    
]
