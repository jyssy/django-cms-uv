from django import forms
from .models import IntegrationNews, SystemStatusNews


class DateInput(forms.DateInput):
    """Custom widget for date fields with HTML5 date picker"""
    input_type = 'date'


class IntegrationNewsForm(forms.ModelForm):
    """Form for creating and updating Integration News"""
    
    INTEGRATION_NEWS_TYPES = [
        ('software_release', 'Software Release'),
        ('new_roadmap', 'New Integration Roadmap'),
        ('changed_roadmap', 'Changed Integration Roadmap'),
        ('new_roadmap_task', 'New Integration Roadmap Task'),
        ('changed_roadmap_task', 'Changed Integration Roadmap Task'),
    ]
    
    AFFECTED_ELEMENTS = [
        ('cloud_roadmap', 'ACCESS Allocated Production Cloud - Integration Roadmap'),
        ('compute_roadmap', 'ACCESS Allocated Production Compute - Integration Roadmap'),
        ('storage_roadmap', 'ACCESS Allocated Production Storage - Integration Roadmap'),
        ('science_gateway_roadmap', 'ACCESS Integrated Science Gateway - Integration Roadmap'),
        ('nagios', 'ACCESS Monitoring Service - Nagios'),
        ('online_service_roadmap', 'ACCESS Production Online Service - Integration Roadmap'),
        ('aws_registry', 'ACCESS Public AWS Container Registry'),
        ('cider', 'CiDeR - CyberInfrastructure Description Repository'),
        ('ipf', 'Information Publishing Framework (IPF) tool for publishing compute resource information'),
    ]
    
    news_type = forms.ChoiceField(
        choices=INTEGRATION_NEWS_TYPES,
        required=True,
        label='Integration News Type',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    affected_element = forms.ChoiceField(
        choices=AFFECTED_ELEMENTS,
        required=True,
        label='Affected Element',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    effective_date = forms.DateField(
        required=True,
        label='Effective Date',
        widget=DateInput(attrs={'class': 'form-control'}),
        help_text='Date when this news becomes effective'
    )
    
    expiration_date = forms.DateField(
        required=False,
        label='Expiration Date',
        widget=DateInput(attrs={'class': 'form-control'}),
        help_text='Date when this news expires (optional)'
    )
    
    email_notification = forms.BooleanField(
        required=False,
        initial=False,
        label='Email everyone',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        help_text='Not yet implemented'
    )
    
    slack_notification = forms.BooleanField(
        required=False,
        initial=False,
        label='Post to Slack',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        help_text='Not yet implemented'
    )
    
    class Meta:
        model = IntegrationNews
        fields = ['title', 'content', 'is_active']
        labels = {
            'title': 'Subject',
            'content': 'News Content',
            'is_active': 'Active'
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter news subject'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Enter news content'
            }),
        }
        help_texts = {
            'content': 'To update news content text please follow formatting guidance at <a href="https://operations.access-ci.org/operational-status-communications" target="_blank">Operational Status Communications</a>',
        }


class SystemStatusNewsForm(forms.ModelForm):
    """Form for creating and updating System and Infrastructure Status News"""
    
    effective_date = forms.DateField(
        required=True,
        label='Effective Date',
        widget=DateInput(attrs={'class': 'form-control'}),
        help_text='Date when this news becomes effective'
    )
    
    expiration_date = forms.DateField(
        required=False,
        label='Expiration Date',
        widget=DateInput(attrs={'class': 'form-control'}),
        help_text='Date when this news expires (optional)'
    )
    
    email_notification = forms.BooleanField(
        required=False,
        initial=False,
        label='Email everyone',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        help_text='Not yet implemented'
    )
    
    slack_notification = forms.BooleanField(
        required=False,
        initial=False,
        label='Post to Slack',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        help_text='Not yet implemented'
    )
    
    class Meta:
        model = SystemStatusNews
        fields = ['title', 'content', 'is_active']
        labels = {
            'title': 'Subject',
            'content': 'News Content',
            'is_active': 'Active'
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter news subject'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Enter news content'
            }),
        }
        help_texts = {
            'content': 'To update news content text please follow formatting guidance at <a href="https://operations.access-ci.org/operational-status-communications" target="_blank">Operational Status Communications</a>',
        }
