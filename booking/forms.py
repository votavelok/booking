from django import forms


class BookingForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=100)
    email = forms.EmailField()
