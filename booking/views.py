from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Booking
from .forms import BookingForm

def home(request):
    """
    Отображает домашнюю страницу и обрабатывает POST запросы для проверки наличия бронирований.

    Аргументы:
        request: объект HTTP запроса.

    Возвращает:
        Отображенный шаблон домашней страницы или перенаправление на страницу бронирования.
    """
    if request.method == 'POST':
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        
        # Запрос в базу данных на наличие существующих бронирований в запрошенный период времени.
        bookings = Booking.objects.filter(start_date__lte=end_date, end_date__gte=start_date)
       
        if bookings.exists():
            # Если бронирования существуют, возвращается шаблон "unavailable".
            return render(request, 'unavailable.html')
        else:
            # Если бронирования отсутствуют, сохраняются даты начала и окончания бронирования в сессии и происходит перенаправление на страницу бронирования.
            request.session['start_date'] = start_date
            request.session['end_date'] = end_date
            return redirect('booking:book')
    return render(request, 'home.html')


def book(request):
    """
    Отображает страницу бронирования и обрабатывает POST запросы для создания новых бронирований.

    Аргументы:
        request: объект HTTP запроса.

    Возвращает:
        Отображенный шаблон страницы бронирования или перенаправление на домашнюю страницу.
    """
    start_date = request.session.get('start_date')
    end_date = request.session.get('end_date')
    
    # Если даты начала и окончания бронирования не сохранены в сессии, происходит перенаправление на домашнюю страницу.
    if not start_date or not end_date:
        return redirect('booking:home')
    form = BookingForm()
    context = {
        'form': form,
        'start_date': start_date,
        'end_date': end_date
    }
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            booking = Booking(name=name, email=email, start_date=start_date, end_date=end_date)
            booking.save()
            request.session.pop('start_date')
            request.session.pop('end_date')
            return redirect('booking:success')
        context['form'] = form
    return render(request, 'book.html', context)


def success(request):
    """
    Отображает страницу успешного бронирования.

    Аргументы:
        request: объект HTTP запроса.

    Возвращает:
        Отображенный шаблон страницы успешного бронирования.
    """
    return render(request, 'success.html')