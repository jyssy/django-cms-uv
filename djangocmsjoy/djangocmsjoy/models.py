from django.db import models
from django.contrib.auth.models import User
from cms.models.pluginmodel import CMSPlugin


class SystemStatusNews(models.Model):
    """News items related to system status, maintenance, outages, etc."""
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'System Status News'
        verbose_name_plural = 'System Status News'
        db_table = 'djangocmsjoy_systemstatusnews'
    
    def __str__(self):
        return self.title


class IntegrationNews(models.Model):
    """News items related to integrations, resource connections, new services, etc."""
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Integration News'
        verbose_name_plural = 'Integration News'
        db_table = 'djangocmsjoy_integrationnews'
    
    def __str__(self):
        return self.title


# CMS Plugin Models for News Feed

class SystemStatusNewsItemPlugin(CMSPlugin):
    """Model for System Status News items added via CMS"""
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    published_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-published_date']  # Newest first
    
    def __str__(self):
        return self.title


class IntegrationNewsItemPlugin(CMSPlugin):
    """Model for Integration News items added via CMS"""
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    published_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-published_date']  # Newest first
    
    def __str__(self):
        return self.title
