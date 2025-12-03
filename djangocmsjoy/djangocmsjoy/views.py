from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import SystemNews, ResourceNews, AccessNews


def index(request):
    """Operations Portal landing page"""
    context = {
        'page': 'index',
    }
    return render(request, 'djangocmsjoy/index.html', context)


def access_news(request):
    """ACCESS News listing page"""
    news_items = AccessNews.objects.filter(is_active=True)
    context = {
        'page': 'access_news',
        'access_news': news_items,
    }
    return render(request, 'djangocmsjoy/access_news.html', context)


def system_news(request):
    """System News listing page"""
    news_items = SystemNews.objects.filter(is_active=True)
    context = {
        'page': 'system_news',
        'system_news': news_items,
    }
    return render(request, 'djangocmsjoy/system_news.html', context)


def resource_news(request):
    """Resource News listing page"""
    news_items = ResourceNews.objects.filter(is_active=True)
    context = {
        'page': 'resource_news',
        'resource_news': news_items,
    }
    return render(request, 'djangocmsjoy/resource_news.html', context)


# Staff-only views for managing news
def is_staff(user):
    return user.is_staff


@login_required
@user_passes_test(is_staff)
def add_system_news(request):
    """Add new system news item"""
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        SystemNews.objects.create(
            title=title,
            content=content,
            author=request.user
        )
        messages.success(request, 'System news added successfully!')
        return redirect('djangocmsjoy:system_news')
    
    context = {'page': 'system_news'}
    return render(request, 'djangocmsjoy/add_system_news.html', context)


@login_required
@user_passes_test(is_staff)
def update_system_news(request, pk):
    """Update existing system news item"""
    news = get_object_or_404(SystemNews, pk=pk)
    
    if request.method == 'POST':
        news.title = request.POST.get('title')
        news.content = request.POST.get('content')
        news.save()
        messages.success(request, 'System news updated successfully!')
        return redirect('djangocmsjoy:system_news')
    
    context = {
        'page': 'system_news',
        'news': news,
    }
    return render(request, 'djangocmsjoy/update_system_news.html', context)


@login_required
@user_passes_test(is_staff)
def add_resource_news(request):
    """Add new resource news item"""
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        ResourceNews.objects.create(
            title=title,
            content=content,
            author=request.user
        )
        messages.success(request, 'Resource news added successfully!')
        return redirect('djangocmsjoy:resource_news')
    
    context = {'page': 'resource_news'}
    return render(request, 'djangocmsjoy/add_resource_news.html', context)


@login_required
@user_passes_test(is_staff)
def update_resource_news(request, pk):
    """Update existing resource news item"""
    news = get_object_or_404(ResourceNews, pk=pk)
    
    if request.method == 'POST':
        news.title = request.POST.get('title')
        news.content = request.POST.get('content')
        news.save()
        messages.success(request, 'Resource news updated successfully!')
        return redirect('djangocmsjoy:resource_news')
    
    context = {
        'page': 'resource_news',
        'news': news,
    }
    return render(request, 'djangocmsjoy/update_resource_news.html', context)


@login_required
@user_passes_test(is_staff)
def add_access_news(request):
    """Add new ACCESS news item"""
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        external_url = request.POST.get('external_url', '')
        AccessNews.objects.create(
            title=title,
            content=content,
            external_url=external_url if external_url else None,
            author=request.user
        )
        messages.success(request, 'ACCESS news added successfully!')
        return redirect('djangocmsjoy:access_news')
    
    context = {'page': 'access_news'}
    return render(request, 'djangocmsjoy/add_access_news.html', context)


@login_required
@user_passes_test(is_staff)
def update_access_news(request, pk):
    """Update existing ACCESS news item"""
    news = get_object_or_404(AccessNews, pk=pk)
    
    if request.method == 'POST':
        news.title = request.POST.get('title')
        news.content = request.POST.get('content')
        news.external_url = request.POST.get('external_url', '') or None
        news.save()
        messages.success(request, 'ACCESS news updated successfully!')
        return redirect('djangocmsjoy:access_news')
    
    context = {
        'page': 'access_news',
        'news': news,
    }
    return render(request, 'djangocmsjoy/update_access_news.html', context)
