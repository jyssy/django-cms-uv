# News System Setup

## Overview

This document explains how the Operations Portal manages news content using custom Django models rather than a third-party blog plugin.

## Why Custom Models?

This project uses custom `SystemStatusNews` and `IntegrationNews` models to keep the system simple and focused:

- **Simpler** - Only the fields you need (title, content, author, is_active)
- **Focused** - No unnecessary blog categories, tags, or SEO fields
- **Standard Django** - Uses Django's built-in permission system that works out of the box
- **No Complexity** - Avoids unnecessary initialization issues
- **Public Read** - News feeds are publicly readable; only create/edit requires permissions

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
cd Operations_PortalCMS_Django
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

## Creating News Items

### Via Django Admin

1. Log into the admin interface: `http://localhost:8000/admin`
2. Find **Operations Portal News** → select either **System Status News** or **Integration News**
3. Click **Add** to create a new item
4. Fill in the fields:
   - **Title** - The headline for the news item
   - **Content** - The news body (HTML supported)
   - **Author** - Select from available editors
   - **Is Active** - Check to make the item visible on the site
5. Click **Save**

The news will automatically appear on the appropriate feed page based on the model type.

## Viewing News

### System Status News
- **URL**: `/infrastructure_news_view`
- Shows all active SystemStatusNews items
- Most recent first

### Integration News
- **URL**: `/integration_news`
- Shows all active IntegrationNews items
- Most recent first

## Permissions

The system uses Django's standard permission framework:

- **add_systemstatusnews** - Create new system status news items
- **change_systemstatusnews** - Edit system status news items
- **delete_systemstatusnews** - Delete system status news items
- **view_systemstatusnews** - View system status news (public, always available)
- **add_integrationnews** - Create new integration news items
- **change_integrationnews** - Edit integration news items
- **delete_integrationnews** - Delete integration news items
- **view_integrationnews** - View integration news (public, always available)

## Model Fields

### SystemStatusNews
- **title** - News headline (CharField, max 200 chars)
- **content** - News body (TextField, HTML supported)
- **author** - Creator/editor (ForeignKey to User)
- **created_at** - Automatically set to creation timestamp
- **updated_at** - Automatically updated on changes
- **is_active** - Controls visibility on the site

### IntegrationNews
- **title** - News headline (CharField, max 200 chars)
- **content** - News body (TextField, HTML supported)
- **author** - Creator/editor (ForeignKey to User)
- **created_at** - Automatically set to creation timestamp
- **updated_at** - Automatically updated on changes
- **is_active** - Controls visibility on the site

## Displaying News in Templates

The news items can be accessed in templates via:

```django
{% load i18n %}

<!-- System Status News -->
{% with system_news=object.systemstatusnews_set.all %}
    {% for item in system_news %}
        <div class="news-item">
            <h3>{{ item.title }}</h3>
            <p>{{ item.content|safe }}</p>
            <small>By {{ item.author.get_full_name }} on {{ item.created_at|date:"M d, Y" }}</small>
        </div>
    {% endfor %}
{% endwith %}

<!-- Integration News -->
{% with integration_news=object.integrationnews_set.all %}
    {% for item in integration_news %}
        <div class="news-item">
            <h3>{{ item.title }}</h3>
            <p>{{ item.content|safe }}</p>
            <small>By {{ item.author.get_full_name }} on {{ item.created_at|date:"M d, Y" }}</small>
        </div>
    {% endwith %}
{% endwith %}
```

## Support

For questions or issues with the news system, refer to the main documentation or contact the ACCESS Operations team.
