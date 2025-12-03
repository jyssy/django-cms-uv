"""
URL configuration for djangocmsjoy application views
Separate from main urls.py to keep CMS urls clean
"""
from django.urls import path
from . import views

app_name = 'djangocmsjoy'

urlpatterns = [
    # Main navigation pages
    path('operations/', views.index, name='index'),
    path('system-status-news/', views.system_status_news, name='system_status_news'),
    path('integration-news/', views.integration_news, name='integration_news'),
    
    # System Status News management
    path('system-status-news/add/', views.add_system_status_news, name='add_system_status_news'),
    path('system-status-news/update/<int:pk>/', views.update_system_status_news, name='update_system_status_news'),
    
    # Integration News management
    path('integration-news/add/', views.add_integration_news, name='add_integration_news'),
    path('integration-news/update/<int:pk>/', views.update_integration_news, name='update_integration_news'),
]
