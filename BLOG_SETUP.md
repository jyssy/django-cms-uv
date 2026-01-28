# Blog Plugin Installation Notes

## Known Issue with djangocms-blog

The `djangocms-blog` plugin has an initialization issue where it tries to query the database before migrations have run. This causes a chicken-and-egg problem during initial setup.

## Workaround

The blog plugin and its dependencies are installed, but the blog app itself is commented out in `settings.py`.

To enable the blog after initial setup:

### 1. Run Initial Migrations (Already Done)
```bash
cd djangocmsjoy
uv run python manage.py migrate
```

### 2. Uncomment Blog in settings.py

Edit `djangocmsjoy/settings.py` and uncomment the blog line:

```python
INSTALLED_APPS = [
    # ... other apps ...
    'aldryn_apphooks_config',
    'djangocms_blog',  # <- Uncomment this line
]
```

### 3. Run Blog Migrations
```bash
uv run python manage.py migrate
```

### 4. Restart Development Server
```bash
uv run python manage.py runserver
```

## Alternative: Use Custom News Plugins

The project already has working custom news plugins that don't have this initialization issue:
- `SystemStatusNewsItemPlugin`
- `IntegrationNewsItemPlugin`

These are simpler and work immediately without the blog setup complexity.

## Blog Features Available After Setup

Once enabled, djangocms-blog provides:
- Blog posts with categories and tags
- Author profiles
- SEO meta tags
- RSS feeds
- Archive views
- Multi-language support
- Frontend editing via Django CMS toolbar

## Status

✅ Dependencies installed  
✅ Initial migrations run  
⚠️ Blog app commented out (prevents initialization error)  
📝 To enable: Follow steps above

---

**Framework drafted by Claude Sonnet 4.5 (January 28, 2026)**  
