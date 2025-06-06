# CPD Yr Wyddgrug Official Website

![Screenshot showing sites responsiveness](screenshots/img24.png)


**CPD Yr Wyddgrug** is a full-stack web application built for a local football club to manage fixtures, results, league standings, and internal team communication. The live site can be found [here.](https://cpd-yrwyddgrug-official-site-600d661005ac.herokuapp.com/)

The site is designed for both **club members** and **public visitors**:
- **Fans** can view recent results, the upcoming fixture, the league table, and the manager’s latest update via the public homepage.
- **Players** can log in to confirm their availability for fixtures and respond to manager posts.
- **Managers** can post team news, track player availability, and receive notifications when players interact.

The application is built using **Django** with a traditional **Model-View-Controller (MVC)** approach and styled using **Bootstrap 5** with custom CSS. The site is mobile responsive and supports dynamic content updates to ensure an accessible and engaging experience for all users.

## Key Features

- ### Role-Based Access Control
  - The platform includes secure login for two types of users — **Managers** and **Players** — each with their own dashboard and permissions. Public users can still access the homepage, fixtures, results, and league table without needing an account.
  - Club members can register using an invite code which would be provided to the club, preventing any user from registering as a player/manager. 

- ### Fixtures & Results Management
  - All upcoming matches and completed results are stored in the system. Fixtures include team logos, match date/time and location. Results display final scores and update the league standings.

- ### Manager Announcements & Posts
  - Managers can post updates to players directly through the system, such as match details, training reminders or tactical updates. Players can read and respond via comments.

- ### Player Availability System
  - Players can mark themselves as **available** or **unavailable** for upcoming fixtures. Fixture cards update dynamically with a coloured border to reflect their selection for easy readability.

- ### League Table Preview
  - A custom-built league table automatically ranks teams based on points and goal difference. CPD Yr Wyddgrug is highlighted for visibility. The table is also responsive for mobile users.

- ### Real-Time Style Notifications
  - Players and managers receive in-dashboard notifications when relevant actions are taken (e.g., availability changed or new message posted). A **red dot** appears in the navbar if new notifications are unread.

- ### Responsive Design with Bootstrap
  - The site uses a mobile-first layout via Bootstrap 5. Key features like the navigation bar, homepage layout and fixture cards adapt fluidly across screen sizes.

## Table of Contents

- [User Stories](#user-stories)
- [User Experience](#user-experience)
- [Wireframe](#wireframe)
- [Database Design](#database-design)
- [Technology Stack](#technology-stack)
- [Fixed Bugs](#fixedbugs)
- [Testing & Validation](#testing--validation)
- [Deployment](#deployment)
- [Future Features](#future-features)
- [Credits](#credits)

## User Stories

The development of this application was guided by a set of user stories defined in [this GitHub project board](https://github.com/users/JLG-96/projects/5).

User stories were written from the perspectives of the three types of users interacting with the site:

### As a Public User:
- I want to view the upcoming fixtures, recent results, and league standings.
- I want to see updates from the manager so I can stay informed about the team’s progress.

### As a Player:
- I want to log in and see my own dashboard with a list of upcoming fixtures.
- I want to mark my availability for each fixture and see what I’ve previously selected.
- I want to read and comment on posts from the manager to stay informed and respond.
- I want to be notified when a new message has been posted by the manager.

### As a Manager:
- I want to post updates to players, including match details and training notices.
- I want to view which players are available or unavailable for each upcoming fixture.
- I want to receive notifications when players comment on my posts or update their availability.

## User Experience
### Typography & Colour Scheme

The project uses the **Arial** and **sans-serif** system fonts to ensure clean readability and compatibility across all modern browsers and devices.

The colour palette is directly inspired by **CPD Yr Wyddgrug’s official club colours**, reinforcing brand identity across the interface:

- <span style="display:inline-block;width:16px;height:16px;background:#dc3545;border:1px solid #ccc;border-radius:3px;margin-right:6px;"></span> **Primary Colour (Club Red):** `#dc3545`
- <span style="display:inline-block;width:16px;height:16px;background:#000000;border:1px solid #ccc;border-radius:3px;margin-right:6px;"></span> **Secondary Colour (Club Black):** `#000000`
- <span style="display:inline-block;width:16px;height:16px;background:#ffffff;border:1px solid #ccc;border-radius:3px;margin-right:6px;"></span> **Accent Colour (White):** `#ffffff`
- <span style="display:inline-block;width:16px;height:16px;background:#f4f4f4;border:1px solid #ccc;border-radius:3px;margin-right:6px;"></span> **Background Colour (Neutral Grey):** `#f4f4f4`

These colours are consistently applied to headers, banners, buttons, and alert elements to create a cohesive visual experience that aligns with the club’s bold and energetic image.

### Agile Planning

This project was developed using agile methodologies over a span of several weeks. A Kanban-style board was used to track development progress, with columns for each stage including **To Do**, **In Progress**, and **Done**.

Development was guided by:

- **MVP Milestones** — the focus was placed on completing core user-facing features before adding enhancements.
- **User Stories** — each card was written with a specific goal in mind, often based on feedback or required functionality.
- **Manual Testing & Iteration** — features were tested in-browser and refined based on real-world behaviour and layout issues.

All user stories were documented and tracked in the GitHub Project board.
**View the full board here:** [CPD Yr Wyddgrug Project Board](https://github.com/users/JLG-96/projects/5)

#### Kanban Board Screenshot
![Kanban Board](screenshots/img12.png)

### Features

<details>
<summary><strong>Navigation Bar</strong></summary>

- The site features a responsive navigation bar that appears across all pages via the shared `base.html` template.
- It adapts to screen sizes using Bootstrap — collapsing into a hamburger menu on smaller devices for improved mobile usability.
- The navbar dynamically updates based on the user's authentication status:
  - **Public users** see links to: Home, Fixtures, Results, and Login.
  - **Players** see: Home, Fixtures, Results, Player Dashboard, and Logout.
  - **Managers** see: Home, Fixtures, Results, Manager Dashboard, and Logout.
- Logged-in users also see a small text tag showing: `Logged in as: <username>` for clarity.
- A red **notification dot** appears next to the Dashboard link if a new notification is present:
  - This red dot serves as a visual cue to prompt users to check their dashboard.
  - The dot disappears only when all notifications have been removed. Otherwise, it moves to the next unread notification.

![Navbar](screenshots/img19.png)

</details>

<details>
<summary><strong>Team Banner</strong></summary>

- A custom banner is displayed at the top of the homepage, featuring:
  - The CPD Yr Wyddgrug club logo (circular image).
  - Club name in bold, large font.
  - Subheadings for Manager name, Home Ground, and Year Founded.
- Designed using custom CSS for a strong visual identity and club branding.
- The banner is hidden on small screens to preserve space and improve readability on mobile.

![Team Banner](screenshots/img14.png)

</details>

<details>
<summary><strong>Role-Based Dashboards</strong></summary>

- Users log in securely and are directed to different dashboards based on their role:
  - **Players** can view fixtures and confirm availability.
  - **Managers** can post announcements to the player dashboard directly and to the homepage for fans. Can also view player availability.
- Public users (fans) can browse the homepage, fixtures, results, and league standings without any need for logging in.
- Registration is restricted using an **invite-only system**, ensuring only club members can access protected features.

</details>

<details>
<summary><strong>Fixtures & Results on Homepage</strong></summary>

- Fixtures display opponent name, club logo, date, time, and location.
- Results include final scores and a match outcome tag (WIN / DRAW / DEFEAT).
- The homepage highlights the most recent result and upcoming fixture only/.
- The full list of upcoming and completed matches can be found on the Fixtures and Results pages.

![Fixtures & Results on Homepage](screenshots/img13.png)

</details>

<details>
<summary><strong>League Table Preview</strong></summary>

- Dynamically generated league table preview sorted by:
  - Total points.
  - Goal difference.
- The table is to emphasise the position of CPD Yr Wyddgrug in relation to the top 3.
- CPD Yr Wyddgrug is automatically highlighted in the table.
- The preview is horizontally scrollable on smaller screens for better mobile usability.

![League Table Preview](screenshots/img16.png)

</details>

<details>
<summary><strong>Manager's comments</strong></summary>

- The **Manager Comments** section allows the club to share public updates with fans via the homepage.
  - Posts can include match previews, team news, transfer updates, or post-game reflections.
- These updates are submitted from the manager dashboard using a simple form interface.
- Fans (public users) can read the 5 most recent comments.
  - The most recent post is shown first and tagged with **"Latest"** for visibility.
  - Users can cycle through recent posts using left/right arrow buttons.
  - Older posts (beyond the 5 most recent) are removed from the homepage view but remain stored in the database.
- If the latest post is deleted, the **"Latest"** tag is reassigned to the next most recent comment.
- Managers can edit or remove their own posts at any time.

![Manager's Comments](screenshots/img15.png)

</details>

<details>
<summary><strong>Manager Posts to Player Dashboard</strong></summary>

- Managers can post announcements to all players, including match details, training reminders, and general updates.
- Each post includes a title, content, and timestamp.
- Players can comment on messages, and managers receive notifications when comments are made.
- Managers can edit or delete their posts.

![Manager Posts to Player Dashboard](screenshots/img17.png)

</details>

<details>
<summary><strong>Player Availability System</strong></summary>

- Players can select whether they are **available** or **unavailable** for each upcoming fixture.
- Fixture cards dynamically update with:
  - A **green border** for availability.
  - A **red border** for unavailability.
- Submitting availability is quick and clearly reflected on the dashboard.
- Availability can also be easily changed by the player - a notification is sent to the manager when availability has been set (including changed).

![Player Availability System](screenshots/img18.png)

</details>

<details>
<summary><strong>Notification System</strong></summary>

- In-dashboard notifications appear when:
  - A manager posts a new message or edits one.
  - A player changes their fixture availability, comments on a message or edits it.
- The most recent notifications include a **"NEW"** tag and are visually highlighted. Notifications are green to help express which is the most recent and go red if they are old.
- A **red dot** appears in the navbar if there are notifications.
- Each notification can be dismissed individually - removal of all notifications removes the red dot.

![Notification System](screenshots/img20.png)

</details>

<details>
<summary><strong>Login and Registration</strong></summary>

  - Accessible from the navbar.
  - Requires a valid **username** and **password**.
  - Authenticated users are redirected to their assigned dashboard (Manager or Player).
  - Invalid credentials return an error message.

- **Registration:**
  - Registration is not publicly available.
   - A one-time **invite code** is required upon first login to complete registration.
  - Members of the club will asign themselves a player / manager upon registration.

</details>

## Wireframe
 A clean layout with structured sections helps fans and club members find key information quickly—whether on desktop or mobile devices.

The wireframe was created to plan the homepage layout and the dynamic content areas.

| Wireframe Screenshot |
|----------------------|
| ![Homepage Wireframe](screenshots/img8.png) |

From this base wireframe, the **Manager Dashboard** and **Player Dashboard** were developed.

The wireframe was used as a guide, rather than a strict template - allowing room for agile evolution based on feedback and functionality needs.

## Database Design

The database was designed using Django’s ORM (Object-Relational Mapping) to support all key club functionalities, ensuring each user interaction is stored and processed effectively.

- **Users** are authenticated through Django’s built-in `User` model. Each user is extended with a `Profile`, defining them as a **Player** or **Manager**.
- **Fixtures** store upcoming and completed match details including opponent, time, location, and score.
- **Results** are derived from completed fixtures and feed into the team’s statistics and league table.
- **Teams** store persistent information about clubs in the league, including their manager, logo, stats, and standings.
- **PlayerAvailability** records a player’s availability status for upcoming matches.
- **ManagerPosts** are public-facing updates from the manager shown on the homepage.
- **ManagerMessages** are private updates sent directly to players.
- **Comments** allow players to reply to internal manager messages.
- **Notifications** track availability updates, new messages, and new comments to keep users informed.

This structure allows full CRUD (Create, Read, Update, Delete) functionality across all relevant areas for both Managers and Players.

- The ERD (Entity Relationship Diagram) was designed on [Lucidchart](https://www.lucidchart.com/)
![ERD Design](screenshots/img21.png)

## Technology Stack

### Technology Used

| Category           | Tool/Library                   | Version        |
|--------------------|--------------------------------|----------------|
| **Backend**        | Django                         | 5.1.6          |
| **Database**       | PostgreSQL (via Heroku)        | -              |
| **Frontend**       | HTML5, CSS3, JavaScript        | -              |
| **Styling**        | Bootstrap 5, Custom CSS        | -              |
| **Media Storage**  | Cloudinary                     | 1.42.2         |
| **Static Files**   | Whitenoise                     | 6.9.0          |
| **Image Handling** | Pillow                         | 11.1.0         |
| **Server**         | Gunicorn                       | 23.0.0         |
| **Environment**    | Python Decouple                | 3.8            |

### Other Dependencies

- `asgiref==3.8.1`  
- `certifi==2025.1.31`  
- `charset-normalizer==3.4.1`  
- `django-cloudinary-storage==0.3.0`  
- `idna==3.10`  
- `requests==2.32.3`  
- `six==1.17.0`  
- `sqlparse==0.5.3`  
- `tzdata==2025.1`  
- `urllib3==2.3.0`

### Tools Used

- **Git & GitHub** – For version control and code hosting.  
- **Gitpod** – Cloud-based IDE used during development.  
- **Heroku** – Deployment platform for hosting the live site.  
- **Cloudinary** – Image hosting and delivery service for team logos.

## Fixed Bugs

<details>
<summary><strong>League Table Not Updating</strong></summary>

**Issue:** Standings were resetting to zero after every update.  
- **Cause:** Incorrect query filtering and a missing opponent-team link in calculations.  
- **Fix:** Refactored `calculate_standings()` to correctly sum matches (both home and away).  
- **Result:** Teams now track points, matches, goals, and rankings accurately.
</details>

<details>
<summary><strong>Fixtures Not Displaying</strong></summary>

**Issue:** Some fixtures were not appearing on the homepage.  
- **Cause:** The query was filtering using only one side of the match (either home or opponent) instead of both.  
- **Fix:** Updated the query to check conditions for both the home team and opponent.  
- **Result:** Upcoming fixtures and recent results now load properly.
</details>

<details>
<summary><strong>Reverse URL Errors</strong></summary>

**Issue:** Navigation links broke due to mismatched URL names (e.g., using "home" instead of "homepage").  
- **Fix:** Revised `urls.py` and updated all template links to reference the correct view names.  
- **Result:** Navigation now functions seamlessly across the site.
</details>

<details>
<summary><strong>Logout Not Working</strong></summary>

**Issue:** The logout link was broken due to an incorrect authentication setup.  
- **Fix:** Connected Django’s built-in `LogoutView` and updated the navbar accordingly.  
- **Result:** Users can now log out and log back in successfully.
</details>

<details>
<summary><strong>Static Files Not Loading on Deployment</strong></summary>

**Issue:** CSS and other static assets were not served on Heroku.  
- **Cause:** The environment variable `DISABLE_COLLECTSTATIC` was set and/or Whitenoise was not properly configured.  
- **Fix:** Removed `DISABLE_COLLECTSTATIC` from Heroku config vars, added `whitenoise.middleware.WhiteNoiseMiddleware` to the MIDDLEWARE list, and ensured correct static file settings (`STATIC_URL`, `STATIC_ROOT`, `STATICFILES_DIRS`).  
- **Result:** Static assets are now correctly collected and served on Heroku.
</details>

<details>
<summary><strong>Media Files Not Persisting</strong></summary>

**Issue:** Uploaded media (e.g., team logos) were not persisting on Heroku due to its ephemeral filesystem.  
- **Cause:** Heroku’s file system is not designed for persistent storage of media uploads.  
- **Fix:** Integrated Cloudinary by setting `DEFAULT_FILE_STORAGE` to `'cloudinary_storage.storage.MediaCloudinaryStorage'` in `settings.py` and configured Cloudinary credentials via environment variables.  
- **Result:** Media files now persist and are reliably served from Cloudinary.
</details>

<details>
<summary><strong>Virtual Environment & Dependency Issues</strong></summary>

**Issue:** Runtime errors due to missing modules (e.g., gunicorn, Pillow, whitenoise).  
- **Cause:** Dependencies were either not installed in the active virtual environment or were missing from `requirements.txt`.  
- **Fix:** Recreated the virtual environment, installed all necessary dependencies using `pip install`, and updated `requirements.txt` with `pip freeze > requirements.txt`.  
- **Result:** All dependencies are now properly installed and recognized in both local and Heroku environments.
</details>

<details>
<summary><strong>Incorrect Model Field Storage for Team Logos</strong></summary>

**Issue:** Team logo fields were automatically storing a `team_logos/` prefix, leading to broken image paths.  
- **Cause:** Using an `ImageField` with `upload_to='team_logos'` forced Django to prepend that directory to the stored filename.  
- **Fix:** Changed the model field for logos to a `CharField` so that only the filename is stored and moved images to `static/team_logos/`.  
- **Result:** Team logos now display correctly using static file paths.
</details>

<details>
<summary><strong>Static Files Not Loading When DEBUG = False</strong></summary>

**Issue:** When DEBUG = False, static files (CSS) were not loading, and the browser console showed MIME type errors.  
- **Cause:** Django does not serve static files in production mode by default.  
- **Fix:** 
  - Updated settings.py with environment-aware `STATICFILES_STORAGE` settings.
  - Ran `collectstatic`.
  - Used `--insecure` mode for local testing with DEBUG off.  
- **Result:** Static files load correctly in both development and production.
</details>

<details>
<summary><strong>Notification Badge Not Displaying</strong></summary>

**Issue:** The red dot indicating a new notification was not appearing on the manager/player dashboards.  
- **Cause:** Unread notifications were not being checked in the navbar.  
- **Fix:** Added logic to check `is_read = False` in the base template.  
- **Result:** Red dot now appears until all notifications are read.
</details>

<details>
<summary><strong>Notification Not Triggering for Edited Comments</strong></summary>

**Issue:** Managers were not notified when players edited their comments.  
- **Cause:** Edit view didn’t create a new notification.  
- **Fix:** Triggered a custom notification on comment update.  
- **Result:** Managers are alerted when a comment is edited.
</details>

<details>
<summary><strong>Player Not Notified of Edited Manager Messages</strong></summary>

**Issue:** Players didn’t get notified when a manager edited a message.  
- **Cause:** No notification logic in the manager edit view.  
- **Fix:** Added a loop to notify all player users.  
- **Result:** Players now receive a notification when a manager message is modified.
</details>

## Testing & Validation
<details>
<summary><strong>Manual Testing</strong></summary>

Manual testing was conducted throughout development to ensure that all pages and functionalities behaved as expected. Tests were carried out on Chrome, Firefox, Safari, and mobile devices.

| Page/Feature              | Expected Behaviour                                                     | Result |
|--------------------------|------------------------------------------------------------------------|--------|
| Homepage                 | Displays team banner, fixture preview, league preview, and news       | ✅     |
| Fixtures Page            | Shows only upcoming fixtures, ordered by date                         | ✅     |
| Results Page             | Lists only completed fixtures with results                            | ✅     |
| League Table             | Displays all teams, sorted by points and goal difference              | ✅     |
| Manager Dashboard        | Allows posting messages, viewing availability, editing & deleting     | ✅     |
| Player Dashboard         | Displays notifications, allows setting availability, and commenting   | ✅     |
| Navigation               | All nav links function correctly and change based on user role        | ✅     |
| Responsive Layout        | Layout adjusts correctly for tablet and mobile views                  | ✅     |
| Login/Logout             | Authenticates and redirects user properly                             | ✅     |
| Notification Dot         | Appears when new items are unread, disappears when cleared            | ✅     |

</details>


<details>
<summary><strong>Automated Testing</strong></summary>

Automated tests were written using Django’s built-in `TestCase` framework to validate core model and view functionality.

To run all tests, execute the following command from your project root:

```bash
python manage.py test

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

```
This output confirms that all tests passed successfully, ensuring key application logic (such as displaying fixtures and results, and handling manager posts) works as expected.
</details>

<details>
<summary><strong>HTML Validation</strong></summary>

The [W3C Markup Validation Service](https://validator.w3.org/) was used to validate all rendered HTML pages. Below are the screenshots of the validation results:

- **Home page:**  
  ![Home page](screenshots/img1.png)

- **Fixtures page:**  
  ![Fixtures page](screenshots/img2.png)

- **Results page:**  
  ![Results page](screenshots/img3.png)

- **League Table page:**  
  ![League table page](screenshots/img4.png)

- **Login page:**  
  ![Login page](screenshots/img5.png)

- **Manager Dashboard:**  
  ![Manager Dashboard](screenshots/img6.png)

- **Player Dashboard:**  
  ![Player Dashboard](screenshots/img7.png)

</details>

<details>
<summary><strong>CSS Validation</strong></summary>

The [W3C CSS Validation Service](https://jigsaw.w3.org/css-validator/) was used to check the stylesheet for any syntax errors or non-compliant styles.

- **CSS Validation Result:**  
  ![CSS validation](screenshots/img9.png)

</details>

<details>
<summary><strong>JavaScript Validation (JSHint)</strong></summary>

- The only custom JavaScript in this project is found in the `home.html` template. It enables post cycling using previous and next buttons.
- The JavaScript was tested using [JSHint](https://jshint.com/).

**ES6 Configuration**  
To allow the use of modern ES6 features such as `let`, `const`, and template literals, the following configuration was enabled in the JSHint configure settings, New JavaScript features (ES6)

**Results:**

- **No critical errors were detected.**
- **Warnings:** Initial warnings for ES6 syntax (e.g., use of `let`, `const`, and template literals) were resolved after enabling the ES6 environment.
- **The code passed all validation checks under this configuration.**
![JSHint testing screenshot](screenshots/img23.png)

</details>

<details>
<summary><strong>Lighthouse Scores</strong></summary>

Lighthouse was used via Chrome DevTools (in Incognito mode);

### Home Page  
![Lighthouse Home](screenshots/img22.png)

</details>

<details>
<summary><strong>JavaScript Testing</strong></summary>

### JavaScript Testing

No JavaScript testing framework (e.g., Jest) was used in this project.

Only a small inline JavaScript snippet is used for non-critical UI cycling of manager posts on the homepage. It does not interact with backend data or affect core application logic, and therefore does not require formal testing.

Manual testing of this functionality was conducted by:
- Reloading the homepage and observing the cycling behavior of manager posts.
- Confirming that posts cycle at appropriate intervals with no overlap or display issues.
- Verifying there were no JavaScript errors or warnings in the browser console (tested in Chrome, Firefox, and Edge).

As such, no package.json or npm-based test setup is included.

</details>

<details>
<summary><strong>Python Code Validation (flake8)</strong></summary>

[flake8](https://flake8.pycqa.org/) was used to check for adherence to PEP8 standards. It has been included in the `requirements.txt` file and was used to identify and correct formatting issues across the project.

The following minor issues were flagged and addressed where appropriate:

- `E501 line too long (>79 characters)` in `settings.py`: These lines were manually refactored by splitting long validator paths across lines for readability and compliance.
- `W291 trailing whitespace`: Fixed.
- `W292 no newline at end of file`: Fixed.
- `W293 blank line contains whitespace`: Fixed.

No functional issues or errors were detected in project code.

</details>

## Deployment

This project was deployed to [Heroku](https://www.heroku.com/) using GitHub integration, with environment variables for configuration and security.

### Heroku Deployment Steps

1. Log in to [Heroku](https://dashboard.heroku.com/) and create a new app.
2. Provide a unique app name and select your region.
3. Navigate to the **Deploy** tab and choose **GitHub** as the deployment method.
4. Connect your GitHub account and search for your repository by name.
5. Leave the deployment branch set to `main`, and connect the repository.

![Heroku GitHub Integration](screenshots/img10.png)  

6. Go to the **Settings** tab and click **Reveal Config Vars**.
7. Add the following configuration keys and provide your own values:
   - `DATABASE_URL`
   - `SECRET_KEY`
   - `CLOUDINARY_URL`

![Heroku Config Vars](screenshots/img11.png)  

8. Under **Buildpacks**, click **Add Buildpack** and select **Python**.
9. Return to the **Deploy** tab and click **Deploy Branch** to begin deployment.
10. Wait for the deployment to complete and verify that the site is live.

### Security Measures

- `DEBUG = False` has been set to ensure production-level security.
- Sensitive variables like `SECRET_KEY`, `DATABASE_URL`, and `CLOUDINARY_URL` are stored in Heroku Config Vars.
- A local `.env` file is used for development and excluded via `.gitignore`.
- All sensitive values are accessed via `os.environ.get()` in `settings.py`.

## Future Features
- **Availability Lockout**  
  A configurable cutoff time (e.g. 24 hours before kickoff) will prevent players from changing their availability, helping managers plan more effectively.
- **Calender functionality**
  Potential to integrate a calendar into both dashboards to more clearly show fixtures and to include scheduled training sessions. Players can set their availability direct to the calendar. Can be sent reminders of important upcoming dates.
- **Contact us section**
  A form page for other teams to fill out to get in contact to schedule friendly games. Other players to get in touch about reequesting to join etc.
- **Automated League Table Updates**  
  Future versions may include logic to auto-update league standings based on match results, reducing manual data entry.
- **Player Stats Dashboard**  
  A personal dashboard for players to track their own appearances, goals, cards, and availability history.
- **Photo Uploads for Teams and Players**  
  Allowing managers to upload photos for team members and match events to personalize the experience.

## Credits

- **Mentor Support:**  
  Special thanks to my Code Institute mentor [Spencer](https://github.com/5pence?tab=repositories) for consistent guidance and constructive feedback throughout the project.

- **Project Inspiration:**  
  The core idea and structure were inspired by the Django Blog walkthrough project provided in the course materials.

- **External Resources:**  
  Assistance with bug fixes, testing, and refinements was supported by:
  - ChatGPT 4o
  - Codeium
  - Stack Overflow
  - GitHub Discussions

- **README Structure & Tone:**  
  The structure and tone of this README were inspired by the [‘Rum Away’ project by Dimitris](https://github.com/Dimitris112/rum-away-testp4), which served as an exemplar.
