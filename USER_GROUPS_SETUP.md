# User Groups and Permissions Setup

This document explains how to manage user permissions for the Operations Portal.

## Why Custom Models Instead of djangocms-blog?

This project uses custom `SystemStatusNews` and `IntegrationNews` models rather than djangocms-blog because:

- **Simpler** - No need for blog categories, tags, SEO fields, RSS feeds, etc.
- **Focused** - Only the fields you need (title, content, author, is_active)
- **Standard Django** - Uses Django's built-in permission system that works out of the box
- **No Complexity** - Avoids djangocms-blog's chicken-and-egg initialization issues
- **Public Read** - News feeds are publicly readable; only create/edit requires permissions

djangocms-blog is installed as a dependency but not enabled. The custom model approach gives you full control with less overhead.

## User Groups

Three groups are available for managing news content:

1. **System Status Editors** - Can add, edit, and delete System Status News only
2. **Integration News Editors** - Can add, edit, and delete Integration News only
3. **All News Editors** - Can manage both types of news

## Initial Setup

Run this command once to create the groups and assign permissions:

```bash
cd Operations_PortalCMS_Django
python manage.py setup_groups
```

## Adding Users to Groups

### Via Django Admin (Web Interface)

1. Go to: `http://localhost:8000/admin/` (or your production URL)
2. Log in with a superuser account
3. Click on **Groups** under the Authentication and Authorization section
4. Click on the group you want to manage (e.g., "System Status Editors")
5. In the "Available users" section, find the user you want to add
6. Double-click the user or select them and click the right arrow to move them to "Chosen users"
7. Click **Save**

### Via Django Shell (Command Line)

```bash
python manage.py shell
```

Then in the shell:

```python
from django.contrib.auth.models import User, Group

# Get the user
user = User.objects.get(username='john_doe')

# Get the group
group = Group.objects.get(name='System Status Editors')

# Add user to group
user.groups.add(group)

# Or add to multiple groups
integration_group = Group.objects.get(name='Integration News Editors')
user.groups.add(integration_group)

# Verify
print(f"User {user.username} is in groups: {', '.join([g.name for g in user.groups.all()])}")
```

## Creating New Users

### Via Django Admin

1. Go to `/admin/auth/user/add/`
2. Enter username and password
3. Click **Save and continue editing**
4. Scroll down to **Groups** and add the user to appropriate groups
5. Fill in additional fields (email, first name, last name, etc.)
6. Click **Save**

### Via Django Shell

```python
from django.contrib.auth.models import User, Group

# Create a new user
user = User.objects.create_user(
    username='jane_smith',
    email='jane@example.com',
    password='secure_password_here',
    first_name='Jane',
    last_name='Smith'
)

# Add to group
group = Group.objects.get(name='Integration News Editors')
user.groups.add(group)
```

## Permissions Breakdown

Each group has the following permissions:

### System Status Editors
- `operations_portalcms_django.add_systemstatusnews`
- `operations_portalcms_django.change_systemstatusnews`
- `operations_portalcms_django.delete_systemstatusnews`
- `operations_portalcms_django.view_systemstatusnews`

### Integration News Editors
- `operations_portalcms_django.add_integrationnews`
- `operations_portalcms_django.change_integrationnews`
- `operations_portalcms_django.delete_integrationnews`
- `operations_portalcms_django.view_integrationnews`

### All News Editors
- All permissions from both groups above

## How It Works in Code

The views use Django's `@permission_required` decorator:

```python
@login_required
@permission_required('operations_portalcms_django.add_systemstatusnews', raise_exception=True)
def add_system_status_news(request):
    # Only users with this permission can access this view
    ...
```

Templates can check permissions:

```django
{% if perms.operations_portalcms_django.add_systemstatusnews %}
    <a href="{% url 'operations_portalcms_django:add_system_status_news' %}">Add News</a>
{% endif %}
```

## Removing Users from Groups

### Via Admin
1. Go to the group in Django admin
2. Select the user in "Chosen users"
3. Click the left arrow to move them back to "Available users"
4. Click **Save**

### Via Shell
```python
from django.contrib.auth.models import User, Group

user = User.objects.get(username='john_doe')
group = Group.objects.get(name='System Status Editors')
user.groups.remove(group)
```

## Best Practices

1. **Principle of Least Privilege** - Only give users the permissions they need
2. **Use Groups** - Don't assign permissions directly to users; use groups
3. **Regular Audits** - Periodically review group memberships
4. **Document Changes** - Keep track of who was added/removed and when
5. **Superuser Caution** - Only grant superuser status to admins who need full access

## Troubleshooting

**User can't access add/edit pages:**
- Check they're logged in
- Verify they're in the correct group: `/admin/auth/user/{id}/`
- Run `python manage.py setup_groups` again if groups are missing

**Permission denied errors:**
- Check the view decorators match the user's permissions
- Verify group permissions at `/admin/auth/group/`

**Changes not taking effect:**
- User may need to log out and back in
- Check Django's session cache settings
