from django.contrib import admin
from .models import Event, Registration

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'location', 'capacity', 'registered_count', 'available_seats', 'organizer')
    list_filter = ('date', 'organizer', 'location')
    search_fields = ('title', 'description', 'location')
    raw_id_fields = ('organizer',)
    date_hierarchy = 'date'

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'registration_date', 'status')
    list_filter = ('status', 'registration_date', 'event')
    search_fields = ('user__username', 'user__email', 'event__title')
    raw_id_fields = ('user', 'event')
