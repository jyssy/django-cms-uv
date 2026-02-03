""" URL configuration for operations_portalcms_django application views
Separate from main urls.py to keep CMS urls clean
"""
from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'operations_portalcms_django'

urlpatterns = [
    # Redirect root to operations page
    path('', RedirectView.as_view(pattern_name='operations_portalcms_django:index', permanent=False), name='home'),
    
    # Main navigation pages
    path('operations/', views.index, name='index'),
    path('infrastructure-news/', views.system_status_news, name='system_status_news'),
    path('integration-news/', views.integration_news, name='integration_news'),
    path('resources/access-allocated/', views.access_allocated_resources, name='access_allocated'),
    
    # Infrastructure News (System and Infrastructure Status) management
    path('infrastructure-news/add/', views.add_system_status_news, name='add_system_status_news'),
    path('infrastructure-news/update/<int:pk>/', views.update_system_status_news, name='update_system_status_news'),
    
    # Integration News management
    path('integration-news/add/', views.add_integration_news, name='add_integration_news'),
    path('integration-news/update/<int:pk>/', views.update_integration_news, name='update_integration_news'),
]
