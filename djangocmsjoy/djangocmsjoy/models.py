from django.db import models
from django.contrib.auth.models import User


class SystemNews(models.Model):
    """News items related to system status, maintenance, outages, etc."""
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'System News'
        verbose_name_plural = 'System News'
    
    def __str__(self):
        return self.title


class ResourceNews(models.Model):
    """News items related to resources, allocations, new services, etc."""
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Resource News'
        verbose_name_plural = 'Resource News'
    
    def __str__(self):
        return self.title


class AccessNews(models.Model):
    """General ACCESS news items - announcements, events, achievements, etc."""
    title = models.CharField(max_length=200)
    content = models.TextField()
    external_url = models.URLField(blank=True, null=True, help_text="Link to external news article")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'ACCESS News'
        verbose_name_plural = 'ACCESS News'
    
    def __str__(self):
        return self.title
