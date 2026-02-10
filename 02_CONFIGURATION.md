# Environment Configuration

This document explains how environment variables are used in the Operations Portal CMS.

## Overview

The application follows the same configuration pattern as other ACCESS Django applications (like serviceindex). Settings are loaded from environment variables, allowing the same codebase to run in development, staging, and production with different configurations.

## Configuration Files

### Local Development: `.env`
For local development, create a `.env` file in the `Operations_PortalCMS_Django` directory:

```bash
cp .env.example .env
# Edit .env with your local settings
```

The `.env` file is automatically loaded when Django starts. **Never commit `.env` to git** - it's in `.gitignore`.

### Production: Environment Variables
In production, set environment variables directly (via deployment scripts, containers, or system configuration). The application will use these instead of `.env`.

## Configuration Variables

### Django Core Settings

- **`DEBUG`** (default: `True`)  
  Set to `False` in production. Controls debug mode.

- **`ALLOWED_HOSTS`** (default: `*`)  
  Comma-separated list of allowed hostnames.  
  Example: `operations.access-ci.org,operations-test.access-ci.org`

- **`DJANGO_SECRET_KEY`** (required in production)  
  Django secret key for cryptographic signing. Generate with:
  ```bash
  python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
  ```

### Database Settings

Follows the same pattern as serviceindex:

- **`DB_DATABASE`** (default: `portalcms1`)  
  PostgreSQL database name

- **`DB_PORT`** (default: `5432`)  
  PostgreSQL port

- **`DB_HOSTNAME_READ`** (default: `localhost`)  
  Database hostname for read operations

- **`DB_HOSTNAME_WRITE`** (default: `localhost`)  
  Database hostname for write operations

- **`DJANGO_USER`** (default: `portalcms_django`)  
  PostgreSQL username

- **`DJANGO_PASS`** (default: empty)  
  PostgreSQL password

### Static Files & Logging

- **`STATIC_ROOT`** (default: `staticfiles`)  
  Path where static files are collected for production

- **`APP_LOG`** (default: `var/portalcms.log`)  
  Path to application log file

- **`APP_VERSION`** (default: `dev`)  
  Application version tag

- **`SYSLOG_SOCK`** (default: `/var/run/syslog`)  
  Syslog socket path

### API Configuration

- **`API_BASE`** (default: empty)  
  Base URL for external APIs if needed

## Example Configurations

### Local Development (`.env`)
```bash
DEBUG=True
ALLOWED_HOSTS=*
DJANGO_USER=jelambeadmin
DJANGO_PASS=
DB_DATABASE=djangocmsjoy
DB_HOSTNAME_READ=localhost
DB_HOSTNAME_WRITE=localhost
```

### Production (JSON template)
```json
{
    "DEBUG": false,
    "ALLOWED_HOSTS": ["operations.access-ci.org"],
    "DB_DATABASE": "portalcms1",
    "DB_PORT": "5432",
    "DB_HOSTNAME_READ": "{{ AMAZON_RDS_HOST_PROD }}",
    "DB_HOSTNAME_WRITE": "{{ AMAZON_RDS_HOST_PROD }}",
    "DJANGO_USER": "portalcms_django",
    "DJANGO_PASS": "{{ DJANGO_PASS }}",
    "DJANGO_SECRET_KEY": "{{ DJANGO_SECRET_KEY }}",
    "STATIC_ROOT": "{{ app_home }}/www/static",
    "APP_LOG": "{{ app_home }}/var/{{ app_name }}.log",
    "APP_VERSION": "{{ app_tag }}",
    "SYSLOG_SOCK": "/var/run/syslog",
    "API_BASE": ""
}
```

## Naming Conventions

This project follows the same naming pattern as other ACCESS Django applications:

| Component | serviceindex | portalcms |
|-----------|--------------|-----------|
| Database | `serviceindex1` | `portalcms1` |
| DB User | `serviceindex_django` | `portalcms_django` |
| App Name | `serviceindex_django` | `operations_portalcms_django` |

## Database Setup

### Local Development
```bash
# Use existing database or create new one
createdb portalcms1
psql portalcms1 -c "CREATE USER portalcms_django WITH PASSWORD 'yourpassword';"
psql portalcms1 -c "GRANT ALL PRIVILEGES ON DATABASE portalcms1 TO portalcms_django;"
psql portalcms1 -c "GRANT ALL PRIVILEGES ON SCHEMA public TO portalcms_django;"
```

### Production
Database and user will be created by infrastructure automation following the standard pattern.

## Deployment

In production, environment variables are set by:
1. Deployment scripts that substitute template variables (e.g., `{{ DJANGO_PASS }}`)
2. Container environment configuration
3. System environment files

The application automatically detects and uses environment variables, falling back to sensible defaults for development.
