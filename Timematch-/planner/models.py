
# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    title = models.CharField(max_length=180)
    code = models.CharField(max_length=8, unique=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')
    finalized_date = models.DateField(null=True, blank=True)
    finalized_start_time = models.TimeField(null=True, blank=True)
    finalized_end_time = models.TimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} ({self.code})'


class EventMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='memberships')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f'{self.user.username} -> {self.event.code}'


class Availability(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = 'available', 'Available'
        MAYBE = 'maybe', 'Maybe'
        BUSY = 'busy', 'Busy'

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='availabilities')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='availabilities')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date', 'start_time']

    def __str__(self):
        return f'{self.event.code} {self.date} {self.start_time}-{self.end_time}'


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    event = models.ForeignKey(Event, null=True, blank=True, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.message