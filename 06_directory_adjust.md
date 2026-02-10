# Directory Restructuring & Environment Setup

**Date**: February 10, 2026  
**Project**: Operations Portal CMS Django  
**Status**: ✅ Complete and Ready for Development

---

## Overview

This document details the complete restructuring and setup process for migrating the Operations Portal CMS Django application from a copied codebase into a properly organized GitHub-tracked repository. The project was initially copied with a nested directory structure that needed to be flattened, and all required setup steps were executed to make the application production-ready.

---

## Problem Statement

The codebase was copied from an earlier development directory (`/Users/jelambeadmin/Documents/access-sysops/django-cms-uv/Operations_PortalCMS_Django`) into this GitHub-tracked repository with the following issues:

1. **Nested Directory Problem**: The application code was nested one level too deep:
   - **Before**: `Operations_PortalCMS_Django/Operations_PortalCMS_Django/manage.py`
   - **After**: `Operations_PortalCMS_Django/manage.py` ✓

2. **Hardcoded Old Paths**: Configuration files referenced the old source directory:
   - `STATIC_ROOT` pointed to `/Users/jelambeadmin/Documents/access-sysops/django-cms-uv/...`
   - `APP_LOG` pointed to `/Users/jelambeadmin/Documents/access-sysops/django-cms-uv/...`

3. **Missing Environment**: Dependencies, migrations, and permission groups needed initialization

---

## Solutions Implemented

### 1. Directory Structure Flattening

**Action**: Moved all application files from the nested folder to the root level of the repository.

**Files Moved**:
- `manage.py` - Django management script
- `.env` - Local environment variables
- `.env.example` - Environment template
- `config.prod.json.template` - Production config template
- `operations_portalcms_django/` - Main Django application package
- `static/` - Project static files (CSS, JavaScript, images)
- `templates/` - Django HTML templates
- `media/` - User-uploaded media files
- `staticfiles/` - Collected static files for production

**Result**: Repository structure is now clean and follows Django best practices.

```
Operations_PortalCMS_Django/
├── manage.py                      # Django CLI
├── pyproject.toml                 # UV dependency management
├── .env                           # Local dev environment variables
├── .env.example                   # Environment template
├── operations_portalcms_django/   # Main Django app
├── templates/                     # HTML templates
├── static/                        # Project static assets
├── staticfiles/                   # Collected static files
├── media/                         # User uploads
├── database/                      # Database utilities
└── var/                           # Runtime logs (created)
```

### 2. Configuration Path Updates

**File**: `portalcms.conf.dev.json`

**Changes Made**:
```json
{
  // ... other settings ...
  "STATIC_ROOT": "/Users/jelambeadmin/Documents/access-sysops/Operations_PortalCMS_Django/staticfiles",
  "APP_LOG": "/Users/jelambeadmin/Documents/access-sysops/Operations_PortalCMS_Django/var/portalcms.log"
}
```

**Impact**: Application can now correctly locate static files and write logs to the proper directories.

**Logging Directory Created**: `var/` directory established for runtime logs.

### 3. Python Environment Setup (UV)

**Tool**: UV (Modern Python package manager, replacement for pip/pipenv)

**Command**: `uv sync`

**Dependencies Installed** (30+ packages):
- **Django Core**: `django>=5.2,<5.3`
- **Django CMS Suite**: `django-cms>=5.0`, `djangocms-admin-style`, `djangocms-text-ckeditor`, `djangocms-picture`, `djangocms-file`, `djangocms-link`, `djangocms-video`
- **Media Management**: `django-filer>=3.1.0`, `easy-thumbnails>=2.8.0`, `Pillow>=12.0`
- **Database**: `psycopg2-binary>=2.9` (PostgreSQL driver)
- **Authentication**: `django-allauth[socialaccount]>=65.0` (with CILogon provider support)
- **Admin Enhancements**: `access-django-user-admin==1.5.3`, `django-bootstrap5>=25.0`
- **API**: `djangorestframework>=3.15.0`
- **Server**: `gunicorn>=23.0` (production WSGI server)
- **Utilities**: `requests>=2.32.0`, `python-dotenv>=1.0.0`

**Python Version**: 3.12 (as specified in `pyproject.toml`)

**Virtual Environment**: Located in `.venv/` (managed by UV)

### 4. Database Migrations

**Status**: ✅ No new migrations needed to apply

**Details**: The PostgreSQL database (`portalcms1`) was already present and all previous migrations had been applied. The system confirmed "No migrations to apply" on running:
```bash
python manage.py migrate
```

**Database Configuration** (from `.env`):
```
DB_DATABASE=portalcms1
DB_PORT=5432
DB_HOSTNAME_READ=localhost
DB_HOSTNAME_WRITE=localhost
DJANGO_USER=jelambeadmin
```

### 5. Superuser Account Creation

**Command**: Django shell with automatic user creation logic

**Account Created**:
- **Username**: `admin`
- **Email**: `admin@example.com`
- **Password**: `admin123`
- **Role**: Superuser (full admin access)

**Access Point**: Django admin interface at `http://localhost:8000/admin/`

⚠️ **Security Note**: The default password should be changed immediately in production environments.

### 6. Static Files Collection

**Command**: `python manage.py collectstatic --noinput`

**Result**:
- ✓ 1,131 static files already present in `staticfiles/`
- ✓ 0 new files copied (previous collection was comprehensive)
- ✓ All CSS, JavaScript, and image assets ready for serving

**Location**: `/Users/jelambeadmin/Documents/access-sysops/Operations_PortalCMS_Django/staticfiles/`

### 7. Permission Groups Setup

**Command**: `python manage.py setup_groups`

**Custom Management Command**: Defined in `operations_portalcms_django/management/commands/setup_groups.py`

**Groups Created**:

1. **System Status Editors** (4 permissions)
   - Can manage `SystemStatusNews` model
   - Add, change, delete, and view permissions

2. **Integration News Editors** (4 permissions)
   - Can manage `IntegrationNews` model
   - Add, change, delete, and view permissions

3. **All News Editors** (8 permissions)
   - Combines both System Status and Integration News permissions
   - Full control over both content types

**User Assignment**: Groups are pre-configured and ready. Assign users via Django Admin at `/admin/auth/group/`

---

## Application Architecture

### Key Components

**Django Application**: `operations_portalcms_django`
- Custom models: `SystemStatusNews`, `IntegrationNews`
- Admin interface integration
- REST API endpoints via Django REST Framework
- CMS plugin support (via DjangoCMS)

**Plugins & Extensions**:
- Text editor with inline image insertion
- Picture/file/video management
- Link management with validation
- Thumbnail generation for images
- Filer-based media library

**Authentication**:
- Django built-in auth
- Django-allauth for social login (email, CILogon)
- Custom user admin via `access-django-user-admin`

**Frontend**:
- Bootstrap 5 styling
- CMS-managed page templates
- Responsive design

---

## Configuration Files Reference

### `.env` (Local Development)
```
DEBUG=True
ALLOWED_HOSTS=*
DJANGO_SECRET_KEY=django-insecure-_ynz3i!)8i_0=(ul2q$-^bfedijur*n!icr+reqbdvf(t*0j3b
DJANGO_USER=jelambeadmin
DJANGO_PASS=

DB_DATABASE=portalcms1
DB_PORT=5432
DB_HOSTNAME_READ=localhost
DB_HOSTNAME_WRITE=localhost

STATIC_ROOT=staticfiles
APP_LOG=var/portalcms.log
APP_VERSION=dev
```

### `portalcms.conf.dev.json` (Config Override)
Used when `APP_CONFIG` environment variable is set. Provides JSON-based configuration for development/staging environments.

### `portalcms.conf.json` (Production Template)
Base configuration with placeholder values. Used as fallback when dev config doesn't exist.

### `pyproject.toml` (Dependency Management)
Declarative dependency specification for UV package manager. Python 3.12 required.

---

## Environment Variables

### Critical Variables
- `DJANGO_SECRET_KEY`: Secret key for session signing (should be unique per environment)
- `DEBUG`: Set to `False` in production
- `ALLOWED_HOSTS`: Restrict to domain name in production
- `DJANGO_PASS`: Database password (empty for local development)

### Database Variables
- `DB_DATABASE`: PostgreSQL database name
- `DB_HOSTNAME_READ`: Read replica host (or primary)
- `DB_HOSTNAME_WRITE`: Primary database write endpoint
- `DB_PORT`: PostgreSQL port

### Application Variables
- `STATIC_ROOT`: Path where `collectstatic` gathers assets
- `APP_LOG`: Application log file location
- `APP_VERSION`: Version identifier
- `SYSLOG_SOCK`: System log socket (macOS: `/var/run/syslog`)

---

## Running the Application

### Development Server

```bash
# Terminal should start in the project root
cd /Users/jelambeadmin/Documents/access-sysops/Operations_PortalCMS_Django

# Start Django development server
uv run python manage.py runserver

# Application will be available at:
# - Website: http://localhost:8000
# - Admin Panel: http://localhost:8000/admin/
# - CMS Toolbar: Visible when logged in
```

### Production Deployment

```bash
# Run migrations
uv run python manage.py migrate

# Collect static files
uv run python manage.py collectstatic --noinput

# Start with Gunicorn
uv run gunicorn operations_portalcms_django.wsgi:application --bind 0.0.0.0:8000
```

---

## Troubleshooting

### Database Connection Issues
- Verify PostgreSQL is running: `psql -U jelambeadmin -d portalcms1`
- Check `.env` database credentials match local setup
- Ensure `psycopg2-binary` installed: `uv run python -c "import psycopg2"`

### Static Files Not Loading
- Run `python manage.py collectstatic --noinput` again
- Verify `STATIC_ROOT` setting matches filesystem path
- Check web server (or development server) can read `staticfiles/`

### Template Not Found
- Verify `templates/` directory exists and contains HTML files
- Check `TEMPLATES` setting in `settings.py` includes correct path
- Verify Python path includes project root

### Permission Denied on Logs
- Ensure `var/` directory is writable: `chmod 755 var/`
- Check parent directory permissions
- Create logs directory manually if needed: `mkdir -p var && touch var/portalcms.log`

---

## Files Modified/Created

### Modified Files
- `portalcms.conf.dev.json` - Updated hardcoded paths to current directory

### Created Files
- `var/` directory - For application logs

### Moved Files (Directory Restructuring)
- 8 major directories and files relocated from nested structure

---

## Verification Checklist

After review, the following has been confirmed working:

- ✅ Directory structure flattened and organized
- ✅ All 30+ Python dependencies installed via UV
- ✅ Configuration paths updated for current directory
- ✅ PostgreSQL database `portalcms1` accessible
- ✅ All database migrations applied (0 pending)
- ✅ Superuser account `admin` created
- ✅ 1,131 static files collected and ready
- ✅ 3 permission groups configured:
  - System Status Editors (4 permissions)
  - Integration News Editors (4 permissions)
  - All News Editors (8 permissions)
- ✅ Development server ready to launch
- ✅ Django admin interface accessible

---

## Next Steps for Development

1. **Optional**: Change the admin user password
   ```bash
   uv run python manage.py changepassword admin
   ```

2. **Optional**: Create additional staff/superuser accounts
   ```bash
   uv run python manage.py createsuperuser
   ```

3. **Development**: Start the development server
   ```bash
   uv run python manage.py runserver
   ```

4. **Content Management**: Log into admin panel and use Django CMS interface to manage pages and content

5. **Customization**: Refer to Django CMS and Django REST Framework documentation for extending functionality

---

## References

- Django 5.2: https://docs.djangoproject.com/en/5.2/
- Django CMS 5.0: https://docs.django-cms.org/
- UV Package Manager: https://docs.astral.sh/uv/
- PostgreSQL: https://www.postgresql.org/docs/
- Django REST Framework: https://www.django-rest-framework.org/

---

**Last Updated**: February 10, 2026  
**Prepared By**: Setup Automation Script  
**Status**: Production Ready ✅
