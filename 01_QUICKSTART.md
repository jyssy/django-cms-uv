# Quick Start Guide - Enhanced Django CMS

## What's New (January 28, 2026)

This Django CMS project now mirrors the Drupal Operations Portal with:
- ✅ Bootstrap 5 responsive design
- ✅ ACCESS branding and color scheme
- ✅ Professional header/footer matching Drupal
- ✅ Infrastructure Integration page template
- ✅ Full media management with Django Filer

## Quick Setup

### 1. Install Dependencies
```bash
cd /Users/jelambeadmin/Documents/access-sysops/django-cms-uv
uv sync
```

### 2. Run Migrations
```bash
cd Operations_PortalCMS_Django
uv run python manage.py migrate
```

### 3. Create Superuser (if needed)
```bash
uv run python manage.py createsuperuser
```

### 4. Collect Static Files
```bash
uv run python manage.py collectstatic --noinput
```

### 5. Run Development Server
```bash
uv run python manage.py runserver
```

### 6. Access the Site
- **Homepage:** http://localhost:8000
- **Admin:** http://localhost:8000/admin
- **Integration News:** http://localhost:8000/integration_news
- **System Status News:** http://localhost:8000/infrastructure_news_view

## Creating Content

### Create a Page
1. Log into admin
2. Navigate to Django CMS → Pages
3. Click "Add page"
4. Choose a template:
   - **Page** - Simple content page
   - **Page with Feature** - Hero section + content
   - **Infrastructure Integration** - Infrastructure class cards

## Available Templates

### 1. Page (page.html)
Simple single-column layout with one content placeholder.

### 2. Page with Feature (feature.html)
Two-column hero section (8/4 split) plus content area below.

### 3. Infrastructure Integration (infrastructure.html)
Full page layout matching Drupal's infrastructure integration page:
- Lead paragraph + hero image
- Information buttons
- Four infrastructure class cards (HPC, Storage, Cloud, Science Gateways)

### 4. Infrastructure Integration (infrastructure.html)
Full page layout matching Drupal's infrastructure integration page:
- Lead paragraph + hero image
- Information buttons
- Four infrastructure class cards (HPC, Storage, Cloud, Science Gateways)

## New Plugins Available

- **Text Editor** - CKEditor 5 rich text editing
- **Picture** - Image uploads with thumbnails
- **File** - File downloads
- **Link** - Internal/external links
- **Video** - Video embeds

## File Structure

```
Operations_PortalCMS_Django/
├── templates/
│   ├── base.html              # Master template (NEW - Enhanced)
│   ├── page.html              # Simple page (UPDATED)
│   ├── feature.html           # Feature page (UPDATED)
│   ├── infrastructure.html    # Infrastructure page (NEW)
│   └── menu.html              # Navigation menu (NEW)
├── static/operations_portalcms_django/
│   └── img/
│       ├── ACCESS-operations.svg
│       ├── ACCESS-pipe.svg
│       ├── NSF_logo.svg       # (NEW)
│       ├── nsf-logo.png
│       └── favicon.ico
└── operations_portalcms_django/
    └── settings.py            # Updated with new apps
```

## Key Features

### Drupal Parity
- Matches Drupal header/footer design
- Same navigation structure
- Identical breadcrumb system
- ACCESS branding colors
- Bootstrap 5 framework

### Advanced Media
- Django Filer for file management
- Automatic thumbnail generation
- Drag-and-drop uploads in admin
- Folder organization

### Advanced Content Management
- CKEditor 5 rich text editing
- Drag-and-drop media uploads
- Automatic image thumbnails
- File organization in Filer

## Troubleshooting

### Missing Static Files
```bash
uv run python manage.py collectstatic
```

### Template Not Found
Check that template name matches CMS_TEMPLATES in settings.py

### Media Upload Errors
```bash
mkdir -p media
chmod 755 media
```

### Missing Templates
Verify all templates are in the templates/ directory

## Next Steps

1. **Content Migration** - Export Drupal content and import to Django
2. **Custom Plugins** - Build ACCESS-specific CMS plugins
3. **API Integration** - Connect to ACCESS APIs
4. **User Authentication** - Set up SSO/OAuth
5. **Production Deployment** - Configure for production environment

## Documentation

Full documentation: [Dev_Processes_localhost.md](Dev_Processes_localhost.md)

See Section 18 for complete Drupal migration guide.

## Support

Questions? Check the documentation or contact the ACCESS Operations team.
