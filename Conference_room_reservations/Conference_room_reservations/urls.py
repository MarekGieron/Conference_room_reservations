"""
URL configuration for Conference_room_reservations project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from reservations.views import new_room, room_list, room_detail, room_delete, modify_room, reserve_room

urlpatterns = [
    path('', room_list, name='rooms'),
    path('room/new/', new_room, name='new_room'),
    path('room/<int:id>/', room_detail, name='room_detail'),
    path('room/delete/<int:id>/', room_delete, name='room_delete'),
    path('rooms/', room_list, name='room_list'),
    path('room/modify/<int:id>/', modify_room, name='modify_room'),
    path('room/reserve/<int:id>/', reserve_room, name='reserve_room'),
]
