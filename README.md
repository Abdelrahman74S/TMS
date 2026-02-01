# TMS - Task Management System

A robust Task Management System built with Django and Django REST Framework (DRF), featuring secure authentication via JWT, project collaboration, and task tracking.

# Features
Custom User Profiles: Extended user model with UUID identification, bio, and location.

Authentication: Secure login, registration, and logout using SimpleJWT with token blacklisting.

Project Management:

Create and manage projects with titles and descriptions.

Assign owners and multiple members to projects.

Role-based membership (Admin, Member).

Task Tracking:

Organize tasks within projects.

Status management (To Do, In Progress, Done).

Priority levels (Low, Medium, High).

Advanced Filtering & Search: Filter projects/tasks by owner, status, or priority, and search through titles and descriptions.

API Documentation: Integrated Swagger and ReDoc for easy API exploration.

# Tech Stack
Backend: Django 6.0

API: Django REST Framework

Authentication: SimpleJWT

Documentation: drf-yasg

Database: SQLite (Development)


# Getting Started
Prerequisites
 Python 3.13+
 Virtual environment (recommended)
 
Installation
1- Clone the repository:
    git clone <repository-url>
    cd tms

2- Install dependencies:
   pip install -r requirements.txt

3- Run Migrations:
   python manage.py migrate

4- Create a Superuser:
   python manage.py createsuperuser

5- Start the Server:
   python manage.py runserver

# API Endpoints

Authentication
POST /api/auth/register/ - Register a new user profile.

POST /api/auth/login/ - Obtain JWT access and refresh tokens.

POST /api/auth/logout/ - Blacklist refresh token.

POST /api/auth/token/refresh/ - Refresh access token.

Board (Projects & Tasks)
GET /api/board/projects/ - List all projects (accessible to owners/members).

POST /api/board/projects/ - Create a new project.

GET /api/board/projects/<uuid:pk>/ - Detailed project view.

GET /api/board/tasks/ - List tasks across accessible projects.

POST /api/board/tasks/ - Create a task within a project.

Documentation
GET /swagger/ - Swagger UI documentation.

GET /redoc/ - ReDoc documentation.

# Permission Logic

Project Owner: Full access to project and its tasks.

Project Admin: Permissions granted via project membership.

Task Creator: Can modify tasks they created.

Project Members: View access to projects they belong to.
