from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.views.decorators.cache import cache_page
from django.urls import reverse_lazy
from .models import SystemStatusNews, IntegrationNews
import requests
from collections import defaultdict


def index(request):
    """Operations Portal landing page"""
    context = {
        'page': 'index',
    }
    return render(request, 'operations_portalcms_django/index.html', context)


def system_status_news(request):
    """System Status News listing page"""
    news_items = SystemStatusNews.objects.filter(is_active=True)
    context = {
        'page': 'system_status_news',
        'system_status_news': news_items,
    }
    return render(request, 'operations_portalcms_django/system_status_news.html', context)


def integration_news(request):
    """Integration News listing page"""
    news_items = IntegrationNews.objects.filter(is_active=True)
    context = {
        'page': 'integration_news',
        'integration_news': news_items,
    }
    return render(request, 'operations_portalcms_django/integration_news.html', context)


# News management views with permission checks

@login_required
@permission_required('operations_portalcms_django.add_systemstatusnews', login_url=reverse_lazy('web:unprivileged'))
def add_system_status_news(request):
    """Add new system status news item"""
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        SystemStatusNews.objects.create(
            title=title,
            content=content,
            author=request.user
        )
        messages.success(request, 'System status news added successfully!')
        return redirect('djangocmsjoy:system_status_news')
    
    context = {'page': 'system_status_news'}
    return render(request, 'operations_portalcms_django/add_system_status_news.html', context)


@login_required
@permission_required('operations_portalcms_django.change_systemstatusnews', login_url=reverse_lazy('web:unprivileged'))
def update_system_status_news(request, pk):
    """Update existing system status news item"""
    news = get_object_or_404(SystemStatusNews, pk=pk)
    
    if request.method == 'POST':
        news.title = request.POST.get('title')
        news.content = request.POST.get('content')
        news.save()
        messages.success(request, 'System status news updated successfully!')
        return redirect('djangocmsjoy:system_status_news')
    
    context = {
        'page': 'system_status_news',
        'news': news,
    }
    return render(request, 'operations_portalcms_django/update_system_status_news.html', context)


@login_required
@permission_required('operations_portalcms_django.add_integrationnews', login_url=reverse_lazy('web:unprivileged'))
def add_integration_news(request):
    """Add new integration news item"""
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        IntegrationNews.objects.create(
            title=title,
            content=content,
            author=request.user
        )
        messages.success(request, 'Integration news added successfully!')
        return redirect('djangocmsjoy:integration_news')
    
    context = {'page': 'integration_news'}
    return render(request, 'operations_portalcms_django/add_integration_news.html', context)


@login_required
@permission_required('operations_portalcms_django.change_integrationnews', login_url=reverse_lazy('web:unprivileged'))
def update_integration_news(request, pk):
    """Update existing integration news item"""
    news = get_object_or_404(IntegrationNews, pk=pk)
    
    if request.method == 'POST':
        news.title = request.POST.get('title')
        news.content = request.POST.get('content')
        news.save()
        messages.success(request, 'Integration news updated successfully!')
        return redirect('djangocmsjoy:integration_news')
    
    context = {
        'page': 'integration_news',
        'news': news,
    }
    return render(request, 'operations_portalcms_django/update_integration_news.html', context)


@cache_page(60 * 15)  # Cache for 15 minutes
def access_allocated_resources(request):
    """Display ACCESS allocated resources from API"""
    api_url = 'https://operations-api.access-ci.org/wh2/cider/v1/access-active/'
    
    resources_by_org = defaultdict(list)
    error_message = None
    
    try:
        headers = {'Accept': 'application/json'}
        response = requests.get(api_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Check if response has content
        if not response.content:
            error_message = "API returned empty response"
            resources_by_org = {}
        else:
            try:
                data = response.json()
                
                # Group resources by organization
                for resource in data.get('results', []):
                    # Use organization name from the resource provider organization field
                    org_name = resource.get('organization_name', 'Unknown Organization')
                    if not org_name or org_name.strip() == '':
                        org_name = 'Unknown Organization'
                    resources_by_org[org_name].append(resource)
                
                # Sort organizations alphabetically
                resources_by_org = dict(sorted(resources_by_org.items()))
                
            except ValueError as json_err:
                error_message = f"Invalid JSON response: {str(json_err)}"
                resources_by_org = {}
        
    except requests.RequestException as e:
        error_message = f"Unable to fetch resources: {str(e)}"
        resources_by_org = {}
    
    context = {
        'page': 'access_allocated',
        'resources_by_org': resources_by_org,
        'error_message': error_message,
    }
    return render(request, 'operations_portalcms_django/access_allocated.html', context)
