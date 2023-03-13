from django.db import models


class Booking(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f'{self.name} ({self.start_date} - {self.end_date})'
