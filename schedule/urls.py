from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.projects, name='projects'),
    path('people/', views.people, name='people'),
    path('schedule/', views.schedule, name='schedule'),
    path('download-ics/<int:pk>/', views.download_ics, name='download_ics'),
]