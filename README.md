# CPD Yr Wyddgrug Official Website

## Description
A full-stack web application where users can keep up to date with local club CPD Yr Wyddgrug. Users can see results, fixtures, league standings, comments from the managers, and team details. Managers can post fixtures, training schedules, and request player availability. Players can view the same information but can also confirm their availability for fixtures and training sessions.

## Current Features
###  **Core Features Implemented**
- **Django project setup & team app creation**
- **Team Model** including:
  - Manager, home ground, founded year, team logo
  - League tracking stats (games played, wins, draws, losses, goals for/against, points)
- **Media file handling** set up for team logos
- **Homepage now includes:**
  - Team banner (team name, logo, manager, home ground, founded year)
  - Upcoming fixture display (or "No upcoming fixtures" if none exist)
  - League table preview (CPD Yr Wyddgrug is **highlighted in bold & uppercase**)
  - Manager's latest comment/news section
- **Results Page** – Displays **only** completed fixtures
- **Fixtures Page** – Displays **only** upcoming fixtures
- **Dynamic League Table** – Automatically updates based on match results:
  - Sorted by **points (highest first)**
  - If points are tied, sorted by **goal difference**
  - Tracks **matches played, wins, draws, losses, goals for/against, points**

###  **User Authentication & Profiles**
- **Login/Logout System Implemented**
  - Users can log in and out from the **navbar**.
  - **Players & Managers must be registered by an admin** (no public registration allowed).
- **User Role System Added**
  - Managers have **access to a Manager Dashboard**.
  - Players have **access to a Player Dashboard**.
- **Profile Setup Required**
  - New users are **redirected to create a profile** before accessing the dashboards.

### **Manager & Player Dashboards**
- **Manager Dashboard**
  - Can post training updates, match information, and team news.
- **Player Dashboard**
  - Players can **confirm availability** for upcoming fixtures and training.
- **Access Restrictions**
  - Visitors **cannot create an account manually**.
  - Users without a profile are **redirected to the profile setup page**.

### **Fixtures & Results System**
- **Matches now store results correctly** (wins, losses, draws calculated dynamically)
- **Standings update instantly** when a match is marked as completed.
- **Fixture Model Fixes:**
  - `match_completed` field replaces `is_played` for clarity.
  - **Correct opponent assignment** (previously fixtures were being saved with incorrect team links).
  - **Goal tracking works correctly** for both teams.

## 🔹 **Upcoming Features**
- **Global Styling & CSS Setup** (Enhancing layout & visuals)
- **Manager Posts (for team updates & news)**
- **Player Availability System Enhancements**
- **Deployment to Cloud**

##  **Bugs Fixed & Issues Resolved**
### **[FIXED] League Table Not Updating**
**Issue:** Standings were resetting to zero after every update.
- **Cause:** Incorrect query filtering, missing opponent-team link in calculations.
- **Fix:** Refactored `calculate_standings()` to correctly sum matches for both home & away teams.
- **Result:** Teams now track points, matches, goals, and ranking correctly.

### **[FIXED] Fixtures Not Displaying**
**Issue:** Some fixtures were not appearing on the homepage.
- **Cause:** `home_or_away` field filtering issue.
- **Fix:** Updated query to check **both** opponent and home team conditions.
- **Result:** Upcoming fixtures and results now load properly.

### **[FIXED] Reverse URL Errors**
**Issue:** Navigation links broke due to mismatched URL names (`home` instead of `homepage`).
- **Fix:** Updated `urls.py` and all template links to reference the correct view names.
- **Result:** Navigation now functions without errors.

### **[FIXED] Logout Not Working**
**Issue:** Logout link was broken due to incorrect authentication setup.
- **Fix:** Connected Django’s built-in `LogoutView` and updated the navbar.
- **Result:** Users can now **log out and log back in** successfully.

##  **Setup & Configuration**
To enable media file handling (team logos), ensure you’ve configured the following in `settings.py`:
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```
Also, add this to `urls.py` to serve media files during development:
```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('team.urls')),  # Main app routes
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

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
  - Login/logout 
  - Redirects to **create profile** if missing 
-  **Dynamic Standings Confirmed**
  - Points update correctly 
  - Goal difference is calculated 
  - Teams are ordered properly 

##  **Next Steps**
- **CSS & Styling Implementation**
- **Manager Post System** (for team announcements & news)
- **Player Availability Enhancements**
- **Deploying the site** to a cloud hosting provider

---