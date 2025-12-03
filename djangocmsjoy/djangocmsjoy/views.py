from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import SystemStatusNews, IntegrationNews


def index(request):
    """Operations Portal landing page"""
    context = {
        'page': 'index',
    }
    return render(request, 'djangocmsjoy/index.html', context)


def system_status_news(request):
    """System Status News listing page"""
    news_items = SystemStatusNews.objects.filter(is_active=True)
    context = {
        'page': 'system_status_news',
        'system_status_news': news_items,
    }
    return render(request, 'djangocmsjoy/system_status_news.html', context)


def integration_news(request):
    """Integration News listing page"""
    news_items = IntegrationNews.objects.filter(is_active=True)
    context = {
        'page': 'integration_news',
        'integration_news': news_items,
    }
    return render(request, 'djangocmsjoy/integration_news.html', context)


# Staff-only views for managing news
def is_staff(user):
    return user.is_staff


@login_required
@user_passes_test(is_staff)
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
    return render(request, 'djangocmsjoy/add_system_status_news.html', context)


@login_required
@user_passes_test(is_staff)
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
    return render(request, 'djangocmsjoy/update_system_status_news.html', context)


@login_required
@user_passes_test(is_staff)
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
    return render(request, 'djangocmsjoy/add_integration_news.html', context)


@login_required
@user_passes_test(is_staff)
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
    return render(request, 'djangocmsjoy/update_integration_news.html', context)
