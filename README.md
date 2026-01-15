Reveria - Instagram Clone

A full-stack Instagram-inspired social media platform built using Flask, SQLAlchemy, SQLite featuring authentication, private/public profiles, posts with images & music, likes, comments, follow requests, and secure deployment.
Live Demo
Visit App: https://reveria-gufx.onrender.com
Overview
Reveria is a modern social media web application inspired by Instagram. It demonstrates key full-stack development concepts, including user authentication, data relationships, file uploads, and dynamic content rendering.

The app highlights:
•	Building production-ready web apps with Flask
•	Managing persistent data with SQLAlchemy & SQLite
•	Serving dynamic content with Jinja2 templates
•	Uploading and handling media (images and audio)
•	Managing private/public accounts and follow requests

Tech Stack
| Category | Technology |
|---------|------------|
| Frontend | HTML5, TailwindCSS, FontAwesome, Jinja2 Templates |
| Backend | Python, Flask |
| Database | SQLite (SQLAlchemy ORM) |
| Authentication | Flask Sessions, Werkzeug Password Hashing |
| File Uploads | Flask `request.files` |
| Utilities | Flask-Migrate, Flask-SQLAlchemy, UUID, Datetime |
| Deployment | Render |

Features
User Accounts
•	Signup/Login/Logout with hashed passwords
•	Public or private account option
•	Profile picture upload
•	Followers & following list
•	Follow request system for private accounts
Posts & Media
•	Upload images & optional music per post
•	Multiple images carousel
•	Captions for posts
•	Like/Unlike posts
•	View liked posts
Interactions
•	Comment on posts (with threaded replies)
•	Accept or decline follow requests
•	Notifications for follow requests
Search & Explore
•	Search users by username
•	Explore public posts
UI/UX
•	Modern dark theme with glassmorphic elements
•	Responsive layout for mobile & desktop
•	Tabs for Posts, Liked, Settings, Followers, Following

Installation & Setup
Clone the repository and install dependencies:

git clone https://github.com/paramjeetdhanjal/reveria.git
cd reveria
python -m venv venv
source venv/bin/activate (Linux/Mac)
venv\Scripts\activate (Windows)
pip install -r requirements.txt

Create the SQLite database:
flask db init
flask db migrate
flask db upgrade

Run the app:
python reveria.py

Open your browser at http://127.0.0.1:5000

Future Improvements
•	Real-time notifications with WebSockets
•	Pagination for feed and explore pages
•	Hashtags & tagging system
•	Chat and Sharing Posts to other users
•	Stories and highlights for user’s Profile 

Author
Paramjeet Dhanjal
GitHub: https://github.com/paramjeetdhanjal
Email: paramjeetkaurdhanjal8@gmail.com

