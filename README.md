# CPD Yr Wyddgrug Official Website

## Description
A full-stack web application where users can keep up to date with local club CPD Yr Wyddgrug. Users can see results, fixtures, league standings, comments from the managers and the team. Managers will be able to post fixtures, training and request availability. Players will be able to view the same thing but will be able to comment on availability for fixtures and training sessions. 

## Current Features
- Initial Django project setup completed. 
- Team app created for managing players and fixtures.
- Team model includes details like manager, home ground, founded year, and stats for league tracking.
- Display of team information via a simple view (`team_list`) that lists team details.
- Media file configuration set up for uploading and displaying team logos.
- Homepage added with:
    - Upcoming fixture display
    - League table preview
    - Manger's comment / news section.

## Future Features
- Models for team and fixtures
- Authentication and role-based access
- User interaction with posts and comments

## Setup and Configuration
- To handle media files (e.g., team logos), ensure you’ve configured the following in your `settings.py`:
    - `MEDIA_URL = '/media/'`
    - `MEDIA_ROOT = BASE_DIR / 'media'`
    - Don't forget to add a static route in `urls.py` to serve media files during development.
  
  Example for `urls.py`:
  ```python
  from django.conf import settings
  from django.conf.urls.static import static
  
  urlpatterns = [
      # Other paths
      path('admin/', admin.site.urls),
      path('teams/', include('team.urls')),  # Add other app URLs here
  ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
