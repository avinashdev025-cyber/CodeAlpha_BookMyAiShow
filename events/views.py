from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.db import transaction
from django.db.models import Q
from .models import Event, Registration

class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(location__icontains=search_query)
            )
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context


class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.get_object()
        
        # Check if current user is registered for this event
        user_registration = None
        if self.request.user.is_authenticated:
            user_registration = Registration.objects.filter(
                user=self.request.user,
                event=event
            ).first()
            
        context['user_registration'] = user_registration
        context['is_registered'] = user_registration and user_registration.status == 'REGISTERED'
        return context


class RegisterEventView(LoginRequiredMixin, View):
    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        
        try:
            with transaction.atomic():
                # Lock the event row to prevent race conditions during concurrent registration checks
                event = Event.objects.select_for_update().get(pk=pk)
                
                registration, created = Registration.objects.get_or_create(
                    user=request.user,
                    event=event,
                    defaults={'status': 'REGISTERED'}
                )
                
                if not created:
                    if registration.status == 'REGISTERED':
                        messages.warning(request, "You are already registered for this event.")
                        return redirect('event_detail', pk=pk)
                    else:
                        # Reactivate cancelled registration
                        if event.is_full:
                            messages.error(request, "Sorry, this event is fully booked.")
                            return redirect('event_detail', pk=pk)
                        registration.status = 'REGISTERED'
                        registration.save()
                        messages.success(request, f"Successfully registered for {event.title}!")
                else:
                    messages.success(request, f"Successfully registered for {event.title}!")
                    
        except Exception as e:
            messages.error(request, f"Registration failed: {str(e)}")
            
        return redirect('event_detail', pk=pk)


class CancelRegistrationView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # The pk is for the registration ID
        registration = get_object_or_404(Registration, pk=pk, user=request.user)
        
        if registration.status == 'CANCELLED':
            messages.warning(request, "This registration is already cancelled.")
        else:
            registration.status = 'CANCELLED'
            registration.save()
            messages.success(request, f"Your registration for '{registration.event.title}' has been cancelled.")
            
        # Redirect to referring page or registrations page
        next_url = request.GET.get('next', 'my_registrations')
        return redirect(next_url)


class MyRegistrationsView(LoginRequiredMixin, ListView):
    model = Registration
    template_name = 'events/my_registrations.html'
    context_object_name = 'registrations'

    def get_queryset(self):
        return Registration.objects.filter(user=self.request.user).select_related('event')


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'events/register.html'
    success_url = reverse_lazy('event_list')

    def form_valid(self, form):
        valid = super().form_valid(form)
        # Automatically log in the user after signing up
        login(self.request, self.object, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(self.request, f"Welcome to BookMyAishow, {self.object.username}! Your account was created.")
        return valid


class LoginUserView(LoginView):
    template_name = 'events/login.html'
    
    def form_valid(self, form):
        messages.success(self.request, f"Welcome back, {form.get_user().username}!")
        return super().form_valid(form)


class LogoutUserView(LogoutView):
    next_page = reverse_lazy('event_list')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "You have been logged out.")
        return super().dispatch(request, *args, **kwargs)
