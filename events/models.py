from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    capacity = models.PositiveIntegerField(help_text="Maximum number of attendees")
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date', 'time']

    def __str__(self):
        return self.title

    @property
    def registered_count(self):
        return self.registrations.filter(status='REGISTERED').count()

    @property
    def available_seats(self):
        return max(0, self.capacity - self.registered_count)

    @property
    def is_full(self):
        return self.available_seats <= 0


class Registration(models.Model):
    STATUS_CHOICES = [
        ('REGISTERED', 'Registered'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registrations')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    registration_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='REGISTERED')
    additional_notes = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('user', 'event')
        ordering = ['-registration_date']

    def __str__(self):
        return f"{self.user.username} - {self.event.title} ({self.get_status_display()})"

    def clean(self):
        # Only check capacity if we are creating a new active registration
        # or changing status to REGISTERED from CANCELLED.
        if self.status == 'REGISTERED':
            # Check if this registration is already created and active (updating other fields)
            is_new_or_reactivating = True
            if self.pk:
                original = Registration.objects.get(pk=self.pk)
                if original.status == 'REGISTERED':
                    is_new_or_reactivating = False

            if is_new_or_reactivating and self.event.is_full:
                raise ValidationError("This event is already full.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
