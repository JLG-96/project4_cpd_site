# CPD Yr Wyddgrug Official Website

## Description
CPD Yr Wyddgrug Official Website is a full-stack web application designed to keep users updated with the latest information about the local football club, CPD Yr Wyddgrug. The site provides a comprehensive platform where users can view match fixtures, results, league standings, team news and updates from the manager. It features distinct dashboards for managers and players: managers can view player avaialbility for upcoming games, post match updates, training reminders and general team announcements straight to the players, whilst players can confirm their availability for upcoming fixtures and reply to the managers messages with comments. Built using Django following an MVC framework approach, the application leverages modern web technologies to ensure a responsive, user-friendly experience.

## Design
- Initial plan, wireframe: ![screenshot](screenshots\img8.png)
This is the initial design. Showing the homepage with the various sections implemented into it. Throughout building of the homepage did the ideas for the separate player / manager dashboards develop.

## Current Features
- **Robust Django Project Setup & Team App Creation**
  - Organized project structure following the MVC pattern.
  
- **Comprehensive Team Model**
  - Captures essential team details: manager, home ground, founded year, and team logo.
  - Tracks league statistics including matches played, wins, draws, losses, goals for/against, and points.
  
- **Media & Static File Handling**
  - Integrated Cloudinary for dynamic media storage of team logos and other uploaded images.
  - Configured Whitenoise for efficient serving of static files.
  
- **Responsive Homepage**
  - Features a team banner displaying club logo, team name, manager details, home ground, and founding year.
  - Shows an upcoming fixture section with relevant opponent logos and match details.
  - Includes a league table preview with CPD Yr Wyddgrug highlighted.
  - Displays the manager's latest comment/news section.
  
- **Dedicated Fixtures & Results Pages**
  - Fixtures Page: Lists only upcoming matches.
  - Results Page: Displays only completed matches.
  
- **Dynamic League Table**
  - Automatically updates team standings based on match results.
  - Sorted primarily by points and secondarily by goal difference.
  
- **User Authentication & Role-Based Access**
  - Secure login/logout system integrated into the navbar.
  - Role differentiation ensuring managers access a Manager Dashboard while players have a Player Dashboard.
  - Enforced profile creation for all users prior to accessing dashboards.


### User Authentication & Profiles
- **Secure Login/Logout System**
  - Integrated into the navbar for easy access.
  - User accounts (both Players and Managers) are created and managed by an admin (public registration is disabled).

- **Role-Based Access Control**
  - Managers are granted exclusive access to a dedicated Manager Dashboard.
  - Players have their own Player Dashboard tailored to their needs.


### Manager & Player Dashboards
- Both dashboards recieve notifications with the newest one being tagged as "NEW".

- **Manager Dashboard**
  - Allows managers to post updates, match information, and team news straight to the players.
  - Provides tools to manage fixtures based on player availability and can communicate club announcements with any user.
  - Gets notified when a player has changed their availability or commented on a message.
  
- **Player Dashboard**
  - Enables players to view upcoming fixtures and confirm their availability.
    - Colour of fixture cards reflects players avaialability for easier viewing.
  - Can write comments back to the manager. 
  - Gets notified when the manager has sent a message.
  
- **Access Restrictions & Profile Enforcement**
  - User accounts (both players and managers) are created and managed exclusively by an administrator (no public registration).

### Fixtures & Results System
- **Dynamic Match Result Recording**
  - Match outcomes (wins, draws, and losses) are automatically calculated based on inputted game data and recorded on the homepage to reflect the most recent result. All results are stored in the results page.
- **Fixture Model Enhancements:**
  - Replaced the `is_played` field with a more descriptive `match_completed` field.
  - Corrected opponent assignment to ensure fixtures accurately reflect the competing teams.
  - Improved goal tracking to reliably record and update scores for both teams.

### Deployment
- **Cloud Deployment & Performance Optimization**
  - Finalised deployment to a cloud platform with optimized handling for static and media files.

## Upcoming Features
- **Enhanced User Analytics**
  - Implement detailed reporting and insights on team performance, match statistics, and user engagement.
  - Player pictures could be uploaded and integrated to the homepage. Statistics for each player and the posting of the man of the match that users could vote for.
  - A possible 'Meet the players' page, providing sporting information about the players but also some personal details for the users to enjoy.
- **Advanced Notification System**
  - Build real-time, push notifications for match updates, team news, and player availability alerts.
- **Calender functionality**
  - Potential to integrate a calendar into both dashboards to more clearly show fixtures and to include scheduled training sessions. Players can set their availability direct to the calendar. Can be sent reminders of important upcoming dates.
- **Contact us section**
  - A form page for other teams to fill out to get in contact to schedule friendly games. Other players to get in touch about reequesting to join etc.
- League table to automatically update upon addition of results rather than manually having to do it. 
- Results to show goalscores names and any players that got an assist / yellow / red card.


## Bugs Fixed & Issues Resolved

### League Table Not Updating
**Issue:** Standings were resetting to zero after every update.  
- **Cause:** Incorrect query filtering and a missing opponent-team link in calculations.  
- **Fix:** Refactored `calculate_standings()` to correctly sum matches (both home and away).  
- **Result:** Teams now track points, matches, goals, and rankings accurately.

### Fixtures Not Displaying
**Issue:** Some fixtures were not appearing on the homepage.  
- **Cause:** The query was filtering using only one side of the match (either home or opponent) instead of both.  
- **Fix:** Updated the query to check conditions for both the home team and opponent.  
- **Result:** Upcoming fixtures and recent results now load properly.

### Reverse URL Errors
**Issue:** Navigation links broke due to mismatched URL names (e.g., using "home" instead of "homepage").  
- **Fix:** Revised `urls.py` and updated all template links to reference the correct view names.  
- **Result:** Navigation now functions seamlessly across the site.

### Logout Not Working
**Issue:** The logout link was broken due to an incorrect authentication setup.  
- **Fix:** Connected Django’s built-in `LogoutView` and updated the navbar accordingly.  
- **Result:** Users can now log out and log back in successfully.

### Static Files Not Loading on Deployment
**Issue:** CSS and other static assets were not served on Heroku.  
- **Cause:** The environment variable `DISABLE_COLLECTSTATIC` was set and/or Whitenoise was not properly configured.  
- **Fix:** Removed `DISABLE_COLLECTSTATIC` from Heroku config vars, added `whitenoise.middleware.WhiteNoiseMiddleware` to the MIDDLEWARE list, and ensured correct static file settings (`STATIC_URL`, `STATIC_ROOT`, `STATICFILES_DIRS`).  
- **Result:** Static assets are now correctly collected and served on Heroku.

### Media Files Not Persisting
**Issue:** Uploaded media (e.g., team logos) were not persisting on Heroku due to its ephemeral filesystem.  
- **Cause:** Heroku’s file system is not designed for persistent storage of media uploads.  
- **Fix:** Integrated Cloudinary by setting `DEFAULT_FILE_STORAGE` to `'cloudinary_storage.storage.MediaCloudinaryStorage'` in `settings.py` and configured Cloudinary credentials via environment variables.  
- **Result:** Media files now persist and are reliably served from Cloudinary.

### Virtual Environment & Dependency Issues
**Issue:** Runtime errors due to missing modules (e.g., gunicorn, Pillow, whitenoise).  
- **Cause:** Dependencies were either not installed in the active virtual environment or were missing from `requirements.txt`.  
- **Fix:** Recreated the virtual environment, installed all necessary dependencies using `pip install`, and updated `requirements.txt` with `pip freeze > requirements.txt`.  
- **Result:** All dependencies are now properly installed and recognized in both local and Heroku environments.

### Incorrect Model Field Storage for Team Logos
**Issue:** Team logo fields were automatically storing a `team_logos/` prefix, leading to broken image paths (e.g., `/static/team_logos/team_logos/rhyd_logo.jpg`).  
- **Cause:** Using an `ImageField` with `upload_to='team_logos'` forces Django to prepend that directory to the stored filename.  
- **Fix:** Changed the model field for logos to a `CharField` so that only the filename (e.g., `rhyd_logo.jpg`) is stored, and manually placed the actual images in the `static/team_logos/` folder.  
- **Result:** Team logos now display correctly with the static file references.

### Static Files Not Loading When DEBUG = False
**Issue:** When DEBUG = False, static files (CSS) were not loading, and the browser console showed MIME type errors (text/html instead of text/css).
- **Casue:** This was caused by Django’s default behavior, which does not serve static files in production mode.
- **Fix:** Updated settings.py to differentiate static handling between development and production:
if DEBUG:
    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
else:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
  - Ran collectstatic to ensure static files were available in production mode:
  python manage.py collectstatic --noinput
  - Used --insecure mode for local testing with DEBUG = False:
  python manage.py runserver --insecure
- **Result:** Static files now load correctly in both development (DEBUG = True) and production (DEBUG = False) environments.
  - The --insecure flag allows static files to be served locally without changing DEBUG back to True.


##  **Setup & Configuration**
### Media & Static Files Configuration
- **Media Files (User Uploads):**  
  In `settings.py`, configure media handling as follows:
  ```python
  MEDIA_URL = '/media/'
  MEDIA_ROOT = BASE_DIR / 'media'
    - Note: With Cloudinary integrated for media storage, uploaded images will be stored remotely. These settings remain useful for local development.

- **Static Files:**
- Configure static files to be served using Whitenoise:
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

- **URL Configuration for Development**
- Add the following to your main urls.py to serve media files during development:
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('team.urls')),  # Main app routes
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

- **Environment Variables (.env)**
- For local development; 
create a .env file in the project root (this file should be added to .gitignore):

  # .env file

  # Django secret key
  SECRET_KEY=your_production_secret_key

  # For local development
  DEBUG=True

  # Cloudinary credentials
  CLOUDINARY_CLOUD_NAME=dmzwtex3f
  CLOUDINARY_API_KEY=213153381958977
  CLOUDINARY_API_SECRET=18_8hXbd-w0wk64V9T3pmJGqeP4


##  **Testing Summary**
### **Manual Testing Performed**
-  **Homepage displays correctly**:
  - Upcoming fixture 
  - Latest result 
  - League table preview 
  - Manager’s comment 
-  **Navigation Works**
  - Fixtures link  (only upcoming matches)
  - Results link  (only completed matches)
- **Base template applied consistently** across all pages
- **User Authentication & Profiles Working**
  - Login/logout functions correctly
-  **Dynamic Standings Confirmed**
  - Points update correctly 
  - Goal difference is calculated 
  - Teams are ordered properly
- **Automated Testing**
- The project includes a suite of automated tests to verify core functionality of the application. These tests cover aspects such as model behavior and view responses.

To run all tests, execute the following command from your project root: (python manage.py test).

- For example, a recent test run produced the following output:
Found 3 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
Manager Posts Retrieved: 0
Latest Result: None
.Manager Posts Retrieved: 0
Latest Result: None
..
----------------------------------------------------------------------
Ran 3 tests in 0.103s

OK
Destroying test database for alias 'default'...

***This output confirms that all tests passed successfully, ensuring that the core application logic (such as displaying fixtures and results, and handling manager posts) is functioning as expected.***

- **Code Style & Coneventions**
  - The project follows PEP8 guidelines.
  - Code is well-documented and uses consistent naming conventions.
  - Files are named consistently for cross-platform compatibility.


- **Validators** 

- Using https://validator.w3.org/nu/#textarea; 
  - ***Home page:*** ![screenshot](screenshots\img1.png)
  - ***Fixtures page:*** ![screenshot](screenshots\img2.png)
  - ***Results page:*** ![screenshot](screenshots\img3.png)
  - ***League Table page:*** ![screenshot](screenshots\img4.png)
  - ***Login page:*** ![screenshot](screenshots\img5.png)
  - ***Manager Dashboard:*** ![screenshot](screenshots\img6.png)
  - ***Player Dashboard:*** ![screenshot](screenshots\img7.png)
    - In the current version of the Player Dashboard, the rendered HTML shows two main validation errors when checked against W3C standards:
      - ***1. Duplicate ID "id_content"***
        - The “View Source” reveals multiple <textarea> elements on the page, each with id="id_content".
        - Despite searching the codebase and templates, the source of these duplicate IDs could not be definitively located or overridden.
        - This may be due to auto-generated IDs from form libraries or partials.
      - ***2. Inline <style> Tags in the <body>***
        - Two <style> blocks appear near the end of the <body> section.
        - HTML5 expects all <style> elements inside <head>, resulting in a validation error.
      **Impact**
      - These issues do not appear to break functionality in browsers.
      - However, they cause warnings or errors in standard validation tools and could potentially cause edge-case rendering issues or conflicts with accessibility tools.

      **Status**
      - We have attempted to trace the source of these issues (via project-wide searches, partial templates, and framework configurations) but have not been able to successfully locate or fix them.
      - Future development will aim to refactor or remove these duplicate IDs and relocate any inlined <style> tags.

      **Attempts to Fix**
      1. Duplicate ID:
        - Code Searches: Searched the entire codebase (templates, partials, forms, models, etc.) for id="id_content". Could not locate any literal use of that string.
        - Override or Rename Field: Investigated whether Django’s (or another framework’s) form system auto-generates this ID. Tried manually overriding or renaming the form field.
        - Removed/Commented Out Code: Temporarily removed/commented out certain form blocks and partials to see if the duplicate id_content disappeared.
        - Result: The duplicate IDs still appear in the final rendered HTML, despite multiple troubleshooting attempts.

      2. Inline <style>:
        - Moving CSS: Attempted to relocate inline <style> blocks to the <head> section or into a standalone stylesheet.
        - Template Inheritance: Checked base templates and partials to ensure no <style> tags were defined at the bottom of <body>.
        - Search for Plugin Injections: Investigated whether a plugin or external script automatically injects CSS.
        - Result: The <style> tags remain in the final HTML output; their exact origin could not be pinpointed.

- Using CSS-Validator: https://jigsaw.w3.org/css-validator/
  - ***CCS Validation*** ![screenshot](screenshots\img9.png)

---