from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse
from .models import Event, Registration
import datetime

class EventRegistrationTests(TestCase):
    def setUp(self):
        # Create users
        self.organizer = User.objects.create_user(username='organizer', password='password123')
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')

        # Create event with capacity 1
        self.event = Event.objects.create(
            title="Tech Hackathon 2026",
            description="A modern 48h hackathon coding event.",
            date=datetime.date.today() + datetime.timedelta(days=10),
            time=datetime.time(9, 0),
            location="Silicon Valley HQ",
            capacity=1,
            organizer=self.organizer
        )

    def test_event_properties(self):
        """Test initial capacity and seat tracking properties."""
        self.assertEqual(self.event.registered_count, 0)
        self.assertEqual(self.event.available_seats, 1)
        self.assertFalse(self.event.is_full)

    def test_successful_registration(self):
        """Test a user can register for an event successfully."""
        registration = Registration.objects.create(
            user=self.user1,
            event=self.event,
            status='REGISTERED'
        )
        self.assertEqual(self.event.registered_count, 1)
        self.assertEqual(self.event.available_seats, 0)
        self.assertTrue(self.event.is_full)
        self.assertEqual(registration.status, 'REGISTERED')

    def test_registration_over_capacity(self):
        """Test that registering when event is full raises validation error."""
        # Fill capacity (capacity = 1)
        Registration.objects.create(user=self.user1, event=self.event, status='REGISTERED')
        
        # Try to register user2 (should fail)
        with self.assertRaises(ValidationError):
            Registration.objects.create(user=self.user2, event=self.event, status='REGISTERED')

    def test_duplicate_registration_prevention(self):
        """Test unique constraints prevent registering the same user twice."""
        Registration.objects.create(user=self.user1, event=self.event, status='REGISTERED')
        
        # Unique constraint check validation runs during save() calling full_clean()
        with self.assertRaises(ValidationError):
            Registration.objects.create(user=self.user1, event=self.event, status='REGISTERED')

    def test_cancellation_frees_up_capacity(self):
        """Test that cancelling a registration updates status and frees up a seat."""
        registration = Registration.objects.create(user=self.user1, event=self.event, status='REGISTERED')
        self.assertTrue(self.event.is_full)

        # Cancel registration
        registration.status = 'CANCELLED'
        registration.save()

        self.assertEqual(self.event.registered_count, 0)
        self.assertEqual(self.event.available_seats, 1)
        self.assertFalse(self.event.is_full)


class EventViewsTests(TestCase):
    def setUp(self):
        self.organizer = User.objects.create_user(username='organizer', password='password123')
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.event = Event.objects.create(
            title="Design Thinking Masterclass",
            description="Learn UI/UX design fundamentals.",
            date=datetime.date.today() + datetime.timedelta(days=5),
            time=datetime.time(14, 0),
            location="Design Lab Studio",
            capacity=10,
            organizer=self.organizer
        )

    def test_event_list_view(self):
        """Test event list page displays events."""
        response = self.client.get(reverse('event_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.event.title)
        self.assertTemplateUsed(response, 'events/event_list.html')

    def test_event_detail_view(self):
        """Test event detail page displays correct information."""
        response = self.client.get(reverse('event_detail', args=[self.event.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.event.description)
        self.assertTemplateUsed(response, 'events/event_detail.html')

    def test_register_event_requires_login(self):
        """Test that registering for an event redirects to login if unauthenticated."""
        response = self.client.post(reverse('register_event', args=[self.event.id]))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_register_event_logged_in(self):
        """Test that registered users can sign up using POST view."""
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('register_event', args=[self.event.id]))
        
        # Should redirect to detail view with success message
        self.assertRedirects(response, reverse('event_detail', args=[self.event.id]))
        
        # Verify db insertion
        reg = Registration.objects.get(user=self.user, event=self.event)
        self.assertEqual(reg.status, 'REGISTERED')

    def test_cancel_registration_view(self):
        """Test cancelling registration through the cancellation view."""
        # Set up active registration first
        registration = Registration.objects.create(user=self.user, event=self.event, status='REGISTERED')
        
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('cancel_registration', args=[registration.id]))
        
        # Should redirect to default next (my_registrations)
        self.assertRedirects(response, reverse('my_registrations'))
        
        # Verify status in database
        registration.refresh_from_db()
        self.assertEqual(registration.status, 'CANCELLED')
