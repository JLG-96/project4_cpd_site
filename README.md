# CPD Yr Wyddgrug Official Website

## Description
A full-stack web application where users can keep up to date with local club **CPD Yr Wyddgrug**. Users can see **results, fixtures, league standings, comments from the managers, and team details**. 

- **Managers** can post **fixtures, training sessions**, and **request player availability**.
- **Players** can **view** the same information and **comment on availability** for fixtures and training sessions.

## Current Features

### General Setup:
- Initial **Django project** setup completed.
- **Team app** created for managing **players and fixtures**.
- **Media file configuration** set up for uploading and displaying **team logos**.

### Homepage Features:
- Displays the **upcoming fixture** dynamically.
- **League table preview** (currently using placeholder data).
- **Manager’s comment/news section**.
- **Latest result** now also featured alongside the next fixture.

### Results Page:
- **Dedicated page for past match results**.
- Displays **opponent, date, time, location**, and **final score** if the match is completed.
- Fixed **"Home/Away" display** in fixture listings.

### Bug Fixes & Improvements:
- **Renamed** `"is played"` field to `"match completed"` for clarity.
- Fixed **incorrect template syntax errors** in results and homepage views.
- Ensured **"Match Completed" field** now correctly updates past matches.

## Future Features:
- **Dynamic League Table** - Fetch real-time standings instead of placeholder data.
- **Authentication & Role-Based Access** - Restrict team management features to **managers** and **players**.
- **User Interaction** - Allow **players** to **comment on training availability** and **fixture selection**.

## Setup and Configuration

### Media Files Setup
To handle media files (e.g., **team logos**), ensure you’ve configured the following in `settings.py`:
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```
Don't forget to add a **static route** in `urls.py` to serve media files during development.

**Example for `urls.py`:**
```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('team.urls')),  # Main app URLs
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---