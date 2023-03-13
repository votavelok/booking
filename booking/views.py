from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Booking
from .forms import BookingForm


def home(request):
    if request.method == 'POST':
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        bookings = Booking.objects.filter(start_date__lte=end_date, end_date__gte=start_date)
        if bookings.exists():
            return render(request, 'unavailable.html')
        else:
            request.session['start_date'] = start_date
            request.session['end_date'] = end_date
            return redirect('booking:book')
    return render(request, 'home.html')


def book(request):
    start_date = request.session.get('start_date')
    end_date = request.session.get('end_date')
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
    return render(request, 'success.html')
