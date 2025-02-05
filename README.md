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
    - Manager's comment / news section.
- Renamed "is played" to "match completed" for clarity.
- Recent result now featured on homepage.
- Created a **results page** that only shows completed fixtures.
- Created a **fixtures page** that only shows remaining upcoming fixtures.
- Implemented **base.html** template for consistent layout across all pages.

## Future Features
- Models for team and fixtures
- Authentication and role-based access
- User interaction with posts and comments
- Linking league position to fixtures for **importance visibility**

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
  ```

## Testing
### **Manual Testing Performed**
- **Homepage loads correctly** with:
  - Upcoming fixture (or displays "No upcoming fixtures" if none exist).
  - Latest result (or displays "No past results available" if none exist).
  - League table preview.
  - Manager's comment section.

- **Navigation works properly**:
  - Clicking on "Fixtures" displays **only** upcoming fixtures.
  - Clicking on "Results" displays **only** completed matches.

- **Base template (`base.html`) applied consistently** to all pages.

### **Edge Cases & Error Handling**
- **What happens if no fixtures are scheduled?**
  - Displays "No upcoming fixtures." 
- **What happens if no results are recorded?**
  - Displays "No past results available."
- **What happens if a fixture is missing required data (e.g., time, location)?**
  - Handled correctly without crashing.

  ### ✅ **Database Reset and Migration Fix**
- **Issue:** Encountered `OperationalError: no such column: team_fixture.opponent_id` due to old database structure conflicting with new migrations.
- **Fix:** 
  1. Deleted `db.sqlite3` to reset the database.
  2. Removed and reapplied migrations for the `team` app.
  3. Created a new superuser for admin access.
  4. Verified all functionality still works after the reset.

- **Testing Confirmation:**
  - ✅ Homepage still correctly displays **upcoming fixtures, latest result, league table, and manager’s comment.**
  - ✅ **Fixtures page** correctly lists **only** future matches.
  - ✅ **Results page** correctly lists **only** completed matches.
  - ✅ Admin panel is working, and team/fixtures can be managed as expected.

### **Known Issues**
- **[FIXED]** Fixtures were not displaying correctly due to a migration issue where `opponent` changed from a `CharField` to a `ForeignKey`. 
  - **Fix:** We removed old migrations, reset the migration history, and applied a fresh migration.
  - **Tested:** Fixtures now load correctly in `/fixtures/`, and opponents display properly.