# Operations Portal CMS - Permissions & Authentication Guide

**Last Updated**: February 10, 2026  
**Django Version**: 5.2  
**Authentication**: CILogon + Django Allauth

---

## Table of Contents
1. [Overview](#overview)
2. [Permission Groups](#permission-groups)
3. [Template Permission Checks](#template-permission-checks)
4. [View Permission Decorators](#view-permission-decorators)
5. [CILogon Authentication Flow](#cilogon-authentication-flow)
6. [Testing Locally](#testing-locally)
7. [Production Deployment](#production-deployment)
8. [Troubleshooting](#troubleshooting)

---

## Overview

The Operations Portal CMS uses **granular permission-based access control** that separates content editing permissions from administrative access. This allows non-staff users to manage specific content types without accessing the Django admin interface.

### Key Principles

- **View-level protection**: All protected views use `@permission_required` decorators
- **Template-level UI**: Templates check specific permissions using `perms.app_label.permission_codename`
- **Group-based assignment**: Users are assigned to groups that grant specific permissions
- **Staff separation**: Content editors don't need `is_staff=True` to edit content

---

## Permission Groups

Three custom permission groups are automatically created by the `setup_groups.py` management command:

### 1. System Status Editors

**Use Case**: Users who manage infrastructure status announcements, outages, maintenance windows

**Permissions** (4 total):
- `operations_portalcms_django.add_systemstatusnews`
- `operations_portalcms_django.change_systemstatusnews`
- `operations_portalcms_django.delete_systemstatusnews`
- `operations_portalcms_django.view_systemstatusnews`

**Can Access**:
- `/infrastructure-news/` (view all system status news)
- `/infrastructure-news/add/` (publish new system status news)
- `/infrastructure-news/update/<id>/` (edit existing items)
- Delete button on edit forms

**Cannot Access**:
- Django admin interface (`/admin/`)
- Integration news management
- CMS page editing

---

### 2. Integration News Editors

**Use Case**: Users who manage integration roadmaps, resource provider communications

**Permissions** (4 total):
- `operations_portalcms_django.add_integrationnews`
- `operations_portalcms_django.change_integrationnews`
- `operations_portalcms_django.delete_integrationnews`
- `operations_portalcms_django.view_integrationnews`

**Can Access**:
- `/integration-news/` (view all integration news)
- `/integration-news/add/` (publish new integration news)
- `/integration-news/update/<id>/` (edit existing items)
- Delete button on edit forms

**Cannot Access**:
- Django admin interface (`/admin/`)
- System status news management
- CMS page editing

---

### 3. All News Editors

**Use Case**: Trusted users who manage both system status and integration news

**Permissions** (8 total):
- All permissions from System Status Editors
- All permissions from Integration News Editors

**Can Access**:
- Everything from both groups above

**Cannot Access**:
- Django admin interface (unless separately granted `is_staff=True`)

---

## Template Permission Checks

### Implementation Pattern

Templates use Django's built-in `perms` context variable to check permissions:

```django
{# Check if user can add system status news #}
{% if perms.operations_portalcms_django.add_systemstatusnews %}
    <a href="{% url 'operations_portalcms_django:add_system_status_news' %}">
        Publish new news
    </a>
{% endif %}

{# Check if user can change/edit system status news #}
{% if perms.operations_portalcms_django.change_systemstatusnews %}
    <a href="{% url 'operations_portalcms_django:update_system_status_news' news.id %}">
        Edit
    </a>
{% endif %}

{# Check if user can delete system status news #}
{% if perms.operations_portalcms_django.delete_systemstatusnews %}
    <button type="submit" name="delete" class="btn btn-danger">Delete</button>
{% endif %}
```

### Templates Updated with Granular Permissions

| Template File | Permission Check | Controls |
|--------------|------------------|----------|
| `infrastructure_news.html` | `perms.operations_portalcms_django.add_systemstatusnews` | "Publish new news" button |
| `infrastructure_news.html` | `perms.operations_portalcms_django.change_systemstatusnews` | "Edit" button per item |
| `integration_news.html` | `perms.operations_portalcms_django.add_integrationnews` | "Publish new news" button |
| `integration_news.html` | `perms.operations_portalcms_django.change_integrationnews` | "Edit" button per item |
| `update_system_status_news.html` | `perms.operations_portalcms_django.delete_systemstatusnews` | "Delete" button |
| `update_integration_news.html` | `perms.operations_portalcms_django.delete_integrationnews` | "Delete" button |
| `update_infrastructure_news.html` | `perms.operations_portalcms_django.delete_systemstatusnews` | "Delete" button |

### Why Not `is_staff`?

**Old Approach** (❌ Don't use):
```django
{% if user.is_staff %}
    <a href="...">Edit</a>
{% endif %}
```

**Problems**:
- Forces all editors to be "staff" users
- Staff users can access `/admin/` interface
- No granular control over who can edit what
- Confusing for users who only manage content

**New Approach** (✅ Use this):
```django
{% if perms.operations_portalcms_django.change_integrationnews %}
    <a href="...">Edit</a>
{% endif %}
```

**Benefits**:
- Non-staff users can edit content
- Granular control (system vs integration news)
- Admin interface remains hidden from content editors
- Clear separation of concerns

---

## View Permission Decorators

### Protection Pattern

All content management views are protected with two decorators:

```python
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse_lazy

@login_required
@permission_required('operations_portalcms_django.add_systemstatusnews', 
                     login_url=reverse_lazy('operations_portalcms_django:unprivileged'))
def add_system_status_news(request):
    """Add new system and infrastructure status news item"""
    # View logic here
```

### How It Works

1. **`@login_required`**: Redirects anonymous users to `/accounts/login/`
2. **`@permission_required`**: Checks if logged-in user has the specific permission
3. **`login_url`**: If permission denied, redirects to `/unprivileged/` (custom error page)

### Protected Views

| View Function | Required Permission | URL Pattern |
|--------------|--------------------|--------------------|
| `add_system_status_news` | `add_systemstatusnews` | `/infrastructure-news/add/` |
| `update_system_status_news` | `change_systemstatusnews` | `/infrastructure-news/update/<pk>/` |
| `add_integration_news` | `add_integrationnews` | `/integration-news/add/` |
| `update_integration_news` | `change_integrationnews` | `/integration-news/update/<pk>/` |

### Unprivileged Error Page

When a user lacks permission, they're redirected to `/unprivileged/` which displays:
- "You are not authorized to access this part of the site."
- "Back to Home" button
- Template: `templates/web/unprivileged.html`

---

## CILogon Authentication Flow

### Initial Login (First Time)

```
1. User clicks "Login with CILogon"
   ↓
2. Redirected to CILogon authentication provider
   ↓
3. User authenticates via their institution
   ↓
4. CILogon redirects back to Django with user info
   ↓
5. Django Allauth creates User account:
   - username: from CILogon
   - email: from CILogon
   - is_authenticated: True
   - is_staff: False (default)
   - is_superuser: False (default)
   - groups: [] (empty)
   ↓
6. User lands on homepage (/)
   ↓
7. User has NO permissions (can only view public content)
```

### Manual Permission Assignment

**After CILogon creates the account, an administrator must:**

1. Log into Django Admin (`/admin/`)
2. Navigate to **Authentication and Authorization** → **Users**
3. Find the CILogon user by username/email
4. Click to edit
5. Scroll to **Groups** section
6. Select appropriate group(s):
   - "System Status Editors" (for infrastructure news)
   - "Integration News Editors" (for integration news)
   - "All News Editors" (for both)
7. Save user

**Optional**: Check `Staff status` if user should access admin interface

### Subsequent Logins

```
1. User clicks "Login with CILogon"
   ↓
2. Authenticates via CILogon
   ↓
3. Django finds existing User account
   ↓
4. Updates user info from CILogon (email, name, etc.)
   ↓
5. User groups/permissions remain intact
   ↓
6. User sees buttons/features based on their assigned permissions
```

---

## Testing Locally

### Test as Superuser (Your Current Setup)

**User**: `admin` / `admin123`

```bash
# Log in at /admin/ or /accounts/login/
# Superusers have ALL permissions automatically
# You'll see all buttons and can access everything
```

**Use Case**: Full administrative testing, setup, and configuration

---

### Test as Content Editor (Non-Staff)

**Create test user:**

1. Navigate to `/admin/auth/user/add/`
2. Create user:
   - Username: `testintegration`
   - Password: `testpass123`
   - **Do NOT check** "Staff status"
   - **Do NOT check** "Superuser status"
3. Save

4. Edit user → Scroll to "Groups"
5. Select: "Integration News Editors"
6. Save

**Test the user:**

1. Log out of admin account
2. Log in as `testintegration` / `testpass123`
3. Navigate to `/integration-news/`

**Expected Results**:
- ✅ Sees "Publish new news" button
- ✅ Sees "Edit" buttons on integration news items
- ✅ Can add/edit/delete integration news
- ❌ Does NOT see admin navigation bar
- ❌ Cannot access `/admin/` (403 Forbidden)
- ❌ Does NOT see system status news add/edit buttons
- ❌ Cannot access `/infrastructure-news/add/` (redirected to unprivileged)

---

### Test Permission Denied Flow

**As non-staff user with integration permissions:**

1. Try to access: `/infrastructure-news/add/`
2. Expected: Redirected to `/unprivileged/`
3. See error message: "You are not authorized..."
4. Click "Back to Home" → Returns to `/`

---

## Production Deployment

### Pre-Deployment Checklist

- [x] Custom permission groups created (`python manage.py setup_groups`)
- [x] Templates use `perms.*` instead of `is_staff`
- [x] Views protected with `@permission_required` decorators
- [x] CILogon redirect URLs configured in CILogon portal
- [x] Django Allauth installed and configured
- [ ] Document permission assignment process for admins

### Initial Setup on Production Server

```bash
# 1. Run migrations
python manage.py migrate

# 2. Create permission groups
python manage.py setup_groups

# 3. Create superuser for administrative tasks
python manage.py createsuperuser

# 4. Collect static files
python manage.py collectstatic --noinput
```

### CILogon Configuration Required

**In CILogon Portal** (https://cilogon.org):
1. Register your production domain
2. Add authorized redirect URLs:
   - `https://your-domain.org/accounts/cilogon/login/callback/`
3. Note your CILogon Client ID and Secret

**In Django Settings** (`settings.py`):
```python
SOCIALACCOUNT_PROVIDERS = {
    'cilogon': {
        'APP': {
            'client_id': 'YOUR_CILOGON_CLIENT_ID',
            'secret': 'YOUR_CILOGON_SECRET',
            'key': ''
        }
    }
}
```

### Post-Deployment User Management

**For each CILogon user that needs editing permissions:**

1. Have user log in via CILogon (creates account)
2. Admin logs into `/admin/`
3. Navigate to Users → Find CILogon user
4. Assign to appropriate group(s)
5. Save

**Group Assignment Guidelines**:
- **System Status Editors**: Users who manage outages, maintenance, status updates
- **Integration News Editors**: Resource providers, integration coordinators
- **All News Editors**: Trusted users who manage all communications
- **Staff Status**: Only for users who need Django admin access

---

## Troubleshooting

### User Can't See Edit Buttons

**Symptom**: User is authenticated but doesn't see "Publish new news" or "Edit" buttons

**Diagnosis**:
1. Check if user is assigned to correct group:
   ```bash
   python manage.py shell
   >>> from django.contrib.auth.models import User
   >>> user = User.objects.get(username='problematic_user')
   >>> user.groups.all()
   # Should show group membership
   >>> user.get_all_permissions()
   # Should show specific permissions
   ```

2. Verify group has correct permissions:
   ```bash
   >>> from django.contrib.auth.models import Group
   >>> group = Group.objects.get(name='Integration News Editors')
   >>> group.permissions.all()
   # Should show 4 permissions for integrationnews
   ```

**Solutions**:
- Assign user to correct group via `/admin/auth/user/`
- Re-run `python manage.py setup_groups` if groups are missing
- Check templates are using `perms.*` not `is_staff`

---

### User Gets "Not Authorized" Error

**Symptom**: User redirected to `/unprivileged/` when clicking add/edit

**Diagnosis**:
```python
# Check exact permission name
python manage.py shell
>>> from django.contrib.contenttypes.models import ContentType
>>> from django.contrib.auth.models import Permission
>>> ct = ContentType.objects.get(app_label='operations_portalcms_django', model='integrationnews')
>>> Permission.objects.filter(content_type=ct)
# Verify permission codenames match decorator requirements
```

**Solutions**:
- Ensure permission decorator matches exactly: `operations_portalcms_django.add_integrationnews`
- Verify user group has been saved (refresh user in admin)
- Check `@permission_required` decorator spelling in views

---

### CILogon Login Fails

**Symptom**: Error after CILogon authentication redirect

**Common Causes**:
1. **Redirect URL mismatch**: Production URL not registered in CILogon
2. **Client ID/Secret wrong**: Check `settings.py` configuration
3. **SSL certificate issues**: CILogon requires HTTPS in production

**Debug Steps**:
```bash
# Check Allauth configuration
python manage.py shell
>>> from allauth.socialaccount.models import SocialApp
>>> SocialApp.objects.all()
# Should show CILogon app with correct credentials
```

**Solutions**:
- Verify redirect URL in CILogon portal matches production domain
- Ensure `ALLOWED_HOSTS` in `settings.py` includes production domain
- Check Django logs for specific error messages

---

### Superuser Doesn't See Buttons

**Symptom**: Even superuser doesn't see edit buttons

**Diagnosis**: Template permission check syntax error

```django
{# WRONG - missing app label #}
{% if perms.add_integrationnews %}

{# CORRECT - full permission path #}
{% if perms.operations_portalcms_django.add_integrationnews %}
```

**Solutions**:
- Verify template uses full permission path: `app_label.permission_codename`
- Check for typos in permission names
- Clear template cache: `python manage.py collectstatic --clear`

---

## Permission Matrix Reference

### Quick Reference Table

| User Type | is_staff | is_superuser | Groups | Can Edit Integration News | Can Edit System Status | Can Access Admin |
|-----------|----------|--------------|--------|---------------------------|------------------------|------------------|
| Anonymous | - | - | - | ❌ | ❌ | ❌ |
| CILogon (new) | False | False | None | ❌ | ❌ | ❌ |
| Integration Editor | False | False | Integration News Editors | ✅ | ❌ | ❌ |
| System Editor | False | False | System Status Editors | ❌ | ✅ | ❌ |
| All News Editor | False | False | All News Editors | ✅ | ✅ | ❌ |
| Staff Editor | True | False | Integration News Editors | ✅ | ❌ | ✅ (limited) |
| Superuser | True | True | Any | ✅ | ✅ | ✅ (full) |

---

## Security Best Practices

### 1. Principle of Least Privilege

- Assign users to the **most restrictive group** that meets their needs
- Don't grant `is_staff` unless user needs admin access
- Don't grant `is_superuser` unless user is a system administrator

### 2. Regular Audits

```bash
# List all staff users
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.filter(is_staff=True).values_list('username', 'email')

# List all superusers
>>> User.objects.filter(is_superuser=True).values_list('username', 'email')

# Review group memberships
>>> from django.contrib.auth.models import Group
>>> for group in Group.objects.all():
...     print(f"\n{group.name}:")
...     for user in group.user_set.all():
...         print(f"  - {user.username}")
```

### 3. Permission Group Maintenance

- Run `python manage.py setup_groups` after:
  - Adding new models
  - Changing permission requirements
  - Fresh database migrations

### 4. CILogon Account Deactivation

When users should no longer have access:
1. Navigate to `/admin/auth/user/`
2. Find user account
3. **Uncheck "Active"** (don't delete - preserves audit trail)
4. Remove from all groups
5. Save

---

## Appendix: Permission Codenames

### System Status News (SystemStatusNews Model)

| Codename | Full Permission | Description |
|----------|----------------|-------------|
| `add_systemstatusnews` | `operations_portalcms_django.add_systemstatusnews` | Add new system status news |
| `change_systemstatusnews` | `operations_portalcms_django.change_systemstatusnews` | Edit existing system status news |
| `delete_systemstatusnews` | `operations_portalcms_django.delete_systemstatusnews` | Delete system status news |
| `view_systemstatusnews` | `operations_portalcms_django.view_systemstatusnews` | View system status news |

### Integration News (IntegrationNews Model)

| Codename | Full Permission | Description |
|----------|----------------|-------------|
| `add_integrationnews` | `operations_portalcms_django.add_integrationnews` | Add new integration news |
| `change_integrationnews` | `operations_portalcms_django.change_integrationnews` | Edit existing integration news |
| `delete_integrationnews` | `operations_portalcms_django.delete_integrationnews` | Delete integration news |
| `view_integrationnews` | `operations_portalcms_django.view_integrationnews` | View integration news |

---

**End of Document**
