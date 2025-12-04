# Development Processes for Django CMS - Localhost

**Project:** ACCESS Operations Portal Django CMS  
**Date:** December 3, 2025  
**Environment:** Local Development (macOS)  
**Python:** 3.13 with UV package manager  
**Django:** 5.2.9  
**Django CMS:** 5.0  
**Database:** PostgreSQL 15  
**Code Assistant:** Claude Sonnet 4.5

---

## Required Packages and Dependencies

### Core Framework
- **Django 5.2.9** - Python web framework
- **django-cms 5.0** - Content Management System for Django
- **psycopg2** or **psycopg2-binary** - PostgreSQL database adapter for Python
- **uv** - Fast Python package manager (alternative to pip/poetry)

### Django CMS Essentials
- **django-treebeard** - Tree structure for CMS page hierarchy
- **django-sekizai** - Template block management (for {% addtoblock %} tags)
- **djangocms-admin-style** - Custom admin interface styling for CMS
- **django-formtools** - Form wizard and preview utilities used by CMS

### CMS Plugins
- **djangocms-text** - Rich text editor plugin with CKEditor 5
- **djangocms-picture** - Image/picture plugin for adding images to CMS pages
- **djangocms-link** - Link plugin for internal and external links
- **djangocms-file** - File upload and download plugin
- **djangocms-video** - Video embedding plugin

### UI Framework
- **django-bootstrap5 25.0+** - Bootstrap 5 integration for Django templates
  - Provides template tags: `{% load django_bootstrap5 %}`
  - Used for forms, buttons, and responsive layout components
  - Must be in INSTALLED_APPS before custom apps

### ACCESS-Specific Components
- **Custom static assets** - ACCESS branding assets copied to djangocmsjoy/static/
  - NSF logo (nsf-logo.png)
  - ACCESS Operations logo (ACCESS-operations.svg)
  - ACCESS standard logo (access-logo.svg)
  - Favicon (favicon.ico)
  - ACCESS color scheme and fonts

### External Resources (CDN)
- **Bootstrap 5.3.x** - CSS framework loaded via CDN in templates
- **jQuery 3.6.1** - JavaScript library for DOM manipulation
- **jQuery UI 1.13.2** - UI widgets and interactions
- **@access-ci/ui 0.8.0** - ACCESS universal navigation menus
  - Loaded via ES module: `https://esm.sh/@access-ci/ui@0.8.0`
  - Provides consistent header menus across ACCESS services
- **Google Fonts - Archivo** - ACCESS brand font family
  - Used for headers and branding elements

### Custom CMS Plugins (Created in this Project)
- **SystemStatusNewsItemPlugin** - Individual system status news item for CMS editor
- **IntegrationNewsItemPlugin** - Individual integration news item for CMS editor
- **SystemStatusNewsFeedPlugin** - Container plugin for system status news items
- **IntegrationNewsFeedPlugin** - Container plugin for integration news items
  - **Note:** These were created as a learning exercise. See "Recommended Alternative" below.

### Recommended Alternative for Production
- **djangocms-blog** - Production-ready blog/news application for Django CMS
  - **PyPI:** `pip install djangocms-blog` or `uv add djangocms-blog`
  - **Documentation:** https://djangocms-blog.readthedocs.io/
  - **GitHub:** https://github.com/nephila/djangocms-blog
  - **Features:**
    * Multi-language support with django-parler
    * Rich text editing with CKEditor integration
    * SEO meta tags (Twitter cards, Open Graph, Google+ snippets)
    * Frontend editing with Django CMS toolbar
    * Configurable permalinks and URL patterns
    * Categories and tags
    * Author profiles
    * RSS/Atom feeds
    * Archive views by date
    * Related posts
    * Comments support (via external apps)
    * Django sitemap integration
    * Per-apphook configuration
    * Wizard integration for easy post creation
    * Desktop notifications
    * Liveblog functionality
    * Auto-setup with django-app-enabler
  - **Dependencies:**
    * django-parler (multilingual support)
    * django-taggit (tagging)
    * djangocms-text-ckeditor (rich text)
    * django-filer (media management)
    * easy-thumbnails (image processing)
  - **Why Use It:**
    * Battle-tested in production
    * Active maintenance (latest release: September 2024)
    * 450+ GitHub stars
    * Comprehensive documentation
    * Built-in SEO optimization
    * Supports Django 3.2 - 4.2
    * Supports Django CMS 3.9 - 3.11+
  - **Installation:**
    ```bash
    uv add djangocms-blog
    # Adds to INSTALLED_APPS:
    # 'djangocms_blog',
    # 'parler',
    # 'taggit',
    # 'taggit_autosuggest',
    # 'meta',
    # 'sortedm2m',
    ```
  - **When to Use Custom Plugins vs djangocms-blog:**
    * **Use djangocms-blog for:** Full-featured blogs, news sites, SEO-critical content
    * **Use custom plugins for:** Simple announcements, learning Django CMS, highly custom workflows

### Static Assets Added
- **nsf-logo.png** - National Science Foundation logo
- **ACCESS-operations.svg** - ACCESS Operations branding logo
- **ACCESS-pipe.svg** - Vertical divider graphic for header
- **access-logo.svg** - Standard ACCESS logo
- **favicon.ico** - Browser tab icon
- **style-serviceindex.css** - Custom CSS for Operations Portal styling

### Development Tools
- **PostgreSQL 15** - Production-grade database
  - Database: `djangocmsjoy`
  - User: `jelambeadmin`
  - Replaces default SQLite for better CMS performance

### Dependencies NOT Installed (Could Be Added Later)
- **django-allauth** - Social authentication framework
  - Not needed for current functionality
  - Would enable: OAuth, social logins, advanced user management
- **djangocms-blog** - Production-ready blog/news application (see Recommended Alternative section)

---

## Table of Contents

1. [Environment Setup](#1-environment-setup)
2. [ACCESS CI Header/Footer Integration](#2-access-ci-headerfooter-integration)
3. [Operations Portal Navigation System](#3-operations-portal-navigation-system)
4. [Universal Menus Integration](#4-universal-menus-integration)
5. [Database Management](#5-database-management)
6. [Static Files Management](#6-static-files-management)
7. [Development Server](#7-development-server)
8. [Testing Procedures](#8-testing-procedures)
9. [Project File Structure](#9-project-file-structure)
10. [Common Commands Reference](#10-common-commands-reference)
11. [Django CMS Settings Reference](#11-django-cms-settings-reference)
12. [Model Refactoring: News Categories Alignment](#12-model-refactoring-news-categories-alignment)
13. [Removing AccessNews Model and External Linking](#13-removing-accessnews-model-and-external-linking)
14. [SQLite to PostgreSQL Migration](#14-sqlite-to-postgresql-migration)
15. [Template Tag and Static File Troubleshooting](#15-template-tag-and-static-file-troubleshooting)
16. [Design Integration: Bootstrap, ACCESS Branding, and Theming](#16-design-integration-bootstrap-access-branding-and-theming)
17. [Custom Django CMS Plugins: News Feed System](#17-custom-django-cms-plugins-news-feed-system)

---

## 1. Environment Setup

### Prerequisites
```bash
# Python 3.13 installed via uv
# PostgreSQL 15 running on localhost:5432
# Database: djangocmsjoy
# User: jelambeadmin
```

### Working Directory
```bash
cd /Users/jelambeadmin/Documents/access-sysops/django-cms-uv
```

### Virtual Environment

**What is UV?**  
UV is a modern Python package and project manager (similar to pip/poetry but much faster) that automatically manages virtual environments. It reads project dependencies from `pyproject.toml` and ensures consistent installations across all development environments.

**Project Configuration:**
- Uses Python 3.13
- Dependencies: Django 5.2.9, djangocms-admin-style 3.3+, psycopg2-binary 2.9+, django-bootstrap5 25.0+
- UV creates a `.venv` directory automatically when you run `uv sync`

### Initial Setup Commands
```bash
# Install dependencies (if needed)
# This reads pyproject.toml and installs all required packages
uv sync

# Run migrations
# Migrations create/update database tables based on Django models
# This must be run after any model changes or initial setup
uv run python djangocmsjoy/manage.py migrate

# Create superuser (if needed)
# Creates an admin account for accessing Django admin panel at /admin/
# You'll be prompted for username, email, and password
uv run python djangocmsjoy/manage.py createsuperuser

# Collect static files
# Copies CSS, JS, images from all apps into a single staticfiles/ directory
# Required for production; optional in development (Django serves files automatically)
uv run python djangocmsjoy/manage.py collectstatic --noinput
```

---

## 2. ACCESS CI Header/Footer Integration

### Overview
Integrated official ACCESS CI organizational branding from [access-ci-org/access-ci-ui](https://github.com/access-ci-org/access-ci-ui) repository.

### Step 2.1: Research Components
**Tool Used:** GitHub repository search on access-ci-org/access-ci-ui  
**Query:** "header footer navigation component HTML template"

**Discovered:**
- React-based components with Shadow DOM
- CSS architecture with ACCESS branding colors
- Logo paths: `src/images/nsf-logo.png` and `src/images/access-logo.svg`
- Footer structure with NSF awards, social links, personas

### Step 2.2: Download Logo Assets
```bash
# Navigate to static images directory
cd djangocmsjoy/static/djangocmsjoy/img/

# Download NSF logo (28KB)
curl -O https://raw.githubusercontent.com/access-ci-org/access-ci-ui/main/src/images/nsf-logo.png

# Download ACCESS logo (7KB)
curl -O https://raw.githubusercontent.com/access-ci-org/access-ci-ui/main/src/images/access-logo.svg

# Return to project root
cd /Users/jelambeadmin/Documents/access-sysops/django-cms-uv
```

**Result:**
- ✅ `static/djangocmsjoy/img/nsf-logo.png` (28,877 bytes)
- ✅ `static/djangocmsjoy/img/access-logo.svg` (7,484 bytes)

### Step 2.3: Create Base Template
**File:** `djangocmsjoy/templates/base.html`

**Components Implemented:**

#### Header Section
- NSF logo (linked to nsf.gov)
- Divider bar
- ACCESS logo (linked to access-ci.org)
- Responsive sizing:
  - Mobile: NSF 49px height, ACCESS 23px height
  - Desktop: NSF 82px height, ACCESS 253px width

#### Navigation Section
- Django CMS page navigation with `{% show_menu 0 100 100 100 %}`
- Teal background (`--teal-700: #1A5B6E`)
- White text with hover effects
- Horizontal dropdown support

#### Footer Section
- NSF awards with 5 grant links: #2138259, #2138286, #2138307, #2137603, #2138296
- NSF disclaimer text
- "Contact ACCESS" link
- Social media: X/Twitter, YouTube, Facebook, LinkedIn
- Personas: Researchers, Educators, Graduate Students, Resource Providers, CI Community
- Utility links: Acceptable Use, Acknowledging ACCESS, Code of Conduct, Privacy Policy
- Footer logos (smaller versions)

#### CSS Variables (ACCESS Branding)
```css
--teal-050: #ECF9F8
--teal-100: #D5F3F0
--teal-400: #4DB8A8
--teal-600: #138597
--teal-700: #1A5B6E
--yellow-200: #FFE69C
--yellow-400: #FFC42D
--orange-400: #FF8C42
--green-400: #52C41A
--red-400: #FF4D4F
--contrast: #232323
--width: 1200px
```

#### Responsive Breakpoints
- Mobile: < 900px
- Desktop: ≥ 900px

### Step 2.4: Update CMS Templates
**Files Modified:**
1. `djangocmsjoy/templates/page.html` - Basic CMS page template
2. `djangocmsjoy/templates/feature.html` - Featured content template

**Changes:**
- Removed standalone HTML structure
- Changed to `{% extends "base.html" %}`
- Used `{% block title %}` and `{% block content %}`
- Maintained CMS placeholders: `{% placeholder "content" %}`
- Removed redundant navigation and static file loading

**Result:**
- ✅ All CMS pages now use ACCESS branding
- ✅ Header and footer appear on every page
- ✅ CMS editing functionality preserved

### Step 2.5: Collect Static Files
```bash
uv run python djangocmsjoy/manage.py collectstatic --noinput
```

**Output:**
```
2 static files copied to '/Users/jelambeadmin/Documents/access-sysops/django-cms-uv/djangocmsjoy/staticfiles'
556 static files total in staticfiles/
```

**Result:**
- ✅ Logo assets available via `{% static %}` tags
- ✅ Ready for development and production serving

---

## 3. Operations Portal Navigation System

### Overview
Created a complete news management system with four sections: Operations Portal landing page, ACCESS News, System News, and Resource News.

### Step 3.1: Create Database Models
**File:** `djangocmsjoy/djangocmsjoy/models.py`

**Models Created:**

#### SystemNews
```python
class SystemNews(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "System News"
```

#### ResourceNews
```python
class ResourceNews(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Resource News"
```

#### AccessNews
```python
class AccessNews(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    external_url = models.URLField(max_length=500, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "ACCESS News"
```

### Step 3.2: Create Database Migrations
```bash
# Create migration file
uv run python djangocmsjoy/manage.py makemigrations djangocmsjoy

# Apply migrations
uv run python djangocmsjoy/manage.py migrate
```

**Result:**
- ✅ Migration file: `djangocmsjoy/migrations/0001_initial.py`
- ✅ Database tables created:
  - `djangocmsjoy_systemnews`
  - `djangocmsjoy_resourcenews`
  - `djangocmsjoy_accessnews`

### Step 3.3: Create View Functions
**File:** `djangocmsjoy/djangocmsjoy/views.py`

**Views Created (12 total):**

#### Public Views (4)
```python
def index(request)           # Operations Portal landing page
def access_news(request)     # ACCESS News listing
def system_news(request)     # System News listing
def resource_news(request)   # Resource News listing
```

#### Staff-Only Management Views (8)
```python
@login_required
@user_passes_test(is_staff)
def add_system_news(request)       # Create new system news
def update_system_news(request, pk) # Edit system news

def add_resource_news(request)       # Create new resource news
def update_resource_news(request, pk) # Edit resource news

def add_access_news(request)       # Create new ACCESS news
def update_access_news(request, pk) # Edit ACCESS news
```

**Helper Function:**
```python
def is_staff(user):
    return user.is_staff
```

### Step 3.4: Configure URL Routing
**File:** `djangocmsjoy/djangocmsjoy/app_urls.py` (NEW)

**Why a Separate URL File?**  
Keeping Operations Portal URLs separate from Django CMS URLs maintains clean separation of concerns. CMS pages use the main `urls.py`, while custom app views use `app_urls.py`.

```python
from django.urls import path
from . import views

# app_name creates a namespace for URL reversing
# Use {% url 'djangocmsjoy:index' %} instead of {% url 'index' %}
# This prevents URL name collisions with other apps
app_name = 'djangocmsjoy'

urlpatterns = [
    # Public views
    path('operations/', views.index, name='index'),
    path('access-news/', views.access_news, name='access_news'),
    path('system-news/', views.system_news, name='system_news'),
    path('resource-news/', views.resource_news, name='resource_news'),
    
    # Management views (staff only)
    path('system-news/add/', views.add_system_news, name='add_system_news'),
    path('system-news/update/<int:pk>/', views.update_system_news, name='update_system_news'),
    path('resource-news/add/', views.add_resource_news, name='add_resource_news'),
    path('resource-news/update/<int:pk>/', views.update_resource_news, name='update_resource_news'),
    path('access-news/add/', views.add_access_news, name='add_access_news'),
    path('access-news/update/<int:pk>/', views.update_access_news, name='update_access_news'),
]
```

**File Modified:** `djangocmsjoy/djangocmsjoy/urls.py`

Added app_urls before cms.urls:
```python
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('djangocmsjoy.app_urls')),  # Operations Portal routes
    path('', include('cms.urls')),  # CMS catch-all (must be last)
]
```

**URL Namespace:** All routes use `djangocmsjoy:` prefix (e.g., `djangocmsjoy:index`)

### Step 3.5: Register Models in Admin
**File:** `djangocmsjoy/djangocmsjoy/admin.py`

```python
from django.contrib import admin
from .models import SystemNews, ResourceNews, AccessNews

@admin.register(SystemNews)
class SystemNewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'content']
    readonly_fields = ['created_at', 'updated_at']
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        super().save_model(request, obj, form, change)

@admin.register(ResourceNews)
class ResourceNewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'content']
    readonly_fields = ['created_at', 'updated_at']
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        super().save_model(request, obj, form, change)

@admin.register(AccessNews)
class AccessNewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'content']
    readonly_fields = ['created_at', 'updated_at']
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        super().save_model(request, obj, form, change)
```

### Step 3.6: Create Templates

#### Operations Portal Landing Page
**File:** `djangocmsjoy/templates/djangocmsjoy/index.html`
- Three overview cards linking to each news section
- Bootstrap styling
- Extends `base_nav_full.html`

#### News Listing Pages (3)
**Files:**
- `djangocmsjoy/templates/djangocmsjoy/access_news.html`
- `djangocmsjoy/templates/djangocmsjoy/system_news.html`
- `djangocmsjoy/templates/djangocmsjoy/resource_news.html`

**Features:**
- Display all active news items
- Show title, date, author, content
- "Add" button for staff users
- "Edit" buttons on each item for staff
- External URL button for ACCESS News (if provided)
- Bootstrap card layout

#### Management Forms (6)
**Files:**
- `djangocmsjoy/templates/djangocmsjoy/add_system_news.html`
- `djangocmsjoy/templates/djangocmsjoy/update_system_news.html`
- `djangocmsjoy/templates/djangocmsjoy/add_resource_news.html`
- `djangocmsjoy/templates/djangocmsjoy/update_resource_news.html`
- `djangocmsjoy/templates/djangocmsjoy/add_access_news.html`
- `djangocmsjoy/templates/djangocmsjoy/update_access_news.html`

**Features:**
- Bootstrap forms
- Title and content fields (textarea for content)
- External URL field for ACCESS News
- Submit and cancel buttons
- Staff-only access (protected by view decorators)

### Step 3.7: Update Base Navigation Template
**File:** `djangocmsjoy/templates/web/base_nav_full.html`

Added fourth navigation tab:
```html
<ul class="nav nav-tabs">
    <li class="nav-item">
        <a class="nav-link {% if page == 'index' %}active{% endif %}" 
           href="{% url 'djangocmsjoy:index' %}">Operations Portal</a>
    </li>
    <li class="nav-item">
        <a class="nav-link {% if page == 'access_news' %}active{% endif %}" 
           href="{% url 'djangocmsjoy:access_news' %}">ACCESS News</a>
    </li>
    <li class="nav-item">
        <a class="nav-link {% if page == 'system_news' %}active{% endif %}" 
           href="{% url 'djangocmsjoy:system_news' %}">System News</a>
    </li>
    <li class="nav-item">
        <a class="nav-link {% if page == 'resource_news' %}active{% endif %}" 
           href="{% url 'djangocmsjoy:resource_news' %}">Resource News</a>
    </li>
</ul>
```

**Features:**
- Active tab highlighting via `page` variable
- Proper URL namespace usage
- Bootstrap nav-tabs styling

### Step 3.8: Integrate Navigation into Base Template
**File:** `djangocmsjoy/templates/base.html`

Added Operations Portal tabs section:
```html
<div class="container-fluid" style="background: #f8f9fa; border-bottom: 1px solid #dee2e6;">
    <div class="container">
        <ul class="nav nav-tabs" style="border: none; padding-top: 0.5rem;">
            <li class="nav-item">
                <a class="nav-link {% if request.resolver_match.url_name == 'index' %}active{% endif %}" 
                   href="{% url 'djangocmsjoy:index' %}">Operations Portal</a>
            </li>
            <li class="nav-item">
                <a class="nav-link {% if request.resolver_match.url_name == 'access_news' %}active{% endif %}" 
                   href="{% url 'djangocmsjoy:access_news' %}">ACCESS News</a>
            </li>
            <li class="nav-item">
                <a class="nav-link {% if request.resolver_match.url_name == 'system_news' %}active{% endif %}" 
                   href="{% url 'djangocmsjoy:system_news' %}">System News</a>
            </li>
            <li class="nav-item">
                <a class="nav-link {% if request.resolver_match.url_name == 'resource_news' %}active{% endif %}" 
                   href="{% url 'djangocmsjoy:resource_news' %}">Resource News</a>
            </li>
        </ul>
    </div>
</div>
```

**Result:**
- ✅ Operations Portal tabs appear on all pages
- ✅ Active state highlighting works
- ✅ Consistent navigation across site

---

## 4. Universal Menus Integration

### Overview
Added official ACCESS-wide universal navigation dropdown menu from ACCESS CI UI library.

### Step 4.1: Add Universal Menus Container and Script
**File Modified:** `djangocmsjoy/templates/base.html`

#### Added Font Link
```html
<link rel="stylesheet" 
      href="https://fonts.googleapis.com/css2?family=Archivo:ital,wdth,wght@0,70,400;0,100,400;0,100,500;0,100,600;0,100,700;0,100,800;1,100,400&display=swap" 
      media="all">
```

#### Added Container (before header)
```html
<div id="universal-menus"></div>
```

#### Added JavaScript Module (before closing body tag)
```html
<script type="module">
    import { universalMenus } from "https://esm.sh/@access-ci/ui@0.8.0";
    
    universalMenus({
        siteName: "Operations Portal",
        target: document.getElementById("universal-menus"),
    });
</script>
```

### Universal Menu Components
The menu automatically includes:
- **ACCESS Home** - Icon link to access-ci.org
- **Allocations** - Link to allocations.access-ci.org
- **Resources** - Link to resource catalog
- **Events & Trainings** - Link to support site
- **Support** - Link to support.access-ci.org
- **News** - ACCESS news
- **About** - About ACCESS
- **Find info for you** - Dropdown with personas (Researchers, Educators, Graduate Students, Resource Providers, CI Community)
- **Search** - ACCESS-wide search
- **Login/My ACCESS** - Login menu or user dropdown (auto-detects login status via cookies)

### Features
- ✅ Responsive design (mobile hamburger menu, desktop horizontal)
- ✅ Shadow DOM for style isolation
- ✅ Auto-detection of login status
- ✅ Highlights "Operations Portal" as current site
- ✅ Dropdown navigation support
- ✅ Accessibility features built-in

---

## 5. Database Management

### PostgreSQL Configuration
**Database:** djangocmsjoy  
**Host:** localhost  
**Port:** 5432  
**User:** jelambeadmin  

### Django Settings
**File:** `djangocmsjoy/djangocmsjoy/settings.py`

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'djangocmsjoy',
        'USER': 'jelambeadmin',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Migration Commands
```bash
# Create migrations for specific app
uv run python djangocmsjoy/manage.py makemigrations djangocmsjoy

# Apply all pending migrations
uv run python djangocmsjoy/manage.py migrate

# List all migrations and their status
uv run python djangocmsjoy/manage.py showmigrations

# Rollback to specific migration (if needed)
uv run python djangocmsjoy/manage.py migrate djangocmsjoy 0001

# Create empty migration (for data migrations)
uv run python djangocmsjoy/manage.py makemigrations --empty djangocmsjoy
```

### Database Tables Created
```
djangocmsjoy_systemnews
djangocmsjoy_resourcenews
djangocmsjoy_accessnews
```

Each table includes:
- id (primary key)
- title (varchar 200)
- content (text)
- external_url (varchar 500, nullable) - AccessNews only
- author_id (foreign key to auth_user)
- created_at (timestamp with timezone)
- updated_at (timestamp with timezone)
- is_active (boolean)

---

## 6. Static Files Management

### Directory Structure
```
djangocmsjoy/
├── static/                           # Source static files
│   └── djangocmsjoy/
│       ├── style-serviceindex.css
│       ├── fonts/
│       └── img/
│           ├── favicon.ico
│           ├── nsf-logo.png          # 28KB
│           ├── access-logo.svg       # 7KB
│           └── ACCS050322_ACCESS_Brand_Operations-RGB.png
│
└── staticfiles/                      # Collected static files (for serving)
    ├── djangocmsjoy/
    ├── admin/
    ├── cms/
    ├── djangocms_admin_style/
    ├── sortedm2m/
    └── treebeard/
```

### Collect Static Files
```bash
# Collect all static files to staticfiles/
uv run python djangocmsjoy/manage.py collectstatic --noinput

# Clear staticfiles and re-collect
rm -rf djangocmsjoy/staticfiles/*
uv run python djangocmsjoy/manage.py collectstatic --noinput
```

### Django Settings for Static Files
**File:** `djangocmsjoy/djangocmsjoy/settings.py`

```python
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
```

### Using Static Files in Templates
```html
{% load static %}

<link rel="icon" type="image/x-icon" href="{% static 'djangocmsjoy/img/favicon.ico' %}">
<img src="{% static 'djangocmsjoy/img/nsf-logo.png' %}" alt="NSF Logo">
<link rel="stylesheet" href="{% static 'djangocmsjoy/style-serviceindex.css' %}">
```

---

## 7. Development Server

### Start Server
```bash
cd /Users/jelambeadmin/Documents/access-sysops/django-cms-uv
uv run python djangocmsjoy/manage.py runserver
```

**Output:**
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
December 03, 2025 - 14:30:00
Django version 5.2.9, using settings 'djangocmsjoy.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

### Access Points
- **Homepage:** http://127.0.0.1:8000/
- **Admin Panel:** http://127.0.0.1:8000/admin/
- **Operations Portal:** http://127.0.0.1:8000/operations/
- **ACCESS News:** http://127.0.0.1:8000/access-news/
- **System News:** http://127.0.0.1:8000/system-news/
- **Resource News:** http://127.0.0.1:8000/resource-news/

### Server Options
```bash
# Run on different port
uv run python djangocmsjoy/manage.py runserver 8080

# Run on specific IP (allow network access)
uv run python djangocmsjoy/manage.py runserver 0.0.0.0:8000

# Disable auto-reload (for debugging)
uv run python djangocmsjoy/manage.py runserver --noreload
```

### Stop Server
Press `CONTROL-C` in the terminal

### Troubleshooting Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000

# Kill process by PID
kill -9 <PID>

# Or use different port
uv run python djangocmsjoy/manage.py runserver 8001
```

---

## 8. Testing Procedures

### Visual Testing Checklist

#### Header/Footer Integration
- [ ] NSF logo displays in header
- [ ] ACCESS logo displays in header
- [ ] Logo divider appears between logos
- [ ] Logos are responsive (smaller on mobile)
- [ ] Header links work (NSF to nsf.gov, ACCESS to access-ci.org)
- [ ] Footer displays NSF award information
- [ ] All 5 NSF award links work
- [ ] Social media links work (X, YouTube, Facebook, LinkedIn)
- [ ] Persona links work (Researchers, Educators, etc.)
- [ ] Utility links work (Acceptable Use, Code of Conduct, etc.)
- [ ] Footer logos display

#### Universal Menus
- [ ] Universal menu appears at top of page
- [ ] Menu items display correctly
- [ ] Dropdown menus work
- [ ] "Operations Portal" is highlighted as current site
- [ ] Login/logout menu displays
- [ ] Search link works
- [ ] Responsive mobile menu works

#### Navigation System
- [ ] Operations Portal tabs display
- [ ] Active tab is highlighted correctly
- [ ] All four tabs link to correct pages
- [ ] CMS page navigation displays (teal bar)
- [ ] CMS dropdown menus work

#### Operations Portal
- [ ] Landing page displays three overview cards
- [ ] Cards link to correct news sections
- [ ] ACCESS News page loads
- [ ] System News page loads
- [ ] Resource News page loads
- [ ] Empty state messages display (if no content)

#### News Management (Staff Users)
- [ ] "Add" buttons appear for staff users
- [ ] "Edit" buttons appear on news items
- [ ] Add forms work and create news
- [ ] Update forms work and save changes
- [ ] Non-staff users cannot access management URLs
- [ ] Author is auto-set on creation

#### Admin Panel
- [ ] System News appears in admin
- [ ] Resource News appears in admin
- [ ] ACCESS News appears in admin
- [ ] List views show all fields
- [ ] Search works
- [ ] Filters work (active status, date)
- [ ] Can add news via admin
- [ ] Can edit news via admin
- [ ] Timestamps are read-only

#### Responsive Design
- [ ] Mobile view (< 900px) displays correctly
- [ ] Desktop view (≥ 900px) displays correctly
- [ ] Navigation adapts to screen size
- [ ] Footer layout adapts to screen size
- [ ] No horizontal scrolling on mobile

### Database Testing
```bash
# Check database connection
uv run python djangocmsjoy/manage.py dbshell

# Verify tables exist
\dt djangocmsjoy*

# Check table structure
\d djangocmsjoy_systemnews

# Exit dbshell
\q
```

### URL Testing
```bash
# Test all URLs are configured correctly
uv run python djangocmsjoy/manage.py show_urls
```

### Template Testing
```bash
# Check for template syntax errors
uv run python djangocmsjoy/manage.py check --tag templates
```

---

## 9. Project File Structure

```
django-cms-uv/
├── pyproject.toml                    # UV project configuration
├── README.md
├── Dev_Processes_localhost.md        # THIS FILE
├── ACCESS-CI-HEADER-FOOTER-INTEGRATION.md
├── NAVIGATION-SETUP.md
├── headers_footers_etc.txt
├── sqlite_to_postgres.txt
├── django-cms-settingspy.txt
│
└── djangocmsjoy/                     # Django project root
    ├── manage.py
    ├── db.sqlite3
    │
    ├── djangocmsjoy/                 # Django app (main configuration)
    │   ├── __init__.py
    │   ├── settings.py               # Django settings
    │   ├── urls.py                   # Main URL configuration
    │   ├── app_urls.py               # Operations Portal URLs
    │   ├── views.py                  # View functions (12 views)
    │   ├── models.py                 # Data models (3 news models)
    │   ├── admin.py                  # Admin configuration
    │   ├── wsgi.py
    │   ├── asgi.py
    │   └── migrations/
    │       ├── __init__.py
    │       └── 0001_initial.py       # News models migration
    │
    ├── templates/
    │   ├── base.html                 # ACCESS CI base template
    │   ├── page.html                 # CMS page template
    │   ├── feature.html              # CMS feature page template
    │   │
    │   ├── djangocmsjoy/             # Operations Portal templates
    │   │   ├── index.html            # Landing page
    │   │   ├── access_news.html      # ACCESS News listing
    │   │   ├── system_news.html      # System News listing
    │   │   ├── resource_news.html    # Resource News listing
    │   │   ├── add_access_news.html
    │   │   ├── update_access_news.html
    │   │   ├── add_system_news.html
    │   │   ├── update_system_news.html
    │   │   ├── add_resource_news.html
    │   │   └── update_resource_news.html
    │   │
    │   └── web/
    │       ├── base_nav_full.html    # Bootstrap navigation template
    │       ├── base_nav_none.html
    │       ├── bootstrap.html
    │       ├── edit_sorry.html
    │       └── unprivileged.html
    │
    ├── static/                       # Source static files
    │   └── djangocmsjoy/
    │       ├── style-serviceindex.css
    │       ├── fonts/
    │       └── img/
    │           ├── favicon.ico
    │           ├── nsf-logo.png      # 28KB - Downloaded
    │           ├── access-logo.svg   # 7KB - Downloaded
    │           └── ACCS050322_ACCESS_Brand_Operations-RGB.png
    │
    └── staticfiles/                  # Collected static files (556 files)
        ├── djangocmsjoy/
        ├── admin/
        ├── cms/
        ├── djangocms_admin_style/
        ├── sortedm2m/
        └── treebeard/
```

---

## 10. Common Commands Reference

### Project Management
```bash
# Navigate to project
cd /Users/jelambeadmin/Documents/access-sysops/django-cms-uv

# Sync dependencies
uv sync

# Add a package
uv add django-package-name

# Remove a package
uv remove django-package-name
```

### Django Management
```bash
# Start development server
uv run python djangocmsjoy/manage.py runserver

# Create superuser
uv run python djangocmsjoy/manage.py createsuperuser

# Open Django shell
uv run python djangocmsjoy/manage.py shell

# Check for issues
uv run python djangocmsjoy/manage.py check
```

### Database Operations
```bash
# Create migrations
uv run python djangocmsjoy/manage.py makemigrations

# Apply migrations
uv run python djangocmsjoy/manage.py migrate

# Show migration status
uv run python djangocmsjoy/manage.py showmigrations

# Open database shell
uv run python djangocmsjoy/manage.py dbshell
```

### Static Files
```bash
# Collect static files
uv run python djangocmsjoy/manage.py collectstatic --noinput

# Find static file location
uv run python djangocmsjoy/manage.py findstatic djangocmsjoy/img/nsf-logo.png
```

### CMS Management
```bash
# Copy languages from one CMS page to another
uv run python djangocmsjoy/manage.py cms copy-lang

# List CMS pages
uv run python djangocmsjoy/manage.py cms list

# Check CMS installation
uv run python djangocmsjoy/manage.py cms check
```

### Testing
```bash
# Run all tests
uv run python djangocmsjoy/manage.py test

# Run specific app tests
uv run python djangocmsjoy/manage.py test djangocmsjoy

# Check templates
uv run python djangocmsjoy/manage.py check --tag templates
```

### Asset Downloads
```bash
# Download from GitHub (example)
cd djangocmsjoy/static/djangocmsjoy/img/
curl -O https://raw.githubusercontent.com/access-ci-org/access-ci-ui/main/src/images/nsf-logo.png
cd /Users/jelambeadmin/Documents/access-sysops/django-cms-uv
```

---

## Summary of Completed Work

### ✅ ACCESS CI Branding Integration
- Official NSF and ACCESS logos installed
- Header with organizational branding
- Footer with NSF awards, social links, personas
- Responsive design (mobile/desktop)
- CSS variables for ACCESS color palette
- Archivo font family integration

### ✅ Universal Navigation
- ACCESS-wide universal menus (top navigation)
- Auto-detecting login status
- Dropdown navigation support
- Responsive mobile/desktop layouts
- Highlights current site (Operations Portal)

### ✅ Operations Portal System
- Four-section navigation (Operations Portal, ACCESS News, System News, Resource News)
- Three database models for news management
- 12 view functions (4 public, 8 staff-only)
- URL routing with djangocmsjoy: namespace
- Admin panel integration
- Bootstrap-styled templates

### ✅ Template System
- Base template with all ACCESS components
- CMS page templates (page.html, feature.html)
- Operations Portal templates (10 files)
- Navigation tab integration
- Responsive layouts

### ✅ Database
- PostgreSQL 15 integration
- Three news tables created
- Migrations applied successfully
- Admin interface configured

### ✅ Static Files
- Logo assets downloaded and deployed
- 556 static files collected
- Proper Django static file configuration

### ✅ Development Environment
- UV package manager configured
- Python 3.13 environment
- Django 5.2.9 with Django CMS 5.0
- Development server functional

---

## Next Steps for Production

1. **Add Content:**
   - Create news items via admin panel
   - Populate CMS pages
   - Add user accounts

2. **Security:**
   - Update SECRET_KEY in settings
   - Set DEBUG = False
   - Configure ALLOWED_HOSTS
   - Set up HTTPS/SSL

3. **Performance:**
   - Configure caching (Redis/Memcached)
   - Set up CDN for static files
   - Enable database connection pooling
   - Implement pagination for news listings

4. **Deployment:**
   - Configure production web server (Nginx/Apache)
   - Set up WSGI server (Gunicorn/uWSGI)
   - Configure systemd service
   - Set up log rotation

5. **Monitoring:**
   - Set up error tracking (Sentry)
   - Configure logging
   - Set up uptime monitoring
   - Database backup automation

---

**Document Version:** 1.0  
**Last Updated:** December 3, 2025  
**Maintained By:** ACCESS Operations Team

---

## 11. Django CMS Settings Reference

### Documentation Links

#### Django CMS Official Documentation
- **Main docs:** https://docs.django-cms.org/
- **Installation guide:** https://docs.django-cms.org/en/latest/introduction/install.html
- **Required apps:** https://docs.django-cms.org/en/latest/how_to/install.html#required-apps
- **Settings reference:** https://docs.django-cms.org/en/latest/reference/configuration.html

#### Related Package Documentation
- **Sekizai (template blocks):** https://django-sekizai.readthedocs.io/
- **Treebeard (page hierarchy):** https://django-treebeard.readthedocs.io/
- **Django Sites Framework:** https://docs.djangoproject.com/en/stable/ref/contrib/sites/

#### Django Core Documentation
- **Settings overview:** https://docs.djangoproject.com/en/5.2/topics/settings/
- **Database configuration:** https://docs.djangoproject.com/en/5.2/ref/settings/#databases

---

### Settings.py Elements Explained

#### BASE_DIR
**Purpose:** Defines the root directory of your Django project  
**Usage:** Used to construct absolute paths for templates, static files, media, and database  
**CMS Relation:** Critical for locating CMS templates and static assets

#### SECRET_KEY
**Purpose:** Cryptographic key for security features (sessions, cookies, CSRF)  
**Usage:** Must be kept secret in production; randomly generated during project creation  
**CMS Relation:** Required for CMS toolbar authentication and secure page editing

#### DEBUG
**Purpose:** Enables detailed error pages and debug information  
**Usage:** Set to True for development, False for production  
**CMS Relation:** When True, shows detailed CMS errors; when False, shows user-friendly error pages

#### ALLOWED_HOSTS
**Purpose:** List of domain names that this Django site can serve  
**Usage:** Empty list for development; must include your domain in production  
**CMS Relation:** Required for CMS to work properly in production; prevents HTTP Host header attacks

---

### INSTALLED_APPS

**Purpose:** Lists all Django applications that are activated in this project  
**CMS Relation:** Critical for CMS functionality; order matters!

#### `'djangocms_admin_style'`
- Provides styled admin interface for Django CMS
- **Must come BEFORE 'django.contrib.admin'**
- Gives the admin panel a modern, CMS-friendly appearance

#### `'django.contrib.admin'`
- Django's built-in admin interface
- Used by CMS for page management and content editing

#### `'django.contrib.auth'`
- Django's authentication system
- CMS uses this for user permissions and access control

#### `'django.contrib.contenttypes'`
- Framework for generic relations between models
- CMS uses this for plugins and page relationships

#### `'django.contrib.sessions'`
- Session framework for tracking user state
- CMS toolbar relies on sessions to maintain editing state

#### `'django.contrib.messages'`
- Framework for temporary messages (success, error notifications)
- CMS uses this to provide feedback when creating/editing pages

#### `'django.contrib.staticfiles'`
- Manages static files (CSS, JavaScript, images)
- Serves CMS admin styles and toolbar JavaScript

#### `'django.contrib.sites'`
- Manages multiple sites from one Django installation
- **REQUIRED by Django CMS**; CMS pages are associated with specific sites

#### `'cms'`
- Core Django CMS application
- Provides page management, placeholders, and content editing

#### `'menus'`
- Django CMS menu system
- Generates navigation automatically from page structure
- Used by `{% show_menu %}` template tag

#### `'treebeard'`
- Tree structure library
- Powers the hierarchical page structure in CMS (parent/child pages)
- Enables drag-and-drop page organization

#### `'sekizai'`
- Template block manager
- Allows plugins and templates to inject CSS/JS into page head/footer
- Used by `{% render_block "css" %}` and `{% render_block "js" %}` tags

#### `'access_django_user_admin'`
- Custom app for your ACCESS CI project
- Project-specific user administration

#### `'djangocmsjoy'`
- Your main application
- Contains your custom templates, views, and models

---

### MIDDLEWARE

**Purpose:** Components that process requests/responses globally  
**CMS Relation:** Django CMS requires specific middleware for proper operation; order matters!

#### `'django.middleware.security.SecurityMiddleware'`
- Provides security enhancements
- Standard Django middleware

#### `'django.contrib.sessions.middleware.SessionMiddleware'`
- Enables session support
- **Required for CMS toolbar** to maintain editing state

#### `'django.middleware.common.CommonMiddleware'`
- Common Django functionality (URL normalization, etc.)
- Standard middleware

#### `'django.middleware.csrf.CsrfViewMiddleware'`
- CSRF protection for forms
- Protects CMS forms from cross-site request forgery

#### `'django.contrib.auth.middleware.AuthenticationMiddleware'`
- Associates users with requests
- **Required for CMS** to identify logged-in editors

#### `'django.contrib.messages.middleware.MessageMiddleware'`
- Enables messages framework
- CMS uses this for user notifications

#### `'django.middleware.clickjacking.XFrameOptionsMiddleware'`
- Protects against clickjacking attacks
- Standard security middleware

#### `'django.middleware.locale.LocaleMiddleware'`
- Enables language selection based on request
- **Required for multilingual CMS sites**

#### `'cms.middleware.user.CurrentUserMiddleware'`
- Makes current user available to CMS
- **Required for CMS permission system**

#### `'cms.middleware.page.CurrentPageMiddleware'`
- Tracks the current CMS page being viewed
- **Required for CMS page rendering**

#### `'cms.middleware.toolbar.ToolbarMiddleware'`
- Renders the CMS editing toolbar
- **Enables frontend editing functionality**

#### `'cms.middleware.language.LanguageCookieMiddleware'`
- Manages language preferences
- **Required for multilingual CMS functionality**

---

### TEMPLATES

**Purpose:** Configuration for Django's template system  
**CMS Relation:** CMS templates must be properly configured

#### `'DIRS': [BASE_DIR / 'templates']`
- Tells Django where to look for templates
- Your CMS page templates (page.html, feature.html) live here

#### `'APP_DIRS': True`
- Allows Django to look for templates in app directories
- Enables CMS to find its own admin templates

#### Context Processors

**`django.template.context_processors.request`**
- Makes request object available in templates
- **Required by CMS toolbar**

**`django.contrib.auth.context_processors.auth`**
- Adds user and permissions to template context
- Used by CMS for permission checks

**`django.template.context_processors.i18n`**
- Adds internationalization variables
- **Required for multilingual CMS**

**`django.template.context_processors.media`**
- Adds MEDIA_URL to context
- Used for CMS uploaded images

**`django.template.context_processors.csrf`**
- Adds CSRF token
- **Required for CMS forms**

**`sekizai.context_processors.sekizai`**
- Enables Sekizai template blocks
- **Required for `{% render_block %}` tags**

**`cms.context_processors.cms_settings`**
- Adds CMS settings to template context
- Makes CMS configuration available in templates

---

### DATABASES

**Purpose:** Database connection configuration  
**CMS Relation:** Stores all CMS pages, content, and structure

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'djangocmsjoy',
        'USER': 'jelambeadmin',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

#### `'ENGINE': 'django.db.backends.postgresql'`
- Database backend being used
- PostgreSQL recommended for production CMS

#### `'NAME': 'djangocmsjoy'`
- Name of the database
- Contains all CMS tables (cms_page, cms_placeholder, etc.)

#### `'USER', 'PASSWORD', 'HOST', 'PORT'`
- Connection credentials
- Required for connecting to PostgreSQL

---

### INTERNATIONALIZATION

#### `LANGUAGE_CODE = 'en'`
- Default language for the site
- CMS uses this as fallback language

#### `LANGUAGES = [('en', 'English')]`
- List of available languages
- CMS can create translated versions of pages

#### `TIME_ZONE = 'UTC'`
- Timezone for date/time storage
- Used for CMS publish dates

#### `USE_I18N = True`
- Enables Django's internationalization system
- **Required for multilingual CMS**

#### `USE_TZ = True`
- Enables timezone-aware datetimes
- Recommended for CMS

#### `SITE_ID = 1`
- ID of the current site in django.contrib.sites
- **REQUIRED by Django CMS**; pages are associated with this site

---

### Django CMS Specific Settings

#### `CMS_CONFIRM_VERSION4 = True`
- Confirms you understand you're using CMS 4/5
- Required setting to prevent migration errors

#### `CMS_TEMPLATES`
```python
CMS_TEMPLATES = [
    ('page.html', 'Basic Page'),
    ('feature.html', 'Featured Page'),
]
```
- Defines available page templates
- Each tuple is (template_file, human_readable_name)
- When creating pages, you choose from these templates
- Templates must exist in your TEMPLATES['DIRS']

#### `CMS_PERMISSION = False`
- Enables granular page permissions
- When False: simpler permission model (staff can edit all pages)
- When True: complex per-page permission system

#### `CMS_PLACEHOLDER_CONF = {}`
- Configuration for placeholders (editable regions)
- Can define plugins allowed, plugin limits, etc.
- Empty dict means default settings for all placeholders

#### `X_FRAME_OPTIONS = 'SAMEORIGIN'`
- Controls if site can be embedded in iframes
- **Required for CMS frontend editing to work**
- Allows toolbar to function properly

---

### STATIC FILES

#### `STATIC_URL = '/static/'`
- URL prefix for static files
- CMS admin CSS/JS served from here

#### `STATIC_ROOT = BASE_DIR / 'staticfiles'`
- Where collectstatic copies all static files
- For production deployment

#### `STATICFILES_DIRS = [BASE_DIR / 'static']`
- Additional locations for static files
- Your custom CSS (style-serviceindex.css) lives here

#### `MEDIA_URL = '/media/'`
- URL prefix for user-uploaded files
- CMS image uploads accessible here

#### `MEDIA_ROOT = BASE_DIR / 'media'`
- Filesystem location for uploaded files
- CMS stores uploaded images here

---

### Critical Relationships for Django CMS

#### 1. Page Structure
- Sites framework (SITE_ID) → CMS pages belong to sites
- Treebeard → Manages page hierarchy
- CMS_TEMPLATES → Defines what templates pages can use

#### 2. Content Editing
- Auth + Sessions → User authentication for editing
- CMS Middleware → Toolbar and page tracking
- Placeholders → Editable regions defined in templates

#### 3. Navigation
- Menus app → Generates navigation from page tree
- `{% show_menu %}` tag → Renders navigation in templates

#### 4. Frontend Display
- Templates with `{% placeholder %}` tags → Editable regions
- Sekizai → Manages CSS/JS injection
- Static files → Serves admin interface and custom styles

#### 5. Data Storage
- PostgreSQL database → All pages, content, structure
- Media folder → User-uploaded images
- Static folder → CSS, JavaScript, fonts

---

### Common Gotchas

#### 1. App Order Matters
- `djangocms_admin_style` must come **BEFORE** `django.contrib.admin`
- Django CMS won't work without `django.contrib.sites`

#### 2. Middleware Order Matters
- CMS middleware must come **after** auth and session middleware
- Language middleware should come early

#### 3. Required Settings
- `SITE_ID` must be set
- `CMS_CONFIRM_VERSION4` must be True
- `X_FRAME_OPTIONS` must allow SAMEORIGIN

#### 4. Templates
- Must load `{% load cms_tags menu_tags sekizai_tags %}`
- Must include `{% cms_toolbar %}` for editing
- Must include `{% render_block %}` for CSS/JS

---

## 12. Model Refactoring: News Categories Alignment

### Overview
This section documents the complete refactoring process to align the Django CMS Operations Portal news category naming with the existing Drupal portal structure. The refactoring renamed "System News" to "System Status News" and "Resource News" to "Integration News" throughout the entire application.

**Date:** December 3, 2025  
**Reason:** Align with Drupal portal naming conventions (Drupal uses `/integration_news` and infrastructure status patterns)  
**Scope:** Models, views, URLs, templates, navigation, migrations

---

### Step 1: Update Model Classes

**File:** `djangocmsjoy/djangocmsjoy/models.py`

**Changes:**
1. Rename `SystemNews` class to `SystemStatusNews`
2. Rename `ResourceNews` class to `IntegrationNews`
3. Add explicit `db_table` meta option to preserve existing database tables
4. Update `verbose_name` and `verbose_name_plural` for admin panel
5. Update docstrings

**Key Code:**
```python
class SystemStatusNews(models.Model):
    """
    Model for system status news, maintenance schedules, and outage notifications.
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)
    author = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'djangocmsjoy_systemstatusnews'  # Preserve existing table
        verbose_name = 'System Status News'
        verbose_name_plural = 'System Status News'
        ordering = ['-published_date']

class IntegrationNews(models.Model):
    """
    Model for integration news, resource connections, and service deployments.
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)
    author = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'djangocmsjoy_integrationnews'  # Preserve existing table
        verbose_name = 'Integration News'
        verbose_name_plural = 'Integration News'
        ordering = ['-published_date']
```

**Critical: Understanding db_table Meta Option**  

By default, Django generates database table names automatically (e.g., `djangocmsjoy_systemnews`). When you rename a model class (e.g., `SystemNews` → `SystemStatusNews`), Django normally wants to rename the table too, which would cause data loss.

The `db_table` meta option explicitly tells Django: "use this exact table name, regardless of the model class name." This allows us to:
- Rename Python classes without changing database tables
- Preserve all existing data
- Update only the Django ORM metadata (ContentType records)

Without `db_table`, renaming models would require:
1. Creating new tables
2. Migrating all data from old tables to new tables
3. Deleting old tables

With `db_table`, we just update the model name and Django references - no data migration needed.

---

### Step 2: Update Admin Panel Registration

**File:** `djangocmsjoy/djangocmsjoy/admin.py`

**Changes:**
1. Rename `SystemNewsAdmin` to `SystemStatusNewsAdmin`
2. Rename `ResourceNewsAdmin` to `IntegrationNewsAdmin`
3. Update import statements
4. Update admin registration calls

**Code:**
```python
from .models import AccessNews, SystemStatusNews, IntegrationNews

@admin.register(SystemStatusNews)
class SystemStatusNewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'is_active')
    list_filter = ('is_active', 'published_date')
    search_fields = ('title', 'content', 'author')
    date_hierarchy = 'published_date'

@admin.register(IntegrationNews)
class IntegrationNewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'is_active')
    list_filter = ('is_active', 'published_date')
    search_fields = ('title', 'content', 'author')
    date_hierarchy = 'published_date'
```

---

### Step 3: Rename View Functions

**File:** `djangocmsjoy/djangocmsjoy/views.py`

**Changes Made (12 functions total):**

#### Public Views (4 functions):
1. `system_news()` → `system_status_news()`
2. `resource_news()` → `integration_news()`

#### Staff-Only Views (8 functions):
3. `add_system_news()` → `add_system_status_news()`
4. `update_system_news()` → `update_system_status_news()`
5. `delete_system_news()` → `delete_system_status_news()`
6. `toggle_system_news()` → `toggle_system_status_news()`
7. `add_resource_news()` → `add_integration_news()`
8. `update_resource_news()` → `update_integration_news()`
9. `delete_resource_news()` → `delete_integration_news()`
10. `toggle_resource_news()` → `toggle_integration_news()`

**Updates in Each View:**
- Model import: `from .models import SystemStatusNews, IntegrationNews`
- Queryset variables: `system_status_news`, `integration_news`
- Context dictionary keys: `'system_status_news'`, `'integration_news'`
- Template paths: `'djangocmsjoy/system_status_news.html'`, etc.
- Redirect URLs: `'djangocmsjoy:system_status_news'`, `'djangocmsjoy:integration_news'`
- Success messages: Updated text to match new names
- Page context: `context['page'] = 'system_status_news'` or `'integration_news'`

**Example:**
```python
def system_status_news(request):
    """Display all active system status news."""
    system_status_news = SystemStatusNews.objects.filter(is_active=True).order_by('-published_date')
    context = {
        'system_status_news': system_status_news,
        'page': 'system_status_news',
    }
    return render(request, 'djangocmsjoy/system_status_news.html', context)

@staff_member_required
def add_system_status_news(request):
    """Add new system status news (staff only)."""
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        author = request.POST.get('author')
        
        SystemStatusNews.objects.create(
            title=title,
            content=content,
            author=author
        )
        messages.success(request, 'System Status News added successfully!')
        return redirect('djangocmsjoy:system_status_news')
    
    context = {'page': 'system_status_news'}
    return render(request, 'djangocmsjoy/add_system_status_news.html', context)
```

---

### Step 4: Update URL Patterns

**File:** `djangocmsjoy/djangocmsjoy/app_urls.py`

**Changes:**
1. Update URL paths:
   - `/system-news/` → `/system-status-news/`
   - `/resource-news/` → `/integration-news/`

2. Update URL names (used in templates with `{% url %}`):
   - `system_news` → `system_status_news`
   - `resource_news` → `integration_news`
   - All related CRUD operation names updated

3. Update view function references

**Code:**
```python
app_name = 'djangocmsjoy'

urlpatterns = [
    path('', views.operations_index, name='operations_index'),
    path('access-news/', views.access_news, name='access_news'),
    
    # System Status News URLs
    path('system-status-news/', views.system_status_news, name='system_status_news'),
    path('system-status-news/add/', views.add_system_status_news, name='add_system_status_news'),
    path('system-status-news/<int:news_id>/update/', views.update_system_status_news, name='update_system_status_news'),
    path('system-status-news/<int:news_id>/delete/', views.delete_system_status_news, name='delete_system_status_news'),
    path('system-status-news/<int:news_id>/toggle/', views.toggle_system_status_news, name='toggle_system_status_news'),
    
    # Integration News URLs
    path('integration-news/', views.integration_news, name='integration_news'),
    path('integration-news/add/', views.add_integration_news, name='add_integration_news'),
    path('integration-news/<int:news_id>/update/', views.update_integration_news, name='update_integration_news'),
    path('integration-news/<int:news_id>/delete/', views.delete_integration_news, name='delete_integration_news'),
    path('integration-news/<int:news_id>/toggle/', views.toggle_integration_news, name='toggle_integration_news'),
]
```

---

### Step 5: Rename Template Files

**Directory:** `djangocmsjoy/templates/djangocmsjoy/`

**Command:**
```bash
cd djangocmsjoy/templates/djangocmsjoy && \
mv system_news.html system_status_news.html && \
mv resource_news.html integration_news.html && \
mv add_system_news.html add_system_status_news.html && \
mv update_system_news.html update_system_status_news.html && \
mv add_resource_news.html add_integration_news.html && \
mv update_resource_news.html update_integration_news.html
```

**Files Renamed (6 total):**
1. `system_news.html` → `system_status_news.html`
2. `resource_news.html` → `integration_news.html`
3. `add_system_news.html` → `add_system_status_news.html`
4. `update_system_news.html` → `update_system_status_news.html`
5. `add_resource_news.html` → `add_integration_news.html`
6. `update_resource_news.html` → `update_integration_news.html`

---

### Step 6: Update Template Content

**Files Updated:** All 6 renamed templates

**Changes in Each Template:**

#### system_status_news.html
- Page title: "System News" → "System Status News"
- Variable name: `system_news` → `system_status_news`
- URL references: `djangocmsjoy:system_news` → `djangocmsjoy:system_status_news`
- Loop variable: `{% for news in system_status_news %}`

#### integration_news.html
- Page title: "Resource News" → "Integration News"
- Variable name: `resource_news` → `integration_news`
- URL references: `djangocmsjoy:resource_news` → `djangocmsjoy:integration_news`
- Loop variable: `{% for news in integration_news %}`

#### add_system_status_news.html
- Page title: "Add System News" → "Add System Status News"
- Cancel URL: `djangocmsjoy:system_news` → `djangocmsjoy:system_status_news`

#### update_system_status_news.html
- Page title: "Update System News" → "Update System Status News"
- Cancel URL: `djangocmsjoy:system_news` → `djangocmsjoy:system_status_news`

#### add_integration_news.html
- Page title: "Add Resource News" → "Add Integration News"
- Cancel URL: `djangocmsjoy:resource_news` → `djangocmsjoy:integration_news`

#### update_integration_news.html
- Page title: "Update Resource News" → "Update Integration News"
- Cancel URL: `djangocmsjoy:resource_news` → `djangocmsjoy:integration_news`

---

### Step 7: Update Navigation in base.html

**File:** `djangocmsjoy/templates/base.html`

**Changes:**
- Operations Portal tab labels
- URL name checks for active tab highlighting
- URL references in href attributes

**Updated Code:**
```html
<ul class="nav nav-tabs">
    <li class="nav-item">
        <a class="nav-link {% if request.resolver_match.url_name == 'operations_index' %}active{% endif %}" 
           href="{% url 'djangocmsjoy:operations_index' %}">
            Operations Portal
        </a>
    </li>
    <li class="nav-item">
        <a class="nav-link {% if request.resolver_match.url_name == 'access_news' %}active{% endif %}" 
           href="{% url 'djangocmsjoy:access_news' %}">
            ACCESS News
        </a>
    </li>
    <li class="nav-item">
        <a class="nav-link {% if request.resolver_match.url_name == 'system_status_news' %}active{% endif %}" 
           href="{% url 'djangocmsjoy:system_status_news' %}">
            System Status News
        </a>
    </li>
    <li class="nav-item">
        <a class="nav-link {% if request.resolver_match.url_name == 'integration_news' %}active{% endif %}" 
           href="{% url 'djangocmsjoy:integration_news' %}">
            Integration News
        </a>
    </li>
</ul>
```

---

### Step 8: Update Navigation in base_nav_full.html

**File:** `djangocmsjoy/templates/web/base_nav_full.html`

**Changes:**
- Bootstrap navigation tab labels
- Page variable checks for active tab highlighting
- URL references in href attributes

**Updated Code:**
```html
<ul class="nav nav-tabs mb-4">
    <li class="nav-item">
        <a class="nav-link {% if page == 'operations' %}active{% endif %}" 
           href="{% url 'djangocmsjoy:operations_index' %}">
            Operations Portal
        </a>
    </li>
    <li class="nav-item">
        <a class="nav-link {% if page == 'access_news' %}active{% endif %}" 
           href="{% url 'djangocmsjoy:access_news' %}">
            ACCESS News
        </a>
    </li>
    <li class="nav-item">
        <a class="nav-link {% if page == 'system_status_news' %}active{% endif %}" 
           href="{% url 'djangocmsjoy:system_status_news' %}">
            System Status News
        </a>
    </li>
    <li class="nav-item">
        <a class="nav-link {% if page == 'integration_news' %}active{% endif %}" 
           href="{% url 'djangocmsjoy:integration_news' %}">
            Integration News
        </a>
    </li>
</ul>
```

---

### Step 9: Update Landing Page Cards

**File:** `djangocmsjoy/templates/djangocmsjoy/index.html`

**Changes:**
- Card 2: Title "System News" → "System Status News"
- Card 2: URL `djangocmsjoy:system_news` → `djangocmsjoy:system_status_news`
- Card 2: Button text updated
- Card 3: Title "Resource News" → "Integration News"
- Card 3: URL `djangocmsjoy:resource_news` → `djangocmsjoy:integration_news`
- Card 3: Button text updated
- Card 3: Description updated to reflect integration focus

**Updated Code:**
```html
<div class="col-md-4">
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">
                <i class="bi bi-exclamation-triangle"></i> System Status News
            </h5>
            <p class="card-text">
                Check system status, maintenance schedules, and outage notifications.
            </p>
            <a href="{% url 'djangocmsjoy:system_status_news' %}" class="btn btn-warning">
                View System Status News
            </a>
        </div>
    </div>
</div>

<div class="col-md-4">
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">
                <i class="bi bi-hdd-network"></i> Integration News
            </h5>
            <p class="card-text">
                Learn about integrations, resource connections, and new service deployments.
            </p>
            <a href="{% url 'djangocmsjoy:integration_news' %}" class="btn btn-success">
                View Integration News
            </a>
        </div>
    </div>
</div>
```

---

### Step 10: Create Database Migration

**Challenge:** Django's automatic migration detection treated model renames as delete+create operations instead of rename operations.

**Solution:** Manually created migration with `RenameModel` operations.

**Command:**
```bash
# Navigate to project directory
cd /Users/jelambeadmin/Documents/access-sysops/django-cms-uv

# Create manual migration file
touch djangocmsjoy/djangocmsjoy/migrations/0002_rename_news_models.py
```

**File Created:** `djangocmsjoy/djangocmsjoy/migrations/0002_rename_news_models.py`

**Content:**
```python
# Generated migration for renaming news models

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangocmsjoy', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SystemNews',
            new_name='SystemStatusNews',
        ),
        migrations.RenameModel(
            old_name='ResourceNews',
            new_name='IntegrationNews',
        ),
    ]
```

**What This Migration Does:**

Django maintains a `django_content_type` table that tracks all models in your project. This table is used by:
- The admin interface (to display model names)
- The permissions system (to assign model-level permissions)
- Generic foreign keys (to reference any model type)
- Django's internal ORM (to map model names to tables)

The `RenameModel` migration operation:
1. Updates ContentType records: `SystemNews` → `SystemStatusNews`
2. Updates permission records: "Can add system news" → "Can add system status news"
3. Preserves existing database tables (due to `db_table` meta option)
4. Updates admin panel model references (what you see in /admin/)
5. Does NOT rename tables or move data

**Why This Migration is Required:**  
Without this migration, Django would still think the old model names exist, causing:
- Admin panel to show "SystemNews" instead of "SystemStatusNews"
- Permission errors when staff try to manage news items
- ImportError exceptions when Django can't find the old model classes

**Important:** The migration does NOT rename database tables. The `db_table` meta option in the models prevents table renaming, ensuring existing data is preserved.

---

### Step 11: Apply Migration

**Command:**
```bash
uv run python djangocmsjoy/manage.py migrate
```

**What 'migrate' Does:**

The `migrate` command:
1. Checks which migrations have already been applied (stored in `django_migrations` table)
2. Identifies unapplied migrations
3. Runs them in order, executing the SQL commands they generate
4. Records each successful migration in the database
5. Rolls back if any migration fails (transactional safety)

**Output:**
```
Operations to perform:
  Apply all migrations: admin, auth, cms, contenttypes, djangocmsjoy, menus, sessions, sites
Running migrations:
  Applying djangocmsjoy.0002_rename_news_models... OK
```

**Database Changes Made:**
- Updated `django_content_type` table: Changed model names from SystemNews/ResourceNews to SystemStatusNews/IntegrationNews
- Updated `auth_permission` table: Changed permission labels to reflect new model names
- Did NOT rename or modify data tables (djangocmsjoy_systemstatusnews, djangocmsjoy_integrationnews remain unchanged)
- Admin panel now displays "System Status News" and "Integration News"
- All Django ORM references now use new model names

---

### Step 12: Testing

**Test Checklist:**

#### Navigation Testing
```bash
# Start development server
uv run python djangocmsjoy/manage.py runserver

# Test URLs:
# http://localhost:8000/operations/
# http://localhost:8000/operations/access-news/
# http://localhost:8000/operations/system-status-news/
# http://localhost:8000/operations/integration-news/
```

#### Functionality Tests
1. ✅ All four tabs appear correctly in navigation
2. ✅ Active tab highlighting works (correct tab shows as active)
3. ✅ Landing page cards have updated titles and URLs
4. ✅ System Status News page displays correctly
5. ✅ Integration News page displays correctly
6. ✅ Admin panel shows new model names
7. ✅ Add/Edit forms work for staff users
8. ✅ Delete/Toggle operations work
9. ✅ URL routing matches new patterns
10. ✅ No broken links or 404 errors

#### Database Verification
```bash
# Check database tables still exist
uv run python djangocmsjoy/manage.py dbshell
```

```sql
-- Verify tables preserved
\dt djangocmsjoy*

-- Check data preserved
SELECT COUNT(*) FROM djangocmsjoy_systemstatusnews;
SELECT COUNT(*) FROM djangocmsjoy_integrationnews;
SELECT COUNT(*) FROM djangocmsjoy_accessnews;

-- Exit
\q
```

---

### Summary of Changes

**Files Modified:**
1. `djangocmsjoy/djangocmsjoy/models.py` - Model class renames with db_table preservation
2. `djangocmsjoy/djangocmsjoy/admin.py` - Admin class renames and imports
3. `djangocmsjoy/djangocmsjoy/views.py` - 12 view function renames with context updates
4. `djangocmsjoy/djangocmsjoy/app_urls.py` - URL pattern and name updates
5. `djangocmsjoy/templates/base.html` - Navigation tab updates
6. `djangocmsjoy/templates/web/base_nav_full.html` - Bootstrap navigation updates
7. `djangocmsjoy/templates/djangocmsjoy/index.html` - Landing page card updates

**Files Renamed (6 templates):**
1. `system_news.html` → `system_status_news.html`
2. `resource_news.html` → `integration_news.html`
3. `add_system_news.html` → `add_system_status_news.html`
4. `update_system_news.html` → `update_system_status_news.html`
5. `add_resource_news.html` → `add_integration_news.html`
6. `update_resource_news.html` → `update_integration_news.html`

**Files Created:**
- `djangocmsjoy/djangocmsjoy/migrations/0002_rename_news_models.py`

**Database Tables (Preserved):**
- `djangocmsjoy_systemstatusnews` (unchanged)
- `djangocmsjoy_integrationnews` (unchanged)
- `djangocmsjoy_accessnews` (unchanged)

**URL Changes:**
- `/operations/system-news/` → `/operations/system-status-news/`
- `/operations/resource-news/` → `/operations/integration-news/`

**Key Success Factors:**
1. Used `db_table` meta option to preserve existing tables and data
2. Created manual migration with `RenameModel` operations
3. Systematically updated all references across 13+ files
4. Updated both navigation templates (base.html and base_nav_full.html)
5. Tested all functionality before finalizing

**Alignment Achieved:**
- Django CMS now matches Drupal portal naming conventions
- "Integration News" aligns with Drupal's `/integration_news` page
- "System Status News" provides clear infrastructure status focus
- Consistent terminology across ACCESS platforms

---

## 13. Removing AccessNews Model and External Linking

### Overview
This section documents the process of removing the locally-managed AccessNews model and replacing it with external links to the official ACCESS-CI news website. This change consolidates news management by delegating ACCESS-wide news to the official ACCESS-CI platform while maintaining local control over Operations Portal-specific news categories (System Status News and Integration News).

**Date:** December 3, 2025  
**Reason:** Eliminate duplication of effort by linking to official ACCESS-CI news instead of curating local copies  
**Impact:** Reduced maintenance burden, single source of truth for ACCESS news, cleaner codebase  
**Scope:** Models, views, URLs, templates, navigation, database migration

**Architectural Decision:**  
This follows the "Don't Repeat Yourself" (DRY) principle and microservices architecture patterns:
- **Separation of Concerns:** ACCESS-CI communications team manages ACCESS-wide news; Operations team manages infrastructure-specific news
- **Single Source of Truth:** Official ACCESS news lives at access-ci.org/news/ (authoritative source)
- **Domain Boundaries:** Operations Portal focuses on operational status, not community announcements
- **API-First Thinking:** External links effectively "consume" the ACCESS-CI news "service" without duplicating it

This pattern is common in enterprise systems where different teams own different domains.

---

### Step 1: Update Navigation to External Links

Before removing the model and views, update navigation templates to link directly to the external ACCESS-CI news website. This ensures users can still access ACCESS news even during the transition.

#### Update base.html Navigation

**File:** `djangocmsjoy/templates/base.html`

**Original Code:**
```html
<li class="nav-item">
    <a class="nav-link {% if request.resolver_match.url_name == 'access_news' %}active{% endif %}" 
       href="{% url 'djangocmsjoy:access_news' %}">
        ACCESS News
    </a>
</li>
```

**Updated Code:**
```html
<li class="nav-item">
    <a class="nav-link" 
       href="https://access-ci.org/news/" target="_blank">
        ACCESS News <i class="bi bi-box-arrow-up-right"></i>
    </a>
</li>
```

**Changes:**
- Removed active state checking (external links don't need active highlighting)
- Changed href to external URL: `https://access-ci.org/news/`
- Added `target="_blank"` to open in new tab
- Added Bootstrap Icons external link icon for visual indication

---

#### Update base_nav_full.html Navigation

**File:** `djangocmsjoy/templates/web/base_nav_full.html`

**Original Code:**
```html
<li class="nav-item">
{% if page == 'access_news' %}<a class="nav-link active" aria-current="page" href="#">
{% else %}<a class="nav-link" href="{% url 'djangocmsjoy:access_news' %}">
{% endif %}ACCESS News</a></li>
```

**Updated Code:**
```html
<li class="nav-item">
<a class="nav-link" href="https://access-ci.org/news/" target="_blank">
    ACCESS News <i class="bi bi-box-arrow-up-right"></i>
</a></li>
```

**Changes:**
- Removed conditional active state logic
- Simplified to single anchor tag with external URL
- Added external link indicator

---

#### Update index.html Landing Page Card

**File:** `djangocmsjoy/templates/djangocmsjoy/index.html`

**Original Code:**
```html
<a href="{% url 'djangocmsjoy:access_news' %}" class="btn btn-primary">
    View ACCESS News
</a>
```

**Updated Code:**
```html
<a href="https://access-ci.org/news/" target="_blank" class="btn btn-primary">
    View ACCESS News <i class="bi bi-box-arrow-up-right"></i>
</a>
```

**Result:** All navigation now directs users to the official ACCESS-CI news page, which is maintained by the ACCESS communications team with comprehensive coverage of ACCESS-wide announcements, events, and updates.

---

### Step 2: Remove AccessNews Model

**File:** `djangocmsjoy/djangocmsjoy/models.py`

**Removed Code:**
```python
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
```

**Rationale:** 
The AccessNews model duplicated effort by requiring staff to manually curate and enter news items that were already being published on the official ACCESS-CI website. The model had an `external_url` field suggesting it was meant to link to external content anyway, making the local storage redundant. Removing this model:
- Eliminates duplicate data entry
- Reduces maintenance overhead
- Ensures users see the most current ACCESS news from the authoritative source
- Simplifies the codebase

---

### Step 3: Remove AccessNews Admin Registration

**File:** `djangocmsjoy/djangocmsjoy/admin.py`

**Removed Import:**
```python
from .models import SystemStatusNews, IntegrationNews, AccessNews
```

**Updated Import:**
```python
from .models import SystemStatusNews, IntegrationNews
```

**Removed Admin Class:**
```python
@admin.register(AccessNews)
class AccessNewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'external_url', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'content']
    readonly_fields = ['created_at', 'updated_at']
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        super().save_model(request, obj, form, change)
```

**Result:** AccessNews no longer appears in the Django admin panel, preventing staff from attempting to add local news entries.

---

### Step 4: Remove AccessNews View Functions

**File:** `djangocmsjoy/djangocmsjoy/views.py`

**Removed Import:**
```python
from .models import SystemStatusNews, IntegrationNews, AccessNews
```

**Updated Import:**
```python
from .models import SystemStatusNews, IntegrationNews
```

**Removed View Functions (3 total):**

#### 1. access_news() - Public listing view
```python
def access_news(request):
    """ACCESS News listing page"""
    news_items = AccessNews.objects.filter(is_active=True)
    context = {
        'page': 'access_news',
        'access_news': news_items,
    }
    return render(request, 'djangocmsjoy/access_news.html', context)
```

#### 2. add_access_news() - Staff-only add view
```python
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
```

#### 3. update_access_news() - Staff-only edit view
```python
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
```

**Rationale:** With no local AccessNews model, these views serve no purpose. All ACCESS news functionality is now handled by the external ACCESS-CI website.

---

### Step 5: Remove AccessNews URL Patterns

**File:** `djangocmsjoy/djangocmsjoy/app_urls.py`

**Removed URL Patterns:**
```python
# Main navigation page
path('access-news/', views.access_news, name='access_news'),

# ACCESS News management
path('access-news/add/', views.add_access_news, name='add_access_news'),
path('access-news/update/<int:pk>/', views.update_access_news, name='update_access_news'),
```

**Final URL Configuration:**
```python
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
```

**Result:** URLs like `/operations/access-news/` are no longer routed, preventing any attempts to access the old views.

---

### Step 6: Remove AccessNews Template Files

**Directory:** `djangocmsjoy/templates/djangocmsjoy/`

**Command:**
```bash
cd /Users/jelambeadmin/Documents/access-sysops/django-cms-uv/djangocmsjoy/templates/djangocmsjoy && \
rm access_news.html add_access_news.html update_access_news.html
```

**Files Deleted (3 total):**
1. `access_news.html` - Public listing template
2. `add_access_news.html` - Staff form for adding news
3. `update_access_news.html` - Staff form for editing news

**Result:** No orphaned template files remain. Django's template loader will not attempt to render non-existent AccessNews templates.

---

### Step 7: Create Database Migration

**Command:**
```bash
cd /Users/jelambeadmin/Documents/access-sysops/django-cms-uv
uv run python djangocmsjoy/manage.py makemigrations djangocmsjoy --name remove_accessnews_model
```

**Output:**
```
Migrations for 'djangocmsjoy':
  djangocmsjoy/djangocmsjoy/migrations/0003_remove_accessnews_model.py
    ~ Change Meta options on integrationnews
    ~ Change Meta options on systemstatusnews
    ~ Rename table for integrationnews to djangocmsjoy_integrationnews
    ~ Rename table for systemstatusnews to djangocmsjoy_systemstatusnews
    - Delete model AccessNews
```

**Migration File:** `djangocmsjoy/djangocmsjoy/migrations/0003_remove_accessnews_model.py`

**What This Migration Does:**
- Drops the `djangocmsjoy_accessnews` database table
- Removes ContentType record for AccessNews model
- Confirms the explicit `db_table` settings for SystemStatusNews and IntegrationNews (from previous refactoring)
- Updates Meta options for the remaining models

**Important Note: Data Loss Warning**  

This migration will **permanently delete all AccessNews data** from the database. The operation:
- Executes SQL: `DROP TABLE djangocmsjoy_accessnews;`
- Removes the table and all its rows from PostgreSQL
- Cannot be undone (unless you have database backups)
- Cascades to delete any foreign key relationships

**Before Running This Migration:**
1. Verify no critical historical data exists in AccessNews
2. Export data if needed: `uv run python manage.py dumpdata djangocmsjoy.AccessNews > access_news_backup.json`
3. Confirm ACCESS-CI website has all important news items
4. Get stakeholder approval for data deletion

**After Migration:**
- The table will not exist in the database
- Attempting to query AccessNews will raise `ProgrammingError: relation does not exist`
- This is expected and correct behavior

---

### Step 8: Apply Migration

**Command:**
```bash
uv run python djangocmsjoy/manage.py migrate
```

**Output:**
```
Operations to perform:
  Apply all migrations: admin, auth, cms, contenttypes, djangocmsjoy, menus, sessions, sites
Running migrations:
  Applying djangocmsjoy.0003_remove_accessnews_model... OK
```

**Database Changes:**
- Table `djangocmsjoy_accessnews` dropped (if it existed)
- ContentType record removed
- Django admin and ORM no longer reference AccessNews

**Verification:**
```bash
# Check database tables
uv run python djangocmsjoy/manage.py dbshell
```

```sql
-- List remaining djangocmsjoy tables
\dt djangocmsjoy*

-- Should show only:
-- djangocmsjoy_systemstatusnews
-- djangocmsjoy_integrationnews

-- Exit
\q
```

---

### Summary of Changes

**Files Modified:**
1. `djangocmsjoy/djangocmsjoy/models.py` - Removed AccessNews model
2. `djangocmsjoy/djangocmsjoy/admin.py` - Removed AccessNewsAdmin registration
3. `djangocmsjoy/djangocmsjoy/views.py` - Removed 3 view functions (access_news, add_access_news, update_access_news)
4. `djangocmsjoy/djangocmsjoy/app_urls.py` - Removed 3 URL patterns
5. `djangocmsjoy/templates/base.html` - Updated ACCESS News link to external URL
6. `djangocmsjoy/templates/web/base_nav_full.html` - Updated ACCESS News link to external URL
7. `djangocmsjoy/templates/djangocmsjoy/index.html` - Updated ACCESS News card link to external URL

**Files Deleted:**
1. `djangocmsjoy/templates/djangocmsjoy/access_news.html`
2. `djangocmsjoy/templates/djangocmsjoy/add_access_news.html`
3. `djangocmsjoy/templates/djangocmsjoy/update_access_news.html`

**Files Created:**
- `djangocmsjoy/djangocmsjoy/migrations/0003_remove_accessnews_model.py`

**Database Changes:**
- Dropped table: `djangocmsjoy_accessnews`
- Removed ContentType record for AccessNews
- Preserved tables: `djangocmsjoy_systemstatusnews`, `djangocmsjoy_integrationnews`

**Remaining Models:**
- `SystemStatusNews` - For infrastructure status, maintenance, and outages
- `IntegrationNews` - For resource integrations and service deployments

**External Link:**
- ACCESS News: https://access-ci.org/news/

---

### Benefits of This Change

#### 1. Single Source of Truth
The official ACCESS-CI website (https://access-ci.org/news/) is maintained by the ACCESS communications team and serves as the authoritative source for ACCESS-wide announcements. By linking directly to it:
- Users always see the most current news
- No delay between official publication and portal availability
- No risk of outdated or incorrect information in the portal

#### 2. Reduced Maintenance Burden
Removing the AccessNews model eliminates:
- Manual data entry by Operations Portal staff
- Duplicate content management
- Need to monitor ACCESS-CI website for new news to replicate
- Ongoing database storage and backups for redundant data

#### 3. Clearer Separation of Concerns
The Operations Portal now focuses exclusively on operations-specific news:
- **System Status News** - Infrastructure-specific: outages, maintenance, performance
- **Integration News** - Operations-specific: new resource connections, service deployments
- **ACCESS News** - Community-wide: delegated to official ACCESS-CI platform

This separation makes it clear which news items require Operations Portal staff attention versus which are handled by the ACCESS communications team.

#### 4. Improved User Experience
- External link icon clearly indicates users are navigating to the official site
- Links open in new tab, allowing users to return to Operations Portal easily
- Users benefit from ACCESS-CI website's superior news browsing features (search, filtering, archives)

#### 5. Simplified Codebase
Removing unused code improves:
- Maintainability (fewer models to manage)
- Performance (fewer database tables to query)
- Testing (fewer components to test)
- Onboarding (new developers have less to learn)

---

### Testing Checklist

✅ **Navigation Testing:**
- Verify ACCESS News link in Operations Portal tabs opens https://access-ci.org/news/
- Verify link opens in new tab/window
- Verify external link icon appears
- Verify System Status News and Integration News tabs still work

✅ **Landing Page Testing:**
- Verify ACCESS News card links to external site
- Verify System Status News and Integration News cards still work
- Verify all buttons and links are functional

✅ **Admin Panel Testing:**
- Verify AccessNews no longer appears in admin
- Verify SystemStatusNews admin still works
- Verify IntegrationNews admin still works

✅ **Database Testing:**
- Verify `djangocmsjoy_accessnews` table removed
- Verify `djangocmsjoy_systemstatusnews` table exists and has data
- Verify `djangocmsjoy_integrationnews` table exists and has data

✅ **URL Testing:**
- Verify `/operations/access-news/` returns 404 (or redirects if configured)
- Verify `/operations/system-status-news/` works
- Verify `/operations/integration-news/` works

---

### Future Considerations

#### Optional: Add URL Redirect
If bookmarks or external links to `/operations/access-news/` need to be preserved, consider adding a redirect in `urls.py`:

```python
from django.views.generic import RedirectView

urlpatterns = [
    # Redirect old ACCESS News URL to external site
    path('operations/access-news/', 
         RedirectView.as_view(url='https://access-ci.org/news/', permanent=True),
         name='access_news_redirect'),
    # ... other patterns
]
```

This would provide a seamless transition for users with old bookmarks.

#### Optional: RSS Feed Integration
For future enhancement, consider displaying a summary of recent ACCESS news on the Operations Portal landing page by consuming the ACCESS-CI news RSS feed:

```python
import feedparser

def index(request):
    # Fetch recent ACCESS news from RSS feed
    feed = feedparser.parse('https://access-ci.org/news/feed/')
    recent_access_news = feed.entries[:3]  # Get 3 most recent
    
    context = {
        'page': 'index',
        'recent_access_news': recent_access_news,
    }
    return render(request, 'djangocmsjoy/index.html', context)
```

This would provide users with a preview of ACCESS news without requiring local data management.

---

## 14. SQLite to PostgreSQL Migration

### Overview
This section documents the complete migration process from SQLite to PostgreSQL for the Django CMS project.

---

### Step 1: Export Data from SQLite

**Command:**
```bash
uv run python djangocmsjoy/manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission > datadump.json
```

**What it does:**
- Exports all data except contenttypes and permissions (which will be recreated by migrations)
- Uses natural keys for foreign keys and primary keys
- Creates a JSON file with all database content

**Result:**
- Created `datadump.json` (4.7KB with 18 objects)
- Includes users, pages, and CMS content

---

### Step 2: Check PostgreSQL Installation

**Command:**
```bash
which psql
```

**Result:**
- PostgreSQL client found at `/opt/homebrew/bin/psql`
- Confirms PostgreSQL is installed and accessible

---

### Step 3: Start PostgreSQL Service

**Command:**
```bash
brew services start postgresql@15
```

**What it does:**
- Starts PostgreSQL 15 service via Homebrew
- Service runs in background

**Result:**
- Successfully started PostgreSQL 15
- Service will auto-start on system reboot

---

### Step 4: Create PostgreSQL Database

**Command:**
```bash
createdb djangocmsjoy
```

**What it does:**
- Creates a new database named "djangocmsjoy"
- Uses your system user (jelambeadmin) as the owner
- No password required for local development

**Result:**
- Database `djangocmsjoy` created successfully
- Ready for Django connection

---

### Step 5: Update Django Settings

**File:** `djangocmsjoy/djangocmsjoy/settings.py`

**Changed from SQLite:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**Changed to PostgreSQL:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'djangocmsjoy',
        'USER': 'jelambeadmin',
        'PASSWORD': '',  # No password for local development
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

**Note:**
- `psycopg2-binary` package was already in dependencies (required for PostgreSQL)
- No additional packages needed

---

### Step 6: Run Migrations on PostgreSQL

**Command:**
```bash
uv run python djangocmsjoy/manage.py migrate
```

**What it does:**
- Creates all database tables in PostgreSQL
- Applies 63 migrations (Django core + Django CMS + custom apps)
- Sets up database schema

**Result:**
- All tables created successfully
- Database structure matches SQLite version
- Ready to receive data

**Tables created include:**
- Django core: auth_user, django_session, etc.
- Django CMS: cms_page, cms_placeholder, cms_cmsplugin, etc.
- Custom apps: djangocmsjoy_systemnews, djangocmsjoy_resourcenews, djangocmsjoy_accessnews

---

### Step 7: Import Data into PostgreSQL

**Command:**
```bash
uv run python djangocmsjoy/manage.py loaddata datadump.json
```

**What it does:**
- Reads data from JSON file
- Imports all objects into PostgreSQL
- Recreates foreign key relationships

**Result:**
- Installed 18 object(s) from 1 fixture(s)
- All users, pages, and CMS content imported
- Data integrity maintained

---

### Step 8: Verify and Restart Server

**Command:**
```bash
uv run python djangocmsjoy/manage.py runserver
```

**What it does:**
- Starts development server
- Connects to PostgreSQL database
- Verifies everything works

**Result:**
- Application now runs on PostgreSQL
- All previous data intact
- Full functionality preserved

---

### PostgreSQL Service Management

#### Start PostgreSQL
```bash
brew services start postgresql@15
```

#### Stop PostgreSQL
```bash
brew services stop postgresql@15
```

#### Check PostgreSQL Status
```bash
brew services list
```

#### Restart PostgreSQL
```bash
brew services restart postgresql@15
```

---

### Database Access

#### Connect to Database Directly
```bash
psql djangocmsjoy
```

#### Common psql Commands
```sql
-- List all tables
\dt

-- Describe table structure
\d djangocmsjoy_systemnews

-- List databases
\l

-- List users/roles
\du

-- Quit psql
\q
```

#### Run SQL Query from Command Line
```bash
psql djangocmsjoy -c "SELECT COUNT(*) FROM cms_page;"
```

---

### Backup and Restore

#### Backup Database
```bash
# Full database backup
pg_dump djangocmsjoy > backup.sql

# Compressed backup
pg_dump djangocmsjoy | gzip > backup.sql.gz

# Custom format (recommended)
pg_dump -Fc djangocmsjoy > backup.dump
```

#### Restore Database
```bash
# From SQL file
psql djangocmsjoy < backup.sql

# From compressed file
gunzip -c backup.sql.gz | psql djangocmsjoy

# From custom format
pg_restore -d djangocmsjoy backup.dump
```

---

### Additional Notes

#### Old SQLite Database
- The file `db.sqlite3` is still in the project but no longer used
- Keep it as a backup or delete it
- Not connected to Django anymore

#### Data Dump File
- `datadump.json` contains the exported data
- Keep as a backup
- Can be used to restore data if needed

#### Database Connection Requirements
- PostgreSQL service must be running
- Database must exist before running migrations
- User must have proper permissions

#### Performance Considerations
- PostgreSQL is more robust than SQLite for production
- Better concurrent access handling
- Superior performance for complex queries
- Recommended for Django CMS in production

#### Security for Production
- Set a strong password for database user
- Use environment variables for credentials
- Don't commit passwords to version control
- Consider SSL connections for production

#### Migration Troubleshooting

**If migration fails:**
1. Drop and recreate database: `dropdb djangocmsjoy && createdb djangocmsjoy`
2. Run migrations again: `uv run python djangocmsjoy/manage.py migrate`
3. Reload data: `uv run python djangocmsjoy/manage.py loaddata datadump.json`

**If data import fails:**
- Check if all migrations ran successfully
- Verify datadump.json is not corrupted
- Try importing in smaller chunks

**Connection errors:**
- Ensure PostgreSQL is running: `brew services list`
- Check database exists: `psql -l`
- Verify user has access: `psql djangocmsjoy`

---

### Header Restructure Attempt and Reversion (Learning Case)

**Date:** December 3, 2025  
**Context:** Attempted to replicate the exact header structure from the production Drupal Operations Portal at operations.access-ci.org

#### Objective
Match the header layout of the Drupal site, which has:
- Horizontal flexbox layout
- Left side: NSF logo → pipe divider → ACCESS Operations logo
- Right side: Navigation menu (Integration News, System Status News)
- All elements in a single header container

#### Implementation Steps

**Step 1: Downloaded Pipe Divider Logo**
```bash
cd djangocmsjoy/static/djangocmsjoy/img
curl -O https://operations.access-ci.org/themes/contrib/b5_ac_conect/logos/ACCESS-pipe.svg
```
- Successfully downloaded 244-byte SVG file
- Verified file exists: `ls -lh ACCESS-pipe.svg`

**Step 2: Analyzed Drupal Site HTML Structure**
User provided the exact HTML from operations.access-ci.org:
```html
<div class="container d-flex w-100 branding-wrapper">
    <div class="d-flex">
        [NSF logo] [pipe divider] [Operations logo]
    </div>
    <div class="region region-nav-main">
        [Navigation items]
    </div>
</div>
```

**Step 3: Restructured base.html Header**
Modified `/djangocmsjoy/templates/base.html` to replicate Drupal structure:

**Changes made:**
- Replaced vertical stacked layout with horizontal flexbox (`d-flex w-100`)
- Added `branding-wrapper` class (Drupal CSS)
- Created left section with NSF logo, pipe divider, Operations logo
- Moved navigation into header as right-aligned section
- Applied Drupal CSS classes: `region-nav-branding`, `region-nav-main`, `navbar-nav`, `nav-level-0`
- Removed separate navigation tabs section below header

**HTML structure implemented:**
```html
<header class="access-header">
    <div class="container d-flex w-100 branding-wrapper">
        <div class="d-flex">
            <a class="nsf-logo" href="https://www.nsf.gov/">
                <img src="nsf-logo.png">
            </a>
            <div class="logo-divider">
                <img src="ACCESS-pipe.svg">
            </div>
            <div class="region region-nav-branding">
                <a href="/" class="site-logo">
                    <img src="ACCESS-operations.svg">
                </a>
            </div>
        </div>
        <div class="region region-nav-main">
            <nav class="navigation menu--main">
                <ul class="navbar-nav">
                    <li><a href="/integration-news/">Integration News</a></li>
                    <li><a href="/system-status-news/">System Status News</a></li>
                </ul>
            </nav>
        </div>
    </div>
</header>
```

#### Problem Encountered

**Issue:** Design broke completely
- Layout rendered incorrectly
- CSS classes from Drupal (branding-wrapper, region-nav-main, etc.) not defined in Bootstrap 5
- Navigation alignment failed
- Visual hierarchy disrupted
- Overall appearance "messed up"

**Root Cause Analysis:**
1. **CSS Class Mismatch:** Drupal uses custom CSS classes (branding-wrapper, region-nav-branding, region-nav-main) that don't exist in Bootstrap 5 or our custom CSS
2. **Missing Styles:** The Drupal classes have associated styles in the Drupal theme that we don't have
3. **Flexbox Complexity:** The nested flexbox structure requires specific CSS to work properly
4. **Bootstrap Integration:** Mixing Drupal-specific classes with Bootstrap classes caused conflicts
5. **No Custom CSS:** Our project doesn't have the corresponding CSS to support the Drupal class structure

#### Resolution: Reverted to Previous Design

**Command:** Used replace_string_in_file to revert base.html

**Restored structure:**
```html
{# ACCESS CI Header #}
<header class="access-header">
    <div class="container">
        <div class="logo">
            <a href="https://www.nsf.gov" class="nsf">
                <img class="nsf-logo" src="nsf-logo.png">
            </a>
            <div class="divider"></div>
            <a href="/" class="access">
                <img class="access-logo" src="ACCESS-operations.svg">
            </a>
        </div>
    </div>
</header>

{# Operations Portal Navigation Tabs #}
<div class="container-fluid">
    <div class="container">
        <ul class="nav nav-tabs">
            <li class="nav-item">
                <a class="nav-link" href="/system-status-news/">System Status News</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="/integration-news/">Integration News</a>
            </li>
        </ul>
    </div>
</div>
```

**Why this works:**
- Uses standard Bootstrap 5 classes (nav, nav-tabs, nav-item, nav-link)
- Simple vertical stacking (header, then navigation)
- Relies only on our existing custom CSS for `.access-header`, `.logo`, `.divider`
- Clean separation of concerns (branding in header, navigation in separate section)

#### Lessons Learned

**1. CSS Dependencies Matter**
- Can't copy HTML structure without the supporting CSS
- Drupal themes have custom CSS that we don't have in Django project
- Bootstrap classes are not interchangeable with Drupal theme classes

**2. Incremental Changes Are Safer**
- Should have tested the layout in stages
- Could have inspected Drupal CSS to understand what classes do
- Could have created matching CSS first, then changed HTML

**3. Different Frameworks, Different Approaches**
- Drupal uses its own CSS framework/patterns
- Django + Bootstrap 5 has different conventions
- Visual similarity doesn't require identical HTML structure

**4. What Would Have Been Needed for Success**
To replicate Drupal layout exactly, we would need:
- Extract CSS for branding-wrapper, region-nav-branding, region-nav-main classes from Drupal theme
- Add those styles to our custom CSS (`static/djangocmsjoy/style-serviceindex.css`)
- Test responsive behavior at different screen sizes
- Ensure Bootstrap 5 classes don't conflict with Drupal classes
- Possibly refactor our existing `.access-header` styles

**5. Alternative Approach**
Instead of copying Drupal HTML structure:
- Inspect Drupal site visually (spacing, colors, fonts, layout)
- Recreate the visual appearance using Bootstrap 5 components
- Use Bootstrap utilities (d-flex, justify-content-between, align-items-center)
- Write minimal custom CSS only for non-Bootstrap styling
- Test thoroughly before committing changes

**6. When to Match Production Sites**
- **Match visually:** Colors, fonts, spacing, layout feel
- **Don't match structurally:** HTML/CSS implementation details should fit the framework being used
- **Focus on UX:** Users care about appearance and behavior, not HTML structure

#### Current Status
- Header: Reverted to working design with NSF logo | divider | Operations logo
- Navigation: Separate tabs section below header (Bootstrap nav-tabs)
- Styling: Stable and functional with existing custom CSS
- Pipe divider: Downloaded and available at `/static/djangocmsjoy/img/ACCESS-pipe.svg` (not currently used but ready if needed)

#### Future Considerations
If we want to match Drupal layout more closely:
1. Use browser dev tools to inspect Drupal CSS
2. Extract relevant styles for branding-wrapper, region-nav-main, etc.
3. Add those styles to our custom CSS file
4. Test layout changes in isolation
5. Consider using Bootstrap's flexbox utilities instead of Drupal classes
6. Validate responsive design at mobile, tablet, desktop sizes

**Conclusion:** Sometimes the simplest solution (separate header and navigation sections with standard Bootstrap components) is better than trying to replicate complex framework-specific structures. Visual similarity can be achieved without identical HTML/CSS implementation.

---

## 15. Template Tag and Static File Troubleshooting

**Date:** December 3, 2025  
**Context:** After removing invalid template tags and fixing static file paths, encountered a series of cascading template errors

### Problem Summary

After implementing CMS news feed plugins and attempting to clean up template dependencies, multiple template errors appeared:
1. Non-existent template tag libraries
2. Invalid template filters
3. Missing URL namespaces
4. Broken static file paths
5. Missing universal menus and improperly sized logos

### Error Resolution Process

#### Issue 1: Invalid Template Tag Library - `get_settings`

**Error:**
```
TemplateSyntaxError: 'get_settings' is not a registered tag library
```

**Root Cause:**
- Template `base_nav_full.html` was loading `{% load get_settings %}` 
- This tag library doesn't exist in the project
- Likely left over from a previous project or copied template

**Files Affected:**
- `djangocmsjoy/templates/web/base_nav_full.html`
- `djangocmsjoy/templates/web/bootstrap.html`
- `djangocmsjoy/templates/web/base_nav_none.html`
- `djangocmsjoy/templates/web/unprivileged.html`

**Solution:**
Removed `{% load get_settings %}` from all affected templates:

```python
# BEFORE
{% load static %}
{% load get_settings %}

# AFTER
{% load static %}
```

**Commands:**
```bash
# Search for all occurrences
grep -r "get_settings" djangocmsjoy/templates/
```

---

#### Issue 2: Invalid Template Filter - `can_admin_users`

**Error:**
```
TemplateSyntaxError: Invalid filter: 'can_admin_users'
```

**Root Cause:**
- Template `base_nav_full.html` used `{% if request.user|can_admin_users %}`
- This custom filter doesn't exist in the project
- Appears to be from `access_django_user_admin` app which has external dependencies

**File Affected:**
- `djangocmsjoy/templates/web/base_nav_full.html`

**Solution:**
Replaced custom filter with standard Django `is_staff` attribute:

```html
<!-- BEFORE -->
{% if request.user|can_admin_users and APP_NAME == 'Service Index' %}
    <li class="nav-item">
        <a class="nav-link" href="{% url 'access_django_user_admin:index' %}">Django User Admin</a>
    </li>
{% endif %}

<!-- AFTER -->
{% if request.user.is_staff %}
    <li class="nav-item">
        <a class="nav-link" href="{% url 'access_django_user_admin:index' %}">Django User Admin</a>
    </li>
{% endif %}
```

---

#### Issue 3: Template Tag Using Non-Existent Settings

**Error:**
```
TemplateSyntaxError: Invalid block tag on line 30: 'settings_value'
```

**Root Cause:**
- Template `bootstrap.html` used `{% settings_value "APP_NAME" %}` and `{% settings_value "APP_VERSION" %}`
- These template tags don't exist in the project
- Related to the removed `get_settings` tag library

**File Affected:**
- `djangocmsjoy/templates/web/bootstrap.html`

**Solution:**
Replaced template tags with hardcoded values:

```html
<!-- BEFORE -->
<h2 class="display-6 fw-bold">{% settings_value "APP_NAME" %}</h2>
<a href="...">{% settings_value "APP_VERSION" %}</a>

<!-- AFTER -->
<h2 class="display-6 fw-bold">ACCESS Operations Portal</h2>
<a href="...">v1.0</a>
```

---

#### Issue 4: Missing URL Namespace - `access_django_user_admin`

**Error:**
```
NoReverseMatch: 'access_django_user_admin' is not a registered namespace
```

**Root Cause:**
- Template referenced `{% url 'access_django_user_admin:index' %}`
- The `access_django_user_admin` app is in INSTALLED_APPS but URLs not included
- App has dependency on `django-allauth` which isn't configured
- Attempting to include URLs caused server crash due to missing allauth dependencies

**Files Affected:**
- `djangocmsjoy/templates/web/base_nav_full.html`
- `djangocmsjoy/djangocmsjoy/urls.py`

**Investigation Steps:**
```bash
# Found the installed package
uv run python -c "import access_django_user_admin; print(access_django_user_admin.__file__)"
# Output: .venv/lib/python3.12/site-packages/access_django_user_admin/__init__.py

# Checked package contents
ls -la .venv/lib/python3.12/site-packages/access_django_user_admin/
# Found: urls.py exists with app_name = 'access_django_user_admin'

# Attempted to include URLs - caused crash
# views.py imports: from allauth.socialaccount.models import SocialAccount
```

**Attempted Solution (Failed):**
```python
# djangocmsjoy/urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('access-django-user-admin/', include('access_django_user_admin.urls')),  # FAILED
    path('', include('djangocmsjoy.app_urls')),
    path('', include('cms.urls')),
]
```

**Error Result:**
```
RuntimeError: Model class allauth.account.models.EmailAddress doesn't declare 
an explicit app_label and isn't in an application in INSTALLED_APPS.
```

**Final Solution:**
Removed the navigation link entirely since the app requires unconfigured dependencies:

```html
<!-- REMOVED from base_nav_full.html -->
{% if request.user.is_staff %}
    <li class="nav-item">
        <a class="nav-link" href="{% url 'access_django_user_admin:index' %}">Django User Admin</a>
    </li>
{% endif %}
```

**URLs remained unchanged:**
```python
# djangocmsjoy/urls.py - Final state
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('djangocmsjoy.app_urls')),
    path('', include('cms.urls')),
]
```

---

#### Issue 5: Broken Static File Paths

**Error (in browser console/terminal):**
```
[03/Dec/2025 21:14:56] "GET /static/services/style-serviceindex.css HTTP/1.1" 404 2020
[03/Dec/2025 21:14:56] "GET /static/services/img/ACCS050322_ACCESS_Brand_Operations-RGB.png HTTP/1.1" 404 2092
```

**Root Cause:**
- Template `bootstrap.html` referenced `/static/services/` paths
- Static files are actually in `/static/djangocmsjoy/` directory
- Caused missing CSS and broken images

**File Affected:**
- `djangocmsjoy/templates/web/bootstrap.html`

**Solution:**
Updated all static file paths to use correct directory:

```html
<!-- BEFORE -->
<link type="text/css" href="{% static 'services/style-serviceindex.css' %}" rel="stylesheet" />
<img src="/static/services/img/ACCS050322_ACCESS_Brand_Operations-RGB.png" alt="Home">

<!-- AFTER -->
<link type="text/css" href="{% static 'djangocmsjoy/style-serviceindex.css' %}" rel="stylesheet" />
<img src="{% static 'djangocmsjoy/img/ACCS050322_ACCESS_Brand_Operations-RGB.png' %}" alt="Home">
```

**Note:** Also changed from hardcoded `/static/` paths to `{% static %}` template tag for proper static file resolution.

---

#### Issue 6: Missing Universal Menus and Tiny Logos

**Problem:**
After fixing template errors, pages loaded but:
- ACCESS universal navigation menus at top were missing
- NSF and ACCESS Operations logos were tiny (mobile size on desktop)
- Favicon not appearing in browser tab

**Root Cause:**
Template `bootstrap.html` was missing:
1. Universal menus `<div>` container and loading script
2. Responsive CSS media queries for logo sizing
3. Google Archivo font (required for ACCESS branding)
4. Favicon link tag

**File Affected:**
- `djangocmsjoy/templates/web/bootstrap.html`

**Solution - Part 1: Added Universal Menus**

Added container div in header block:
```html
{% block serviceindex_global_header %}
{# ACCESS Universal Navigation #}
<div id="universal-menus"></div>

<header class="access-header">
    <!-- header content -->
</header>
{% endblock %}
```

Added loading script at end of page:
```html
{% block bootstrap5_extra_script %}
    <script src="https://code.jquery.com/jquery-3.6.1.min.js" ...></script>
    <script src="https://code.jquery.com/ui/1.13.2/jquery-ui.min.js" ...></script>
    
    {# ACCESS Universal Menus Script #}
    <script type="module">
        import { universalMenus } from "https://esm.sh/@access-ci/ui@0.8.0";
        
        universalMenus({
            siteName: "Operations Portal",
            target: document.getElementById("universal-menus"),
        });
    </script>
    
    {% block page_extra_scripts %}{% endblock %}
{% endblock %}
```

**Solution - Part 2: Added Responsive Logo Sizing**

Added CSS with media queries for proper sizing:
```css
<style media="screen" type="text/css">
    .access-header .container {
        box-sizing: content-box;
        height: 84px;
        padding-top: 20px;
    }
    
    .nsf-logo {
        height: 49px;  /* Small screen size */
    }
    
    .access-logo {
        height: 23px;  /* Small screen size */
        margin-top: 12px;
    }
    
    .logo .divider {
        border-right: 2px solid #bbbbbb;
        height: 40px;
        margin: 4px 15px 0 12px;
        width: 0;
    }
    
    /* Desktop sizes */
    @media (min-width: 900px) {
        .access-header .container {
            height: 144px;
            padding-top: 52px;
        }
        
        .nsf-logo {
            height: 82px;  /* Large screen size */
        }
        
        .access-logo {
            height: auto;
            margin-top: 22px;
            width: 253px;  /* Large screen size */
        }
        
        .logo .divider {
            height: 70px;
            margin: 6px 23px 0 20px;
        }
    }
</style>
```

**Solution - Part 3: Added Required Fonts and Favicon**

```html
{% block bootstrap5_extra_head %}
    <link rel="icon" type="image/x-icon" href="{% static 'djangocmsjoy/img/favicon.ico' %}">
    <link type="text/css" href="//code.jquery.com/ui/1.13.2/themes/smoothness/jquery-ui.css" rel="stylesheet" />
    <link type="text/css" href="{% static 'djangocmsjoy/style-serviceindex.css' %}" rel="stylesheet" />
    <link rel="stylesheet" 
          href="https://fonts.googleapis.com/css2?family=Archivo:ital,wdth,wght@0,70,400;0,100,400;0,100,500;0,100,600;0,100,700;0,100,800;1,100,400&display=swap" 
          media="all">
{% endblock %}
```

---

### Key Lessons Learned

#### 1. Template Inheritance Chain Matters
- `system_status_news.html` extends `base_nav_full.html`
- `base_nav_full.html` extends `bootstrap.html`
- `bootstrap.html` extends `django_bootstrap5/bootstrap5.html`
- Errors in parent templates cascade to all children

#### 2. Package Dependencies
- Just because a package is in INSTALLED_APPS doesn't mean it's fully usable
- `access_django_user_admin` requires `django-allauth` configuration
- Check package imports before including URLs
- External dependencies can cause silent failures

#### 3. Static File Path Conventions
- Use `{% static 'app_name/path' %}` template tag, not hardcoded `/static/`
- Ensures proper static file resolution in all environments
- Makes paths work with STATIC_URL settings changes

#### 4. Template Tag Libraries
- Always verify custom template tags exist before using `{% load %}`
- Standard Django tags: `static`, `i18n`, `l10n`, `tz`, `cache`
- Django CMS tags: `cms_tags`, `menu_tags`, `sekizai_tags`
- Check package documentation for custom tag libraries

#### 5. Responsive Design Requirements
- Always include mobile and desktop CSS
- Use media queries for different screen sizes
- Test at multiple viewport widths
- ACCESS branding requires specific sizing at different breakpoints

#### 6. Debugging Template Errors
**Process:**
1. Read the full error traceback carefully
2. Identify the template file causing the error
3. Check template inheritance chain
4. Verify all `{% load %}` statements are valid
5. Search codebase for similar usage patterns
6. Test fixes by restarting server (clears template cache)

**Useful commands:**
```bash
# Find all templates loading a specific tag library
grep -r "{% load tag_name %}" djangocmsjoy/templates/

# Find all usages of a template tag
grep -r "{% tag_name" djangocmsjoy/templates/

# Find all static file references
grep -r "{% static" djangocmsjoy/templates/

# Check what's in a package
ls -la .venv/lib/python3.12/site-packages/package_name/

# Test if package can be imported
uv run python -c "import package_name; print(package_name.__file__)"
```

---

### Testing Checklist After Template Changes

- [ ] Server starts without errors
- [ ] Home page loads (`http://localhost:8000/`)
- [ ] All navigation links work
- [ ] Static files load (check browser console for 404s)
- [ ] Universal menus appear at top
- [ ] Logos are properly sized on desktop
- [ ] Logos are properly sized on mobile (resize browser)
- [ ] Favicon appears in browser tab
- [ ] No template syntax errors in logs
- [ ] All URL reversals work (no NoReverseMatch errors)
- [ ] CSS styling loads correctly
- [ ] JavaScript loads without console errors

---

### Final Working Configuration

**Templates Structure:**
```
djangocmsjoy/templates/
├── base.html                           # CMS pages (with full ACCESS branding)
├── web/
│   ├── bootstrap.html                  # Base for news pages (with universal menus)
│   ├── base_nav_full.html             # News pages with navigation tabs
│   ├── base_nav_none.html             # Minimal wrapper
│   └── unprivileged.html              # Error page
└── djangocmsjoy/
    ├── index.html                      # Operations Portal landing
    ├── system_status_news.html         # System news listing
    ├── integration_news.html           # Integration news listing
    └── plugins/                        # CMS plugin templates
```

**Static Files Structure:**
```
djangocmsjoy/static/djangocmsjoy/
├── style-serviceindex.css
├── img/
│   ├── nsf-logo.png                    # NSF logo (82px height desktop)
│   ├── ACCESS-operations.svg            # Operations logo (253px width desktop)
│   ├── access-logo.svg                  # Standard ACCESS logo
│   ├── favicon.ico                      # Browser tab icon
│   └── ACCS050322_ACCESS_Brand_Operations-RGB.png
└── fonts/
```

**URLs Configuration:**
```python
# djangocmsjoy/urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('djangocmsjoy.app_urls')),  # News views
    path('', include('cms.urls')),               # CMS catch-all (keep last)
]
```

**INSTALLED_APPS (relevant for templates):**
```python
INSTALLED_APPS = [
    'djangocms_admin_style',
    'django.contrib.admin',
    # ... other django apps ...
    'cms',
    'menus',
    'treebeard',
    'sekizai',
    'django_bootstrap5',            # Bootstrap 5 template tags
    'djangocmsjoy',
]
```

---

### Prevention Strategies

1. **Before removing or changing template tags:**
   - Search entire codebase for usage
   - Check all templates in inheritance chain
   - Test in development before committing

2. **When adding external packages:**
   - Review package dependencies first
   - Check if package requires additional configuration
   - Test package imports before adding to INSTALLED_APPS
   - Verify URLs don't have dependency conflicts

3. **For static files:**
   - Always use `{% static %}` template tag
   - Never hardcode `/static/` paths
   - Keep consistent directory structure
   - Document where assets are located

4. **Documentation:**
   - Record all template tag libraries in use
   - Document external package requirements
   - Note any custom filters or tags
   - Keep this troubleshooting guide updated

---

## 16. Design Integration: Bootstrap, ACCESS Branding, and Theming

**Date:** December 4, 2025  
**Context:** Comprehensive overview of how Bootstrap 5, ACCESS branding elements, and custom theming were integrated into the Django CMS project

### Overview

This Django CMS project uses a layered design approach combining:
1. **Bootstrap 5** - Core responsive framework
2. **django-bootstrap5** - Django integration package
3. **ACCESS CI Branding** - Official ACCESS design elements
4. **Custom CSS** - Project-specific styling

### Bootstrap 5 Integration

#### Package Installation

**Already installed in this project** (present in `pyproject.toml`):
```toml
[project]
dependencies = [
    "django-bootstrap5>=25.0",
    # ... other dependencies
]
```

**If starting a new project, you would install with:**
```bash
uv add django-bootstrap5
```

**Purpose:** Provides Django template tags for Bootstrap 5 components, forms, and utilities.

#### Configuration in settings.py
```python
INSTALLED_APPS = [
    # ... other apps ...
    'django_bootstrap5',  # Must be before custom apps to allow overrides
    'djangocmsjoy',
]
```

#### Base Template Structure

**File:** `djangocmsjoy/templates/web/bootstrap.html`

This template extends `django_bootstrap5/bootstrap5.html` which provides:
- Proper HTML5 doctype
- Bootstrap 5 CSS from CDN
- Bootstrap 5 JavaScript bundle
- Responsive viewport meta tag
- jQuery integration

**Key Template Blocks:**
```django
{% extends 'django_bootstrap5/bootstrap5.html' %}

{% block bootstrap5_title %}
    {# Sets the <title> tag #}
{% endblock %}

{% block bootstrap5_extra_head %}
    {# Additional <head> content: fonts, custom CSS, favicon #}
{% endblock %}

{% block bootstrap5_content %}
    {# Main page content #}
{% endblock %}

{% block bootstrap5_extra_script %}
    {# JavaScript at end of <body> #}
{% endblock %}
```

#### django-bootstrap5 Template Tags

**Available in templates after:**
```django
{% load django_bootstrap5 %}
```

**Common tags used:**
- `{% bootstrap_css %}` - Includes Bootstrap CSS
- `{% bootstrap_javascript %}` - Includes Bootstrap JS bundle
- `{% bootstrap_messages %}` - Renders Django messages as Bootstrap alerts
- `{% bootstrap_form %}` - Renders forms with Bootstrap styling
- `{% bootstrap_button %}` - Creates Bootstrap-styled buttons

### ACCESS Branding Elements

ACCESS branding is implemented through multiple components to match the official ACCESS CI design system.

#### 1. ACCESS Universal Navigation Menus

**Package:** `@access-ci/ui` (version 0.8.0)  
**Delivery:** ES Module via CDN  
**Purpose:** Provides consistent navigation across all ACCESS applications

**Implementation in bootstrap.html:**
```html
{# Container for universal menus #}
<div id="universal-menus"></div>

{# Loading script #}
<script type="module">
    import { universalMenus } from "https://esm.sh/@access-ci/ui@0.8.0";
    
    universalMenus({
        siteName: "Operations Portal",
        target: document.getElementById("universal-menus"),
    });
</script>
```

**What it provides:**
- Top navigation bar with ACCESS logo
- Links to ACCESS support, documentation, allocations
- User login/profile menu (when authenticated)
- Consistent header across all ACCESS services
- Responsive mobile menu

#### 2. ACCESS Typography

**Font:** Archivo (Google Fonts)  
**Loaded in bootstrap.html:**
```html
<link rel="stylesheet" 
      href="https://fonts.googleapis.com/css2?family=Archivo:ital,wdth,wght@0,70,400;0,100,400;0,100,500;0,100,600;0,100,700;0,100,800;1,100,400&display=swap" 
      media="all">
```

**Font weights used:**
- 400 (normal) - Body text
- 500 (medium) - Emphasized text
- 600 (semi-bold) - Subheadings
- 700 (bold) - Headings, buttons
- 800 (extra-bold) - Large headings

**Applied in style-serviceindex.css:**
```css
body {
   font: normal 14px Archivo, Verdana, Helvetica;
   color: #333;
   background-color: #fff;
}
```

#### 3. ACCESS Color Palette

**Defined in style-serviceindex.css as CSS variables:**

```css
:root {
    --bs-dark: #1A5B6E;           /* ACCESS Teal Dark */
    --bs-dark-rgb: 26, 91, 110;
    
    --bs-light: #ECF9F8;          /* ACCESS Teal Light */
    --bs-light-rgb: 236, 249, 248;
    
    --bs-primary: #FFC42D;        /* ACCESS Yellow */
    --bs-primary-rgb: 255, 196, 45;
    
    --bs-secondary: #138597;      /* ACCESS Teal Medium */
    --bs-secondary-rgb: 19, 133, 151;
}
```

**Helper classes:**
```css
.bg-access-dark {
    background-color: #1A5B6E;    /* Used for headers, emphasis */
}

.bg-access-medium {
    background-color: #138597;    /* Used for secondary elements */
}

.bg-access-light {
    background-color: #ECF9F8;    /* Used for backgrounds, panels */
}
```

**Button styling (ACCESS standard):**
```css
.btn-access-auth {
    font-family: Archivo;
    font-size: 14px;
    font-weight: 700;
    color: #000;
    background-color: #fec42d;    /* ACCESS Yellow */
    border-color: #fec42d;
    border-radius: 0;             /* Square corners per ACCESS design */
    border-width: 4px;
    padding: 8px;
}

.btn-access-auth:hover {
    background-color: #fff;
    border-color: #000;
}
```

#### 4. ACCESS Logos and Brand Assets

**Location:** `djangocmsjoy/static/djangocmsjoy/img/`

**NSF Logo:**
- File: `nsf-logo.png`
- Usage: Required on all NSF-funded project pages
- Desktop size: 82px height
- Mobile size: 49px height
- Position: Left side of header

**ACCESS Operations Logo:**
- File: `ACCESS-operations.svg`
- Usage: Primary branding for Operations Portal
- Desktop size: 253px width
- Mobile size: 23px height
- Position: Right of NSF logo (after divider)

**Standard ACCESS Logo:**
- File: `access-logo.svg`
- Usage: Alternative branding option
- Scalable vector graphic

**Favicon:**
- File: `favicon.ico`
- Usage: Browser tab icon
- Size: 16x16, 32x32, 48x48 (multi-resolution)

#### 5. Header Structure with Responsive Logos

**Implemented in bootstrap.html:**

```html
<style media="screen" type="text/css">
    .access-header {
        background-color: white;
        border-bottom: 1px solid #dee2e6;
    }
    
    .access-header .container {
        box-sizing: content-box;
        height: 84px;        /* Mobile height */
        padding-top: 20px;
    }
    
    .logo {
        align-items: start;
        display: flex;
        flex-direction: row;
    }
    
    /* Mobile/small screen sizes */
    .nsf-logo {
        height: 49px;
    }
    
    .access-logo {
        height: 23px;
        margin-top: 12px;
    }
    
    .logo .divider {
        border-right: 2px solid #bbbbbb;
        height: 40px;
        margin: 4px 15px 0 12px;
        width: 0;
    }
    
    /* Desktop sizes - 900px and above */
    @media (min-width: 900px) {
        .access-header .container {
            height: 144px;      /* Desktop height */
            padding-top: 52px;
        }
        
        .nsf-logo {
            height: 82px;       /* Larger on desktop */
        }
        
        .access-logo {
            height: auto;
            margin-top: 22px;
            width: 253px;       /* Fixed width on desktop */
        }
        
        .logo .divider {
            height: 70px;       /* Taller divider on desktop */
            margin: 6px 23px 0 20px;
        }
    }
</style>

{# Header HTML structure #}
<div id="universal-menus"></div>

<header class="access-header">
    <div class="container">
        <div class="logo">
            <a href="https://www.nsf.gov" target="_blank" rel="noopener">
                <img class="nsf-logo" 
                     src="{% static 'djangocmsjoy/img/nsf-logo.png' %}" 
                     alt="NSF Logo">
            </a>
            <div class="divider"></div>
            <a href="/">
                <img class="access-logo" 
                     src="{% static 'djangocmsjoy/img/ACCESS-operations.svg' %}" 
                     alt="ACCESS Operations Portal">
            </a>
        </div>
    </div>
</header>
```

**Responsive behavior:**
- **< 900px (mobile/tablet):** Smaller logos, compact header (84px)
- **≥ 900px (desktop):** Larger logos, spacious header (144px)
- **Flexbox layout:** Ensures logos stay aligned
- **Divider:** Visual separator matches header height

### Custom CSS Integration

**File:** `djangocmsjoy/static/djangocmsjoy/style-serviceindex.css`

#### Typography Hierarchy

```css
h1 {
    font-size: 36px;
    color: #333;
}

h2 {
    font-size: 24px;
    color: #333;
}

h3 {
    font-size: 20px;
    color: #333;
}

h4 {
    font-size: 18px;
    color: #333;
}

h5 {
    font-size: 16px;
    color: #333;
}

.access-intro {
    font-size: 24px;   /* For introductory paragraphs */
}

.access-paragraph {
    font-size: 18px;   /* For emphasized content */
}
```

#### Body Styling

```css
body {
   font: normal 14px Archivo, Verdana, Helvetica;
   color: #333;              /* Readable dark gray */
   background-color: #fff;   /* Clean white background */
}
```

**Why #333 instead of #000:**
- Softer on eyes than pure black
- Better readability for long-form content
- Matches modern web design standards
- Maintains sufficient contrast (WCAG AA compliant)

#### Bootstrap Component Overrides

**Card headers:**
```css
.card > .card-header {
    color: #31708f;
    background-color: #d9edf7;
    border-color: #bce8f1;
}
```

**Navigation pills:**
```css
.nav-pills li {
    color: #428bca !important;
}

.nav-pills a:hover {
    color: #000000 !important;
}

.nav-pills > li.active {
    background-color: #428bca !important;
}

.nav-pills > li.active > a {
    color: #fff;
    text-decoration: none;
}
```

### Template Inheritance Chain

Understanding how templates stack provides complete theming:

```
django_bootstrap5/bootstrap5.html (from package)
    ↓ extends
web/bootstrap.html (custom, adds ACCESS elements)
    ↓ extends
web/base_nav_full.html (adds navigation tabs)
    ↓ extends
djangocmsjoy/system_status_news.html (page content)
```

**Each level adds:**

1. **bootstrap5.html** (django-bootstrap5 package)
   - HTML5 doctype
   - Bootstrap CSS from CDN
   - Bootstrap JavaScript
   - Responsive meta tags
   - Basic structure

2. **web/bootstrap.html** (custom)
   - Favicon
   - Google Fonts (Archivo)
   - Custom CSS (style-serviceindex.css)
   - jQuery and jQuery UI
   - ACCESS universal menus script
   - Header with NSF and ACCESS logos
   - Responsive logo sizing

3. **web/base_nav_full.html** (custom)
   - Navigation tabs (System Status News, Integration News)
   - Bootstrap message display
   - Content container

4. **Page templates** (system_status_news.html, etc.)
   - Page-specific content
   - News item listings
   - Forms, tables, etc.

### Static Files Management

#### Directory Structure

```
djangocmsjoy/
├── static/djangocmsjoy/          # Source files (version controlled)
│   ├── style-serviceindex.css
│   ├── img/
│   │   ├── nsf-logo.png
│   │   ├── ACCESS-operations.svg
│   │   ├── access-logo.svg
│   │   └── favicon.ico
│   └── fonts/
└── staticfiles/                   # Collected files (not version controlled)
    └── djangocmsjoy/
        └── [mirrored structure]
```

#### Collecting Static Files

**Command:**
```bash
uv run python djangocmsjoy/manage.py collectstatic --noinput
```

**What it does:**
1. Gathers all static files from installed apps
2. Copies to `STATIC_ROOT` (staticfiles/ directory)
3. Preserves directory structure
4. Overwrites existing files (--noinput skips confirmation)

**When to run:**
- After modifying CSS/JavaScript
- After adding new images/fonts
- Before deploying to production
- After installing/uninstalling packages with static files

#### Static Files in Templates

**Correct usage:**
```django
{% load static %}
<link rel="stylesheet" href="{% static 'djangocmsjoy/style-serviceindex.css' %}">
<img src="{% static 'djangocmsjoy/img/nsf-logo.png' %}" alt="NSF Logo">
```

**Why use {% static %} tag:**
- Works with any STATIC_URL setting
- Handles CDN configurations
- Generates proper paths in all environments
- Required for Django's static files system

**Settings.py configuration:**
```python
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'djangocmsjoy' / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'djangocmsjoy' / 'static',
]
```

### jQuery and jQuery UI Integration

**Purpose:** Required for interactive components and legacy plugins

**Included in bootstrap.html:**
```html
<script src="https://code.jquery.com/jquery-3.6.1.min.js" 
        integrity="sha256-o88AwQnZB+VDvE9tvIXrMQaPlFFSUTR+nldQm1LuPXQ=" 
        crossorigin="anonymous"></script>

<script src="https://code.jquery.com/ui/1.13.2/jquery-ui.min.js" 
        integrity="sha256-lSjKY0/srUM9BE3dPm+c4fBo1dky2v27Gdjm2uoZaL0=" 
        crossorigin="anonymous"></script>
```

**jQuery UI CSS:**
```html
<link type="text/css" 
      href="//code.jquery.com/ui/1.13.2/themes/smoothness/jquery-ui.css" 
      rel="stylesheet" />
```

**Used for:**
- Date pickers in forms
- Accordions and tabs
- Drag-and-drop functionality
- Custom UI widgets
- Legacy ACCESS components

### Glyphicons Font Integration

**Custom font-face definition in style-serviceindex.css:**

```css
@font-face {
    font-family: 'Glyphicons Halflings';
    src: url('/static/djangocmsjoy/fonts/glyphicons-halflings-regular.eot');
    src: url('/static/djangocmsjoy/fonts/glyphicons-halflings-regular.eot?#iefix') format('embedded-opentype'),
         url('/static/djangocmsjoy/fonts/glyphicons-halflings-regular.woff') format('woff'),
         url('/static/djangocmsjoy/fonts/glyphicons-halflings-regular.ttf') format('truetype'),
         url('/static/djangocmsjoy/fonts/glyphicons-halflings-regular.svg#glyphicons_halflingsregular') format('svg');
}

.glyphicon {
    position: relative;
    top: 1px;
    display: inline-block;
    font-family: 'Glyphicons Halflings';
    font-style: normal;
    font-weight: 400;
    line-height: 1;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}
```

**Available icons:**
```css
.glyphicon-chevron-up:before { content: "\e113"; }
.glyphicon-chevron-down:before { content: "\e114"; }
.glyphicon-pencil:before { content: "\270f"; }
.glyphicon-plus:before { content: "\2b"; }
.glyphicon-remove:before { content: "\e014"; }
.glyphicon-info-sign:before { content: "\e086"; }
```

**Usage in templates:**
```html
<span class="glyphicon glyphicon-plus"></span> Add New
<button><span class="glyphicon glyphicon-pencil"></span> Edit</button>
```

### Design System Summary

#### Design Layers
1. **Foundation:** Bootstrap 5 (responsive grid, components)
2. **Integration:** django-bootstrap5 (Django template tags)
3. **Branding:** ACCESS colors, logos, typography
4. **Custom:** Project-specific styles and overrides

#### Color Usage Guidelines
- **Teal Dark (#1A5B6E):** Primary buttons, headers, emphasis
- **Teal Medium (#138597):** Links, secondary elements
- **Teal Light (#ECF9F8):** Backgrounds, panels
- **Yellow (#FFC42D):** Call-to-action buttons, highlights
- **Text (#333):** Body text, headings (readable gray)
- **White (#fff):** Backgrounds, cards, containers

#### Typography Scale
- **Body:** 14px (comfortable reading size)
- **Headings:** 36px → 16px (h1 → h5)
- **Intro text:** 24px (larger paragraphs)
- **Emphasis:** 18px (highlighted content)

#### Responsive Breakpoints
- **< 900px:** Mobile/tablet layout
- **≥ 900px:** Desktop layout
- **Bootstrap default breakpoints also active:**
  - xs: < 576px
  - sm: ≥ 576px
  - md: ≥ 768px
  - lg: ≥ 992px
  - xl: ≥ 1200px
  - xxl: ≥ 1400px

### Key Design Files Reference

**Templates:**
- `djangocmsjoy/templates/web/bootstrap.html` - Base template with all design elements
- `djangocmsjoy/templates/web/base_nav_full.html` - Navigation wrapper
- `djangocmsjoy/templates/base.html` - Django CMS pages base

**Stylesheets:**
- `djangocmsjoy/static/djangocmsjoy/style-serviceindex.css` - Custom CSS (508 lines)
- Bootstrap 5 CSS - Loaded via CDN
- jQuery UI CSS - Loaded via CDN

**Assets:**
- `djangocmsjoy/static/djangocmsjoy/img/` - Logos, icons
- `djangocmsjoy/static/djangocmsjoy/fonts/` - Glyphicons

**Scripts:**
- jQuery 3.6.1 - DOM manipulation
- jQuery UI 1.13.2 - UI widgets
- Bootstrap 5 JS - Component behavior
- @access-ci/ui - Universal menus

### Testing Design Changes

**After modifying CSS:**
```bash
# 1. Collect static files
uv run python djangocmsjoy/manage.py collectstatic --noinput

# 2. Restart server (if running)
# Press Ctrl+C then:
uv run python djangocmsjoy/manage.py runserver

# 3. Hard refresh browser
# Chrome/Firefox: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows/Linux)
# Safari: Cmd+Option+R
```

**Check for issues:**
1. Static files loading (no 404s in browser console)
2. Logos display at correct sizes
3. Colors match ACCESS palette
4. Text is readable (sufficient contrast)
5. Responsive layout works at different screen sizes
6. Universal menus load at top

### Troubleshooting Design Issues

**Static files not loading:**
```bash
# Verify STATIC_URL in settings
python -c "from djangocmsjoy.settings import STATIC_URL; print(STATIC_URL)"

# Check if collectstatic was run
ls -la djangocmsjoy/staticfiles/djangocmsjoy/

# Force clear and recollect
rm -rf djangocmsjoy/staticfiles/
uv run python djangocmsjoy/manage.py collectstatic --noinput
```

**Universal menus not appearing:**
- Check browser console for JavaScript errors
- Verify `<div id="universal-menus"></div>` exists in template
- Ensure script runs after div is rendered
- Check network tab for ESM module loading

**Wrong colors displaying:**
- Verify CSS variables in `:root`
- Check for conflicting Bootstrap theme
- Clear browser cache
- Inspect element to see which styles are applied

**Logos wrong size:**
- Check media query breakpoint (900px)
- Verify static file paths are correct
- Test at different screen widths
- Look for conflicting CSS rules

---

## 17. Custom Django CMS Plugins: News Feed System

### Overview

This project implements custom Django CMS plugins to create an editable news feed system directly in the CMS interface. The system uses a **parent-child plugin architecture** where container plugins hold individual news item plugins, enabling content editors to manage news without writing code or accessing the database.

### Architecture Pattern: Container + Item Plugins

The plugin system consists of 4 custom plugins organized in pairs:

**System Status News:**
- `SystemStatusNewsFeedPlugin` (container) - Displays feed of system status items
- `SystemStatusNewsItemPluginPublisher` (child) - Individual system status news item

**Integration News:**
- `IntegrationNewsFeedPlugin` (container) - Displays feed of integration items
- `IntegrationNewsItemPluginPublisher` (child) - Individual integration news item

This pattern creates a hierarchical structure where:
1. Editor adds a Feed Container plugin to a CMS page
2. Editor adds News Item plugins inside the container
3. Feed automatically sorts items by date (newest first)
4. Items render with consistent formatting

### How CMS Plugins Work

Django CMS plugins are reusable content components that:
- Appear in the CMS toolbar for content editors to add to pages
- Have database models to store their configuration/content
- Use templates to render their HTML output
- Can contain other plugins (parent-child relationships)
- Integrate with Django's admin forms for editing

### Plugin Component Structure

Each plugin requires 3 files:

1. **Model** (`models.py`) - Database table storing plugin data
2. **Plugin Class** (`cms_plugins.py`) - Defines behavior and registration
3. **Template** (`templates/djangocmsjoy/plugins/*.html`) - HTML output

### Code Implementation

#### 1. Plugin Models (djangocmsjoy/models.py)

Models extend `CMSPlugin` instead of `models.Model` to gain CMS-specific functionality:

```python
from django.db import models
from django.contrib.auth.models import User
from cms.models.pluginmodel import CMSPlugin


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
```

**Key Features:**
- `CMSPlugin` parent class provides page association, position, language, and plugin tree hierarchy
- `auto_now_add=True` automatically timestamps when item is created
- `ForeignKey(User)` tracks who created each news item
- `ordering = ['-published_date']` sorts newest first by default
- `__str__()` method displays title in admin interface

#### 2. Plugin Classes (djangocmsjoy/cms_plugins.py)

Plugin classes define how the plugins behave in the CMS:

```python
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from .models import SystemStatusNewsItemPlugin, IntegrationNewsItemPlugin


@plugin_pool.register_plugin
class SystemStatusNewsItemPluginPublisher(CMSPluginBase):
    """CMS Plugin for adding System Status News items"""
    model = SystemStatusNewsItemPlugin
    name = "System Status News Item"
    render_template = "djangocmsjoy/plugins/system_status_news_item.html"
    cache = False
    
    fieldsets = [
        (None, {
            'fields': ('title', 'content', 'author')
        }),
    ]
    
    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        context['instance'] = instance
        return context


@plugin_pool.register_plugin
class IntegrationNewsItemPluginPublisher(CMSPluginBase):
    """CMS Plugin for adding Integration News items"""
    model = IntegrationNewsItemPlugin
    name = "Integration News Item"
    render_template = "djangocmsjoy/plugins/integration_news_item.html"
    cache = False
    
    fieldsets = [
        (None, {
            'fields': ('title', 'content', 'author')
        }),
    ]
    
    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        context['instance'] = instance
        return context


@plugin_pool.register_plugin
class SystemStatusNewsFeedPlugin(CMSPluginBase):
    """CMS Plugin to display all System Status News items in chronological order"""
    model = CMSPlugin
    name = "System Status News Feed"
    render_template = "djangocmsjoy/plugins/system_status_news_feed.html"
    cache = False
    allow_children = True
    child_classes = ['SystemStatusNewsItemPluginPublisher']
    
    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        # Get all child news items, ordered by date (newest first)
        children = instance.child_plugin_instances or []
        news_items = [child for child in children if isinstance(child, SystemStatusNewsItemPlugin)]
        news_items.sort(key=lambda x: x.published_date, reverse=True)
        context['news_items'] = news_items
        return context


@plugin_pool.register_plugin
class IntegrationNewsFeedPlugin(CMSPluginBase):
    """CMS Plugin to display all Integration News items in chronological order"""
    model = CMSPlugin
    name = "Integration News Feed"
    render_template = "djangocmsjoy/plugins/integration_news_feed.html"
    cache = False
    allow_children = True
    child_classes = ['IntegrationNewsItemPluginPublisher']
    
    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        # Get all child news items, ordered by date (newest first)
        children = instance.child_plugin_instances or []
        news_items = [child for child in children if isinstance(child, IntegrationNewsItemPlugin)]
        news_items.sort(key=lambda x: x.published_date, reverse=True)
        context['news_items'] = news_items
        return context
```

**Key Attributes Explained:**

| Attribute | Purpose |
|-----------|---------|
| `@plugin_pool.register_plugin` | Decorator that registers plugin with Django CMS, making it appear in toolbar |
| `model` | Database model storing plugin data |
| `name` | Display name shown in CMS toolbar dropdown |
| `render_template` | Path to HTML template for rendering |
| `cache = False` | Disables caching so news updates appear immediately |
| `fieldsets` | Defines form fields shown in admin popup when editing |
| `allow_children = True` | Allows this plugin to contain other plugins (container) |
| `child_classes` | List of plugin class names allowed as children (enforces structure) |

**The `render()` Method:**
- Called when plugin is displayed on page
- `context` - Template context dictionary
- `instance` - The plugin model instance with all data
- `placeholder` - CMS placeholder where plugin is placed
- Adds data to context that templates can access

#### 3. Plugin Templates

**Feed Container Template** (`djangocmsjoy/plugins/system_status_news_feed.html`):

```html
{# Template for System Status News Feed Container #}
<div class="news-feed system-status-news-feed">
    <div class="news-feed-header mb-4">
        <h2>System Status News</h2>
        <p class="text-muted">Updates about infrastructure status, maintenance, and system operations</p>
    </div>
    <div class="news-items">
        {% for plugin in instance.child_plugin_instances %}
            {% load cms_tags %}
            {% render_plugin plugin %}
        {% empty %}
            <p class="text-muted">No news items yet. Add your first news item using the CMS toolbar above.</p>
        {% endfor %}
    </div>
</div>
```

**News Item Template** (`djangocmsjoy/plugins/system_status_news_item.html`):

```html
{# Template for individual System Status News item #}
<div class="news-item mb-4 p-3 border-bottom">
    <h3 class="news-title">{{ instance.title }}</h3>
    <div class="news-meta text-muted small mb-2">
        <span class="news-author">By {{ instance.author.get_full_name|default:instance.author.username }}</span>
        <span class="news-date ms-2">{{ instance.published_date|date:"F j, Y g:i A" }}</span>
    </div>
    <div class="news-content">
        {{ instance.content|linebreaks }}
    </div>
</div>
```

**Integration News Templates:**
Nearly identical but with different CSS classes and descriptions (`integration_news_feed.html` and `integration_news_item.html`).

**Template Features:**
- `{% load cms_tags %}` - Loads CMS template tags
- `{% render_plugin plugin %}` - Renders child plugin using its template
- `instance.child_plugin_instances` - List of all child plugins provided by CMS
- `{{ instance.title }}` - Accesses model fields
- `|linebreaks` - Django filter converting newlines to `<br>` and `<p>` tags
- `|date:"F j, Y g:i A"` - Formats datetime (e.g., "December 4, 2025 2:30 PM")
- Bootstrap classes (`mb-4`, `p-3`, `border-bottom`, etc.) for styling

### How the System Enables Functionality

#### Content Editor Workflow:

1. **Navigate to CMS page** in edit mode (click "Edit Page" in toolbar)

2. **Add Feed Container:**
   - Click "+" in page placeholder
   - Select "System Status News Feed" or "Integration News Feed"
   - Container appears with empty state message

3. **Add News Items:**
   - Click "+" inside the container
   - Only allowed child type appears ("System Status News Item")
   - Fill form popup:
     * **Title:** News headline
     * **Content:** News body text
     * **Author:** Select from user dropdown
   - Click Save
   - Published date automatically set to now

4. **Add More Items:**
   - Repeat process to add more news items
   - Items automatically sort newest first
   - Drag to reorder if needed

5. **Edit/Delete Items:**
   - Click pencil icon to edit
   - Click X to delete
   - Changes save immediately

6. **Publish Page:**
   - Click "Publish page changes"
   - News feed now visible to public

#### Behind the Scenes:

When page loads, Django CMS:
1. Finds all plugins in page placeholders
2. Calls each plugin's `render()` method
3. Feed plugin gathers `child_plugin_instances`
4. Sorts children by `published_date` (newest first)
5. Template loops through children
6. `{% render_plugin %}` renders each child with its template
7. Child templates access `instance.title`, `instance.content`, etc.
8. HTML output combines into complete feed

### Database Schema

After running migrations, these tables exist:

**djangocmsjoy_systemstatusnewsitemplugin:**
- id (primary key)
- cmsplugin_ptr_id (foreign key to cms_cmsplugin)
- title (varchar 200)
- content (text)
- author_id (foreign key to auth_user)
- published_date (datetime)

**djangocmsjoy_integrationnewsitemplugin:**
- Same structure as system status table

**cms_cmsplugin:**
- Built-in CMS table storing:
  - position (order in placeholder)
  - placeholder_id (which placeholder)
  - language (for multilingual sites)
  - plugin_type (class name)
  - parent_id (for child plugins)

The plugin tables have a **one-to-one relationship** with `cms_cmsplugin` via `cmsplugin_ptr_id`, inheriting CMS-specific fields while adding custom fields.

### Key Enabling Features

| Feature | How It Enables Functionality |
|---------|------------------------------|
| `@plugin_pool.register_plugin` | Makes plugin available in CMS toolbar for content editors |
| `allow_children=True` | Creates container that can hold other plugins |
| `child_classes` | Enforces which plugins can be added inside (prevents mixing news types) |
| `cache=False` | Ensures news updates appear immediately without cache clearing |
| `instance.child_plugin_instances` | CMS automatically provides list of all children |
| `published_date` with `auto_now_add` | Automatic timestamp without editor input |
| Inheriting `CMSPlugin` | Provides page association, position, language, plugin tree hierarchy |
| `{% render_plugin %}` tag | Recursive rendering - each child renders with its own template |
| `fieldsets` | Controls admin form layout - only shows relevant fields |
| Model `ordering = ['-published_date']` | Default sort order for database queries |
| `def __str__()` | Display text in admin interface and dropdowns |

### Commands for Creating Plugins

#### 1. Create Plugin Models

Add to `djangocmsjoy/models.py`:

```bash
# No special command - just edit the file
```

#### 2. Create Database Tables

After adding models:

```bash
uv run python djangocmsjoy/manage.py makemigrations
uv run python djangocmsjoy/manage.py migrate
```

#### 3. Create Plugin Classes

Add to `djangocmsjoy/cms_plugins.py`:

```bash
# No special command - just edit the file
```

#### 4. Create Plugin Templates

Create files in `djangocmsjoy/templates/djangocmsjoy/plugins/`:

```bash
mkdir -p djangocmsjoy/templates/djangocmsjoy/plugins
touch djangocmsjoy/templates/djangocmsjoy/plugins/system_status_news_feed.html
touch djangocmsjoy/templates/djangocmsjoy/plugins/system_status_news_item.html
touch djangocmsjoy/templates/djangocmsjoy/plugins/integration_news_feed.html
touch djangocmsjoy/templates/djangocmsjoy/plugins/integration_news_item.html
```

#### 5. Restart Development Server

After creating plugins:

```bash
# Stop server (Ctrl+C) and restart
uv run python djangocmsjoy/manage.py runserver
```

Django CMS automatically detects registered plugins on startup.

#### 6. Verify Plugins Available

Check CMS toolbar:
1. Navigate to any CMS page
2. Enter edit mode
3. Click "+" in a placeholder
4. Look for plugin names in dropdown

Or check in Django shell:

```bash
uv run python djangocmsjoy/manage.py shell
```

```python
from cms.plugin_pool import plugin_pool
print(plugin_pool.get_all_plugins())
# Should list your custom plugins
```

### Testing Custom Plugins

#### Unit Test Example

Create `djangocmsjoy/tests/test_plugins.py`:

```python
from django.test import TestCase
from django.contrib.auth.models import User
from cms.api import create_page, add_plugin
from cms.models import Placeholder
from djangocmsjoy.models import SystemStatusNewsItemPlugin


class NewsPluginTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@test.com', 'pass')
        self.page = create_page(
            title='Test Page',
            template='page.html',
            language='en'
        )
        self.placeholder = self.page.placeholders.get(slot='content')
    
    def test_news_feed_plugin_creation(self):
        """Test creating a news feed container plugin"""
        feed_plugin = add_plugin(
            self.placeholder,
            'SystemStatusNewsFeedPlugin',
            'en'
        )
        self.assertEqual(feed_plugin.plugin_type, 'SystemStatusNewsFeedPlugin')
    
    def test_news_item_plugin_creation(self):
        """Test creating a news item plugin"""
        feed_plugin = add_plugin(
            self.placeholder,
            'SystemStatusNewsFeedPlugin',
            'en'
        )
        
        item_plugin = add_plugin(
            self.placeholder,
            'SystemStatusNewsItemPluginPublisher',
            'en',
            target=feed_plugin,
            title='Test News',
            content='Test content',
            author=self.user
        )
        
        self.assertEqual(item_plugin.title, 'Test News')
        self.assertEqual(item_plugin.author, self.user)
    
    def test_news_items_sorted_by_date(self):
        """Test that news items are sorted newest first"""
        feed_plugin = add_plugin(
            self.placeholder,
            'SystemStatusNewsFeedPlugin',
            'en'
        )
        
        # Create two items
        item1 = add_plugin(
            self.placeholder,
            'SystemStatusNewsItemPluginPublisher',
            'en',
            target=feed_plugin,
            title='Older News',
            content='Content',
            author=self.user
        )
        
        item2 = add_plugin(
            self.placeholder,
            'SystemStatusNewsItemPluginPublisher',
            'en',
            target=feed_plugin,
            title='Newer News',
            content='Content',
            author=self.user
        )
        
        # Get plugin instance and check order
        from djangocmsjoy.cms_plugins import SystemStatusNewsFeedPlugin
        plugin_instance = SystemStatusNewsFeedPlugin()
        context = {}
        rendered_context = plugin_instance.render(context, feed_plugin, self.placeholder)
        
        news_items = rendered_context['news_items']
        self.assertEqual(news_items[0].title, 'Newer News')
        self.assertEqual(news_items[1].title, 'Older News')
```

#### Run Tests

```bash
uv run python djangocmsjoy/manage.py test djangocmsjoy.tests.test_plugins
```

### Troubleshooting

**Plugin doesn't appear in toolbar:**
- Check `@plugin_pool.register_plugin` decorator is present
- Verify `cms_plugins.py` is in app directory
- Ensure app is in `INSTALLED_APPS` in settings.py
- Restart development server
- Clear browser cache

**Form fields not showing:**
- Check `fieldsets` configuration in plugin class
- Verify model fields exist and are not auto-generated
- Look for typos in field names

**Template not rendering:**
- Verify `render_template` path matches actual file location
- Check template directory is in `TEMPLATES['DIRS']` or app `templates/` folder
- Look for template syntax errors
- Check Django template loader can find the file

**Children not displaying:**
- Verify `allow_children = True` on parent plugin
- Check `child_classes` list has correct plugin class names (not model names)
- Ensure `{% render_plugin %}` tag is in parent template
- Verify `{% load cms_tags %}` is present

**Data not saving:**
- Run `makemigrations` and `migrate` after creating/changing models
- Check model field definitions match form fields
- Look for database errors in console
- Verify foreign key relationships (User model)

**Items not sorted correctly:**
- Check `Meta.ordering` in model
- Verify `sort()` logic in `render()` method
- Ensure `published_date` field has values
- Check `reverse=True` for descending order

**Plugin crashes page:**
- Check server console for Python errors
- Verify all model instances have required fields
- Test `__str__()` method doesn't crash
- Check for None values in foreign keys

### Advanced: Customizing Plugin Behavior

#### Adding Configuration Options

Make feed plugin configurable (show N most recent items):

```python
class SystemStatusNewsFeedConfig(CMSPlugin):
    """Configuration for news feed display"""
    max_items = models.IntegerField(default=10, help_text="Maximum items to display")


@plugin_pool.register_plugin
class SystemStatusNewsFeedPlugin(CMSPluginBase):
    model = SystemStatusNewsFeedConfig  # Use config model instead of CMSPlugin
    name = "System Status News Feed"
    render_template = "djangocmsjoy/plugins/system_status_news_feed.html"
    cache = False
    allow_children = True
    child_classes = ['SystemStatusNewsItemPluginPublisher']
    
    fieldsets = [
        (None, {
            'fields': ('max_items',)
        }),
    ]
    
    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        children = instance.child_plugin_instances or []
        news_items = [child for child in children if isinstance(child, SystemStatusNewsItemPlugin)]
        news_items.sort(key=lambda x: x.published_date, reverse=True)
        
        # Limit to configured number
        context['news_items'] = news_items[:instance.max_items]
        return context
```

#### Adding Rich Text Support

Install CKEditor plugin:

```bash
uv add djangocms-text-ckeditor
```

Update model:

```python
from djangocms_text_ckeditor.fields import HTMLField

class SystemStatusNewsItemPlugin(CMSPlugin):
    title = models.CharField(max_length=200)
    content = HTMLField()  # Rich text instead of TextField
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    published_date = models.DateTimeField(auto_now_add=True)
```

Update template:

```html
<div class="news-content">
    {{ instance.content|safe }}  {# |safe renders HTML, not escaped text #}
</div>
```

#### Adding Image Support

Using Django Filer:

```bash
uv add django-filer easy-thumbnails
```

Update model:

```python
from filer.fields.image import FilerImageField

class SystemStatusNewsItemPlugin(CMSPlugin):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = FilerImageField(null=True, blank=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    published_date = models.DateTimeField(auto_now_add=True)
```

Update template:

```html
<div class="news-item mb-4 p-3 border-bottom">
    {% if instance.image %}
        <img src="{{ instance.image.url }}" alt="{{ instance.title }}" class="img-fluid mb-2">
    {% endif %}
    <h3 class="news-title">{{ instance.title }}</h3>
    <!-- ... rest of template ... -->
</div>
```

### Production Alternative: djangocms-blog

For production deployments, consider using the battle-tested **djangocms-blog** package instead of custom plugins:

```bash
uv add djangocms-blog
```

**Advantages:**
- SEO optimization (meta tags, Open Graph, Twitter cards)
- Multi-language support
- Categories and tags
- RSS feeds
- Author profiles
- Archive views
- Related posts
- Sitemap integration
- Wizard for easy post creation
- Active maintenance and community support

**Documentation:** https://djangocms-blog.readthedocs.io/

The custom plugins in this project are excellent for learning CMS plugin development, but djangocms-blog offers more features and has been tested in production environments.

---

**Document Version:** 1.5  
**Last Updated:** December 4, 2025  
**Maintained By:** ACCESS Operations Team
