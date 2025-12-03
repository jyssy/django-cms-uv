# ACCESS CI Header/Footer Integration By Claude Sonnet 4.6

## Overview
This Django CMS application now includes the standard ACCESS CI organizational header and footer components from the [access-ci-org/access-ci-ui](https://github.com/access-ci-org/access-ci-ui) repository.

## What Was Implemented

### 1. Base Template (templates/base.html)
Created a comprehensive base template that includes:

**Header Components:**
- NSF logo (linked to nsf.gov)
- ACCESS logo (linked to access-ci.org)
- Divider between logos
- CMS page navigation menu (teal background)
- Responsive design (mobile and desktop layouts)

**Footer Components:**
- NSF award information with links to all 5 grants
- NSF disclaimer text
- Contact ACCESS link
- Social media links (X/Twitter, YouTube, Facebook, LinkedIn)
- Persona links (Researchers, Educators, Graduate Students, etc.)
- Footer logos (smaller versions)
- Utility links (Acceptable Use, Acknowledging ACCESS, Code of Conduct, Privacy Policy)

### 2. Branding & Design
**ACCESS CI Color Palette:**
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
--width: 1200px (max container width)
```

**Typography:**
- Font family: "Archivo" from Google Fonts
- Fallback: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif

**Responsive Breakpoints:**
- Mobile: < 900px
- Desktop: ≥ 900px

### 3. Updated Templates
**page.html** - Basic CMS page template:
- Now extends base.html
- Uses `{% block content %}` for page-specific content
- Includes page title and content placeholder

**feature.html** - CMS page with feature section:
- Now extends base.html
- Includes feature placeholder (teal background)
- Includes standard content placeholder

### 4. Assets
**Downloaded Logo Images:**
- `static/djangocmsjoy/img/nsf-logo.png` (28KB)
- `static/djangocmsjoy/img/access-logo.svg` (7KB)

**Existing Assets:**
- `static/djangocmsjoy/img/favicon.ico` (ACCESS favicon)
- `static/djangocmsjoy/style-serviceindex.css` (Custom branding CSS)
- `static/djangocmsjoy/img/ACCS050322_ACCESS_Brand_Operations-RGB.png` (ACCESS logo)

## File Structure
```
djangocmsjoy/
├── templates/
│   ├── base.html                    # NEW: Base template with header/footer
│   ├── page.html                    # UPDATED: Extends base.html
│   ├── feature.html                 # UPDATED: Extends base.html
│   └── djangocmsjoy/
│       ├── system_news.html
│       ├── resource_news.html
│       └── ...
└── static/djangocmsjoy/
    ├── style-serviceindex.css
    └── img/
        ├── favicon.ico
        ├── nsf-logo.png             # NEW: From ACCESS CI UI repo
        ├── access-logo.svg          # NEW: From ACCESS CI UI repo
        └── ACCS050322_ACCESS_Brand_Operations-RGB.png
```

## Header Layout

```
┌────────────────────────────────────────────────────────────┐
│  [NSF Logo]  |  [ACCESS Logo]                              │
└────────────────────────────────────────────────────────────┘
┌────────────────────────────────────────────────────────────┐
│  Navigation: [Home] [Page 1] [Page 2] ...                  │
└────────────────────────────────────────────────────────────┘
```

## Footer Layout

```
┌────────────────────────────────────────────────────────────┐
│  ACCESS is supported by NSF under awards:                  │
│  #2138259, #2138286, #2138307, #2137603, #2138296         │
│                                                             │
│  Any opinions... do not necessarily reflect NSF views.     │
│                                                             │
│  Contact ACCESS                                            │
│  [X] [YouTube] [Facebook] [LinkedIn]                       │
│                                                             │
│  For:                                                       │
│  • Researchers                                             │
│  • Educators                                               │
│  • Graduate Students                                       │
│  • Resource Providers                                      │
│  • CI Community                                            │
├────────────────────────────────────────────────────────────┤
│  [NSF Logo] | [ACCESS Logo]                                │
│  Acceptable Use | Acknowledging ACCESS | Code of Conduct   │
│  Privacy Policy                                            │
└────────────────────────────────────────────────────────────┘
```

## Features Implemented

### Responsive Design
- **Mobile (< 900px):**
  - Smaller logos (NSF: 49px, ACCESS: 23px height)
  - Vertical footer layout
  - Stacked elements
  
- **Desktop (≥ 900px):**
  - Larger logos (NSF: 82px, ACCESS: 253px width)
  - Horizontal footer layout
  - Side-by-side elements

### Navigation
- Django CMS menu system integrated with `{% show_menu 0 100 100 100 %}`
- Teal background (--teal-700: #1A5B6E)
- White text with hover effects

### Accessibility
- Alt text on all images
- Semantic HTML structure
- Proper link colors and hover states
- Container max-width for readability

## Testing

**Server Command:**
```bash
cd /Users/jelambeadmin/Documents/access-sysops/django-cms-uv
uv run python djangocmsjoy/manage.py runserver
```

**Access:**
- Development server: http://127.0.0.1:8000/
- Admin panel: http://127.0.0.1:8000/admin/

**What to Check:**
1. ✅ NSF and ACCESS logos display in header
2. ✅ Navigation menu shows CMS pages
3. ✅ Footer displays all NSF awards with links
4. ✅ Social media icons link correctly
5. ✅ Persona links work
6. ✅ Utility links in footer
7. ✅ Responsive layout (test mobile/desktop)
8. ✅ Custom ACCESS CSS still applies
9. ✅ CMS toolbar appears when logged in
10. ✅ Page editing works normally

## Static Files

After any template or static file changes, run:
```bash
uv run python djangocmsjoy/manage.py collectstatic --noinput
```

This copies files from `static/` to `staticfiles/` for serving.

## Django CMS Integration

The base template includes:
- `{% cms_toolbar %}` - CMS editing toolbar (top of page)
- `{% show_menu 0 100 100 100 %}` - Page navigation menu
- `{% block content %}` - Area for page templates to fill
- `{% render_block "css" %}` and `{% render_block "js" %}` - For Sekizai

## Customization

To customize the header/footer:

1. **Change branding colors:** Edit CSS variables in `base.html` `<style>` section
2. **Modify footer text:** Edit footer section in `base.html`
3. **Add/remove links:** Update footer links in `base.html`
4. **Change navigation style:** Edit `.cms-nav` CSS in `base.html`

## References

- ACCESS CI UI Repository: https://github.com/access-ci-org/access-ci-ui
- NSF Awards:
  - [#2138259](https://www.nsf.gov/awardsearch/show-award/?AWD_ID=2138259)
  - [#2138286](https://www.nsf.gov/awardsearch/show-award/?AWD_ID=2138286)
  - [#2138307](https://www.nsf.gov/awardsearch/show-award/?AWD_ID=2138307)
  - [#2137603](https://www.nsf.gov/awardsearch/show-award/?AWD_ID=2137603)
  - [#2138296](https://www.nsf.gov/awardsearch/show-award/?AWD_ID=2138296)

## Notes

- The ACCESS CI UI components are React-based, but this implementation uses pure HTML/CSS extracted from their component library
- Django template comments `{# #}` inside `<style>` tags may show linter warnings but don't affect functionality
- All external links open in the same window (standard web behavior)
- Logo images are served as static files through Django's static file system

---

**Integration Date:** December 3, 2025  
**Django CMS Version:** 5.0  
**Django Version:** 5.2.9  
**Python Version:** 3.13
