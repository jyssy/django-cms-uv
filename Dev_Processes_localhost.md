# Development Processes for Django CMS - Localhost

**Project:** ACCESS Operations Portal Django CMS  
**Date:** December 3, 2025  
**Environment:** Local Development (macOS)  
**Python:** 3.13 with UV package manager  
**Django:** 5.2.9  
**Django CMS:** 5.0  
**Database:** PostgreSQL 15

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
12. [SQLite to PostgreSQL Migration](#12-sqlite-to-postgresql-migration)

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
UV automatically manages the virtual environment based on `pyproject.toml`:
- Uses Python 3.13
- Dependencies: Django 5.2.9, djangocms-admin-style 3.3+, psycopg2-binary 2.9+, django-bootstrap5 25.0+

### Initial Setup Commands
```bash
# Install dependencies (if needed)
uv sync

# Run migrations
uv run python djangocmsjoy/manage.py migrate

# Create superuser (if needed)
uv run python djangocmsjoy/manage.py createsuperuser

# Collect static files
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

```python
from django.urls import path
from . import views

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

## 12. SQLite to PostgreSQL Migration

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

**Document Version:** 1.1  
**Last Updated:** December 3, 2025  
**Maintained By:** ACCESS Operations Team
