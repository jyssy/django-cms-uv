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
    path('access-news/', views.access_news, name='access_news'),
    path('system-news/', views.system_news, name='system_news'),
    path('resource-news/', views.resource_news, name='resource_news'),
    
    # System News management
    path('system-news/add/', views.add_system_news, name='add_system_news'),
    path('system-news/update/<int:pk>/', views.update_system_news, name='update_system_news'),
    
    # Resource News management
    path('resource-news/add/', views.add_resource_news, name='add_resource_news'),
    path('resource-news/update/<int:pk>/', views.update_resource_news, name='update_resource_news'),
    
    # ACCESS News management
    path('access-news/add/', views.add_access_news, name='add_access_news'),
    path('access-news/update/<int:pk>/', views.update_access_news, name='update_access_news'),
]
