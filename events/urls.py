from django.urls import path
from . import views

urlpatterns = [
    path('', views.EventListView.as_view(), name='event_list'),
    path('event/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('event/<int:pk>/register/', views.RegisterEventView.as_view(), name='register_event'),
    path('registration/<int:pk>/cancel/', views.CancelRegistrationView.as_view(), name='cancel_registration'),
    path('my-registrations/', views.MyRegistrationsView.as_view(), name='my_registrations'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.LogoutUserView.as_view(), name='logout'),
]
