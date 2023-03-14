from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('', views.home, name='home'),
    path('book/', views.book, name='book'),
    path('success/', views.success, name='success'),
    
]
