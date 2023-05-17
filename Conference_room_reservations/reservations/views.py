from django.shortcuts import redirect
from .models import Room
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from reservations.models import Room, Reservation


def new_room(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        projector_available = request.POST.get('projector_available') == 'on'

        # check if room with this name already exists
        if Room.objects.filter(name=name).exists():
            error_message = 'Sala o podanej nazwie już istnieje'
            return render(request, 'new_room.html', {'error_message': error_message})

        # check if capacity is a positive number
        try:
            capacity = int(capacity)
            if capacity <= 0:
                raise ValueError
        except ValueError:
            error_message = 'Pojemność sali musi być liczbą dodatnią'
            return render(request, 'new_room.html', {'error_message': error_message})

        # create new room object and save to database
        new_room = Room(name=name, capacity=capacity, projector_available=projector_available)
        new_room.save()

        # redirect to main page
        return redirect('rooms')

    # if request method is GET, display new room form
    return render(request, 'new_room.html')


def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'room_list.html', {'rooms': rooms})


def room_detail(request, id):
    room = get_object_or_404(Room, id=id)
    return render(request, 'room_detail.html', {'room': room})


def room_delete(request, id):
    room = get_object_or_404(Room, id=id)
    room.delete()
    return redirect('room_list')


def modify_room(request, id):
    try:
        room = Room.objects.get(id=id)
    except Room.DoesNotExist:
        error_message = 'Sala o podanym identyfikatorze nie istnieje'
        return render(request, 'room_list.html', {'error_message': error_message})

    if request.method == 'POST':
        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        projector_available = request.POST.get('projector_available') == 'on'

        # check if capacity is a positive number
        try:
            capacity = int(capacity)
            if capacity <= 0:
                raise ValueError
        except ValueError:
            error_message = 'Pojemność sali musi być liczbą dodatnią'
            return render(request, 'modify_room.html', {'room': room, 'error_message': error_message})

        # check if room with this name already exists
        if Room.objects.filter(name=name).exclude(id=id).exists():
            error_message = 'Sala o podanej nazwie już istnieje'
            return render(request, 'modify_room.html', {'room': room, 'error_message': error_message})

        # update room object and save changes to the database
        room.name = name
        room.capacity = capacity
        room.projector_available = projector_available
        room.save()

        # redirect to the room list page
        return redirect('rooms')

    # if request method is GET, display room modification form
    return render(request, 'modify_room.html', {'room': room})


def reserve_room(request, id):
    try:
        room = Room.objects.get(id=id)
    except Room.DoesNotExist:
        error_message = 'Sala o podanym identyfikatorze nie istnieje'
        return render(request, 'room_list.html', {'error_message': error_message})

    if request.method == 'POST':
        comment = request.POST.get('comment')
        date = request.POST.get('date')

        # Check if room is already reserved on the given date
        if Reservation.objects.filter(room=room, date=date).exists():
            error_message = 'Sala jest już zarezerwowana na ten dzień'
            return render(request, 'reserve_room.html', {'room': room, 'error_message': error_message})

        # Check if the date is not in the past
        if date < str(timezone.now().date()):
            error_message = 'Nie można zarezerwować sali w przeszłości'
            return render(request, 'reserve_room.html', {'room': room, 'error_message': error_message})

        # Create a new reservation object and save it to the database
        new_reservation = Reservation(date=date, room=room, comment=comment)
        new_reservation.save()

        # Redirect to the room list page
        return redirect('rooms')

    # If request method is GET, display reservation form
    return render(request, 'reserve_room.html', {'room': room})
