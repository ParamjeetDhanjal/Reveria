# Reveria – Instagram Clone

A full-stack Instagram-inspired social media platform built using **Flask**, **SQLAlchemy**, and **SQLite**, featuring authentication, private/public profiles, posts with images & music, likes, comments, follow requests, and secure deployment.

**Live Demo:**  
https://reveria-gufx.onrender.com

---

## Overview

Reveria is a modern social media web application inspired by Instagram. It demonstrates key full-stack development concepts, including user authentication, relational data handling, file uploads, and dynamic content rendering.

### The app highlights:
- Building production-ready web applications with Flask
- Managing persistent data using SQLAlchemy & SQLite
- Serving dynamic content with Jinja2 templates
- Uploading and handling media (images and audio)
- Managing private/public accounts and follow requests

---

## Tech Stack

| Category | Technology |
|--------|------------|
| Frontend | HTML5, TailwindCSS, FontAwesome, Jinja2 Templates |
| Backend | Python, Flask |
| Database | SQLite (SQLAlchemy ORM) |
| Authentication | Flask Sessions, Werkzeug Password Hashing |
| File Uploads | Flask `request.files` |
| Utilities | Flask-Migrate, Flask-SQLAlchemy, UUID, Datetime |
| Deployment | Render |

---

## Features

### User Accounts
- Signup / Login / Logout with hashed passwords
- Public or private account option
- Profile picture upload
- Followers & following system
- Follow request system for private accounts

### Posts & Media
- Upload images with optional background music
- Multiple image carousel per post
- Captions for posts
- Like / Unlike posts
- View liked posts

### Interactions
- Comment on posts (with threaded replies)
- Accept or decline follow requests
- Notifications for follow requests

### Search & Explore
- Search users by username
- Explore public posts

### UI / UX
- Modern dark theme with glassmorphic elements
- Responsive layout for mobile & desktop
- Tabs for Posts, Liked, Settings, Followers, Following

---

## Installation & Setup

Clone the repository:
git clone https://github.com/paramjeetdhanjal/reveria.git
cd reveria

Open your browser at: http://127.0.0.1:5000

## Future Improvements
- Real-time notifications using WebSockets
- Pagination for feed and explore pages
- Hashtags and user tagging system
- Chat and post sharing
- Stories and profile highlights

## Author
- Paramjeet Dhanjal
- GitHub: https://github.com/paramjeetdhanjal
- Email: paramjeetkaurdhanjal8@gmail.com
